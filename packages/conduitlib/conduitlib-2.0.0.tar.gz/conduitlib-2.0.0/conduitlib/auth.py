# Copyright 2020 Software Factory Labs, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import logging
from pathlib import Path
from typing import Optional, Callable
from contextlib import contextmanager
import yaml
from cryptography.fernet import Fernet

logger = logging.getLogger(__name__)

auth_dir: Optional[Path] = None
secret_path: Optional[Path] = None

secrets: Optional[dict] = None


def setup(etc_dir: Path, load_cfg_from_yaml: Callable):
    logger.debug(f'etc_dir: {etc_dir}, load_cfg_from_yaml: {load_cfg_from_yaml}')

    # create paths
    global auth_dir
    auth_dir = etc_dir / 'auth'
    auth_dir.mkdir(parents=True, exist_ok=True)
    logger.debug(f'auth_dir: {auth_dir}')

    global secret_path
    secret_path = auth_dir / 'secret'
    logger.debug(f'secret_path: {secret_path}')

    # create key if it does not exist
    if not secret_path.exists():
        logger.debug(f'secret file ({secret_path}) does not exist')
        _create_key_file()
    else:
        with secret_path.open() as f:
            contents = f.read()

        if not contents:
            logger.debug(f'secret file ({secret_path}) empty')
            _create_key_file()

        del contents

        secret_file_perms = os.stat(secret_path).st_mode & 0o777
        desired_perms = 0o600
        if secret_file_perms != desired_perms:
            logging.warning(f'Secret file perms ({oct(secret_file_perms)[2:]}) not secure. '
                            f'Changing to {oct(desired_perms)[2:]}')
            os.chmod(secret_path, desired_perms)

    # load connections config file and encrypt any plaintext passwords
    secrets_filename = 'secrets.yaml'

    logger.debug('loading secrets')
    global secrets
    secrets = load_cfg_from_yaml(secrets_filename, no_exist_ok=True, local_only=True)

    if secrets is None:
        secrets = {}

    change = False

    for secret_id, secret_text in secrets.items():
        if secret_text.startswith('$1$'):
            continue

        logger.info(f'Encrypting secret for "{secret_id}"')

        secrets[secret_id] = f'$1${_encrypt(secret_text).decode()}'
        del secret_text

        change = True

    if change:
        with (etc_dir / f'local/{secrets_filename}').open('w') as f:
            yaml.safe_dump(secrets, f)

    logger.debug(f'loaded secrets: {list(secrets.keys())}')


@contextmanager
def get_secret(secret_id: str) -> str:
    try:
        encrypted_password = secrets.get(secret_id, None)

        if encrypted_password is None:
            raise Exception(f'No secret found for "{secret_id}"')

        encrypted_password = encrypted_password.split('$')[2]

        password = _decrypt(encrypted_password.encode())
        try:
            yield password
        finally:
            del password
    except Exception as e:
        logger.exception(e)
        raise


def _create_key_file():
    logger.info('Creating secret key')
    with secret_path.open('wb') as f:
        key = Fernet.generate_key()
        f.write(key)
        del key

    os.chmod(secret_path, 0o400)


def _encrypt(plaintext: str) -> bytes:
    with _get_fernet() as f:
        return f.encrypt(plaintext.encode())


def _decrypt(ciphertext: bytes) -> str:
    with _get_fernet() as f:
        return f.decrypt(ciphertext).decode()


@contextmanager
def _get_fernet() -> Fernet:
    with secret_path.open() as f:
        key = f.read()

    fern = Fernet(key)

    try:
        yield fern
    finally:
        del fern
        del key

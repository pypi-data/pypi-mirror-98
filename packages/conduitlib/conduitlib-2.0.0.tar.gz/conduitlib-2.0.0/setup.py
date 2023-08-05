import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

with open(os.path.join(here, 'requirements.txt')) as file:
    requires = file.readlines()

with open(os.path.join(here, 'requirements-dev.txt')) as file:
    dev_requires = file.readlines()

setup(
    name='conduitlib',
    version='2.0.0',
    description='A library containing common elements to Conduit and Conduit plugins.',
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python',
        'Intended Audience :: Developers',
    ],
    author='Eric Frechette',
    author_email='eric@softwarefactorylabs.com',
    # url='',
    # keywords='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require={
        'dev': dev_requires,
    },
    python_requires='>=3.8,<3.9',
)

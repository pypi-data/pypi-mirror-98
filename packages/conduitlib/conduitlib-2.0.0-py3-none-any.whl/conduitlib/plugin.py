"""Module containing classes for Plugin and Trigger. Also contains LoggerAdapters for the Plugin and Trigger classes."""
import logging
from typing import Optional
from . import util


class Plugin:
    """
    A plugin for a workflow. Used as a 'template' for a workflow task. Gets instantiated each time a workflow runs.
    """
    def __init__(self, workflow: str, instance_id: int, args: Optional[dict] = None):
        """
        Initialize this plugin object.
        :param workflow: the name of the workflow this plugin (as a task) is s part of
        :param instance_id: the instance ID of the workflow run this plugin (as a task) is a part of
        :param args: an optional dictionary containing arguments for this plugin
        """
        self.workflow = workflow
        self.instance_id = instance_id
        self.args = args if args is not None else {}

        self.logger = PluginLoggerAdapter(util.get_class_logger(self), self.workflow, self.instance_id)

    def execute(self, data: Optional[dict] = None) -> Optional[dict]:
        """
        Execute the task instantiated using this plugin in a workflow. Should be overridden by subclass.
        :param data: optional dictionary containing data from the previous workflow task.
        :return: optional dictionary containing data to pass on to the next workflow task.
        """
        raise NotImplementedError


class Trigger:
    """A trigger for a workflow. Used to determine when a workflow executes."""
    def __init__(self, workflow: str, args: Optional[dict] = None):
        """
        Initialize this trigger object.
        :param workflow: the name of the workflow this trigger is a part of
        :param args: an optional dictionary containing arguments for this trigger
        """
        self.workflow = workflow
        self.args = args if args is not None else {}

        self.logger = TriggerLoggerAdapter(util.get_class_logger(self), self.workflow)

    def run(self):
        """
        Initialize this trigger. Should be overridden by subclass.
        """
        raise NotImplementedError


class PluginLoggerAdapter(logging.LoggerAdapter):
    """LoggerAdapter for the Plugin class. Prepends '[WORKFLOW_NAME:INSTANCE_ID]' to the log message."""
    def __init__(self, logger: logging.Logger, workflow: str, instance_id: int):
        super().__init__(logger, {})
        self.workflow = workflow
        self.instance_id = instance_id

    def process(self, msg, kwargs):
        return f'[{self.workflow}:{self.instance_id}] {msg}', kwargs


class TriggerLoggerAdapter(logging.LoggerAdapter):
    """Logger adapter for the Trigger class. Prepends '[WORKFLOW_NAME]' to the log message."""
    def __init__(self, logger: logging.Logger, workflow: str):
        super().__init__(logger, {})
        self.workflow = workflow

    def process(self, msg, kwargs):
        return f'[{self.workflow}] {msg}', kwargs

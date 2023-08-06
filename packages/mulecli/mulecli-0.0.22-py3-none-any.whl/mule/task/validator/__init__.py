import os
import pkg_resources
import re
import time
from pydoc import locate

from mule.task.error import messages
from mule.util import file_util
from mule.util import get_dict_value

DEFAULT_MULE_CONFIGS = {
    'packages': [
        'mule.task'
    ]
}

DEFAULT_MULE_CONFIG_PATH = "~/.mule/config.yaml"


validators = {
    "env": re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*=.+"),
    "volumes": re.compile(r".+:.+")
}


def get_plugin(name):
    return [
        entry_point.load()
        for entry_point in pkg_resources.iter_entry_points(group="mule.plugin")
        if name == entry_point.name
    ]


def getValidatedMuleConfigFile():
    config_file_path = os.path.abspath(os.path.expanduser(DEFAULT_MULE_CONFIG_PATH))
    mule_configs = DEFAULT_MULE_CONFIGS
    if os.path.isfile(config_file_path):
        mule_configs_from_file = file_util.read_yaml_file(config_file_path)
        mule_configs.update(mule_configs_from_file)
    return mule_configs


def validate(field, f):
    try:
        if not f:
            return
        if not validators[field].match(f):
            raise ValueError
        return True
    except TypeError:
        raise Exception(messages.AGENT_FIELD_WRONG_TYPE.format(
            field,
            f,
            str,
            type(field)
        ))
    except ValueError:
        raise Exception(messages.AGENT_FIELD_WRONG_FORMAT.format(
            field,
            f
        ))


def validate_agent_block(agent_block, field):
    # Note that "env" and "volumes" fields are optional in an agent,
    # so it's ok to return if not found in dict.
    if field not in agent_block:
        return
    fields = agent_block[field]
    if type(fields) is list:
        for f in fields:
            validate(field, f)
        validate_list(f"agent.{field}", fields)
    else:
        validate_block(f"agent.{field}", fields)


def get_validated_mule_yaml(mule_config):
    mule_config_keys = mule_config.keys()

    if not "jobs" in mule_config_keys:
        raise Exception(messages.FIELD_NOT_FOUND.format("jobs"))
    if not "tasks" in mule_config_keys:
        raise Exception(messages.FIELD_NOT_FOUND.format("tasks"))

    # Note that agents are optional!
    if "agents" in mule_config:
        for field in ["env", "volumes"]:
            for agent in mule_config["agents"]:
                validate_agent_block(agent, field)
        agent_configs = mule_config["agents"]
    else:
        agent_configs = []

    jobs_configs = mule_config["jobs"]
    task_configs = mule_config["tasks"]

    mule_configs = [
        ("jobs", jobs_configs, validate_block),
        ("tasks", task_configs, validate_tasks)
    ]

    if len(agent_configs):
        mule_configs.append(("agents", agent_configs, validate_list))

    for (name, config, fn) in mule_configs:
        try:
            fn(name, config)
        except Exception as error:
            raise Exception(messages.FIELD_VALUE_COULD_NOT_BE_VALIDATED.format(
                name,
                str(error)
            ))

    return {
        "agents": agent_configs,
        "jobs": jobs_configs,
        "tasks": task_configs
    }


def validate_block(name, config):
    if not type(config) == dict:
        raise Exception(messages.FIELD_VALUE_WRONG_TYPE.format(name, dict, type(config)))


def validate_list(name, config):
    if not type(config) == list:
        raise Exception(messages.FIELD_VALUE_WRONG_TYPE.format(name, list, type(config)))


def validate_tasks(name, task_configs):
    validate_list(name, task_configs)
    for index, config in enumerate(task_configs):
        validate_block(name, config)


def validate_typed_fields(task_id, task_fields, task_required_typed_fields, task_optional_typed_fields):
    for required_field, required_field_type in task_required_typed_fields:
        required_field_index = required_field.split('.')
        required_field_value = get_dict_value(task_fields, required_field_index)
        if required_field_value is None:
            raise Exception(messages.TASK_MISSING_REQUIRED_FIELDS.format(
                task_id,
                required_field,
                task_required_typed_fields,
            ))
        if not type(required_field_value) == required_field_type:
            raise Exception(messages.TASK_FIELD_IS_WRONG_TYPE.format(
                task_id,
                required_field,
                required_field_type,
                type(required_field_value)
            ))
    for optional_field, optional_field_type in task_optional_typed_fields:
        optional_field_index = optional_field.split('.')
        optional_field_value = get_dict_value(task_fields, optional_field_index)
        if not optional_field_value is None:
            if not type(optional_field_value) == optional_field_type:
                raise Exception(messages.TASK_FIELD_IS_WRONG_TYPE.format(
                    task_id,
                    optional_field,
                    optional_field_type,
                    type(optional_field_value)
                ))


def validateTaskConfig(task_config):
    if not 'task' in task_config:
        raise Exception(messages.TASK_FIELD_MISSING)


def getValidatedTask(task_config):
    mule_config = getValidatedMuleConfigFile()
    task_name = task_config['task']
    for package in mule_config['packages']:
        task_obj = locate(f"{package}.{task_name}")
        if not task_obj is None:
            return task_obj(task_config)
    raise Exception(messages.CANNOT_LOCATE_TASK.format(task_name))


def get_validated_task_dependency_chain(job_context, dependency_edges):
    # This is basically dfs, so these tuples represent edges
    # Index 0 is the requested task and index 1 is the
    # requesting task. Organizing the problem this way helps
    # with cycle detection. I'm reversing this list so
    # it starts out as stack
    dependency_edges.reverse()
    tasks_tbd = []
    seen_dependency_edges = []
    # Give mule 10 seconds to decipher dependency tree
    # if it takes longer than this, mule is probably in
    # an infinite loop
    timeout = time.time() + 10
    while len(dependency_edges) > 0:
        if time.time() > timeout:
            raise Exception(messages.TASK_DEPENDENCY_CHAIN_TIMEOUT)
        dependency_edge = dependency_edges.pop(0)
        if dependency_edge in seen_dependency_edges:
            raise Exception(messages.TASK_DEPENDENCY_CYCLIC_DEPENDENCY.format(dependency_edge[1], dependency_edge[0]))
        seen_dependency_edges.append(dependency_edge)
        task_context = job_context.get_field(f"{dependency_edge[0]}")
        if task_context is None:
            raise Exception(messages.CANNOT_LOCATE_TASK_CONFIGS.format(dependency_edge[1], dependency_edge[0]))
        if not 'completed' in task_context:
            if not 'task' in task_context:
                task_instance = getValidatedTask(task_context['inputs'])
            if task_instance in tasks_tbd:
                # Our graph has different nodes with the same name.
                # These nodes are the same as far as we're concerned
                # so when we see repeats, we'll delete the earlier
                # nodes. The ones that show up later get executed
                # first, and we only want these to be executed once.
                tasks_tbd.remove(task_instance)
            tasks_tbd.append(task_instance)
            for dependency_edge in task_instance.get_dependency_edges():
                dependency_edges.insert(0, dependency_edge)
    # Reversing the list because we started with
    # the targeted task and ended with the earliest
    # dependency in the chain. Since these are
    # dependencies we're working with, we want
    # those executed first.
    tasks_tbd.reverse()
    return tasks_tbd


def validate_required_task_fields_present(task_id, fields, required_fields):
    for field in required_fields:
        if not field in fields.keys():
            raise Exception(messages.TASK_MISSING_REQUIRED_FIELDS.format(
                task_id,
                field,
                str(required_fields)
            ))

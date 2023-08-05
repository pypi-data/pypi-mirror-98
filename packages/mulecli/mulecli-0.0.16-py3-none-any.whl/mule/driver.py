import yaml
import mule.task.parser
import mule.task.validator as validator
import mule.util.yaml.env_var_loader as yaml_util
from mule.util import JobContext, file_util, update_dict
from mule.task.error import messages
from mule.task import Job
from termcolor import cprint
import sys

def main():
    args = mule.task.parser.parseArgs()
    try:
        mule_yamls = args.file
        if len(args.file) == 0:
            mule_yamls.append('mule.yaml')
        mule_config = _read_mule_yamls(mule_yamls)
        parsed_mule_config = yaml_util.readYamlWithEnvVars(yaml.dump(mule_config))
        jobs_config, task_configs, agent_configs = validator.getValidatedMuleYaml(parsed_mule_config)
        if args.list_jobs:
            _list_jobs(jobs_config)
        elif args.list_tasks:
            _list_tasks(task_configs)
        else:
            _execute_job(jobs_config, task_configs, agent_configs, args.JOB)
    except Exception as error:
        cprint(
            messages.MULE_DRIVER_EXCEPTION.format(args.JOB, args.file, error),
            'red',
            attrs=['bold'],
            file = sys.stderr
        )
        raise error

def _read_mule_yamls(mule_yamls):
    mule_config = {}
    for mule_yaml in mule_yamls:
        update_dict(
            mule_config,
            file_util.readYamlFile(mule_yaml),
            overwrite_lists=False
        )
    return mule_config

def _list_jobs(jobs_config):
    for job in jobs_config.keys():
        print(job)

def _list_tasks(task_configs):
    for task in task_configs:
        if 'name' in task.keys():
            print(f"{task['task']}.{task['name']}")
        else:
            print(task['task'])

def _execute_job(jobs_config, task_configs, agent_configs, job):
    if not job in jobs_config:
        raise Exception(messages.JOB_NOT_FOUND.format(job))
    job_config = jobs_config[job]
    job_config.update({
        'agent_configs': agent_configs,
        'task_configs': task_configs,
        'name': job
    })
    job = Job(job_config)
    job_context = JobContext(agent_configs)

    return job.execute(job_context)


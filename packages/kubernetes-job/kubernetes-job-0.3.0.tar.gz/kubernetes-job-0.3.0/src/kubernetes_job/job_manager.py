import logging
import yaml
import datetime
import os
import socket
from pathlib import Path
from typing import Iterator

from kubernetes import client
from kubernetes.utils import create_from_dict
from kubernetes.client.models import V1Job, V1Status

from .job_func_def import JobFuncDef, JobMeta

logger = logging.getLogger(__name__)

K8S_CONTAINER_NAME = 'kubernetes-job'
K8S_ENV_VAR_NAME = 'KUBERNETES_JOB_FUNC'
K8S_DEFAULT_NAMESPACE = 'default'


current_job: [JobFuncDef, None] = None


def _gen_id(name: str, dt: datetime) -> str:
    """Generate a job id from the name and the given datetime"""
    return f"{name or K8S_CONTAINER_NAME}-{dt.strftime('%Y%m%d%H%M%S%f')}"


def job_name(job: [str, V1Job]) -> str:
    """Return the name of a job"""
    return job if job is str else job.metadata.name


def is_failed(job: V1Job):
    """Return True if the job is failed"""
    return bool(job.status.failed)


def is_succeeded(job: V1Job):
    """Return True if the job has succeeded"""
    return bool(job.status.succeeded)


def is_completed(job: V1Job):
    """Return True if the job has completed (either failed or succeeded)"""
    return is_failed(job) or is_succeeded(job)


def is_active(job: V1Job):
    """Return True if the job is active (running)"""
    return bool(job.status.active)


def job_status(job: V1Job) -> str:
    """Return SUCCEEDED, FAILED, ACTIVE, or PENDING, depending on the status of the job"""
    if is_failed(job):
        return 'FAILED'
    elif is_succeeded(job):
        return 'SUCCEEDED'
    elif is_active(job):
        return 'ACTIVE'
    else:
        return 'PENDING'


class JobManager:
    """
    Kubernetes JobManager

    :param k8s_client: Kubernetes OpenAPI client
    :param k8s_job_spec: `dict` or path to YAML file containing the spec for the job worker
    :param namespace: Kubernetes k8s_namespace (default: 'default')
    """

    k8s_client = None
    k8s_job_spec = None
    k8s_namespace = None

    def __init__(self, k8s_client: client.ApiClient,
                 k8s_job_spec: [dict, str],
                 namespace: str = K8S_DEFAULT_NAMESPACE
                 ):
        """
        Initialize the JobManager

        :param k8s_client: Kubernetes OpenAPI client
        :param k8s_job_spec: `dict` or path to YAML file containing the spec for the job worker
        :param namespace: Kubernetes k8s_namespace
        """

        self.k8s_client = k8s_client
        self.k8s_job_spec = k8s_job_spec
        self.k8s_namespace = namespace

    def create_job(self, func, *func_args, **func_kwargs) -> V1Job:
        """
        Create a job

        :param func: Function pointer
        :param func_args: Args to submit to the function
        :param func_kwargs: Kwargs to submit to the function
        :return: V1Job
        """
        if self.k8s_job_spec is dict:
            yml_document = self.k8s_job_spec
        else:
            with Path(self.k8s_job_spec).open() as f:
                yml_document = yaml.safe_load(f)

        # add function call as environment variable
        metadata = yml_document['metadata']
        container = yml_document['spec']['template']['spec']['containers'][0]

        # set name by combining existing name (or default) with a timestamp
        dt_scheduled = datetime.datetime.utcnow()
        name = _gen_id(metadata.get('name'), dt_scheduled)
        metadata['name'] = name

        # set command; check if explicitly specified
        cmd = container.get('command')
        if cmd:
            logger.info(f"Job spec contains Docker command '{cmd}'; make sure this command calls 'kubernetes-job' to start the job runner.")
        else:
            container['command'] = ['kubernetes-job']

        # create metadata
        meta = JobMeta()
        meta.name = name
        meta.dt_scheduled = dt_scheduled
        meta.host = socket.gethostname()

        # serialize function call
        job = JobFuncDef(func, args=func_args, kwargs=func_kwargs, meta=meta)

        env_vars = container.get('env', [])
        env_vars.append({
            'name': K8S_ENV_VAR_NAME,
            'value': job.dump()
        })
        container['env'] = env_vars

        # create the job
        yml = yaml.dump(yml_document)
        logger.info(f"Creating K8s job '{name}'; calling function {func.__name__}")
        logger.info(f"Spec:\n{yml}")

        api_response = create_from_dict(self.k8s_client, yml_document, namespace=self.k8s_namespace)

        return api_response[0]

    def delete_job(self, job: [str, V1Job], grace_period_seconds: int = 0, propagation_policy: str = 'Background') -> V1Status:
        """
        Delete a Job

        :param job: Name or V1Job instance
        :param grace_period_seconds: (default: 0)
        :param propagation_policy: (default: 'Background')
        :return: V1Status
        """
        name = job_name(job)
        logger.debug(f"Deleting job '{name}")

        api_instance = client.BatchV1Api(self.k8s_client)
        api_response = api_instance.delete_namespaced_job(name, self.k8s_namespace,
                                                          grace_period_seconds=grace_period_seconds,
                                                          propagation_policy=propagation_policy)

        return api_response

    def list_jobs(self, field_selector=None, label_selector=None) -> Iterator[V1Job]:
        """
        List job objects

        :param field_selector: A selector to restrict the list of returned objects by their fields. Defaults to everything.
        :param label_selector: A selector to restrict the list of returned objects by their labels. Defaults to everything.
        :return: Iterator of V1Job
        """
        api_instance = client.BatchV1Api(self.k8s_client)

        paging_token = None
        has_more = True

        # retrieve all jobs in this k8s_namespace
        # this may take several calls to the API
        while has_more:
            api_response = api_instance.list_namespaced_job(self.k8s_namespace,
                                                            _continue=paging_token,
                                                            field_selector=field_selector,
                                                            label_selector=label_selector)

            # yield results
            for job in api_response.items:
                yield job

            # get _continue paging token
            paging_token = api_response.metadata._continue if api_response.metadata else None
            has_more = paging_token

    def read_job(self, job: [str, V1Job]) -> V1Job:
        """
        Read the status of the specified Job

        :param job: Name or V1Job instance
        :return: V1Job
        """
        name = job_name(job)
        api_instance = client.BatchV1Api(self.k8s_client)
        return api_instance.read_namespaced_job(name, namespace=self.k8s_namespace)

    def clean_jobs(self, field_selector=None, label_selector=None):
        """
        Clean up completed jobs

        :param field_selector: A selector to restrict the list of returned objects by their fields. Defaults to everything.
        :param label_selector: A selector to restrict the list of returned objects by their labels. Defaults to everything.
        """

        for job in self.list_jobs(field_selector=field_selector, label_selector=label_selector):
            if is_completed(job):
                logger.debug(f"Cleanup up job '{job_name(job)}; status: {job_status(job)}")
                self.delete_job(job)

    @staticmethod
    def execute_job(job_func_def: str = None):
        """
        Execute the JobFuncDef specified in the func_spec

        :param job_func_def: Serialized job definition
        :return: Job function return value (if any)
        """

        logger.info("Executing default job")

        global current_job

        try:
            func_def = job_func_def or os.getenv(K8S_ENV_VAR_NAME)
            if not func_def:
                raise ValueError(f"Argument 'job_func_def' is missing, and environment var '{K8S_ENV_VAR_NAME}' is not set either.")

            current_job = JobFuncDef.load(func_def)
            return current_job.execute()
        except Exception as e:
            logger.fatal(e)
            raise

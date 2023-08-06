import os

from kubernetes_job.job_func_def import JobFuncDef, JobMeta
from kubernetes_job.job_manager import K8S_ENV_VAR_NAME
from kubernetes_job.__main__ import execute

from .funcs import add, calc_pi, no_args_no_kwargs, kwargs_only

args = (1, 2)
kwargs = {'info': "snafu"}
meta = JobMeta()
meta.name = 'test'
meta.host = 'tester'


def test_serialize():
    a = (100, 1)
    k = {}

    j = JobFuncDef(calc_pi, args=a, kwargs=k)

    assert j.func == calc_pi
    assert j.args == a
    assert j.kwargs == k

    dump = j.dump()


def test_deserialize():
    j = JobFuncDef(add, args=args, kwargs=kwargs, meta=meta)
    dump = j.dump()
    j = None

    j2 = JobFuncDef.load(dump)

    assert j2.func == add
    assert j2.args == args
    assert j2.kwargs == kwargs
    assert j2.meta.name == meta.name

    assert j2.execute() == 3


def test_deserialize_no_args():
    j = JobFuncDef(no_args_no_kwargs)
    dump = j.dump()
    j = None

    j2 = JobFuncDef.load(dump)

    assert j2.func == no_args_no_kwargs
    assert j2.execute() == no_args_no_kwargs.__name__


def test_deserialize_kwargs_only():
    j = JobFuncDef(kwargs_only, kwargs={'foo': 1, 'bar': 2})
    dump = j.dump()
    j = None

    j2 = JobFuncDef.load(dump)

    assert j2.func == kwargs_only
    assert j2.execute() == kwargs_only.__name__


def test_execution_current_job():
    j = JobFuncDef(add, args=(3, 4))
    os.environ[K8S_ENV_VAR_NAME] = j.dump()

    result = execute()

    assert result == 7


if __name__ == "__main__":
    test_serialize()

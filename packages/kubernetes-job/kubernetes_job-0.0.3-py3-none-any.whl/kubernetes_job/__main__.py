import logging
import sys
from .job_manager import JobManager

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)


def execute():
    return JobManager.execute_job()


if __name__ == '__main__':
    execute()
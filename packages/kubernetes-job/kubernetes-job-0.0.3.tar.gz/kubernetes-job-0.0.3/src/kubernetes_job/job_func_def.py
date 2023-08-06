import pickle
import codecs
import logging
import datetime
import zlib

logger = logging.getLogger(__name__)


class JobMeta:
    name: str = '[JOB-NAME]'
    dt_scheduled: datetime = datetime.datetime.min
    host: str = '[HOST]'


class JobFuncDef:
    """Helper class to hold the job function definition"""

    """Pointer to the job function"""
    func = None

    """Args for the job function"""
    args = None

    """Kwargs for the job function"""
    kwargs = None

    """Metadata for the job"""
    meta: JobMeta = None

    def __init__(self, func, args=None, kwargs=None, meta: JobMeta = None):
        """
        Initialize the job function definition

        :param func: Pointer to the job function
        :param args: Args for the job function
        :param kwargs: Kwargs for the job function
        :param meta: Metadata for the job
        """
        self.func = func
        self.args = args or []
        self.kwargs = kwargs or {}
        self.meta = meta or JobMeta()

    def dump(self) -> str:
        """Dump the job function definition to a base64 string"""
        return codecs.encode(zlib.compress(pickle.dumps(self)), "base64").decode()

    def execute(self):
        """Execute the job function"""
        logger.info(f"=== Starting job {self.meta.name}, submitted from {self.meta.host} at {self.meta.dt_scheduled.isoformat()} ===")
        logger.debug(f"Job func: {self.func.__name__}")

        return self.func(*self.args, **self.kwargs)

    @staticmethod
    def load(s: str) -> 'JobFuncDef':
        """Load the job function definition from a base64 string"""
        return pickle.loads(zlib.decompress(codecs.decode(s.encode(), "base64")))


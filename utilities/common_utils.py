"""
Common utility function
"""
import logging, os
from datetime import datetime
import functools
import time


DATE_TIME = "%m_%d_%H_%M_%Y"

_nameToLevel = {
#    'CRITICAL': logging.CRITICAL,
#    'FATAL': logging.FATAL,  # FATAL = CRITICAL
#    'ERROR': logging.ERROR,
#    'WARN': logging.WARNING,
   'INFO': logging.INFO,
   'DEBUG': logging.DEBUG,
}


def get_logger(name=__name__, log_file=None, log_level=logging.DEBUG, log_level_name=''):
    """ default log level DEBUG """
    logger = logging.getLogger(name)
    if name == 'app':
        fmt= '%(asctime)s %(filename)10s %(levelname)s L %(lineno)d: %(message)s'
    else:
        fmt= '%(asctime)s %(name)s %(levelname)s L %(lineno)d: %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(format=fmt, datefmt=datefmt)
    if log_file is not None:
        log_file_folder = os.path.split(log_file)[0]
        if log_file_folder:
            os.makedirs(log_file_folder, exist_ok=True)
        fh = logging.FileHandler(log_file, 'a', encoding='utf-8')
        fh.setFormatter(logging.Formatter(fmt, datefmt))
        logger.addHandler(fh)
    if log_level_name in _nameToLevel:
        log_level = _nameToLevel[log_level_name]
    logger.setLevel(log_level)
    return logger


def save_args(args):
    t0 = datetime.now().strftime(DATE_TIME)
    if args.output_dir is not None:
        os.makedirs(args.output_dir, exist_ok=True)
        with open(os.path.join(args.output_dir, f"args-{t0}.txt"), "w", encoding='utf-8') as f:
            for arg, value in vars(args).items():
                f.write(f"{arg}: {value}\n")


def func_time_print(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        t0 = time.time()
        res = func(*args, **kw)
        _total_seconds = time.time() - t0
        total_seconds = int(_total_seconds)
        hours = total_seconds // 3600
        total_seconds = total_seconds % 3600
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        print(f'call {func.__name__}() uses hours:mm:ss {hours}:{minutes}:{seconds}')        
        print(f'call {func.__name__}() uses total seconds {_total_seconds:.3f}')        
        return res
    return wrapper
    
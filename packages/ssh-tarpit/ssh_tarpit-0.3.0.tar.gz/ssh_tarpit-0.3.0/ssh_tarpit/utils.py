import asyncio
import logging


def setup_logger(name, verbosity, logfile=False):
    logger = logging.getLogger(name)
    logger.setLevel(verbosity)
    handler = logging.StreamHandler()
    handler.setLevel(verbosity)
    handler.setFormatter(logging.Formatter('%(asctime)s '
                                           '%(levelname)-8s '
                                           '%(name)s: %(message)s',
                                           '%Y-%m-%d %H:%M:%S'))
    logger.addHandler(handler)
    if logfile:
        fh = logging.FileHandler(logfile)
        fh.setLevel(level=verbosity)
        fh.setFormatter(logging.Formatter('%(asctime)s '
                                          '%(levelname)-8s '
                                          '%(name)s: %(message)s',
                                          '%Y-%m-%d %H:%M:%S'))
        logger.addHandler(fh)
    return logger


def enable_uvloop():
    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    except ImportError:
        return False
    else:
        return True

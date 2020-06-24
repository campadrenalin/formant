from formant.template import template

def make_logger():
    '''
    Use a function here, to reduce namespace pollution.
    '''
    import logging
    logger = logging.getLogger('formant')
    stderr = logging.StreamHandler()
    formatter = logging.Formatter("%(name)s:%(levelname)s - %(message)s")
    stderr.setFormatter(formatter)
    logger.addHandler(stderr)
    return logger

logger = make_logger()

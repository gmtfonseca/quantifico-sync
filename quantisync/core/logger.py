import logging
import sys


class LoggerFactory:

    @classmethod
    def getDevLogger(cls):
        cls._disableThirdPartyLoggers()
        level = logging.DEBUG
        formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger = logging.getLogger('devLogger')
        logger.setLevel(level)
        logger.addHandler(handler)
        logger.propagate = False
        return logger

    @classmethod
    def getProdLogger(cls, path):
        cls._disableThirdPartyLoggers()
        level = logging.ERROR
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler = logging.FileHandler(path)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        logger = logging.getLogger('prodLogger')
        logger.setLevel(level)
        logger.addHandler(handler)
        logger.propagate = False
        return logger

    @classmethod
    def _disableThirdPartyLoggers(cls):
        logging.getLogger('urllib3').setLevel(logging.CRITICAL)

    @classmethod
    def getRootLogger(cls):
        return logging.getLogger('')

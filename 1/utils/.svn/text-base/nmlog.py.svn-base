import logging
from config import LOG_PATH

class Logger(object):
    def __init__(self):
        logger = logging.getLogger()
        hdr = logging.FileHandler(LOG_PATH)
        #formatter = logging.Formatter('%(asctime)s    %(levelname)s    %(message)s')
        formatter = logging.Formatter('%(asctime)s    %(message)s')
        hdr.setFormatter(formatter)
        logger.addHandler(hdr)
        logger.setLevel(logging.NOTSET)

        self.l = logger

    def _format_msg(self, req, resp):
        return '%s    %s    %s' % (resp.status_code,
                                   req.method.upper()+req.get_full_path(),
                                   ''.join(resp.content[:500].split()))

    def log(self, req, resp, error=False):
        msg = self._format_msg(req, resp)
        if error:
            self.l.error(msg)
        else:
            self.l.info(msg)

    def info(self, msg):
        self.l.info(msg)

    def error(self, msg):
        self.l.error(msg)

def get_logger():
    return Logger()

import logging

import coilmq.start

logger = logging.getLogger(__name__)

try:
    coilmq.start.main()
except (KeyboardInterrupt, SystemExit):
    pass
except Exception as e:
    logger.error("Server terminated due to error: %s" % e)
    logger.exception(e)

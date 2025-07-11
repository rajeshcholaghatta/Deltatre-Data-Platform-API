import logging
import os

def get_logger(name="bddLogger", log_file="logs/test.log"):
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger(name)

    if not logger.handlers:  # Ensures handlers aren't added multiple times
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # File handler
        fh = logging.FileHandler(log_file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        # Console handler (optional)
#        ch = logging.StreamHandler()
 #       ch.setFormatter(formatter)
  #      logger.addHandler(ch)

    return logger
import logging


def configure_logger():
    logger = logging.getLogger('my_logger')
    logger.setLevel(logging.DEBUG)  # Capture all levels of log

    # File Handler for error logs
    error_handler = logging.FileHandler('errors.log')
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    error_handler.setFormatter(error_formatter)

    # File Handler for info logs
    info_handler = logging.FileHandler('info.log')
    info_handler.setLevel(logging.INFO)
    info_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    info_handler.setFormatter(info_formatter)

    # Stream Handler for console output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # Set to DEBUG to capture all types of logs
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)

    # Add handlers to the logger
    logger.addHandler(error_handler)
    logger.addHandler(info_handler)
    logger.addHandler(console_handler)

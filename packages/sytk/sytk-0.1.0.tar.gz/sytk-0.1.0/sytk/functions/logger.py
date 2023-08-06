import logging
from typing import Union, Optional
from os import PathLike


def get_logger(
        name: str,
        level: Union[int, str],
        fmt: Optional[str] = None,
        filename: Optional[Union[str, PathLike]] = None,
        mode: Optional[str] = None
) -> logging.Logger:
    formatter = logging.Formatter(fmt=fmt)

    if filename is not None:
        handler = logging.FileHandler(filename=filename, mode=mode)
    else:
        handler = logging.StreamHandler()

    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(level)

    return logger

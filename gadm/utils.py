"""
Supportive utility methods for gadm library
"""

import logging
import os

import requests
import tqdm
from fake_useragent import UserAgent

__all__ = ["download_url"]


def download_url(
    url: str,
    file_path: str,
    timeout_sec: float = 60,
    logger: logging.Logger = logging.getLogger(),
) -> None:
    """download file from url

    Parameters
    ----------
    url : str
        url of file to download
    file_path : str
        local path of the file
    """
    res0 = requests.head(url)
    assert "Content-Length" in res0.headers
    file_size = int(res0.headers["Content-Length"])

    if os.path.isfile(file_path) and os.path.getsize(file_path) == file_size:
        return

    try:
        headers = {"User-Agent": str(UserAgent().random)}
        res = requests.get(url, stream=True, timeout=timeout_sec, headers=headers)
    except requests.exceptions.Timeout as e:
        logger.exception(f"Failed to fetch data due to time out: {e}")
        return

    with open(file_path, "wb") as _f:
        pbar = tqdm.tqdm(total=file_size, unit="B", unit_scale=True)
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                _f.write(chunk)
            pbar.update(len(chunk))
        pbar.close()

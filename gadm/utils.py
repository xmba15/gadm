"""
Supportive utility methods for gadm library
"""

import os

import requests
import tqdm

__all__ = ["download_url"]


def download_url(url: str, file_path: str) -> None:
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

    res = requests.get(url, stream=True)

    with open(file_path, "wb") as _f:
        pbar = tqdm.tqdm(total=file_size, unit="B", unit_scale=True)
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:
                _f.write(chunk)
            pbar.update(len(chunk))
        pbar.close()

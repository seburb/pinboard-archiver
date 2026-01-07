import requests
from config import USER_AGENT

def pinboard_to_archive_time_formatter(timestamp):
    """
    Pinboard format: YYYY-MM-DDTHH:MM:SSZ
    archive.org format: YYYYMMDDHHMMSS
    """
    return (
        timestamp.replace("-", "")
        .replace(":", "")
        .replace("T", "")
        .replace("Z", "")
    )


def site_is_online(url, timeout=10):
    """
    Check availablity of URL, first with HEAD method to save bandwith,
    if this fails, try GET,
    then fail completely
    TODO: Extend to other status codes
    """
    headers = {"User-Agent": USER_AGENT}

    try:
        r = requests.head(
            url,
            headers=headers,
            allow_redirects=True,
            timeout=timeout,
        )
        if r.status_code == 200:
            return True
    except requests.RequestException:
        pass

    try:
        r = requests.get(
            url,
            headers=headers,
            allow_redirects=True,
            timeout=timeout,
            stream=True,
        )
        return r.status_code == 200
    except requests.RequestException:
        return False
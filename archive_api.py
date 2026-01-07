import time
import requests
from urllib.parse import quote
from config import ARCHIVE_API_CDX, ARCHIVE_API_SAVE, USER_AGENT
from logging_config import setup_logger

logger = setup_logger()


def closest_archive_snapshot(url, timestamp, timeout=60):
    params = {
        "url": url,
        "limit": 1,
        "sort": "closest",
        "from": timestamp[:8],
        "to": timestamp[:8],
        "output": "json",
    }

    try:
        r = requests.get(ARCHIVE_API_CDX, params=params, timeout=timeout)
        r.raise_for_status()
        data = r.json()

        if len(data) > 1:
            _, ts, original_url, *_ = data[1]
            return f"https://web.archive.org/web/{ts}/{original_url}"

    except requests.RequestException as e:
        logger.warning("CDX lookup failed for %s: %s", url, e)

    return None


def save_to_archive(url, retries=3):
    headers = {"User-Agent": USER_AGENT}

    for attempt in range(1, retries + 1):
        try:
            save_url = f"{ARCHIVE_API_SAVE}/{quote(url)}"
            print(f"  --> Saving to archive.org (attempt {attempt})")

            r = requests.get(
                save_url,
                headers=headers,
                timeout=240,
                allow_redirects=False,
            )

            if r.status_code == 302:
                archived = r.headers.get("Content-Location") or r.headers.get("Location")
                if archived:
                    if not archived.startswith("http"):
                        archived = "https://web.archive.org" + archived
                    return archived

        except requests.RequestException as e:
            logger.warning(
                "Wayback save attempt %s failed for %s: %s",
                attempt, url, e,
            )

        time.sleep(5 * attempt)

    return None
import requests

from config import (
    PINBOARD_API_TOKEN,
    PINBOARD_PAGE_SIZE,
    PINBOARD_API_ALL,
    PINBOARD_API_ADD,
    ARCHIVED_MARKER,
    ARCHIVED_TAG,
    LINKROT_TAG,
)

def fetch_all_bookmarks():
    """
    Fetch all bookmarks from Pinboard API
    Use limit from constant PAGE_SIZE per call
    """
    all_bookmarks = []
    start = 0

    while True:
        params = {
            "auth_token": PINBOARD_API_TOKEN,
            "format": "json",
            "start": start,
            "results": PINBOARD_PAGE_SIZE,
        }

        r = requests.get(PINBOARD_API_ALL, params=params, timeout=100)
        r.raise_for_status()
        batch = r.json()

        if not batch:
            break

        all_bookmarks.extend(batch)
        start += PINBOARD_PAGE_SIZE
        print(f"Fetched {len(all_bookmarks)} bookmarks")

    return all_bookmarks


def update_pinboard(bookmark, archive_link):
    """
    Fetch all bookmarks from Pinboard API
    Max is 1000 entries per call, use limit from constant PAGE_SIZE
    """
    old_extended = bookmark.get("extended", "") or ""
    tags = bookmark.get("tags", "") or ""

    if ARCHIVED_MARKER in old_extended:
        print("Already updated, skipping")
        return

    tag_set = set(tags.split())

    if archive_link:
        tag_set.add(ARCHIVED_TAG)
        new_extended = (
            old_extended + "\n\n" + f"{ARCHIVED_MARKER} {archive_link}"
        ).strip()
    else:
        tag_set.add(LINKROT_TAG)
        new_extended = old_extended

    params = {
        "auth_token": PINBOARD_API_TOKEN,
        "url": bookmark["href"],
        "description": bookmark["description"], # This is the title, stays unchanged
        "extended": new_extended,               # This is the description, update
        "tags": " ".join(sorted(tag_set)),
        "replace": "yes",
        "format": "json",
    }

    r = requests.get(PINBOARD_API_ADD, params=params, timeout=30)
    if r.status_code == 200:
        print("  --> Updated Pinboard")
    else:
        print("X Pinboard update failed:", r.text)
import requests
from config import (
    PINBOARD_API_TOKEN,
    PAGE_SIZE,
    PINBOARD_API_ALL,
    PINBOARD_API_ADD,
    ARCHIVED_MARKER,
    ARCHIVED_TAG,
    LINKROT_TAG,
)

def fetch_all_bookmarks():
    all_bookmarks = []
    start = 0

    while True:
        params = {
            "auth_token": PINBOARD_API_TOKEN,
            "format": "json",
            "start": start,
            "results": PAGE_SIZE,
        }

        r = requests.get(PINBOARD_API_ALL, params=params, timeout=100)
        r.raise_for_status()
        batch = r.json()

        if not batch:
            break

        all_bookmarks.extend(batch)
        start += PAGE_SIZE
        print(f"Fetched {len(all_bookmarks)} bookmarks")

    return all_bookmarks


def update_pinboard(bookmark, archive_link):
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
        "description": bookmark["description"],
        "extended": new_extended,
        "tags": " ".join(sorted(tag_set)),
        "replace": "yes",
        "format": "json",
    }

    r = requests.get(PINBOARD_API_ADD, params=params, timeout=30)
    if r.status_code == 200:
        print("  --> Updated Pinboard")
    else:
        print("X Pinboard update failed:", r.text)
import time

from config import (
    ARCHIVED_MARKER,
    LINKROT_TAG,
    PINBOARD_API_TOKEN,
    SLEEP_SECONDS,
)
from pinboard_api import (
    fetch_all_bookmarks,
    update_pinboard,
)
from archive_api import (
    closest_archive_snapshot,
    save_to_archive,
)
from utils import (
    pinboard_to_archive_time_formatter,
    site_is_online,
)

def main():
    if not PINBOARD_API_TOKEN:
        raise RuntimeError(
            "PINBOARD_API_TOKEN is not set. "
            "Create a .env file or set the environment variable."
        )
        sys.exit(1)


    bookmarks = fetch_all_bookmarks()
    total = len(bookmarks)
    print(f"\nTotal bookmarks: {total}")

    for idx, bm in enumerate(bookmarks, start=1):
        url = bm["href"]
        extended = bm.get("extended", "") or ""
        tags = bm.get("tags", "")
        saved_time = bm.get("time")

        print(f"\n[{idx} / {total}] Processing:", url)

        if (
            ARCHIVED_MARKER in extended
            or "archive.org" in url
            or "archive.is" in url
            or "archive.fo" in url
        ):
            print("Already archived, skipping")
            continue

        if LINKROT_TAG in tags:
            print("Already tried archiving, skipping")
            continue

        timestamp = pinboard_to_archive_time_formatter(saved_time)

        print("  --> Search for closest snapshot at archive.org")
        archived = closest_archive_snapshot(url, timestamp)

        if not archived:
            print("  --> No snapshot found, checking site availability")
            if site_is_online(url):
                archived = save_to_archive(url)
            else:
                print("  X Site appears offline")

        update_pinboard(bm, archived)
        time.sleep(SLEEP_SECONDS)


if __name__ == "__main__":
    main()
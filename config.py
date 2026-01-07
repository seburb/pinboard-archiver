import os
from dotenv import load_dotenv

load_dotenv()

ARCHIVE_API_CDX  = "https://web.archive.org/cdx/search/cdx"
ARCHIVE_API_SAVE = "https://web.archive.org/save"
PINBOARD_API_ALL = "https://api.pinboard.in/v1/posts/all"
PINBOARD_API_ADD = "https://api.pinboard.in/v1/posts/add"

PINBOARD_API_TOKEN = os.getenv("PINBOARD_API_TOKEN")

PAGE_SIZE = 500
SLEEP_SECONDS = 5

ARCHIVED_MARKER = "Archived at:"
ARCHIVED_TAG = "archived"
LINKROT_TAG = "_possible_linkrot"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

LOG_FILE = "pinboard_archiver.log"
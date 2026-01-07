# Pinboard Archiver
> 404 is the loneliest number

Pinboard Archiver is a script that automatically archives the web content of every bookmark saved in [Pinboard.in](https://pinboard.in/)

Pinboard does offer an archival service itself, this project does not aim to replace it but to add redundancy and to ensure bookmarks are preserved even if the original site or the complete service goes offline. Plus: Snapshots saved to archive.org are publicly accessible.

## How It Works
Every bookmark from pinboard.in is loaded for the user with the given API token. If not archived yet, the script queries the CDX API of archive.org for snapshots close to the timestamp of the bookmark.

If no snapshot exist and the website is still available pinbord-archiver creates a snapshot in archive.org and adds the link to the bookmark's description and tags it as archived.

If the bookmarked site is offline and there is no snapshot available, the site is marked as linkrot.

The script is meant to be used in a cronjob or to be run manually.

Errors are logged to a log file, progress and status can be monitored via stdout.

## Setup and Usage
Get your secret token from [Pinboard's settings](https://pinboard.in/settings/password), add it to an `.env` or provide it as environment variable at runtime.

Change constants and names in `configs.py` to adapt to your needs.

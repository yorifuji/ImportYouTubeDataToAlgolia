# Import YouTube Data to Algolia

Importing uploaded video data from YouTube channels into Algolia.

# Requirement

- Python 3.x or Docker

# Setup

- Set Your Environment Info in `.env`
  - `DEVELOPER_KEY`
    - YouTube Data API KEY, https://developers.google.com/youtube/v3/getting-started
  - `ALGOLIA_APP_ID`
  - `ALGOLIA_API_KEY`
  - `ALGOLIA_INDEX_NAME`
    - Algolia https://www.algolia.com/doc/guides/getting-started/quick-start/

# Usage

local

> pip install -r requirements.txt && python import_youtube_data_to_algolia.py <channel_id>

Docker

> make build && make run <channeld_id>

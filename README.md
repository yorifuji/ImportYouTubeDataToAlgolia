# Import YouTube Data to Algolia

Importing uploaded video data from YouTube channels into Algolia.

# Requirement

- Python 3.x

# Setup

- `pip install -r requirements.txt`
- Set Your Environment Info in `.env`
    - YouTube Data API, API KEY
        - https://developers.google.com/youtube/v3/getting-started
        - `DEVELOPER_KEY`
    - Algolia
        - https://www.algolia.com/doc/guides/getting-started/quick-start/
        - `ALGOLIA_APP_ID`
        - `ALGOLIA_API_KEY`
        - `ALGOLIA_INDEX_NAME`

# Usage

- `python import_youtube_data_to_algolia.py [channel_id]`

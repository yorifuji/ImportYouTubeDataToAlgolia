# -*- coding: utf-8 -*-

import json
import datetime
from os import getenv
import sys

from dotenv import load_dotenv, find_dotenv
import googleapiclient.discovery
from algoliasearch.search_client import SearchClient

load_dotenv(find_dotenv())

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = getenv('DEVELOPER_KEY')
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)


ALGOLIA_APP_ID = getenv('ALGOLIA_APP_ID')
ALGOLIA_API_KEY = getenv('ALGOLIA_API_KEY')
ALGOLIA_INDEX_NAME = getenv('ALGOLIA_INDEX_NAME')


# python - How do you split a list into evenly sized chunks? - Stack Overflow
# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_uploads_playlist_id(channelId):
    request = youtube.channels().list(
        part="contentDetails",
        id=channelId,
        fields="items/contentDetails/relatedPlaylists/uploads"
    )
    response = request.execute()
    return response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]


def get_video_id_in_playlist(playlistId):
    video_id_list = []

    request = youtube.playlistItems().list(
        part="snippet",
        maxResults=50,
        playlistId=playlistId,
        fields="nextPageToken,items/snippet/resourceId/videoId"
    )

    while request:
        response = request.execute()
        video_id_list.extend(list(
            map(lambda item: item["snippet"]["resourceId"]["videoId"], response["items"])))
        request = youtube.playlistItems().list_next(request, response)

    return video_id_list


def get_video_items(video_id_list):
    video_items = []

    chunk_list = list(chunks(video_id_list, 50))  # max 50 id per request.
    for chunk in chunk_list:
        video_ids = ",".join(chunk)
        request = youtube.videos().list(
            part="snippet,statistics",
            id=video_ids,
            fields="items(id,snippet(title,description,publishedAt,thumbnails),statistics(viewCount,likeCount))"
        )
        response = request.execute()
        video_items.extend(response["items"])

    return video_items


def get_best_image_url(item):
    qualities = ['maxres', 'standard', 'high', 'medium', 'default']
    for quality in qualities:
        if quality in item['snippet']['thumbnails'].keys():
            return item['snippet']['thumbnails'][quality]['url']
    return ''


def make_publishiedAt_unixtime(item):
    return int(datetime.datetime.fromisoformat(item["snippet"]["publishedAt"].replace('Z', '+00:00')).timestamp())


def make_embed_url(item):
    return 'https://www.youtube.com/embed/%s' % item["id"]


def convertToJSON(video_items):
    return list(map(lambda item: {
        'id': item["id"],
        'title': item["snippet"]["title"],
        'description': item["snippet"]["description"],
        'publishedAt': item["snippet"]["publishedAt"],
        'publishedAtUnixTime': make_publishiedAt_unixtime(item),
        'views': int(item["statistics"]["viewCount"]) if 'viewCount' in item["statistics"].keys() else 0,
        'likes': int(item["statistics"]["likeCount"]) if 'likeCount' in item["statistics"].keys() else 0,
        'image': get_best_image_url(item),
        'url': make_embed_url(item),
    }, video_items))


def generateAlgoliaObjects(json_items):
    objects = json_items[:]
    for object in objects:
        object['objectID'] = object["id"]
    return objects


def save_to_algolia(objects):
    client = SearchClient.create(ALGOLIA_APP_ID, ALGOLIA_API_KEY)
    index = client.init_index(ALGOLIA_INDEX_NAME)

    index.save_objects(objects).wait()

    # set searchable attributes and languages.
    index.set_settings({
        'searchableAttributes': [
            'title',
            'description'
        ],
        'indexLanguages': ['ja'],
        'queryLanguages': ['ja'],
    }).wait()

    # objects = index.search('カレー',  {'hitsPerPage': 1})
    # print_json(objects, sort_keys=False)


def print_json(jsonObject, sort_keys=True):
    print(json.dumps(jsonObject, sort_keys=sort_keys, indent=2, ensure_ascii=False))


def main(channelId):
    uploads_playlist_id = get_uploads_playlist_id(channelId)
    video_id_list = get_video_id_in_playlist(uploads_playlist_id)
    video_item_list = get_video_items(video_id_list)
    # print_json(video_item_list)

    video_item_json = convertToJSON(video_item_list)
    # print_json(video_item_json, sort_keys=False)

    objects = generateAlgoliaObjects(video_item_json)
    # print_json(objects)

    save_to_algolia(objects)


if __name__ == "__main__":
    main(sys.argv[1])

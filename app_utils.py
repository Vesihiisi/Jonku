import json
import time

import flickr_api as flickr


def load_json(filepath):
    return json.load(open(filepath))


def process_keys(keys):
    return keys.split()


def get_current_time():
    return int(time.time())


def get_timestamp_days_ago(days):
    current = get_current_time()
    days_in_seconds = int(days) * 86400
    return str(current - days_in_seconds)


def get_photo_info(photo):
    photo_dict = {}
    photo_info = photo.getInfo()
    photo_dict["url"] = photo_info["urls"]["url"][0]["text"]
    photo_dict["title"] = photo.title
    photo_dict["uploaded"] = photo_info["dateuploaded"]
    photo_dict["geo"] = photo_info.get("location")
    photo_dict["user"] = {}
    photo_dict["user"]["username"] = photo_info["owner"].username
    photo_dict["user"]["profile"] = photo_info["owner"].getProfileUrl()
    return photo_dict


def make_walker(arguments):
    return flickr.Walker(flickr.Photo.search,
                         text=arguments["keyword"],
                         license="4,5",
                         min_upload_date=arguments["since"],
                         has_geo=arguments["geo"])

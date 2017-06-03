import json
import time

import flask as f
import flickr_api as flickr

CREDENTIALS_PATH = "config.json"

DEFAULT_DAYS = 1

app = f.Flask(__name__)


def load_api_credentials():
    return json.load(open(CREDENTIALS_PATH))


def process_keys(keys):
    return keys.split()


def get_current_time():
    return int(time.time())


def get_timestamp_days_ago(days):
    current = get_current_time()
    days_in_seconds = int(days) * 86400
    return str(current - days_in_seconds)


def make_walker(arguments):
    return flickr.Walker(flickr.Photo.search,
                         text=arguments["keyword"],
                         license="4,5",
                         min_upload_date=arguments["since"],
                         has_geo=arguments["geo"])


def process_query():
    arguments = {}
    arguments["tags"] = process_keys(f.request.args.get('keys'))
    arguments["since"] = get_timestamp_days_ago(
        f.request.args.get('days') or DEFAULT_DAYS)
    geo = f.request.args.get('geo')
    if geo.lower() == "true":
        arguments["geo"] = True
    else:
        arguments["geo"] = False
    return arguments


@app.route('/api/search', methods=['GET'])
def search():
    credentials = load_api_credentials()
    flickr.set_keys(api_key=credentials["api_key"],
                    api_secret=credentials["api_secret"])
    query = process_query()
    hits = []
    for tag in query["tags"]:
        arguments = {"keyword": tag,
                     "since": query["since"],
                     "geo": query["geo"]
                     }
        print(arguments)
        walker = make_walker(arguments)
        for x in range(0, 2):
            photo = walker.next()
            photo_info = photo.getInfo()
            url = photo_info["urls"]["url"][0]["text"]
            title = photo.title
            uploaded = photo_info["dateuploaded"]
            photo_info = {"title": title,
                          "url": url,
                          "uploaded": uploaded}
            try:
                geolocation = photo.getLocation()
                photo_info["geo"] = {
                    "lat": geolocation.latitude,
                    "lon": geolocation.longitude,
                    "country": geolocation.country["text"]}
            except flickr.flickrerrors.FlickrAPIError:
                geolocation = None
            hits.append(photo_info)
    return f.jsonify({'keys': query["tags"],
                      "since": query["since"],
                      "hits": hits})


if __name__ == '__main__':
    load_api_credentials()
    app.run(debug=True)

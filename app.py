import flask as f
import flickr_api as flickr

import app_utils as utils

CREDENTIALS_PATH = "config.json"

DEFAULT_DAYS = 1

app = f.Flask(__name__)


def process_query():
    arguments = {}
    arguments["tags"] = utils.process_keys(f.request.args.get('keys'))
    arguments["since"] = utils.get_timestamp_days_ago(
        f.request.args.get('days') or DEFAULT_DAYS)
    geo = f.request.args.get('geo')
    if geo and geo.lower() == "true":
        arguments["geo"] = True
    else:
        arguments["geo"] = False
    return arguments


@app.route('/api/user', methods=['GET'])
def user():
    credentials = utils.load_json(CREDENTIALS_PATH)
    flickr.set_keys(api_key=credentials["api_key"],
                    api_secret=credentials["api_secret"])
    username = f.request.args.get('username')
    person = flickr.Person.findByUserName(username)
    photos = person.getPublicPhotos()
    return f.jsonify({
        "result": username})


@app.route('/api/search', methods=['GET'])
def search():
    credentials = utils.load_json(CREDENTIALS_PATH)
    flickr.set_keys(api_key=credentials["api_key"],
                    api_secret=credentials["api_secret"])
    query = process_query()
    hits = []
    for tag in query["tags"]:
        arguments = {"keyword": tag,
                     "since": query["since"],
                     "geo": query["geo"]
                     }
        walker = utils.make_walker(arguments)
        walker_length = walker.__len__()
        if walker_length == 0:
            return "nope"
        else:
            for x in range(walker_length):
                # for x in range(3):
                photo = walker.next()
                photo_info = utils.get_photo_info(photo)
                hits.append(photo_info)
    return f.jsonify({'keys': query["tags"],
                      "since": query["since"],
                      "hits": hits})


if __name__ == '__main__':
    app.run(debug=True)

import flask as f
import flickr_api as flickr

import app_utils as utils

CREDENTIALS_PATH = "config.json"

DEFAULT_DAYS = 1

app = f.Flask(__name__)


def process_query():
    arguments = {}
    tags = f.request.args.get('keys')
    arguments["min_upload_date"] = utils.get_timestamp_days_ago(
        f.request.args.get('days') or DEFAULT_DAYS)
    geo = f.request.args.get('geo')
    user = f.request.args.get('user')
    if geo and geo.lower() == "true":
        arguments["has_geo"] = True
    if user:
        person = flickr.Person.findByUserName(user)
        arguments["user_id"] = person.id
    if tags:
        arguments["text"] = utils.process_keys(tags)
    arguments["license"] = "4,5"
    print(arguments)
    return arguments


@app.route('/api/search', methods=['GET'])
def search():
    credentials = utils.load_json(CREDENTIALS_PATH)
    flickr.set_keys(api_key=credentials["api_key"],
                    api_secret=credentials["api_secret"])
    query = process_query()
    walkers = utils.construct_walkers(query)
    print("created {} walkers".format(len(walkers)))
    hits = []
    for w in walkers:
        walker_length = w.__len__()
        print("Walker with {} items.".format(walker_length))
        if walker_length == 0:
            pass
        else:
            for x in range(walker_length):
                photo = w.next()
                print(photo.title)
                photo_info = utils.get_photo_info(photo)
                hits.append(photo_info)
    return f.jsonify({"_query": query, "hits": hits})


if __name__ == '__main__':
    app.run(debug=True)

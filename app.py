import json
import flask as f
import flickr_api as flickr

CREDENTIALS_PATH = "config.json"

DEFAULT_HOURS = 24

app = f.Flask(__name__)


def load_api_credentials():
    return json.load(open(CREDENTIALS_PATH))


def process_keys(keys):
    return keys.split()


def make_walker(arguments):
    return flickr.Walker(flickr.Photo.search,
                         text=arguments["keyword"],
                         license="4,5")


@app.route('/api/search', methods=['GET'])
def search():
    credentials = load_api_credentials()
    flickr.set_keys(api_key=credentials["api_key"],
                    api_secret=credentials["api_secret"])
    tags = process_keys(f.request.args.get('keys'))
    hits = []
    for tag in tags:
        arguments = {"keyword": tag}
        walker = make_walker(arguments)
        for x in range(0, 10):
            photo = walker.next()
            photo_info = photo.getInfo()
            url = photo_info["urls"]["url"][0]["text"]
            title = photo.title
            # geolocation = photo.getLocation()
            uploaded = photo_info["dateuploaded"]
            hits.append({"title": title, "url": url, "uploaded": uploaded})
    return f.jsonify({'keys': tags, "hits": hits})


if __name__ == '__main__':
    load_api_credentials()
    app.run(debug=True)

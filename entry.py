import os
from flask import Flask
from flask_caching import Cache
import anilist

dirname = os.path.dirname(__file__)

config = {
    "CACHE_TYPE": "filesystem",
    "CACHE_DIR": os.path.join(dirname, "tmp"),
    "CACHE_DEFAULT_TIMEOUT": 300,
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
client = anilist.Client()
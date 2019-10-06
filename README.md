# Music Transliterator

Run with `FLASK_ENV=development FLASK_APP=app.py flask run`.

## Requirements
- MongoDB
- Yahoo Japan Morphological Analysis API key
- Python 3

## Python 3 dependencies

```
pip3 install -U flask flask_mongoengine mutagen flask_cors pypinyin
```

## `config.cfg`

```
MONGODB_SETTINGS = {
    'db': 'database_name',  # name of mongodb database
    'host': 'mongodb+srv://username:password@host/database_name'  # URL to the database
}

YAHOO_JP_APP_ID = "Yahoo Japan Morphological Analysis API key"

MUSIC_PATH = "/home/blueset/Music"  # path to music files
```
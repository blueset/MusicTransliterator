from flask import Flask, render_template, request
from flask_mongoengine import MongoEngine
from database import db, Music
from tag_editor import filter_extensions, MusicTag
from typing import Iterable
from datetime import datetime
from flask_cors import CORS
from transliterator import PinyinTransliterator, HiraganaTransliterator

import glob
import json

app = Flask(__name__, static_url_path='',
            static_folder='music-transliterator/dist')
CORS(app)
app.config.from_pyfile('config.cfg')
db.init_app(app)
HiraganaTransliterator.set_app_id(app.config['YAHOO_JP_APP_ID'])


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/refresh')
def refresh():
    files = set(filter_extensions(
        glob.glob(app.config['MUSIC_PATH'] + '/**/*', recursive=True)
    ))
    old_files: Iterable[Music] = Music.objects

    for i in old_files:
        if i.file in files:
            tag = MusicTag(i.file)
            if i.title != tag.title or \
                i.album != tag.album or \
                i.artist != tag.artist:
                i.reviewed = False
                i.last_scan = i.last_update = datetime.now()
            i.title = tag.title
            i.album = tag.album
            i.artist = tag.artist
            i.title_key = tag.title_sort
            i.artist_key = tag.artist_sort
            i.album_key = tag.album_sort
            i.save()
            files.remove(i.file)
        else:
            i.delete()
    
    for i in files:
        tag = MusicTag(i)
        # dump(i)
        # dump(tag)
        entry = Music(
            file = i,
            title = tag.title,
            artist = tag.artist,
            album = tag.album,
            title_key = tag.artist_sort,
            artist_key = tag.artist_sort,
            album_key = tag.album_sort
        )
        entry.save()

    return {
        "status": "ok"
    }
                
@app.route('/songs', methods=['GET'])
def load_songs():
    data = [json.loads(i.to_json()) for i in Music.objects]
    return {
        "status": "ok",
        "data": data
    }


@app.route('/songs/<song_id>', methods=['GET'])
def get_song(song_id):
    entry: Music = Music.objects.get_or_404(id=song_id)
    return {
        "status": "ok",
        "data": json.loads(entry.to_json())
    }

@app.route('/songs/<song_id>', methods=['POST'])
def update_song(song_id):
    entry: Music = Music.objects.get_or_404(id=song_id)
    update = request.json
    if 'title' in update:
        entry.title = str(update['title'])
    if 'album' in update:
        entry.album = str(update['album'])
    if 'artist' in update:
        entry.artist = str(update['artist'])
    if 'title_key' in update:
        entry.title_key = str(update['title_key'])
    if 'album_key' in update:
        entry.album_key = str(update['album_key'])
    if 'artist_key' in update:
        entry.artist_key = str(update['artist_key'])
    entry.reviewed = True
    entry.last_update = datetime.now()

    tag = MusicTag(entry.file)
    tag.title = str(update['title'])
    tag.album = str(update['album'])
    tag.artist = str(update['artist'])
    tag.title_sort = str(update['title_key'])
    tag.album_sort = str(update['album_key'])
    tag.artist_sort = str(update['artist_key'])
    tag.save()

    entry.save()
    return {
        "status": "ok",
        "data": json.loads(entry.to_json())
    }


@app.route('/transliterate/zh')
def transliterate_zh():
    text = request.args.get('text', '')
    return PinyinTransliterator.transiterate(text)


@app.route('/transliterate/ja')
def transliterate_ja():
    text = request.args.get('text', '')
    return HiraganaTransliterator.transiterate(text)

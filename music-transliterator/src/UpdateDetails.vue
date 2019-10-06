<template>
    <v-ons-page>
        <v-ons-toolbar>
            <div class="left">
                <v-ons-back-button>Songs</v-ons-back-button>
            </div>
            <div class="center">Edit song #{{index}}: {{item.title}} </div>
            <div class="right">
                <v-ons-icon icon="md-check-circle" class="list-item__icon" v-if="item.reviewed" style="color: #4CAF50"></v-ons-icon>
            </div>
        </v-ons-toolbar>

        <v-ons-list>
            <v-ons-list-item>
                File: {{ item.file }}
            </v-ons-list-item>
            <v-ons-list-item>
                <div class="center">
                    <v-ons-input placeholder="Title" float v-model="item.title" modifier="material"></v-ons-input>
                </div>
            </v-ons-list-item>
            <v-ons-list-item>
                <div class="center">
                    <v-ons-input placeholder="Title key" float v-model="item.title_key" modifier="material"></v-ons-input>
                </div>
            </v-ons-list-item>
            <v-ons-list-item>
                <div class="center">
                    <v-ons-input placeholder="Artist" float v-model="item.artist" modifier="material"></v-ons-input>
                </div>
            </v-ons-list-item>
            <v-ons-list-item>
                <div class="center">
                    <v-ons-input placeholder="Artist key" float v-model="item.artist_key" modifier="material"></v-ons-input>
                </div>
            </v-ons-list-item>
            <v-ons-list-item>
                <div class="center">
                    <v-ons-input placeholder="Album" float v-model="item.album" modifier="material"></v-ons-input>
                </div>
            </v-ons-list-item>
            <v-ons-list-item>
                <div class="center">
                    <v-ons-input placeholder="Album key" float v-model="item.album_key" modifier="material"></v-ons-input>
                </div>
            </v-ons-list-item>
            <v-ons-list-item>
                <div class="flex-r" style="width: 100%">
                    <v-ons-button :disabled="index === 0" @click="prev" modifier="light">
                        <v-ons-icon icon="md-chevron-left"></v-ons-icon>
                    </v-ons-button>
                    <div class="flex-c" style="flex-grow: 1">
                        <div class="flex-r">
                            <v-ons-button @click="fillZh" modifier="outline" style="flex-grow: 1">zh</v-ons-button>
                            <v-ons-button @click="fillJa" modifier="outline" style="flex-grow: 1">ja</v-ons-button>
                            <v-ons-button @click="clear" modifier="outline" style="flex-grow: 1"><v-ons-icon icon="md-close"></v-ons-icon></v-ons-button>
                        </div>
                        <v-ons-button @click="submit" :disabled="saving">
                            <v-ons-icon icon="md-floppy" v-if="!saving"></v-ons-icon>
                            <v-ons-icon spin icon="md-spinner" v-if="saving"></v-ons-icon>
                        </v-ons-button>
                    </div>
                    <v-ons-button :disabled="index === items.length - 1" @click="next" modifier="light">
                        <v-ons-icon icon="md-chevron-right"></v-ons-icon>
                    </v-ons-button>
                </div>
            </v-ons-list-item>
        </v-ons-list>
    </v-ons-page>
</template>

<script>
import axios from 'axios';
import qs from 'qs';

export default {
    data() {
        return {
            saving: false
        }
    },
    methods: {
        prev() {
            if (this.index > 0) {
                this.item = this.items[--this.index];
            }
        },
        next() {
            if (this.index < this.items.length - 1) {
                this.item = this.items[++this.index];
            }
        },
        clear() {
            this.item.title_key = "";
            this.item.artist_key = "";
            this.item.album_key = "";
        },
        buildQuery(text) {
            return qs.stringify({text: text});
        },
        fillZh() {
            var self = this;
            axios.get('transliterate/zh?' + this.buildQuery(this.item.title), {
                responseType: 'text'
            }).then((result) => {
                self.item.title_key = result.data;
            });
            axios.get('transliterate/zh?' + this.buildQuery(this.item.album), {
                responseType: 'text'
            }).then((result) => {
                self.item.album_key = result.data;
            });
            axios.get('transliterate/zh?' + this.buildQuery(this.item.artist), {
                responseType: 'text'
            }).then((result) => {
                self.item.artist_key = result.data;
            });
        },
        fillJa() {
            var self = this;
            axios.get('transliterate/ja?' + this.buildQuery(this.item.title), {
                responseType: 'text'
            }).then((result) => {
                self.item.title_key = result.data;
            });
            axios.get('transliterate/ja?' + this.buildQuery(this.item.album), {
                responseType: 'text'
            }).then((result) => {
                self.item.album_key = result.data;
            });
            axios.get('transliterate/ja?' + this.buildQuery(this.item.artist), {
                responseType: 'text'
            }).then((result) => {
                self.item.artist_key = result.data;
            });
        },
        submit() {
            this.saving = true;
            var self = this;
            axios.post('./songs/' + this.item._id.$oid, {
                title: this.item.title,
                title_key: this.item.title_key,
                artist: this.item.artist,
                artist_key: this.item.artist_key,
                album: this.item.album,
                album_key: this.item.album_key,
            }).then((result) => {
                Object.assign(self.item, result.data.data);
                this.saving = false;
            }); //.catch(() => {this.saving = false; console.log('Failed.')});
        }
    }
}
</script>

<style>
ons-input {
    width: 100%;
}

ons-button {
    margin: 5px;
}

.flex-r {
    display: flex;
    flex-direction: row;
}

.flex-c {
    display: flex;
    flex-direction: column;
}
</style>


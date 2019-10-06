<template page="app">
  <v-ons-page>
    <v-ons-toolbar>
      <div class="left">
        <v-ons-toolbar-button @click="refresh">
          <v-ons-icon icon="md-refresh" v-if="!refreshing"></v-ons-icon>
          <v-ons-icon spin icon="md-spinner" v-if="refreshing"></v-ons-icon>
        </v-ons-toolbar-button>
      </div>
      <div class="center">Songs</div>
      <div class="right">
        <v-ons-toolbar-button @click="showFilterSheet = true">
          <v-ons-icon icon="md-filter-list"></v-ons-icon>
        </v-ons-toolbar-button>
      </div>
    </v-ons-toolbar>
    <v-ons-list>
      <v-ons-lazy-repeat
        :render-item="renderItem"
        :length="listSize"
        :calculate-item-height="() => {return 120;}"
      >
      </v-ons-lazy-repeat>
    </v-ons-list>

    <v-ons-action-sheet
      :visible.sync="showFilterSheet"
      cancelable
      title="Filter"
      modifier="material"
    >
      <v-ons-action-sheet-button :icon="showReviewed ? 'md-square-o' : 'md-check-square'"
        @click="showReviewed = !showReviewed; rerender()">
        Reviewed {{ showReviewed ? 'shown' : 'hidden' }}
      </v-ons-action-sheet-button>
      <v-ons-action-sheet-button :icon="showUnreviewed ? 'md-square-o' : 'md-check-square'"
        @click="showUnreviewed = !showUnreviewed; rerender()">
        Unreviewed {{ showUnreviewed ? 'shown' : 'hidden' }}
      </v-ons-action-sheet-button>
    </v-ons-action-sheet>
  </v-ons-page>
</template>

<script>
import axios from 'axios';
import Vue from 'vue';
import UpdateDetails from './UpdateDetails.vue';

export default {
  data () {
    return {
      items: [],
      showReviewed: false,
      showUnreviewed: true,
      showFilterSheet: false,
      refreshing: true
    }
  },
  computed: {
    shownItems() {
      return this.items.filter((item) => (this.showReviewed && item.reviewed) || (this.showUnreviewed && !item.reviewed));
    },
    listSize() {
      return this.shownItems.length;
    }
  },
  methods: {
    reload() {
      axios.get('./songs')
          .then(resp => {
              this.items = resp.data.data;
              this.refreshing = false;
          });
    },
    refresh() {
      var self = this;
      this.refreshing = true;
      axios.get('./refresh')
        .then(() => {
            self.reload();
        });
    },
    showSongDetails(index, item) {
      var self = this;
      this.$emit('push-page', {
        extends: UpdateDetails,
        data() {
          return {
            item: item,
            items: self.shownItems,
            index: index
          }
        }
      });
    },
    rerender() {
      this.$emit('refresh');
    },
    renderItem(index) {
      var self = this;
      return new Vue({
        template: `<v-ons-list-item
          :key="item._id.$oid" tappable @click="showSongDetails(index, item)">
          <div class="center">
            <span class="list-item__title">{{ item.title }}</span>
            <span class="list-item__subtitle">{{ item.artist }}</span>
            <span class="list-item__subtitle">{{ item.album }}</span>
          </div>
          <div class="right">
            <v-ons-icon icon="md-check-circle" class="list-item__icon" v-if="item.reviewed" style="color: #4CAF50"></v-ons-icon>
          </div>
        </v-ons-list-item>`,
        data() {
          return {
            item: self.shownItems[index],
            index: index,
            showSongDetails(index, item) {
              self.$emit('push-page', {
                extends: UpdateDetails,
                data() {
                  return {
                    item: item,
                    items: self.shownItems,
                    index: index
                  }
                }
              });
            }
          }
        }
        // Set item data using 'index'
      });
    }
  },
  mounted () {
    this.reload();
  }
}
</script>

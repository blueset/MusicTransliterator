<template>
  <v-ons-navigator swipeable 
    :page-stack="pageStack"
    @push-page="pageStack.push($event)">
  </v-ons-navigator>
</template>

<script>
import List from './List.vue';

export default {
  template: "#main",
  data() {
    return {
      pageStack: [List]
    }
  }
}
</script>

<style>
</style>

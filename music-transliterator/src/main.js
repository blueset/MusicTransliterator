import Vue from 'vue'
import App from './App.vue'

// Webpack CSS import
import 'onsenui/css/onsenui.css';
import 'onsenui/css/onsen-css-components.css';

import VueOnsen from 'vue-onsenui'; // This imports 'onsenui', so no need to import it separately

Vue.config.productionTip = false



Vue.use(VueOnsen); // VueOnsen set here as plugin to VUE. Done automatically if a call to window.Vue exists in the startup code.

new Vue({
  render: h => h(App),
  beforeCreate() {
    // this.$ons.platform.select('android');
  }
}).$mount('#app')

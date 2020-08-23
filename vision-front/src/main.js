import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify';
import router from './router'

import VueSpeech from 'vue-speech'

Vue.config.productionTip = false
Vue.use(VueSpeech)
new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')

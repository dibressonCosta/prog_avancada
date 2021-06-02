import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
//import VueResource from 'vue-resource'
import VueTextareaAutosize from 'vue-textarea-autosize'
//import Axios from 'axios'
import "./assets/styles.scss";

Vue.use(VueTextareaAutosize);

Vue.config.productionTip = false

new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')

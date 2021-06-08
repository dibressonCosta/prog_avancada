import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
//import VueResource from 'vue-resource'
import VueTextareaAutosize from 'vue-textarea-autosize'
//import Axios from 'axios'
import "./assets/styles.scss";
import VueSweetalert2 from 'vue-sweetalert2';
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'sweetalert2/dist/sweetalert2.min.css';

const options = {
  confirmButtonColor: '#EF5350',
  cancelButtonColor: '#ff7674',
};

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.use(VueSweetalert2, options);
Vue.use(VueTextareaAutosize);

Vue.config.productionTip = false

new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')

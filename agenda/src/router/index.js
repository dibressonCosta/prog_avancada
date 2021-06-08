import Vue from 'vue'
import VueRouter from 'vue-router'
import Agenda from '../views/Agenda.vue'
import Login from '../views/Login.vue'
import Cadastro from '../views/Cadastro.vue'
import axios from 'axios';

axios.defaults.headers.common["Content-Type"] = "application/json";
axios.defaults.headers.common["Access-Control-Allow-Origin"] = "*";
function AdminAuth(to,from,next){
  if(localStorage.getItem('token') != undefined){
    var dados = {
      email: localStorage.getItem('email'),
      id: localStorage.getItem('id'),
    }
    axios.defaults.headers.common = {'Authorization': `bearer ${localStorage.getItem('token')}`}
    axios.post("http://localhost:5000/validate",dados).then(res=>{
      console.log(res)
      next();
    }).catch(err =>{
      localStorage.clear();
      console.log(err.response)
      next("/login");
    })
  }else{
    next("/login");
    localStorage.clear();
  }
}
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Agenda',
    component: Agenda,
    beforeEnter: AdminAuth
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/cadastro',
    name: 'Cadastro',
    component: Cadastro
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router

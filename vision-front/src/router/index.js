import Vue from "vue";
import Router from "vue-router";
import Service from '@/container/Service';


const Dashboard = () => import('@/components/HelloWorld');
Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
  {path: "/",
  component: Service,
  children: [
  {
    path: '',
    name: "dashboard",
    components: {default: Dashboard }
  },
  {
    path: '/test',
    name: "dashboard",
    components: {default: Dashboard }
  },
  ]}
  ]
})

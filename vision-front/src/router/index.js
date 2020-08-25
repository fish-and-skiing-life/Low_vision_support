import Vue from "vue";
import Router from "vue-router";
import Service from '@/container/Service';


const Dashboard = () => import('@/components/HelloWorld');
const Category = () => import('@/components/Category');
const News = () => import('@/components/News');
const NewsList = () => import('@/components/NewsList');
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
    path: '/category',
    name: "category",
    components: {default: Category }
  },
  {
    path: '/news-list',
    name: "news-list",
    components: {default: NewsList }
  },
  {
    path: '/news',
    name: "news",
    components: {default: News }
  },
  ]}
  ]
})

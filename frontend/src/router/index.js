// frontend/src/router/index.js
import { createRouter, createWebHistory } from "vue-router"
import InstrumentList from "../views/InstrumentList.vue"
import InstrumentDetail from "../views/InstrumentDetail.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "instruments",
      component: InstrumentList
    },
    {
      path: "/instruments/:id",
      name: "instrumentDetail",
      component: InstrumentDetail,
      props: true
    }
  ]
})

export default router

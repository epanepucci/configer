// frontend/src/router/index.js
import { createRouter, createWebHistory } from "vue-router";

// Import views
const InstrumentList = () => import("../views/InstrumentList.vue");
const InstrumentDetail = () => import("../views/InstrumentDetail.vue");

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "instruments",
      component: InstrumentList,
    },
    {
      path: "/instruments/:id",
      name: "instrumentDetail",
      component: InstrumentDetail,
      props: true,
    },
  ],
});

export default router;

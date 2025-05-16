// frontend/src/main.js
import { createApp } from "vue"
import { createPinia } from "pinia"
import App from "./App.vue"
import router from "./router"

// PrimeVue
import PrimeVue from "primevue/config"
import Button from "primevue/button"
import InputText from "primevue/inputtext"
import Dropdown from "primevue/dropdown"
import DataTable from "primevue/datatable"
import Column from "primevue/column"
import Dialog from "primevue/dialog"
import Toast from "primevue/toast"
import ToastService from "primevue/toastservice"
import TabView from "primevue/tabview"
import TabPanel from "primevue/tabpanel"

// PrimeVue styles
import "primevue/resources/themes/lara-light-blue/theme.css"
import "primevue/resources/primevue.min.css"
import "primeicons/primeicons.css"
import "primeflex/primeflex.css"

const app = createApp(App)

// Setup Pinia
app.use(createPinia())
app.use(router)

// Setup PrimeVue
app.use(PrimeVue)
app.use(ToastService)

// Register PrimeVue components
app.component("Button", Button)
app.component("InputText", InputText)
app.component("Dropdown", Dropdown)
app.component("DataTable", DataTable)
app.component("Column", Column)
app.component("Dialog", Dialog)
app.component("Toast", Toast)
app.component("TabView", TabView)
app.component("TabPanel", TabPanel)

app.mount("#app")

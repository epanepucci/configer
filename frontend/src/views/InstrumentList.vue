<template>
    <div class="instruments-container">
        <div class="p-d-flex p-jc-between p-ai-center mb-3">
            <h2>Instruments</h2>
            <Button
                label="Add Instrument"
                icon="pi pi-plus"
                @click="openNewDialog"
            />
        </div>

        <DataTable
            :value="instruments"
            :loading="loading"
            v-model:selection="selectedInstrument"
            selectionMode="single"
            dataKey="id"
            class="p-datatable-sm"
            :paginator="instruments.length > 10"
            :rows="10"
            :rowHover="true"
            responsiveLayout="scroll"
        >
            <Column field="id" header="ID" sortable></Column>
            <Column field="name" header="Name" sortable></Column>
            <Column field="type" header="Type" sortable></Column>
            <Column field="location" header="Location" sortable></Column>
            <Column field="last_updated" header="Last Updated" sortable>
                <template #body="slotProps">
                    {{ formatDate(slotProps.data.last_updated) }}
                </template>
            </Column>
            <Column header="Actions">
                <template #body="slotProps">
                    <Button
                        icon="pi pi-cog"
                        class="p-button-text p-button-sm"
                        @click="navigateToDetail(slotProps.data)"
                    />
                </template>
            </Column>
        </DataTable>

        <!-- New Instrument Dialog -->
        <Dialog
            v-model:visible="displayNewDialog"
            header="Add New Instrument"
            :modal="true"
            :closable="true"
            :style="{ width: '450px' }"
        >
            <div class="p-fluid">
                <div class="field">
                    <label for="id">ID</label>
                    <InputText id="id" v-model="newInstrument.id" />
                </div>
                <div class="field">
                    <label for="name">Name</label>
                    <InputText id="name" v-model="newInstrument.name" />
                </div>
                <div class="field">
                    <label for="type">Type</label>
                    <InputText id="type" v-model="newInstrument.type" />
                </div>
                <div class="field">
                    <label for="location">Location</label>
                    <InputText id="location" v-model="newInstrument.location" />
                </div>
            </div>
            <template #footer>
                <Button
                    label="Cancel"
                    icon="pi pi-times"
                    class="p-button-text"
                    @click="closeNewDialog"
                />
                <Button
                    label="Save"
                    icon="pi pi-check"
                    @click="saveNewInstrument"
                />
            </template>
        </Dialog>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useToast } from "primevue/usetoast";
import { useInstrumentsStore } from "../stores/instruments";

const router = useRouter();
const toast = useToast();
const instrumentsStore = useInstrumentsStore();

// Reactive state
const selectedInstrument = ref(null);
const displayNewDialog = ref(false);
const newInstrument = ref({
    id: "",
    name: "",
    type: "",
    location: "",
});

// Computed properties
const instruments = computed(() => instrumentsStore.instruments);
const loading = computed(() => instrumentsStore.loading);

// Lifecycle hooks
onMounted(async () => {
    await instrumentsStore.fetchInstruments();
});

// Methods
function navigateToDetail(instrument) {
    router.push({ name: "instrumentDetail", params: { id: instrument.id } });
}

function openNewDialog() {
    displayNewDialog.value = true;
    newInstrument.value = {
        id: "",
        name: "",
        type: "",
        location: "",
    };
}

function closeNewDialog() {
    displayNewDialog.value = false;
}

async function saveNewInstrument() {
    try {
        await instrumentsStore.createInstrument(newInstrument.value);
        toast.add({
            severity: "success",
            summary: "Success",
            detail: "Instrument created successfully",
            life: 3000,
        });
        closeNewDialog();
    } catch (error) {
        toast.add({
            severity: "error",
            summary: "Error",
            detail: error.message || "Failed to create instrument",
            life: 5000,
        });
    }
}

function formatDate(dateStr) {
    if (!dateStr) return "Never";
    const date = new Date(dateStr);
    return new Intl.DateTimeFormat("en-US", {
        year: "numeric",
        month: "short",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
    }).format(date);
}
</script>

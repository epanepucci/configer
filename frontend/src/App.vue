<!-- frontend/src/views/InstrumentList.vue -->
<template>
    <div class="instruments-container">
        <div class="p-d-flex p-jc-between p-ai-center mb-3">
            <h2>Instruments</h2>
            <button class="p-button p-component" @click="openNewDialog">
                <span
                    class="p-button-icon p-button-icon-left pi pi-plus"
                ></span>
                <span class="p-button-label">Add Instrument</span>
            </button>
        </div>

        <div v-if="instruments.length === 0" class="empty-state">
            <p>No instruments found. Click "Add Instrument" to create one.</p>
        </div>

        <div v-else>
            <!-- Table will go here -->
            <div
                v-for="instrument in instruments"
                :key="instrument.id"
                class="instrument-card"
            >
                <h3>{{ instrument.name }}</h3>
                <p>Type: {{ instrument.type }}</p>
                <p>Location: {{ instrument.location || "N/A" }}</p>
                <button
                    class="p-button p-component p-button-text"
                    @click="navigateToDetail(instrument)"
                >
                    <span class="p-button-icon pi pi-cog"></span>
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const instruments = ref([]);

function openNewDialog() {
    alert("This would open a dialog to add a new instrument");
    // For testing, let's add a dummy instrument
    instruments.value.push({
        id: "test001",
        name: "Test Instrument",
        type: "prototype",
        location: "Development Lab",
    });
}

function navigateToDetail(instrument) {
    router.push({ name: "instrumentDetail", params: { id: instrument.id } });
}
</script>

<style scoped>
.instruments-container {
    max-width: 1200px;
    margin: 0 auto;
}

.empty-state {
    padding: 2rem;
    text-align: center;
    background-color: #f8f9fa;
    border-radius: 8px;
    margin-top: 2rem;
}

.instrument-card {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 1rem;
    display: flex;
    flex-direction: column;
    background-color: white;
}
</style>

<!-- frontend/src/views/InstrumentDetail.vue (continued) -->
<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useToast } from "primevue/usetoast";
import { useInstrumentsStore } from "../stores/instruments";
import { useConfigsStore } from "../stores/configs";
import { useSnapshotsStore } from "../stores/snapshots";
import ConfigEditor from "../components/config/ConfigEditor.vue";

const route = useRoute();
const router = useRouter();
const toast = useToast();

const instrumentsStore = useInstrumentsStore();
const configsStore = useConfigsStore();
const snapshotsStore = useSnapshotsStore();

// Instrument ID from route params
const instrumentId = computed(() => route.params.id);

// Reactive state
const configData = ref({});
const hasConfigChanges = ref(false);
const originalConfig = ref({});
const saveComment = ref("");
const displaySaveDialog = ref(false);
const displayVersionDialog = ref(false);
const selectedVersion = ref(null);
const versionDetails = ref([]);
const displaySnapshotDialog = ref(false);
const newSnapshot = ref({ name: "", description: "" });
const displaySnapshotViewDialog = ref(false);
const selectedSnapshot = ref(null);
const snapshotDetails = ref([]);

// Computed properties
const instrument = computed(() =>
    instrumentsStore.getInstrumentById(instrumentId.value),
);
const loading = computed(() => instrumentsStore.loading);
const configLoading = computed(() => configsStore.loading);
const versions = computed(() => configsStore.versions);
const versionsLoading = computed(() => configsStore.loading);
const snapshots = computed(() => snapshotsStore.snapshots);
const snapshotsLoading = computed(() => snapshotsStore.loading);

// Lifecycle hooks
onMounted(async () => {
    if (!instrumentsStore.instruments.length) {
        await instrumentsStore.fetchInstruments();
    }

    await loadInstrumentData();
});

// Watch for changes in instrument ID
watch(instrumentId, async () => {
    await loadInstrumentData();
});

// Methods
async function loadInstrumentData() {
    // Reset stores
    configsStore.resetState();
    snapshotsStore.resetState();

    // Load data
    await Promise.all([
        configsStore.fetchConfig(instrumentId.value),
        configsStore.fetchVersions(instrumentId.value),
        snapshotsStore.fetchSnapshots(instrumentId.value),
    ]);

    // Set initial config data
    configData.value = JSON.parse(JSON.stringify(configsStore.currentConfig));
    originalConfig.value = JSON.parse(
        JSON.stringify(configsStore.currentConfig),
    );

    // Load version details
    await loadVersionDetails();

    // Load snapshot details
    await loadSnapshotDetails();
}

function goBack() {
    router.push({ name: "instruments" });
}

function handleConfigChange(newValue) {
    configData.value = newValue;
    hasConfigChanges.value =
        JSON.stringify(configData.value) !==
        JSON.stringify(originalConfig.value);
}

function saveConfig() {
    if (!hasConfigChanges.value) {
        toast.add({
            severity: "info",
            summary: "No Changes",
            detail: "No changes to save",
            life: 3000,
        });
        return;
    }

    displaySaveDialog.value = true;
}

async function confirmSaveConfig() {
    try {
        const result = await configsStore.updateConfig(
            instrumentId.value,
            configData.value,
            saveComment.value,
        );

        // Update local state
        originalConfig.value = JSON.parse(JSON.stringify(configData.value));
        hasConfigChanges.value = false;

        // Refresh version history
        await configsStore.fetchVersions(instrumentId.value);
        await loadVersionDetails();

        // Success message
        toast.add({
            severity: "success",
            summary: "Success",
            detail: "Configuration updated successfully",
            life: 3000,
        });

        // Close dialog
        displaySaveDialog.value = false;
        saveComment.value = "";
    } catch (error) {
        toast.add({
            severity: "error",
            summary: "Error",
            detail: error.message || "Failed to update configuration",
            life: 5000,
        });
    }
}

function downloadConfig() {
    const dataStr = JSON.stringify(configData.value, null, 2);
    const dataUri =
        "data:application/json;charset=utf-8," + encodeURIComponent(dataStr);

    const exportFileName = `${instrument.value.name}-config.json`;

    const linkElement = document.createElement("a");
    linkElement.setAttribute("href", dataUri);
    linkElement.setAttribute("download", exportFileName);
    linkElement.click();
}

async function loadVersionDetails() {
    // Get full version data for each version ID
    const versionPromises = versions.value.map((versionId) =>
        configsStore.fetchVersion(instrumentId.value, versionId),
    );

    try {
        const results = await Promise.all(versionPromises);
        versionDetails.value = results.filter(Boolean).reverse(); // Latest first
    } catch (error) {
        console.error("Error loading version details:", error);
    }
}

function viewVersion(version) {
    selectedVersion.value = version;
    displayVersionDialog.value = true;
}

function openSnapshotDialog() {
    newSnapshot.value = { name: "", description: "" };
    displaySnapshotDialog.value = true;
}

async function createSnapshot() {
    if (!newSnapshot.value.name) {
        toast.add({
            severity: "error",
            summary: "Error",
            detail: "Snapshot name is required",
            life: 3000,
        });
        return;
    }

    try {
        await snapshotsStore.createSnapshot(
            instrumentId.value,
            newSnapshot.value,
        );

        // Refresh snapshots
        await snapshotsStore.fetchSnapshots(instrumentId.value);
        await loadSnapshotDetails();

        // Success message
        toast.add({
            severity: "success",
            summary: "Success",
            detail: "Snapshot created successfully",
            life: 3000,
        });

        // Close dialog
        displaySnapshotDialog.value = false;
    } catch (error) {
        toast.add({
            severity: "error",
            summary: "Error",
            detail: error.message || "Failed to create snapshot",
            life: 5000,
        });
    }
}

async function loadSnapshotDetails() {
    // Get full snapshot data for each snapshot name
    const snapshotPromises = snapshots.value.map((snapshotName) =>
        snapshotsStore.fetchSnapshot(instrumentId.value, snapshotName),
    );

    try {
        const results = await Promise.all(snapshotPromises);
        snapshotDetails.value = results.filter(Boolean).reverse(); // Latest first
    } catch (error) {
        console.error("Error loading snapshot details:", error);
    }
}

function viewSnapshot(snapshot) {
    selectedSnapshot.value = snapshot;
    displaySnapshotViewDialog.value = true;
}

async function restoreSnapshotConfig() {
    if (!selectedSnapshot.value) return;

    try {
        // Update current config with snapshot data
        await configsStore.updateConfig(
            instrumentId.value,
            selectedSnapshot.value.data,
            `Restored from snapshot: ${selectedSnapshot.value.snapshot_name}`,
        );

        // Update local state
        configData.value = JSON.parse(
            JSON.stringify(selectedSnapshot.value.data),
        );
        originalConfig.value = JSON.parse(
            JSON.stringify(selectedSnapshot.value.data),
        );
        hasConfigChanges.value = false;

        // Refresh version history
        await configsStore.fetchVersions(instrumentId.value);
        await loadVersionDetails();

        // Success message
        toast.add({
            severity: "success",
            summary: "Success",
            detail: `Configuration restored from snapshot: ${selectedSnapshot.value.snapshot_name}`,
            life: 3000,
        });

        // Close dialog
        displaySnapshotViewDialog.value = false;
    } catch (error) {
        toast.add({
            severity: "error",
            summary: "Error",
            detail: error.message || "Failed to restore configuration",
            life: 5000,
        });
    }
}

function formatDate(dateStr) {
    if (!dateStr) return "N/A";
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

<style scoped>
.instrument-detail-container {
    max-width: 1200px;
    margin: 0 auto;
}

.change-item {
    margin-bottom: 1rem;
    padding: 0.5rem;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
}

.old-value,
.new-value {
    display: flex;
    margin-top: 0.25rem;
}

.label {
    width: 50px;
    color: #666;
}

.value {
    flex: 1;
    word-break: break-all;
}

.old-value .value {
    text-decoration: line-through;
    color: #f44336;
}

.new-value .value {
    color: #4caf50;
}
</style>

<!-- frontend/src/components/config/ConfigEditor.vue -->
<template>
    <div class="config-editor">
        <div
            v-if="!config || Object.keys(config).length === 0"
            class="empty-config"
        >
            <p>No configuration parameters yet</p>
            <Button
                v-if="!readonly"
                label="Add Parameter"
                icon="pi pi-plus"
                @click="addParameter"
            />
        </div>

        <div v-else class="config-parameters">
            <div class="parameter-controls mb-3" v-if="!readonly">
                <Button
                    label="Add Parameter"
                    icon="pi pi-plus"
                    @click="addParameter"
                />
            </div>

            <div
                v-for="(value, key) in config"
                :key="key"
                class="parameter-item p-3 mb-2"
            >
                <div class="p-grid">
                    <div class="p-col-12 p-md-3">
                        <div class="parameter-key">
                            <InputText
                                v-if="!readonly"
                                v-model="editableKeys[key]"
                                class="w-full"
                                @change="updateParameterKey(key)"
                            />
                            <strong v-else>{{ key }}</strong>
                        </div>
                    </div>

                    <div class="p-col-12 p-md-7">
                        <div class="parameter-value">
                            <!-- String value -->
                            <template v-if="typeof value === 'string'">
                                <InputText
                                    v-model="config[key]"
                                    class="w-full"
                                    :readonly="readonly"
                                    @input="emitUpdate"
                                />
                            </template>

                            <!-- Number value -->
                            <template v-else-if="typeof value === 'number'">
                                <InputNumber
                                    v-model="config[key]"
                                    class="w-full"
                                    :readonly="readonly"
                                    @input="emitUpdate"
                                />
                            </template>

                            <!-- Boolean value -->
                            <template v-else-if="typeof value === 'boolean'">
                                <ToggleButton
                                    v-model="config[key]"
                                    onLabel="True"
                                    offLabel="False"
                                    :disabled="readonly"
                                    @change="emitUpdate"
                                />
                            </template>

                            <!-- Object value (nested) -->
                            <template
                                v-else-if="
                                    typeof value === 'object' &&
                                    value !== null &&
                                    !Array.isArray(value)
                                "
                            >
                                <div class="nested-object">
                                    <ConfigEditor
                                        v-model="config[key]"
                                        :readonly="readonly"
                                        @update:modelValue="emitUpdate"
                                    />
                                </div>
                            </template>

                            <!-- Array value -->
                            <template v-else-if="Array.isArray(value)">
                                <div class="array-value">
                                    <div
                                        v-for="(item, index) in value"
                                        :key="index"
                                        class="array-item p-2 mb-1"
                                    >
                                        <div class="p-inputgroup">
                                            <!-- String item -->
                                            <template
                                                v-if="typeof item === 'string'"
                                            >
                                                <InputText
                                                    v-model="config[key][index]"
                                                    :readonly="readonly"
                                                    @input="emitUpdate"
                                                />
                                            </template>

                                            <!-- Number item -->
                                            <template
                                                v-else-if="
                                                    typeof item === 'number'
                                                "
                                            >
                                                <InputNumber
                                                    v-model="config[key][index]"
                                                    :readonly="readonly"
                                                    @input="emitUpdate"
                                                />
                                            </template>

                                            <!-- Remove button -->
                                            <Button
                                                v-if="!readonly"
                                                icon="pi pi-times"
                                                class="p-button-danger"
                                                @click="
                                                    removeArrayItem(key, index)
                                                "
                                            />
                                        </div>
                                    </div>

                                    <!-- Add array item button -->
                                    <Button
                                        v-if="!readonly"
                                        label="Add Item"
                                        icon="pi pi-plus"
                                        class="p-button-text p-button-sm mt-2"
                                        @click="addArrayItem(key)"
                                    />
                                </div>
                            </template>

                            <!-- Unknown type -->
                            <template v-else>
                                <div class="text-muted">
                                    {{ JSON.stringify(value) }}
                                </div>
                            </template>
                        </div>
                    </div>

                    <div class="p-col-12 p-md-2" v-if="!readonly">
                        <div class="parameter-actions">
                            <Button
                                icon="pi pi-trash"
                                class="p-button-danger p-button-text"
                                @click="removeParameter(key)"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Add Parameter Dialog -->
        <Dialog
            v-model:visible="displayAddDialog"
            header="Add Parameter"
            :modal="true"
            :closable="true"
            :style="{ width: '450px' }"
        >
            <div class="p-fluid">
                <div class="field">
                    <label for="paramKey">Parameter Name</label>
                    <InputText id="paramKey" v-model="newParam.key" />
                </div>
                <div class="field">
                    <label for="paramType">Parameter Type</label>
                    <Dropdown
                        id="paramType"
                        v-model="newParam.type"
                        :options="paramTypes"
                        optionLabel="label"
                        optionValue="value"
                        placeholder="Select Type"
                    />
                </div>
                <div class="field" v-if="newParam.type === 'string'">
                    <label for="paramValueString">Value</label>
                    <InputText
                        id="paramValueString"
                        v-model="newParam.valueString"
                    />
                </div>
                <div class="field" v-if="newParam.type === 'number'">
                    <label for="paramValueNumber">Value</label>
                    <InputNumber
                        id="paramValueNumber"
                        v-model="newParam.valueNumber"
                    />
                </div>
                <div class="field" v-if="newParam.type === 'boolean'">
                    <label for="paramValueBoolean">Value</label>
                    <ToggleButton
                        id="paramValueBoolean"
                        v-model="newParam.valueBoolean"
                        onLabel="True"
                        offLabel="False"
                    />
                </div>
            </div>
            <template #footer>
                <Button
                    label="Cancel"
                    icon="pi pi-times"
                    class="p-button-text"
                    @click="cancelAddParameter"
                />
                <Button
                    label="Add"
                    icon="pi pi-check"
                    @click="confirmAddParameter"
                />
            </template>
        </Dialog>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useToast } from "primevue/usetoast";
import InputNumber from "primevue/inputnumber";
import ToggleButton from "primevue/togglebutton";
import Dropdown from "primevue/dropdown";

const props = defineProps({
    modelValue: {
        type: Object,
        default: () => ({}),
    },
    readonly: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(["update:modelValue"]);

const toast = useToast();

// Reactive state
const config = ref({});
const editableKeys = ref({});
const displayAddDialog = ref(false);
const newParam = ref({
    key: "",
    type: "string",
    valueString: "",
    valueNumber: 0,
    valueBoolean: false,
});

// Parameter type options
const paramTypes = [
    { label: "String", value: "string" },
    { label: "Number", value: "number" },
    { label: "Boolean", value: "boolean" },
    { label: "Array", value: "array" },
    { label: "Object", value: "object" },
];

// Watch for external changes to model value
watch(
    () => props.modelValue,
    (newVal) => {
        // Deep copy to avoid direct reference
        config.value = JSON.parse(JSON.stringify(newVal || {}));

        // Initialize editable keys
        Object.keys(config.value).forEach((key) => {
            editableKeys.value[key] = key;
        });
    },
    { immediate: true, deep: true },
);

// Methods
function emitUpdate() {
    emit("update:modelValue", config.value);
}

function addParameter() {
    // Reset new parameter form
    newParam.value = {
        key: "",
        type: "string",
        valueString: "",
        valueNumber: 0,
        valueBoolean: false,
    };

    // Show dialog
    displayAddDialog.value = true;
}

function cancelAddParameter() {
    displayAddDialog.value = false;
}

function confirmAddParameter() {
    // Validate key
    if (!newParam.value.key.trim()) {
        toast.add({
            severity: "error",
            summary: "Error",
            detail: "Parameter name is required",
            life: 3000,
        });
        return;
    }

    // Check for duplicate key
    if (config.value[newParam.value.key]) {
        toast.add({
            severity: "error",
            summary: "Error",
            detail: "Parameter name already exists",
            life: 3000,
        });
        return;
    }

    // Get value based on type
    let value;
    switch (newParam.value.type) {
        case "string":
            value = newParam.value.valueString;
            break;
        case "number":
            value = newParam.value.valueNumber;
            break;
        case "boolean":
            value = newParam.value.valueBoolean;
            break;
        case "array":
            value = [];
            break;
        case "object":
            value = {};
            break;
        default:
            value = "";
    }

    // Add to config
    config.value = {
        ...config.value,
        [newParam.value.key]: value,
    };

    // Add to editable keys
    editableKeys.value[newParam.value.key] = newParam.value.key;

    // Emit update
    emitUpdate();

    // Close dialog
    displayAddDialog.value = false;
}

function removeParameter(key) {
    // Create new object without the key
    const { [key]: removed, ...rest } = config.value;
    config.value = rest;

    // Remove from editable keys
    delete editableKeys.value[key];

    // Emit update
    emitUpdate();
}

function updateParameterKey(oldKey) {
    const newKey = editableKeys.value[oldKey];

    // If key hasn't changed
    if (oldKey === newKey) return;

    // Validate new key
    if (!newKey.trim()) {
        // Reset to old key
        editableKeys.value[oldKey] = oldKey;
        toast.add({
            severity: "error",
            summary: "Error",
            detail: "Parameter name cannot be empty",
            life: 3000,
        });
        return;
    }

    // Check for duplicate key
    if (config.value[newKey]) {
        // Reset to old key
        editableKeys.value[oldKey] = oldKey;
        toast.add({
            severity: "error",
            summary: "Error",
            detail: "Parameter name already exists",
            life: 3000,
        });
        return;
    }

    // Create new object with updated key
    const newConfig = {};

    Object.keys(config.value).forEach((key) => {
        if (key === oldKey) {
            newConfig[newKey] = config.value[oldKey];
        } else {
            newConfig[key] = config.value[key];
        }
    });

    // Update config
    config.value = newConfig;

    // Update editable keys
    delete editableKeys.value[oldKey];
    editableKeys.value[newKey] = newKey;

    // Emit update
    emitUpdate();
}

function addArrayItem(key) {
    // If not an array, do nothing
    if (!Array.isArray(config.value[key])) return;

    // Add empty item based on array type
    const arrayType =
        config.value[key].length > 0 ? typeof config.value[key][0] : "string";

    let newItem;
    switch (arrayType) {
        case "number":
            newItem = 0;
            break;
        case "boolean":
            newItem = false;
            break;
        case "object":
            newItem = {};
            break;
        case "string":
        default:
            newItem = "";
    }

    // Add to array
    config.value[key].push(newItem);

    // Emit update
    emitUpdate();
}

function removeArrayItem(key, index) {
    // If not an array, do nothing
    if (!Array.isArray(config.value[key])) return;

    // Remove item at index
    config.value[key].splice(index, 1);

    // Emit update
    emitUpdate();
}
</script>

<style scoped>
.config-editor {
    margin-bottom: 1rem;
}

.empty-config {
    text-align: center;
    padding: 2rem;
    background-color: #f8f9fa;
    border-radius: 4px;
}

.parameter-item {
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    background-color: #f8f9fa;
}

.nested-object {
    margin-top: 0.5rem;
    padding: 0.5rem;
    border-left: 3px solid #3b82f6;
    background-color: rgba(59, 130, 246, 0.05);
}

.array-item {
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    background-color: white;
}
</style>

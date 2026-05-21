<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-sheet">
      <div class="modal-title">
        {{ locale === 'pl' ? task.name_pl : task.name }}
      </div>

      <!-- Steps -->
      <div style="margin-bottom:16px;">
        <div class="card-title">{{ $t('maintenance.steps') }}</div>
        <ol class="step-list">
          <li v-for="step in task.steps" :key="step.order" class="step-item">
            <span class="step-num">{{ step.order }}</span>
            <div>
              <div>{{ locale === 'pl' ? step.text_pl : step.text_en }}</div>
              <div v-if="locale === 'pl'" style="font-size:11px;color:var(--text-muted);margin-top:2px;">
                {{ step.text_en }}
              </div>
            </div>
          </li>
        </ol>
      </div>

      <!-- Parts checkboxes -->
      <div v-if="task.required_parts.length" class="parts-list">
        <div class="card-title">{{ $t('maintenance.partsReplaced') }}</div>
        <div v-for="part in partsList" :key="part.supply_name" class="part-item">
          <input type="checkbox" v-model="part.checked" :id="'part_' + part.supply_name" />
          <label :for="'part_' + part.supply_name" style="font-size:13px;cursor:pointer;">
            {{ part.supply_name }} × {{ part.quantity }} {{ part.unit }}
          </label>
        </div>
      </div>

      <!-- Notes -->
      <div style="margin-top:12px;">
        <textarea v-model="notes"
          :placeholder="$t('maintenance.steps')"
          style="width:100%;background:var(--bg);border:1px solid var(--border);border-radius:6px;color:var(--text);padding:8px;font-size:13px;height:50px;resize:none;">
        </textarea>
      </div>

      <div class="modal-footer">
        <button class="btn btn-secondary" style="flex:1" @click="$emit('close')">
          {{ $t('maintenance.cancel') }}
        </button>
        <button class="btn btn-primary" style="flex:1" @click="confirm">
          {{ $t('maintenance.confirm') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

const props = defineProps({ task: Object })
const emit = defineEmits(['close', 'done'])

const notes = ref('')

const partsList = ref(
  props.task.required_parts.map(p => ({ ...p, checked: false }))
)

function confirm() {
  const replaced = partsList.value
    .filter(p => p.checked)
    .map(p => ({ supply_id: p.supply_id, supply_name: p.supply_name, quantity: p.quantity }))
  emit('done', props.task.id, replaced, notes.value || null)
}
</script>

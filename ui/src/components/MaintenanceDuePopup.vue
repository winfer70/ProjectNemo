<template>
  <!-- Global "maintenance overdue" banner - shown on every tab, not just
       Schedule. Dismissing a task calls the snooze endpoint (not just a
       local hide) so the hourly Telegram reminder keeps nagging until the
       task is actually completed - see api/services/scheduler.py's
       maintenance_snooze_reminder job. -->
  <Teleport to="body">
    <div v-if="visibleTasks.length" class="maint-popup">
      <div class="maint-popup-hd">
        <span class="maint-popup-ico">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 4l9 15H3l9-15z"/><path d="M12 10v4"/><circle cx="12" cy="16.5" r="0.6" fill="currentColor" stroke="none"/>
          </svg>
        </span>
        <span class="maint-popup-title">
          {{ locale === 'pl' ? `Zaległa konserwacja (${visibleTasks.length})` : `Maintenance overdue (${visibleTasks.length})` }}
        </span>
      </div>
      <div class="maint-popup-body">
        <div v-for="task in visibleTasks" :key="task.id" class="maint-popup-row">
          <span class="maint-popup-name">{{ locale === 'pl' ? task.name_pl : task.name }}</span>
          <button class="btn btn-sm btn-ghost" :disabled="dismissing === task.id" @click="dismiss(task)">
            {{ locale === 'pl' ? 'Odrzuć' : 'Dismiss' }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useMaintenanceStore } from '../stores/maintenance'

const { locale } = useI18n()
const maintenanceStore = useMaintenanceStore()

// Session-local "already dismissed" set - dismissing hides a task from this
// banner immediately, while the snooze POST keeps the hourly Telegram
// reminder running server-side regardless of what the UI shows.
const dismissedIds = ref(new Set())
const dismissing = ref(null)

const overdueTasks = computed(() =>
  maintenanceStore.tasks.filter(t => t.next_due && new Date(t.next_due) < new Date())
)

const visibleTasks = computed(() =>
  overdueTasks.value.filter(t => !dismissedIds.value.has(t.id))
)

async function dismiss(task) {
  dismissing.value = task.id
  try {
    await maintenanceStore.snoozeTask(task.id)
  } catch (err) {
    // Snooze call failed - still hide it locally so the banner isn't stuck;
    // the hourly job simply won't have a fresh snooze row until retried.
  } finally {
    dismissedIds.value = new Set([...dismissedIds.value, task.id])
    dismissing.value = null
  }
}

onMounted(() => {
  // Global banner - guarantee task data is loaded even if the user never
  // visits the Schedule tab (the only view that otherwise fetches this).
  if (!maintenanceStore.tasks.length) maintenanceStore.fetchTasks()
})
</script>

<style scoped>
.maint-popup {
  position: fixed;
  top: 12px;
  left: 12px;
  right: 12px;
  max-width: 420px;
  margin: 0 auto;
  z-index: 55;
  background: var(--surface);
  border: 1px solid var(--border);
  border-left: 3px solid var(--warning);
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
  overflow: hidden;
  animation: maint-popup-in 0.2s ease;
}
@keyframes maint-popup-in {
  from { opacity: 0; transform: translateY(-6px); }
  to { opacity: 1; transform: translateY(0); }
}
.maint-popup-hd {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
}
.maint-popup-ico { color: var(--warning); display: flex; flex-shrink: 0; }
.maint-popup-title { font-size: 13px; font-weight: 700; color: var(--text); }
.maint-popup-body {
  display: flex;
  flex-direction: column;
  border-top: 1px solid var(--border);
  max-height: 200px;
  overflow-y: auto;
}
.maint-popup-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 8px 12px;
}
.maint-popup-row + .maint-popup-row { border-top: 1px solid var(--border); }
.maint-popup-name {
  font-size: 12.5px;
  color: var(--text);
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>

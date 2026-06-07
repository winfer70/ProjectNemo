<template>
  <div>
    <!-- In-progress maintenance banner -->
    <div v-if="inProgressTask" class="banner warm">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 4l9 15H3l9-15z"/><path d="M12 10v4"/><circle cx="12" cy="16.5" r="0.6" fill="currentColor" stroke="none"/>
      </svg>
      <span style="flex:1">{{ locale === 'pl' ? `${locale === 'pl' ? inProgressTask.name_pl : inProgressTask.name} w toku` : `${inProgressTask.name} in progress` }}</span>
      <button class="btn btn-sm btn-warm" @click="maintenanceStore.completeTask(inProgressTask.id)">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <path d="M4 12.5l5 5 11-12"/>
        </svg>
        {{ locale === 'pl' ? 'Zakończ' : 'Finish' }}
      </button>
    </div>

    <!-- ═══════════════════════════ TODAY TILE ═══════════════════════════ -->
    <div class="tile" :class="{ feeding: scheduleStore.feedStatus.paused }">
      <div class="tile-hd">
        <h2>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="4.5" width="18" height="16" rx="2.5"/><path d="M3 9h18"/><path d="M8 2.5v4"/><path d="M16 2.5v4"/><path d="M8.5 14.5l2.2 2.2 4-4.4"/>
          </svg>
          {{ locale === 'pl' ? 'DZISIAJ' : 'TODAY' }}
        </h2>
        <span class="meta">{{ todayLabel }}</span>
      </div>
      <hr class="divider">
      <div class="tile-body">
        <div v-if="calendarStore.todayTasks.length === 0" class="empty">
          <span class="em">🎉</span>
          <span>{{ locale === 'pl' ? 'Brak zadań na dziś' : 'No tasks for today' }}</span>
        </div>
        <template v-else>
          <div v-for="task in calendarStore.todayTasks" :key="task.id + '_' + task.date">
            <div
              class="task"
              :class="{ done: task.completed, overdue: task.overdue_days > 0 && !task.completed }"
              @click="!task.completed && toggleExpanded(task.id + '_' + task.date)"
            >
              <span class="task-ico">
                <span v-if="task.completed" style="color:var(--success)">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="9"/><path d="M8 12.2l2.6 2.6L16 9"/>
                  </svg>
                </span>
                <span v-else-if="task.overdue_days > 0" style="color:var(--danger)">
                  <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M12 4l9 15H3l9-15z"/><path d="M12 10v4"/><circle cx="12" cy="16.5" r="0.6" fill="currentColor" stroke="none"/>
                  </svg>
                </span>
                <span v-else style="color:var(--accent)">
                  <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="9"/><path d="M12 7v5.5l3.5 2"/>
                  </svg>
                </span>
              </span>
              <span class="task-label">
                <span class="t">{{ locale === 'pl' ? task.name_pl : task.name }}</span>
              </span>
              <span v-if="task.completed" class="task-badge b-done">{{ locale === 'pl' ? 'zrobione' : 'done' }}</span>
              <span v-else-if="task.overdue_days > 0" class="task-badge b-overdue">{{ task.overdue_days }} {{ locale === 'pl' ? 'dni po' : 'days over' }}</span>
              <span v-else class="task-badge b-pending">{{ locale === 'pl' ? 'dziś' : 'today' }}</span>
            </div>
            <div v-if="expandedTask === (task.id + '_' + task.date) && !task.completed" class="task-actions">
              <button class="btn btn-sm btn-success" @click="completeTask(task)">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M4 12.5l5 5 11-12"/>
                </svg>
                {{ locale === 'pl' ? 'Zrobione' : 'Done' }}
              </button>
              <button class="btn btn-sm" @click="expandedTask = null">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 1.5"/><path d="M5 4l4 2"/><path d="M19 4l-4 2"/>
                </svg>
                {{ locale === 'pl' ? 'Drzemka' : 'Snooze' }}
              </button>
              <button class="btn btn-sm" @click="expandedTask = null">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="4.5" width="18" height="16" rx="2.5"/><path d="M3 9.5h18"/><path d="M8 2.5v4"/><path d="M16 2.5v4"/>
                </svg>
                {{ locale === 'pl' ? 'Jutro' : 'Tomorrow' }}
              </button>
            </div>
          </div>
        </template>
      </div>
      <hr class="divider">
      <div class="tile-body" style="padding-top:14px">
        <!-- Feeding active state -->
        <div v-if="scheduleStore.feedStatus.paused" class="fade-in">
          <div class="row" style="justify-content:center;color:var(--accent-warm);font-weight:700;font-size:13px;margin-bottom:10px;gap:6px">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 4l9 15H3l9-15z"/><path d="M12 10v4"/><circle cx="12" cy="16.5" r="0.6" fill="currentColor" stroke="none"/>
            </svg>
            {{ locale === 'pl' ? 'Karmienie aktywne · 3 min' : 'Feeding active · 3 min' }}
          </div>
          <div class="row" style="gap:10px">
            <div class="bar warm" style="flex:1"><i :style="{ width: feedProgressPct + '%' }"></i></div>
            <span class="tnum" style="font-weight:700;font-size:14px;min-width:42px;text-align:right">{{ feedCountdownStr }}</span>
          </div>
          <div class="muted" style="font-size:12px;text-align:center;margin:7px 0 12px">{{ locale === 'pl' ? 'pozostało' : 'remaining' }}</div>
          <button class="btn btn-danger-o btn-block" @click="handleCancelFeed">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M6 6l12 12"/><path d="M18 6L6 18"/>
            </svg>
            {{ locale === 'pl' ? 'Anuluj karmienie' : 'Cancel Feeding' }}
          </button>
        </div>
        <!-- Feed Now button -->
        <button v-else class="btn btn-warm btn-block btn-lg" @click="handleFeedNow">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M16 12c0 0 3-4 6-4-1 2-1 6 0 8-3 0-6-4-6-4z"/><path d="M16 12c-3-4-9-4-12 0 3 4 9 4 12 0z"/><circle cx="7" cy="11" r="0.6" fill="currentColor" stroke="none"/>
          </svg>
          {{ locale === 'pl' ? 'Karm Teraz' : 'Feed Now' }}
        </button>
      </div>
      <div class="tile-body" style="padding-top:0;padding-bottom:14px">
        <button class="btn btn-sm btn-ghost btn-block" style="margin-top:8px" @click="openCalEdit(null)">
          + {{ locale === 'pl' ? 'Dodaj' : 'Add' }}
        </button>
      </div>
    </div>

    <!-- ═══════════════════════════ DOSING TILE ═══════════════════════════ -->
    <div class="tile">
      <div class="tile-hd">
        <h2>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>
          </svg>
          {{ locale === 'pl' ? 'DAWKOWANIE' : 'DOSING' }}
        </h2>
        <button class="btn btn-sm btn-ghost" @click="openDoseEdit(null)">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 5v14"/><path d="M5 12h14"/>
          </svg>
          {{ locale === 'pl' ? 'Dodaj' : 'Add' }}
        </button>
      </div>
      <hr class="divider">
      <div class="tile-body">
        <div v-if="scheduleStore.dosingTasks.length === 0" class="empty">
          <span>{{ locale === 'pl' ? 'Brak dawkowań' : 'No doses configured' }}</span>
          <button class="btn btn-sm btn-accent" @click="openDoseEdit(null)">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 5v14"/><path d="M5 12h14"/>
            </svg>
            {{ locale === 'pl' ? 'Dodaj' : 'Add' }}
          </button>
        </div>
        <div
          v-for="(task, i) in scheduleStore.dosingTasks"
          :key="task.id"
          :style="{ paddingTop: '12px', paddingBottom: '12px', borderTop: i > 0 ? '1px solid var(--border)' : 'none' }"
        >
          <div class="row" style="justify-content:space-between;margin-bottom:0">
            <div class="row" style="gap:9px;min-width:0;flex:1">
              <span style="color:var(--accent);display:flex;flex-shrink:0">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>
                </svg>
              </span>
              <span style="font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{{ locale === 'pl' ? task.supply_name_pl : task.supply_name }}</span>
              <span class="muted tnum" style="font-size:13px;white-space:nowrap">{{ task.dose_amount }}{{ task.dose_unit }}<span v-if="task.time_of_day"> · {{ task.time_of_day }}</span></span>
            </div>
            <div class="row" style="gap:6px;flex-shrink:0">
              <button class="btn icon-btn" :class="{ 'btn-success': task.done_today }" @click="scheduleStore.completeDose(task.id)">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M4 12.5l5 5 11-12"/>
                </svg>
              </button>
              <button class="btn icon-btn btn-ghost" @click="openDoseEdit(task)">
                <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M4 20h4L19 9l-4-4L4 16v4z"/><path d="M14 6l4 4"/>
                </svg>
              </button>
            </div>
          </div>
          <div class="spread" style="margin:9px 0 6px;font-size:12px">
            <span class="muted">
              {{ locale === 'pl' ? 'Pozostało:' : 'Left:' }}
              <b class="tnum" style="color:var(--text)">{{ task.supply_current_amount ?? '—' }}{{ task.supply_unit }}</b>
            </span>
            <span class="muted tnum">{{ supplyPct(task) }}%</span>
          </div>
          <div class="bar" :class="supplyBarClass(supplyPct(task))">
            <i :style="{ width: Math.max(0, Math.min(100, supplyPct(task))) + '%' }"></i>
          </div>
          <button class="btn btn-sm btn-ghost" style="margin-top:10px" @click="openRestock(task)">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 5v9"/><path d="M8 10l4 4 4-4"/><path d="M5 19h14"/>
            </svg>
            {{ locale === 'pl' ? 'Uzupełnij' : 'Restock' }}
          </button>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════ LIGHTING TILE ═══════════════════════════ -->
    <div class="tile">
      <div class="tile-hd">
        <h2>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 18h6"/><path d="M10 21h4"/>
            <path d="M12 3a6 6 0 0 0-4 10.5c.7.7 1 1.3 1 2.5h6c0-1.2.3-1.8 1-2.5A6 6 0 0 0 12 3z"/>
          </svg>
          {{ locale === 'pl' ? 'OŚWIETLENIE' : 'LIGHTING' }}
        </h2>
        <span class="chip">
          BLE
          <span class="dot" :class="sensorsStore.bleConnected ? 'on' : 'off'"></span>
        </span>
      </div>
      <hr class="divider">
      <div class="tile-body" style="padding-top:13px">
        <div class="spread">
          <div class="row" style="gap:10px">
            <span class="dev-ico" :style="{ color: lightOn && sensorsStore.bleConnected ? 'var(--warning)' : 'var(--text-muted)' }">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M9 18h6"/><path d="M10 21h4"/>
                <path d="M12 3a6 6 0 0 0-4 10.5c.7.7 1 1.3 1 2.5h6c0-1.2.3-1.8 1-2.5A6 6 0 0 0 12 3z"/>
              </svg>
            </span>
            <div>
              <div style="font-weight:600">{{ locale === 'pl' ? 'Światło' : 'Light' }}</div>
              <div class="row" style="gap:6px;font-size:12px;margin-top:2px" @click="!sensorsStore.bleConnected && handleBleConnect()">
                <span class="muted">BLE: {{ sensorsStore.bleConnected ? (locale === 'pl' ? 'połączony' : 'connected') : (locale === 'pl' ? 'rozłączony' : 'disconnected') }}</span>
                <span class="dot" :class="sensorsStore.bleConnected ? 'on' : 'off'"></span>
                <span v-if="!sensorsStore.bleConnected" style="color:var(--accent);cursor:pointer;font-weight:600">
                  {{ locale === 'pl' ? 'Połącz' : 'Tap to reconnect' }}
                </span>
              </div>
            </div>
          </div>
          <button
            class="toggle accent"
            :class="{ on: lightOn, disabled: !sensorsStore.bleConnected }"
            :disabled="!sensorsStore.bleConnected"
            :aria-pressed="lightOn"
            @click="toggleLight"
          ></button>
        </div>
        <div v-if="bleError" style="font-size:11px;color:var(--danger);margin-top:8px">BLE: {{ bleError }}</div>
        <div v-if="sensorsStore.bleConnected" class="channel-sliders">
          <div v-for="key in ['r', 'g', 'b', 'w']" :key="key" class="row" style="gap:8px;margin-top:10px">
            <span class="channel-label" :style="{ color: channelColors[key] }">{{ key.toUpperCase() }}</span>
            <input type="range" min="0" max="100" v-model.number="channels[key]" @input="pushChannels" style="flex:1">
            <span class="muted tnum" style="font-size:12px;min-width:32px;text-align:right">{{ channels[key] }}%</span>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════ ROW: MAINTENANCE + PLUGS ═══════════════════════════ -->
    <div class="row2">
      <!-- MAINTENANCE TILE -->
      <div class="tile">
        <div class="tile-hd">
          <h2>
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="3.2"/>
              <path d="M12 3v2.5"/><path d="M12 18.5V21"/><path d="M3 12h2.5"/><path d="M18.5 12H21"/>
              <path d="M5.5 5.5l1.8 1.8"/><path d="M16.7 16.7l1.8 1.8"/>
              <path d="M18.5 5.5l-1.8 1.8"/><path d="M7.3 16.7l-1.8 1.8"/>
            </svg>
            {{ locale === 'pl' ? 'KONSERWACJA' : 'MAINT.' }}
          </h2>
        </div>
        <hr class="divider">
        <div class="tile-body" style="padding-top:6px">
          <div v-if="maintenanceStore.tasks.length === 0" class="empty">
            <span>{{ locale === 'pl' ? 'Brak zadań' : 'No tasks' }}</span>
          </div>
          <div
            v-for="(task, i) in maintenanceStore.tasks"
            :key="task.id"
            class="maint-row"
            :class="{ overdue: maintDays(task) < 0 && !task.started_at, 'maint-row--first': i === 0 }"
          >
            <div class="spread" style="margin-bottom:8px">
              <div class="row" style="gap:8px;min-width:0;flex:1;overflow:hidden">
                <span style="display:flex;flex-shrink:0" :style="{ color: maintDays(task) < 0 && !task.started_at ? 'var(--danger)' : 'var(--text-muted)' }">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="3.2"/>
                    <path d="M12 3v2.5"/><path d="M12 18.5V21"/><path d="M3 12h2.5"/><path d="M18.5 12H21"/>
                    <path d="M5.5 5.5l1.8 1.8"/><path d="M16.7 16.7l1.8 1.8"/>
                    <path d="M18.5 5.5l-1.8 1.8"/><path d="M7.3 16.7l-1.8 1.8"/>
                  </svg>
                </span>
                <span
                  style="font-size:13px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap"
                  :style="{ fontWeight: maintDays(task) < 0 && !task.started_at ? 700 : 500 }"
                >{{ locale === 'pl' ? task.name_pl : task.name }}</span>
              </div>
              <span
                class="task-badge"
                :class="task.started_at ? 'b-pending' : maintDays(task) < 0 ? 'b-overdue' : 'b-due'"
                style="flex-shrink:0;margin-left:6px"
              >
                <template v-if="task.started_at">{{ locale === 'pl' ? 'W toku' : 'In prog.' }}</template>
                <template v-else-if="maintDays(task) < 0">{{ Math.abs(maintDays(task)) }}{{ locale === 'pl' ? ' po' : ' over' }}</template>
                <template v-else>{{ maintDays(task) }}{{ locale === 'pl' ? ' dni' : 'd' }}</template>
              </span>
            </div>
            <button
              class="btn btn-sm btn-block"
              :class="{ 'btn-success': !!task.started_at }"
              @click="handleMaintToggle(task)"
            >
              <template v-if="task.started_at">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M4 12.5l5 5 11-12"/>
                </svg>
                {{ locale === 'pl' ? 'Zakończ' : 'Finish' }}
              </template>
              <template v-else>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M7 5l11 7-11 7V5z"/>
                </svg>
                {{ locale === 'pl' ? 'Start' : 'Start' }}
              </template>
            </button>
          </div>
        </div>
      </div>

      <!-- PLUGS TILE -->
      <div class="tile">
        <div class="tile-hd">
          <h2>{{ locale === 'pl' ? 'WTYCZKI' : 'PLUGS' }}</h2>
        </div>
        <hr class="divider">
        <div class="tile-body" style="padding-top:4px">
          <div v-if="sensorsStore.devices.length === 0" class="empty">
            <span>{{ locale === 'pl' ? 'Brak urządzeń' : 'No devices' }}</span>
          </div>
          <div
            v-for="device in sensorsStore.devices"
            :key="device.entity_id"
            class="dev"
            :class="{ off: device.state !== 'on' }"
            style="padding:9px 6px;margin:0 -4px"
            @click="sheetDevice = device"
          >
            <span class="dev-ico" style="width:26px;height:26px">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <template v-if="device.role === 'filter'">
                  <circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/>
                  <path d="M12 4v3"/><path d="M12 17v3"/><path d="M4 12h3"/><path d="M17 12h3"/>
                </template>
                <template v-else-if="device.role === 'heater'">
                  <path d="M7 4v16"/><path d="M12 4v16"/><path d="M17 4v16"/>
                  <rect x="3" y="7" width="18" height="10" rx="2"/>
                </template>
                <template v-else-if="device.role === 'air'">
                  <path d="M5 9a3 3 0 1 1 3 3H3"/><path d="M11 7a2.4 2.4 0 1 1 2.5 2.5"/>
                  <path d="M14 16a3 3 0 1 0 3-3h-6"/>
                </template>
                <template v-else-if="device.role === 'light'">
                  <path d="M9 18h6"/><path d="M10 21h4"/>
                  <path d="M12 3a6 6 0 0 0-4 10.5c.7.7 1 1.3 1 2.5h6c0-1.2.3-1.8 1-2.5A6 6 0 0 0 12 3z"/>
                </template>
                <template v-else>
                  <path d="M9 3v6"/><path d="M15 3v6"/>
                  <path d="M7 9h10v3a5 5 0 0 1-10 0V9z"/><path d="M12 17v4"/>
                </template>
              </svg>
            </span>
            <div class="dev-name">
              <div class="n" style="font-size:12.5px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{{ locale === 'pl' ? device.name_pl : device.name }}</div>
              <div class="w">{{ device.state === 'on' ? (device.watts ?? 0) : 0 }}W</div>
            </div>
            <span v-if="device.state !== 'on' && !scheduleStore.feedStatus.paused && !hasAnyInProgressMaintenance" class="warn-ico">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 4l9 15H3l9-15z"/><path d="M12 10v4"/><circle cx="12" cy="16.5" r="0.6" fill="currentColor" stroke="none"/>
              </svg>
            </span>
            <span v-else class="dot" :class="device.state === 'on' ? 'on' : 'off'"></span>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════ RESTOCK MODAL ═══════════════════════════ -->
    <div v-if="restockDose" class="backdrop" @click.self="restockDose = null">
      <div class="modal">
        <h3 class="modal-title">{{ locale === 'pl' ? 'Uzupełnij zapas' : 'Restock supply' }}</h3>
        <p class="modal-sub">{{ locale === 'pl' ? restockDose.supply_name_pl : restockDose.supply_name }}</p>
        <div class="field">
          <label>{{ locale === 'pl' ? 'Ile dodajesz?' : 'How much to add?' }}</label>
          <div class="input-row">
            <input class="input" type="number" inputmode="decimal" v-model="restockAmount" autofocus>
            <span class="unit">{{ restockDose.supply_unit }}</span>
          </div>
        </div>
        <div class="modal-actions">
          <button class="btn btn-block" @click="restockDose = null">{{ locale === 'pl' ? 'Anuluj' : 'Cancel' }}</button>
          <button class="btn btn-accent btn-block" @click="handleRestock">{{ locale === 'pl' ? 'Potwierdź' : 'Confirm' }}</button>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════ DOSE EDIT MODAL ═══════════════════════════ -->
    <div v-if="doseEditOpen" class="backdrop" @click.self="doseEditOpen = false">
      <div class="modal">
        <h3 class="modal-title">{{ doseEditTask ? (locale === 'pl' ? 'Edytuj dawkę' : 'Edit dose') : (locale === 'pl' ? 'Nowa dawka' : 'Add dose') }}</h3>
        <div class="field">
          <label>{{ locale === 'pl' ? 'Nazwa (PL)' : 'Name (PL)' }}</label>
          <input class="input" v-model="doseForm.name_pl" placeholder="Nawóz…">
        </div>
        <div class="field">
          <label>Name (EN)</label>
          <input class="input" v-model="doseForm.name" placeholder="Fertilizer…">
        </div>
        <div class="row" style="gap:12px;align-items:flex-start">
          <div class="field" style="flex:1;margin-bottom:0">
            <label>{{ locale === 'pl' ? 'Dawka' : 'Amount' }}</label>
            <div class="input-row">
              <input class="input" type="number" inputmode="decimal" v-model="doseForm.amount">
              <span class="unit">{{ doseForm.unit }}</span>
            </div>
          </div>
          <div class="field" style="width:110px;margin-bottom:0">
            <label>{{ locale === 'pl' ? 'Godzina' : 'Time' }}</label>
            <input class="input" type="time" v-model="doseForm.time">
          </div>
        </div>
        <div class="field" style="margin-top:14px">
          <label>{{ locale === 'pl' ? 'Jednostka' : 'Unit' }}</label>
          <select class="select" v-model="doseForm.unit">
            <option value="ml">ml</option>
            <option value="g">g</option>
            <option value="drops">{{ locale === 'pl' ? 'krople' : 'drops' }}</option>
          </select>
        </div>
        <div class="modal-actions">
          <button class="btn btn-block" @click="doseEditOpen = false">{{ locale === 'pl' ? 'Anuluj' : 'Cancel' }}</button>
          <button class="btn btn-accent btn-block" @click="saveDose">{{ locale === 'pl' ? 'Zapisz' : 'Save' }}</button>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════ CALENDAR EDIT MODAL (full-screen) ═══════════════════════════ -->
    <div v-if="calEditOpen" class="backdrop" style="align-items:stretch;justify-content:center">
      <div class="modal full">
        <div class="spread" style="padding:16px 16px 14px;border-bottom:1px solid var(--border);flex-shrink:0">
          <button class="btn icon-btn btn-ghost" @click="calEditOpen = false">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M6 6l12 12"/><path d="M18 6L6 18"/>
            </svg>
          </button>
          <span style="font-weight:700;font-size:16px">{{ calEditTask ? (locale === 'pl' ? 'Edytuj zadanie' : 'Edit task') : (locale === 'pl' ? 'Nowe zadanie' : 'New task') }}</span>
          <button class="btn btn-sm btn-accent" @click="saveCalTask">{{ locale === 'pl' ? 'Zapisz' : 'Save' }}</button>
        </div>
        <div style="padding:16px;overflow-y:auto;flex:1">
          <div class="field">
            <label>{{ locale === 'pl' ? 'Tytuł (PL)' : 'Title (PL)' }}</label>
            <input class="input" v-model="calForm.name_pl" autofocus placeholder="Wymiana wody…">
          </div>
          <div class="field">
            <label>Title (EN)</label>
            <input class="input" v-model="calForm.name" placeholder="Water change…">
          </div>
          <div class="field">
            <label>{{ locale === 'pl' ? 'Data' : 'Date' }}</label>
            <input class="input" type="date" v-model="calForm.date">
          </div>
          <div class="field">
            <label>{{ locale === 'pl' ? 'Powtarzanie' : 'Repeat' }}</label>
            <div class="seg" style="flex-wrap:wrap">
              <button :class="{ on: calForm.repeat === 'once' }" @click="calForm.repeat = 'once'">{{ locale === 'pl' ? 'Raz' : 'Once' }}</button>
              <button :class="{ on: calForm.repeat === 'daily' }" @click="calForm.repeat = 'daily'">{{ locale === 'pl' ? 'Codziennie' : 'Daily' }}</button>
              <button :class="{ on: calForm.repeat === 'ndays' }" @click="calForm.repeat = 'ndays'">{{ locale === 'pl' ? 'Co N dni' : 'N days' }}</button>
              <button :class="{ on: calForm.repeat === 'weekdays' }" @click="calForm.repeat = 'weekdays'">{{ locale === 'pl' ? 'Robocze' : 'Weekdays' }}</button>
            </div>
          </div>
          <div class="field">
            <label>{{ locale === 'pl' ? 'Notatki' : 'Notes' }}</label>
            <textarea class="input" rows="3" v-model="calForm.notes" style="resize:none"></textarea>
          </div>
        </div>
      </div>
    </div>

    <!-- ═══════════════════════════ PLUG SHEET (bottom sheet) ═══════════════════════════ -->
    <div v-if="sheetDevice" class="backdrop" @click.self="sheetDevice = null">
      <div class="sheet">
        <div class="sheet-handle"></div>
        <div class="sheet-body">
          <div class="spread" style="margin-bottom:4px">
            <div class="row" style="gap:10px">
              <span class="dev-ico" style="width:36px;height:36px" :style="{ color: sheetDevice.state === 'on' ? 'var(--accent)' : 'var(--danger)' }">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <template v-if="sheetDevice.role === 'filter'">
                    <circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/>
                    <path d="M12 4v3"/><path d="M12 17v3"/><path d="M4 12h3"/><path d="M17 12h3"/>
                  </template>
                  <template v-else-if="sheetDevice.role === 'heater'">
                    <path d="M7 4v16"/><path d="M12 4v16"/><path d="M17 4v16"/>
                    <rect x="3" y="7" width="18" height="10" rx="2"/>
                  </template>
                  <template v-else-if="sheetDevice.role === 'air'">
                    <path d="M5 9a3 3 0 1 1 3 3H3"/><path d="M11 7a2.4 2.4 0 1 1 2.5 2.5"/>
                    <path d="M14 16a3 3 0 1 0 3-3h-6"/>
                  </template>
                  <template v-else-if="sheetDevice.role === 'light'">
                    <path d="M9 18h6"/><path d="M10 21h4"/>
                    <path d="M12 3a6 6 0 0 0-4 10.5c.7.7 1 1.3 1 2.5h6c0-1.2.3-1.8 1-2.5A6 6 0 0 0 12 3z"/>
                  </template>
                  <template v-else>
                    <path d="M9 3v6"/><path d="M15 3v6"/>
                    <path d="M7 9h10v3a5 5 0 0 1-10 0V9z"/><path d="M12 17v4"/>
                  </template>
                </svg>
              </span>
              <div>
                <div style="font-size:17px;font-weight:700">{{ locale === 'pl' ? sheetDevice.name_pl : sheetDevice.name }}</div>
                <div class="mono muted" style="font-size:11px">{{ sheetDevice.entity_id }}</div>
              </div>
            </div>
          </div>
          <div style="margin-top:14px;margin-bottom:18px">
            <div class="kv">
              <span class="k">{{ locale === 'pl' ? 'Status' : 'Status' }}</span>
              <span class="v row" style="gap:7px" :style="{ color: sheetDevice.state === 'on' ? 'var(--success)' : 'var(--danger)' }">
                <span class="dot" :class="sheetDevice.state === 'on' ? 'on' : 'off'"></span>
                {{ sheetDevice.state === 'on' ? (locale === 'pl' ? 'Włączony' : 'On') : (locale === 'pl' ? 'Wyłączony' : 'Off') }}
              </span>
            </div>
            <div class="kv">
              <span class="k">{{ locale === 'pl' ? 'Moc' : 'Power' }}</span>
              <span class="v tnum">{{ sheetDevice.state === 'on' ? (sheetDevice.watts ?? 0) : 0 }}W</span>
            </div>
            <div class="kv">
              <span class="k">{{ locale === 'pl' ? 'Zużycie dziś' : 'Usage today' }}</span>
              <span class="v tnum">{{ (sheetDevice.kwh_today ?? 0).toFixed(2) }} kWh</span>
            </div>
          </div>
          <div class="modal-actions">
            <button
              class="btn btn-block"
              :class="sheetDevice.state === 'on' ? 'btn-danger-o' : 'btn-success'"
              @click="handlePlugToggle(sheetDevice)"
            >{{ sheetDevice.state === 'on' ? (locale === 'pl' ? 'Wyłącz' : 'Turn Off') : (locale === 'pl' ? 'Włącz' : 'Turn On') }}</button>
            <button class="btn btn-block" @click="sheetDevice = null">{{ locale === 'pl' ? 'Zamknij' : 'Close' }}</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { inject } from 'vue'
import { useScheduleStore } from '../stores/schedule'
import { useCalendarStore } from '../stores/calendar'
import { useMaintenanceStore } from '../stores/maintenance'
import { useSensorsStore } from '../stores/sensors'
import * as bleService from '../services/bleService'

const showToast = inject('showToast', () => {})
const { locale } = useI18n()

const scheduleStore = useScheduleStore()
const calendarStore = useCalendarStore()
const maintenanceStore = useMaintenanceStore()
const sensorsStore = useSensorsStore()

// ─── BLE / Lighting ───────────────────────────────────────────────────────────
const bleError = ref(null)
const channels = ref({ r: 60, g: 40, b: 100, w: 80 })
const savedChannels = ref({ r: 60, g: 40, b: 100, w: 80 })
const channelColors = { r: '#ff4444', g: '#44ff88', b: '#4488ff', w: '#ffffaa' }

const lightOn = computed(() =>
  channels.value.r > 0 || channels.value.g > 0 || channels.value.b > 0 || channels.value.w > 0
)

function pushChannels() {
  if (!bleService.isConnected()) return
  const { r, g, b, w } = channels.value
  if (r > 0 || g > 0 || b > 0 || w > 0) savedChannels.value = { r, g, b, w }
  bleService.setChannels(r, g, b, w)
}

async function toggleLight() {
  if (!bleService.isConnected()) return
  if (lightOn.value) {
    savedChannels.value = { ...channels.value }
    channels.value = { r: 0, g: 0, b: 0, w: 0 }
  } else {
    channels.value = { ...savedChannels.value }
  }
  await pushChannels()
}

async function handleBleConnect() {
  bleError.value = null
  try {
    await bleService.connect()
    sensorsStore.bleConnected = true
  } catch (err) {
    bleError.value = err.message || String(err)
  }
}

// ─── Feed countdown ───────────────────────────────────────────────────────────
const FEED_TOTAL_SECS = 180
const feedSecsLeft = ref(0)
let countdownTimer = null

function startCountdown() {
  stopCountdown()
  feedSecsLeft.value = scheduleStore.feedStatus.resume_in_secs ?? FEED_TOTAL_SECS
  countdownTimer = setInterval(() => {
    if (feedSecsLeft.value > 0) feedSecsLeft.value--
    else stopCountdown()
  }, 1000)
}

function stopCountdown() {
  if (countdownTimer) { clearInterval(countdownTimer); countdownTimer = null }
}

watch(() => scheduleStore.feedStatus.paused, (paused) => {
  if (paused) startCountdown()
  else stopCountdown()
}, { immediate: true })

// Re-sync local counter when store poll updates the remaining time
watch(() => scheduleStore.feedStatus.resume_in_secs, (secs) => {
  if (secs != null && scheduleStore.feedStatus.paused && Math.abs(secs - feedSecsLeft.value) > 3) {
    feedSecsLeft.value = secs
  }
})

const feedProgressPct = computed(() => {
  return Math.max(0, Math.min(100, (1 - feedSecsLeft.value / FEED_TOTAL_SECS) * 100))
})

const feedCountdownStr = computed(() => {
  const s = feedSecsLeft.value
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`
})

// ─── Today tile ───────────────────────────────────────────────────────────────
const expandedTask = ref(null)

const todayLabel = computed(() => {
  const d = new Date()
  return d.toLocaleDateString(locale.value === 'pl' ? 'pl-PL' : 'en-IE', {
    weekday: 'long', day: 'numeric', month: 'long',
  })
})

function toggleExpanded(key) {
  expandedTask.value = expandedTask.value === key ? null : key
}

async function completeTask(task) {
  await calendarStore.toggleComplete(task.id, task.date)
  expandedTask.value = null
}

async function handleFeedNow() {
  try {
    await scheduleStore.feedNow()
  } catch (err) {
    showToast(locale.value === 'pl' ? 'Błąd karmienia' : 'Feed error')
  }
}

async function handleCancelFeed() {
  try {
    await scheduleStore.cancelFeed()
  } catch (err) {
    showToast(locale.value === 'pl' ? 'Błąd anulowania' : 'Cancel error')
  }
}

// ─── Dosing ───────────────────────────────────────────────────────────────────
const supplyPct = (task) => {
  if (!task.supply_current_amount || !task.supply_min_threshold) return 100
  const max = task.supply_min_threshold * 3
  return Math.round((task.supply_current_amount / max) * 100)
}

const supplyBarClass = (pct) => {
  if (pct > 50) return 'green'
  if (pct >= 20) return 'yellow'
  return 'red'
}

// Restock modal
const restockDose = ref(null)
const restockAmount = ref(0)

function openRestock(task) {
  restockDose.value = task
  restockAmount.value = 0
}

async function handleRestock() {
  if (!restockDose.value || restockAmount.value <= 0) return
  try {
    await scheduleStore.restockSupply(restockDose.value.supply_id, restockAmount.value)
    restockDose.value = null
    showToast(locale.value === 'pl' ? 'Uzupełniono' : 'Restocked')
  } catch (err) {
    showToast(locale.value === 'pl' ? 'Błąd' : 'Error')
  }
}

// Dose edit modal
const doseEditOpen = ref(false)
const doseEditTask = ref(null)
const doseForm = reactive({ name_pl: '', name: '', amount: '', unit: 'ml', time: '08:00' })

function openDoseEdit(task) {
  doseEditTask.value = task
  if (task) {
    doseForm.name_pl = task.supply_name_pl ?? ''
    doseForm.name = task.supply_name ?? ''
    doseForm.amount = String(task.dose_amount ?? '')
    doseForm.unit = task.dose_unit ?? 'ml'
    doseForm.time = task.time_of_day ?? '08:00'
  } else {
    doseForm.name_pl = ''
    doseForm.name = ''
    doseForm.amount = ''
    doseForm.unit = 'ml'
    doseForm.time = '08:00'
  }
  doseEditOpen.value = true
}

async function saveDose() {
  const data = {
    supply_name: doseForm.name,
    supply_name_pl: doseForm.name_pl,
    dose_amount: parseFloat(doseForm.amount) || 0,
    dose_unit: doseForm.unit,
    time_of_day: doseForm.time || null,
  }
  try {
    if (doseEditTask.value) {
      await scheduleStore.updateDosingTask(doseEditTask.value.id, data)
    } else {
      await scheduleStore.createDosingTask(data)
    }
    doseEditOpen.value = false
    showToast(locale.value === 'pl' ? 'Zapisano' : 'Saved')
  } catch (err) {
    showToast(locale.value === 'pl' ? 'Błąd zapisu' : 'Save error')
  }
}

// ─── Calendar edit modal ──────────────────────────────────────────────────────
const calEditOpen = ref(false)
const calEditTask = ref(null)
const calForm = reactive({ name_pl: '', name: '', date: '', repeat: 'once', notes: '' })

function openCalEdit(task) {
  calEditTask.value = task
  if (task) {
    calForm.name_pl = task.name_pl ?? ''
    calForm.name = task.name ?? ''
    calForm.date = task.date ?? new Date().toISOString().slice(0, 10)
    calForm.repeat = task.recurrence_type ?? 'once'
    calForm.notes = task.notes ?? ''
  } else {
    calForm.name_pl = ''
    calForm.name = ''
    calForm.date = new Date().toISOString().slice(0, 10)
    calForm.repeat = 'once'
    calForm.notes = ''
  }
  calEditOpen.value = true
}

async function saveCalTask() {
  const data = {
    name_pl: calForm.name_pl,
    name: calForm.name,
    start_date: calForm.date,
    recurrence_type: calForm.repeat,
    notes: calForm.notes,
  }
  try {
    if (calEditTask.value) {
      await calendarStore.updateTask(calEditTask.value.id, data)
    } else {
      await calendarStore.createTask(data)
    }
    calEditOpen.value = false
    showToast(locale.value === 'pl' ? 'Zapisano' : 'Saved')
  } catch (err) {
    showToast(locale.value === 'pl' ? 'Błąd zapisu' : 'Save error')
  }
}

// ─── Maintenance ──────────────────────────────────────────────────────────────
const maintDays = (task) => {
  if (!task.next_due) return 0
  return Math.ceil((new Date(task.next_due) - Date.now()) / 86400000)
}

const inProgressTask = computed(() =>
  maintenanceStore.tasks.find(t => t.started_at !== null) ?? null
)

const hasAnyInProgressMaintenance = computed(() =>
  maintenanceStore.tasks.some(t => t.started_at !== null)
)

async function handleMaintToggle(task) {
  try {
    if (task.started_at) {
      await maintenanceStore.completeTask(task.id)
      showToast(locale.value === 'pl' ? 'Zakończono' : 'Completed')
    } else {
      await maintenanceStore.startTask(task.id)
      showToast(locale.value === 'pl' ? 'Rozpoczęto' : 'Started')
    }
  } catch (err) {
    showToast(locale.value === 'pl' ? 'Błąd' : 'Error')
  }
}

// ─── Plugs ────────────────────────────────────────────────────────────────────
const sheetDevice = ref(null)

async function handlePlugToggle(device) {
  try {
    await sensorsStore.toggleDevice(device.entity_id)
    const updated = sensorsStore.devices.find(d => d.entity_id === device.entity_id)
    if (updated) sheetDevice.value = updated
  } catch (err) {
    showToast(locale.value === 'pl' ? 'Błąd' : 'Error')
  }
}

// ─── Lifecycle ────────────────────────────────────────────────────────────────
onMounted(async () => {
  await Promise.all([
    scheduleStore.fetchDosing(),
    calendarStore.fetchToday(),
    maintenanceStore.fetchTasks(),
    sensorsStore.fetchDevices(),
    scheduleStore.pollFeedStatus(),
  ])
  if (scheduleStore.feedStatus.paused) scheduleStore.startStatusPolling?.()
})

onUnmounted(() => {
  stopCountdown()
})
</script>

<style scoped>
/* Maintenance rows — not in nemo.css */
.maint-row {
  padding: 10px 2px;
  border-top: 1px solid var(--border);
}
.maint-row--first {
  border-top: none;
}
.maint-row.overdue {
  box-shadow: inset 3px 0 0 var(--danger);
  padding-left: 9px;
}

/* Channel sliders */
.channel-label {
  width: 14px;
  font-size: 12px;
  font-weight: 700;
  flex-shrink: 0;
}
input[type='range'] {
  accent-color: var(--accent);
}
</style>

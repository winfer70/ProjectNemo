<template>
  <div>
    <TankSwitcher allow-combined />

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

    <!-- ═══════════════════════════ TODAY TILE(S) ═══════════════════════════ -->
    <!-- One tile per displayedTankIds entry - single mode = just the active
         tank, combined mode = both tanks stacked, each independently
         interactive (its own Feed Now / task list). -->
    <div v-for="tid in displayedTankIds" :key="'today-' + tid" class="tile" :class="{ feeding: scheduleStore.feedStatusFor(tid).paused }">
      <div class="tile-hd">
        <h2>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="4.5" width="18" height="16" rx="2.5"/><path d="M3 9h18"/><path d="M8 2.5v4"/><path d="M16 2.5v4"/><path d="M8.5 14.5l2.2 2.2 4-4.4"/>
          </svg>
          {{ locale === 'pl' ? 'DZISIAJ' : 'TODAY' }}
          <span v-if="tankStore.viewMode === 'combined'" class="muted" style="font-size:11px;font-weight:600;text-transform:none;margin-left:4px">· {{ tankDisplay(tid).name }}</span>
        </h2>
        <span class="meta">{{ todayLabel }}</span>
      </div>
      <hr class="divider">
      <div class="tile-body today-split">
        <!-- Temperature widget -->
        <div class="today-temp">
          <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/>
          </svg>
          <span class="temp-value" :class="tankDisplay(tid).tempClass">
            {{ tankDisplay(tid).temperature != null ? tankDisplay(tid).temperature + '°C' : '—' }}
          </span>
          <span class="temp-label">{{ tankDisplay(tid).name }}</span>
        </div>
        <!-- Task list -->
        <div class="today-tasks">
          <div v-if="tasksFor(tid).length === 0" class="empty">
            <span class="em">🎉</span>
            <span>{{ locale === 'pl' ? 'Brak zadań na dziś' : 'No tasks for today' }}</span>
          </div>
          <template v-else>
            <div v-for="task in tasksFor(tid)" :key="task.id + '_' + task.date">
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
                <div v-if="task.amount" style="font-size:13px;font-weight:600;color:var(--accent);background:var(--surface-2,rgba(255,255,255,0.04));border-radius:8px;padding:7px 12px">
                  {{ task.amount }}
                </div>
                <div v-if="task.notes_pl" style="font-size:12.5px;color:var(--text-muted);white-space:pre-line;line-height:1.65;background:var(--surface-2,rgba(255,255,255,0.04));border-radius:8px;padding:9px 12px">
                  {{ task.notes_pl }}
                </div>
                <div class="task-actions-btns">
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
            </div>
          </template>
        </div>
      </div>
      <hr class="divider">
      <div class="tile-body" style="padding-top:14px">
        <!-- Feeding active state -->
        <div v-if="scheduleStore.feedStatusFor(tid).paused" class="fade-in">
          <div class="row" style="justify-content:center;color:var(--accent-warm);font-weight:700;font-size:13px;margin-bottom:10px;gap:6px">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 4l9 15H3l9-15z"/><path d="M12 10v4"/><circle cx="12" cy="16.5" r="0.6" fill="currentColor" stroke="none"/>
            </svg>
            {{ locale === 'pl' ? 'Karmienie aktywne · 3 min' : 'Feeding active · 3 min' }}
          </div>
          <div class="row" style="gap:10px">
            <div class="bar warm" style="flex:1"><i :style="{ width: feedProgressPctFor(tid) + '%' }"></i></div>
            <span class="tnum" style="font-weight:700;font-size:14px;min-width:42px;text-align:right">{{ feedCountdownStrFor(tid) }}</span>
          </div>
          <div class="muted" style="font-size:12px;text-align:center;margin:7px 0 12px">{{ locale === 'pl' ? 'pozostało' : 'remaining' }}</div>
          <button class="btn btn-danger-o btn-block" @click="handleCancelFeed(tid)">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M6 6l12 12"/><path d="M18 6L6 18"/>
            </svg>
            {{ locale === 'pl' ? 'Anuluj karmienie' : 'Cancel Feeding' }}
          </button>
        </div>
        <!-- Feed Now button -->
        <button v-else class="btn btn-warm btn-block btn-lg" @click="handleFeedNow(tid)">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M16 12c0 0 3-4 6-4-1 2-1 6 0 8-3 0-6-4-6-4z"/><path d="M16 12c-3-4-9-4-12 0 3 4 9 4 12 0z"/><circle cx="7" cy="11" r="0.6" fill="currentColor" stroke="none"/>
          </svg>
          {{ locale === 'pl' ? 'Karm Teraz' : 'Feed Now' }}
        </button>
      </div>
      <div class="tile-body" style="padding-top:0;padding-bottom:14px">
        <button class="btn btn-sm btn-ghost btn-block" style="margin-top:8px" @click="openCalEdit(null, tid)">
          + {{ locale === 'pl' ? 'Dodaj' : 'Add' }}
        </button>
      </div>
    </div>

    <!-- ═══════════════════════════ LIGHTING TILE ═══════════════════════════ -->
    <div v-if="tankStore.activeTankId === 1" class="tile">
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

    <!-- Tank 2 lighting: plain on/off outlet, no BLE/RGBW controller -->
    <div v-else class="tile">
      <div class="tile-hd">
        <h2>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 18h6"/><path d="M10 21h4"/>
            <path d="M12 3a6 6 0 0 0-4 10.5c.7.7 1 1.3 1 2.5h6c0-1.2.3-1.8 1-2.5A6 6 0 0 0 12 3z"/>
          </svg>
          {{ locale === 'pl' ? 'OŚWIETLENIE' : 'LIGHTING' }}
        </h2>
      </div>
      <hr class="divider">
      <div class="tile-body" style="padding-top:13px">
        <div class="spread">
          <div class="row" style="gap:10px">
            <span class="dev-ico" :style="{ color: tank2LightOn ? 'var(--warning)' : 'var(--text-muted)' }">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M9 18h6"/><path d="M10 21h4"/>
                <path d="M12 3a6 6 0 0 0-4 10.5c.7.7 1 1.3 1 2.5h6c0-1.2.3-1.8 1-2.5A6 6 0 0 0 12 3z"/>
              </svg>
            </span>
            <div style="font-weight:600">{{ locale === 'pl' ? 'Światło' : 'Light' }}</div>
          </div>
          <button
            class="toggle accent"
            :class="{ on: tank2LightOn }"
            :aria-pressed="tank2LightOn"
            @click="toggleTank2Light"
          ></button>
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
          <div v-if="filteredMaintenanceTasks.length === 0" class="empty">
            <span>{{ locale === 'pl' ? 'Brak zadań' : 'No tasks' }}</span>
          </div>
          <div
            v-for="(task, i) in filteredMaintenanceTasks"
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
          <div v-if="filteredPlugDevices.length === 0" class="empty">
            <span>{{ locale === 'pl' ? 'Brak urządzeń' : 'No devices' }}</span>
          </div>
          <div
            v-for="device in filteredPlugDevices"
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
              <div class="w">
                <span>{{ device.state === 'on' ? (device.watts ?? 0) : 0 }}W</span>
                <span v-if="device.kwh_today != null" style="margin-left:5px;opacity:0.65">{{ device.kwh_today.toFixed(2) }} kWh</span>
              </div>
            </div>
            <span v-if="device.state !== 'on' && !scheduleStore.feedStatusFor(tankStore.activeTankId).paused && !hasAnyInProgressMaintenance" class="warn-ico">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 4l9 15H3l9-15z"/><path d="M12 10v4"/><circle cx="12" cy="16.5" r="0.6" fill="currentColor" stroke="none"/>
              </svg>
            </span>
            <span v-else class="dot" :class="device.state === 'on' ? 'on' : 'off'"></span>
          </div>
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
import { useTankSelectorStore } from '../stores/tankSelector'
import TankSwitcher from '../components/TankSwitcher.vue'
import * as bleService from '../services/bleService'

const showToast = inject('showToast', () => {})
const { locale } = useI18n()

const scheduleStore = useScheduleStore()
const calendarStore = useCalendarStore()
const maintenanceStore = useMaintenanceStore()
const sensorsStore = useSensorsStore()
const tankStore = useTankSelectorStore()

const filteredMaintenanceTasks = computed(() => maintenanceStore.tasks.filter(tankStore.matchesActiveTank))
const filteredPlugDevices = computed(() => sensorsStore.devices.filter(tankStore.matchesActiveTank))

// Tank 2's Led outlet - plain on/off, no BLE/RGBW controller like Tank 1
const tank2LightOn = computed(() => {
  const d = sensorsStore.devices.find(d => d.role === 'light' && d.tank_id === 2)
  return d?.state === 'on'
})

async function toggleTank2Light() {
  const d = sensorsStore.devices.find(d => d.role === 'light' && d.tank_id === 2)
  if (!d) return
  try {
    await sensorsStore.toggleDevice(d.entity_id)
  } catch (err) {
    showToast(locale.value === 'pl' ? 'Błąd' : 'Error')
  }
}

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

// ─── Feed countdown (per tank, so both tanks can count down independently
// when the combined view is active) ────────────────────────────────────────
const FEED_TOTAL_SECS = 180
const feedSecsLeftByTank = reactive({})
const countdownTimers = {}

function startCountdown(tankId) {
  stopCountdown(tankId)
  feedSecsLeftByTank[tankId] = scheduleStore.feedStatusFor(tankId).resume_in_secs ?? FEED_TOTAL_SECS
  countdownTimers[tankId] = setInterval(() => {
    if (feedSecsLeftByTank[tankId] > 0) feedSecsLeftByTank[tankId]--
    else stopCountdown(tankId)
  }, 1000)
}

function stopCountdown(tankId) {
  if (countdownTimers[tankId]) {
    clearInterval(countdownTimers[tankId])
    delete countdownTimers[tankId]
  }
}

function stopAllCountdowns() {
  for (const tankId of Object.keys(countdownTimers)) stopCountdown(tankId)
}

// Known tank ids - watched unconditionally, harmless if a tank doesn't exist
// (feedStatusFor() falls back to a stable "not paused" default).
for (const tid of [1, 2]) {
  watch(() => scheduleStore.feedStatusFor(tid).paused, (paused) => {
    if (paused) startCountdown(tid)
    else stopCountdown(tid)
  }, { immediate: true })

  watch(() => scheduleStore.feedStatusFor(tid).resume_in_secs, (secs) => {
    if (secs != null && scheduleStore.feedStatusFor(tid).paused && Math.abs(secs - (feedSecsLeftByTank[tid] ?? 0)) > 3) {
      feedSecsLeftByTank[tid] = secs
    }
  })
}

function feedProgressPctFor(tankId) {
  const s = feedSecsLeftByTank[tankId] ?? 0
  return Math.max(0, Math.min(100, (1 - s / FEED_TOTAL_SECS) * 100))
}

function feedCountdownStrFor(tankId) {
  const s = feedSecsLeftByTank[tankId] ?? 0
  return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`
}

// ─── Today tile(s) ────────────────────────────────────────────────────────────
const expandedTask = ref(null)

const todayLabel = computed(() => {
  const d = new Date()
  return d.toLocaleDateString(locale.value === 'pl' ? 'pl-PL' : 'en-IE', {
    weekday: 'long', day: 'numeric', month: 'long',
  })
})

// Single-tank mode shows just the active tank; combined mode shows one tile
// per known tank, independently interactive.
const displayedTankIds = computed(() =>
  tankStore.viewMode === 'combined' ? tankStore.tanks.map(t => t.id) : [tankStore.activeTankId]
)

const tempClass = computed(() => {
  const t = sensorsStore.current.temperature
  if (t == null) return 'temp-null'
  return t >= 24.5 && t <= 27.5 ? 'temp-ok' : 'temp-warn'
})

function classifyTemp(t) {
  if (t == null) return 'temp-null'
  return t >= 24.5 && t <= 27.5 ? 'temp-ok' : 'temp-warn'
}

// Falls back to the single legacy `temperature` field if the API hasn't
// been redeployed with the multi-tank `tanks` array yet.
function tankDisplay(tankId) {
  const tanks = sensorsStore.current.tanks
  const match = tanks?.find(t => Number(t.id) === tankId)
  if (match) return { ...match, tempClass: classifyTemp(match.temperature) }
  return {
    id: tankId,
    name: tankStore.tanks.find(t => t.id === tankId)?.name ?? '',
    temperature: tankId === 1 ? sensorsStore.current.temperature : null,
    tempClass: tankId === 1 ? tempClass.value : 'temp-null',
  }
}

function tasksFor(tankId) {
  return calendarStore.todayTasksByTank[tankId] ?? []
}

function toggleExpanded(key) {
  expandedTask.value = expandedTask.value === key ? null : key
}

async function completeTask(task) {
  await calendarStore.toggleComplete(task.id, task.date)
  expandedTask.value = null
}

async function handleFeedNow(tankId) {
  try {
    await scheduleStore.feedNow(tankId)
  } catch (err) {
    showToast(locale.value === 'pl' ? 'Błąd karmienia' : 'Feed error')
  }
}

async function handleCancelFeed(tankId) {
  try {
    await scheduleStore.cancelFeed(tankId)
  } catch (err) {
    showToast(locale.value === 'pl' ? 'Błąd anulowania' : 'Cancel error')
  }
}

// ─── Calendar edit modal ──────────────────────────────────────────────────────
const calEditOpen = ref(false)
const calEditTask = ref(null)
const calForm = reactive({ name_pl: '', name: '', date: '', repeat: 'once', notes: '', tankId: 1 })

function openCalEdit(task, tankId = tankStore.activeTankId) {
  calEditTask.value = task
  if (task) {
    calForm.name_pl = task.name_pl ?? ''
    calForm.name = task.name ?? ''
    calForm.date = task.date ?? new Date().toISOString().slice(0, 10)
    calForm.repeat = task.recurrence_type ?? 'once'
    calForm.notes = task.notes ?? ''
    calForm.tankId = task.tank_id ?? tankId
  } else {
    calForm.name_pl = ''
    calForm.name = ''
    calForm.date = new Date().toISOString().slice(0, 10)
    calForm.repeat = 'once'
    calForm.notes = ''
    calForm.tankId = tankId
  }
  calEditOpen.value = true
}

async function saveCalTask() {
  const data = {
    tank_id: calForm.tankId,
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
async function loadTankScopedData(tankId) {
  await Promise.all([
    calendarStore.fetchToday(tankId),
    scheduleStore.fetchFeedings(tankId),
    scheduleStore.pollFeedStatus(tankId),
  ])
  if (scheduleStore.feedStatusFor(tankId).paused) scheduleStore.startStatusPolling(tankId)
}

async function loadDisplayedTanksData() {
  await Promise.all(displayedTankIds.value.map(loadTankScopedData))
}

onMounted(async () => {
  await Promise.all([
    maintenanceStore.fetchTasks(),
    sensorsStore.fetchDevices(),
    loadDisplayedTanksData(),
  ])
})

// Combined mode needs both tanks' data; single mode only needs the active one.
watch(() => [tankStore.activeTankId, tankStore.viewMode], () => {
  loadDisplayedTanksData()
})

onUnmounted(() => {
  stopAllCountdowns()
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

/* Today split layout */
.today-split {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}
.today-temp {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 50%;
  flex-shrink: 0;
  gap: 6px;
  color: var(--text-muted);
  padding: 10px 8px 6px;
  border-right: 1px solid var(--border);
}
.today-temp-multi {
  flex-direction: row;
  justify-content: space-evenly;
  gap: 4px;
}
.today-temp-tank {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  min-width: 0;
}
.today-temp-multi .temp-value {
  font-size: 28px;
}
.today-temp-multi .temp-label {
  max-width: 90px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.temp-value {
  font-size: 42px;
  font-weight: 700;
  line-height: 1;
  font-variant-numeric: tabular-nums;
}
.temp-ok { color: var(--success); }
.temp-warn { color: var(--danger); }
.temp-null { color: var(--text-muted); }
.temp-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
}
.today-tasks {
  flex: 1;
  min-width: 0;
  padding-left: 4px;
}
</style>

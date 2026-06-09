<template>
  <div class="tile">
    <div class="tile-hd">
      <h2>
        <svg width="21" height="21" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:middle;margin-right:8px"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
        {{ locale === 'en' ? 'SETTINGS' : 'USTAWIENIA' }}
      </h2>
    </div>
    <hr class="divider" />
    <div class="tile-body">
      <div class="field" style="margin-bottom:24px">
        <label class="field-label">{{ locale === 'en' ? 'Font Size' : 'Rozmiar czcionki' }}</label>
        <div style="display:flex;align-items:center;gap:10px">
          <span class="muted" style="font-size:11px;white-space:nowrap">-100%</span>
          <input
            type="range"
            class="input"
            min="-100"
            max="100"
            step="1"
            :value="fontScale"
            @input="onSliderInput"
            style="width:100%;margin:10px 0"
          />
          <span class="muted" style="font-size:11px;white-space:nowrap">+100%</span>
        </div>
        <div style="display:flex;align-items:center;justify-content:space-between">
          <span class="muted" style="font-size:13px;text-align:center;flex:1">{{ scaleLabel }}</span>
          <button class="btn btn-ghost" style="font-size:12px" @click="resetScale">Reset</button>
        </div>
      </div>

      <div class="field">
        <label class="field-label">{{ locale === 'en' ? 'Language' : 'Język' }}</label>
        <div style="display:flex;gap:8px;margin-top:8px">
          <button class="seg" :class="{ on: locale === 'en' }" @click="setLocale('en')">EN</button>
          <button class="seg" :class="{ on: locale === 'pl' }" @click="setLocale('pl')">PL</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { inject, computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

const { fontScale, setFontScale } = inject('fontScale')

const scaleLabel = computed(() => {
  if (fontScale.value === 0) return 'Default'
  return fontScale.value > 0 ? `+${fontScale.value}%` : `${fontScale.value}%`
})

function onSliderInput(e) {
  setFontScale(Number(e.target.value))
}

function resetScale() {
  setFontScale(0)
}

function setLocale(lang) {
  locale.value = lang
  localStorage.setItem('nemo_locale', lang)
}
</script>

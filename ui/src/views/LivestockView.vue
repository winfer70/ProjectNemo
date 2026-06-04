<template>
  <div class="ls-container">

    <!-- ── Fish section ─────────────────────────────────────────── -->
    <div class="ls-section-header">
      <span class="ls-section-title">{{ locale === 'pl' ? 'Ryby' : 'Fish' }}</span>
      <span class="badge ls-count-badge">{{ FISH.length }} {{ locale === 'pl' ? 'gatunków' : 'species' }}</span>
    </div>

    <div v-for="fish in FISH" :key="fish.latin" class="card ls-fish-card">
      <div class="ls-media-row">
        <img :src="fish.img" :alt="fish.latin" class="ls-thumb" loading="lazy" />
        <div class="ls-media-body">
          <div class="ls-card-top">
            <div class="ls-card-name-block">
              <div class="ls-name">{{ locale === 'pl' ? fish.name_pl : fish.name_en }}</div>
              <div class="ls-latin">{{ fish.latin }}</div>
            </div>
            <span class="badge" :class="statusBadgeClass(fish.status)">{{ statusLabel(fish.status) }}</span>
          </div>
          <div class="ls-badges-row">
            <span class="badge ls-badge-qty">× {{ fish.qty }}</span>
            <span class="badge ls-badge-zone">{{ fish.zone }}</span>
            <span class="badge ls-badge-temp">🌡 {{ fish.temp }}</span>
          </div>
          <div class="ls-notes">{{ fish.notes_pl }}</div>
        </div>
      </div>
    </div>

    <!-- ── Plants section ───────────────────────────────────────── -->
    <div class="ls-section-header ls-section-gap">
      <span class="ls-section-title">{{ locale === 'pl' ? 'Rośliny' : 'Plants' }}</span>
      <span class="badge ls-count-badge">{{ PLANTS.length }} {{ locale === 'pl' ? 'gatunków' : 'species' }}</span>
    </div>

    <div v-for="plant in PLANTS" :key="plant.latin" class="card ls-plant-card">
      <div class="ls-media-row">
        <img :src="plant.img" :alt="plant.latin" class="ls-thumb" loading="lazy" />
        <div class="ls-media-body">
          <div class="ls-card-top">
            <div class="ls-card-name-block">
              <div class="ls-name">{{ locale === 'pl' ? plant.name_pl : plant.name_en }}</div>
              <div class="ls-latin">{{ plant.latin }}</div>
            </div>
            <span class="badge ls-badge-location">{{ plant.location }}</span>
          </div>
          <div class="ls-notes">{{ plant.notes_pl }}</div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const { locale } = useI18n()

// ── Fish stocking data ────────────────────────────────────────
const FISH = [
  { name_en: 'Pearl Gourami',              name_pl: 'Gurami Mozaikowe',                 latin: 'Trichopodus leerii',                      qty: 2,  zone: 'Top/Mid',      status: 'in_tank', temp: '24–28°C', notes_pl: 'Para (1M+1F). Ryba labiryntowa — potrzebuje dostępu do powierzchni.',   img: 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Trichopodus_leerii_Natural_History_Museum_University_of_Pisa.jpg/330px-Trichopodus_leerii_Natural_History_Museum_University_of_Pisa.jpg' },
  { name_en: 'Five-Banded Barb',           name_pl: 'Brzanka Pięciopręga',              latin: 'Desmopuntius pentazona',                  qty: 18, zone: 'Mid',          status: 'in_tank', temp: '23–26°C', notes_pl: 'Ławica. 12 już w akwarium + 6 dochodzi 16 czerwca.',                    img: 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Cyprinidae_Desmopuntius_pentazona_1.jpg/330px-Cyprinidae_Desmopuntius_pentazona_1.jpg' },
  { name_en: 'Cardinal Tetra',             name_pl: 'Neon Czerwony',                    latin: 'Paracheirodon axelrodi',                  qty: 18, zone: 'Mid',          status: 'step_2a', temp: '23–27°C', notes_pl: 'Ławica. 12 szt. przybywa 16 czerwca, 6 szt. 30 czerwca.',             img: 'https://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Cardinal_Paracheirodon_axelrodi_%283%29.jpg/330px-Cardinal_Paracheirodon_axelrodi_%283%29.jpg' },
  { name_en: 'Corydoras Sterbai',          name_pl: 'Kirysek Sterbai',                  latin: 'Corydoras sterbai',                       qty: 8,  zone: 'Bottom',       status: 'step_2b', temp: '25–28°C', notes_pl: 'Dno/piasek. Przybywa 30 czerwca.',                                      img: 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Corydoras_Sterbai.jpg/330px-Corydoras_Sterbai.jpg' },
  { name_en: 'Panda Garra',                name_pl: 'Garra Panda',                      latin: 'Garra flavatra',                          qty: 4,  zone: 'Rocks/Wood',   status: 'step_2a', temp: '23–27°C', notes_pl: '2 szt. 16 czerwca, 2 szt. 30 czerwca. Potrzebuje biofilmu na skałach.', img: 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Panda_Garra.jpg/330px-Panda_Garra.jpg' },
  { name_en: 'Red Apistogramma Double Red',name_pl: 'Pielęgniczka Agassiza Double Red', latin: 'Apistogramma agassizii "Double Red"',    qty: 2,  zone: 'Bottom/Caves', status: 'step_2b', temp: '24–27°C', notes_pl: 'Para. Przybywa 30 czerwca. Zajmują kokosy.',                             img: 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8f/Apistogramma_agassizii_in_aquarium.jpg/330px-Apistogramma_agassizii_in_aquarium.jpg' },
  { name_en: 'Otocinclus',                 name_pl: 'Otonek Pospolity',                 latin: 'Otocinclus vittatus',                     qty: 6,  zone: 'Leaves/Glass', status: 'step_3',  temp: '22–26°C', notes_pl: 'Przybywa 14 lipca. Czyści liście i szyby.',                             img: 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Otocinclus_vittatus.jpg/330px-Otocinclus_vittatus.jpg' },
  { name_en: 'Amano Shrimp',               name_pl: 'Krewetka Amano',                  latin: 'Caridina multidentata',                   qty: 6,  zone: 'Everywhere',   status: 'in_tank', temp: '20–27°C', notes_pl: 'Już w akwarium. Czyści biofilm z korzenia.',                            img: 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Amano_Garnele_%2885281493%29.jpeg/330px-Amano_Garnele_%2885281493%29.jpeg' },
]

// ── Plant data ────────────────────────────────────────────────
const PLANTS = [
  { name_en: 'Amazon Sword', name_pl: 'Żabienica (Echinodorus)', latin: 'Echinodorus bleheri',     location: 'Right island', notes_pl: 'Duże liście. Otocinclus poleruje liście. Nawóz kapsułkowy co 6 mies.', img: 'https://upload.wikimedia.org/wikipedia/commons/d/d0/Echinodorus_bleheri.jpg' },
  { name_en: 'Limnophila',   name_pl: 'Limnofila',              latin: 'Limnophila sessiliflora', location: 'Left island',  notes_pl: 'Krzaczasta. Daje schronienie przy powierzchni dla Gurami.',           img: 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Limnophila_sessiliflora.jpg/330px-Limnophila_sessiliflora.jpg' },
  { name_en: 'Cryptocoryne', name_pl: 'Kryptokoryna',           latin: 'Cryptocoryne sp.',        location: 'Midground',    notes_pl: 'Niska technika. Żywi się z podłoża i odpadów ryb.',                   img: 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Cryptocoryne_wendtii_Green.jpg/330px-Cryptocoryne_wendtii_Green.jpg' },
  { name_en: 'Anubias',      name_pl: 'Anubias',                latin: 'Anubias barteri',         location: 'On wood/rock', notes_pl: 'Przywiązana do korzenia lub Dragon Stone. Niska technika.',            img: 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Anubias_barteri_var_glabra.jpg/330px-Anubias_barteri_var_glabra.jpg' },
  { name_en: 'Ludwigia',     name_pl: 'Ludwigia',               latin: 'Ludwigia sp.',            location: 'Background',   notes_pl: 'Czerwienieje pod czerwonym światłem Aquasky.',                         img: 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Ludwigia_repens.JPG/330px-Ludwigia_repens.JPG' },
]

// ── Status helpers ────────────────────────────────────────────
function statusLabel(status) {
  const labels = locale.value === 'pl'
    ? { in_tank: '✅ W akwarium', step_2a: '🛒 16 cze', step_2b: '🛒 30 cze', step_3: '🛒 14 lip' }
    : { in_tank: '✅ In tank',    step_2a: '🛒 Jun 16', step_2b: '🛒 Jun 30', step_3: '🛒 Jul 14' }
  return labels[status] ?? status
}

function statusBadgeClass(status) {
  if (status === 'in_tank') return 'ls-status-green'
  if (status === 'step_2a' || status === 'step_2b') return 'ls-status-blue'
  return 'ls-status-grey'
}
</script>

<style scoped>
/* ── Container ───────────────────────────────────────────────── */
.ls-container {
  padding-bottom: 8px;
}

/* ── Section headers ─────────────────────────────────────────── */
.ls-section-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}
.ls-section-gap {
  margin-top: 16px;
}
.ls-section-title {
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--text-muted);
}
.ls-count-badge {
  background: rgba(0, 180, 216, 0.12);
  color: var(--accent);
  border: 1px solid rgba(0, 180, 216, 0.25);
}

/* ── Fish / Plant cards ──────────────────────────────────────── */
.ls-fish-card,
.ls-plant-card {
  margin-bottom: 8px;
}

/* ── Media row: thumbnail + body ─────────────────────────────── */
.ls-media-row {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}
.ls-thumb {
  width: 80px;
  height: 60px;
  object-fit: cover;
  border-radius: 6px;
  flex-shrink: 0;
  background: rgba(255,255,255,0.04);
}
.ls-media-body {
  flex: 1;
  min-width: 0;
}

/* ── Card top row: name block + status badge ─────────────────── */
.ls-card-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 6px;
}
.ls-card-name-block {
  flex: 1;
  min-width: 0;
}
.ls-name {
  font-size: 15px;
  font-weight: 700;
  color: var(--text);
  line-height: 1.3;
}
.ls-latin {
  font-size: 11px;
  font-style: italic;
  color: var(--text-muted);
  margin-top: 2px;
}

/* ── Badge row ───────────────────────────────────────────────── */
.ls-badges-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 8px;
}

/* ── Individual badge styles ─────────────────────────────────── */
.ls-badge-qty {
  background: rgba(255, 255, 255, 0.06);
  color: var(--text);
  border: 1px solid var(--border);
  font-weight: 700;
}
.ls-badge-zone {
  background: rgba(72, 202, 228, 0.10);
  color: var(--accent2);
  border: 1px solid rgba(72, 202, 228, 0.20);
}
.ls-badge-temp {
  background: rgba(230, 57, 70, 0.10);
  color: #f4a261;
  border: 1px solid rgba(230, 57, 70, 0.20);
}
.ls-badge-location {
  background: rgba(46, 196, 182, 0.10);
  color: var(--ok);
  border: 1px solid rgba(46, 196, 182, 0.20);
  white-space: nowrap;
}

/* ── Status badges ───────────────────────────────────────────── */
.ls-status-green {
  background: rgba(46, 196, 182, 0.15);
  color: var(--ok);
  border: 1px solid rgba(46, 196, 182, 0.30);
  white-space: nowrap;
  flex-shrink: 0;
}
.ls-status-blue {
  background: rgba(0, 180, 216, 0.15);
  color: var(--accent);
  border: 1px solid rgba(0, 180, 216, 0.30);
  white-space: nowrap;
  flex-shrink: 0;
}
.ls-status-grey {
  background: rgba(123, 163, 190, 0.10);
  color: var(--text-muted);
  border: 1px solid var(--border);
  white-space: nowrap;
  flex-shrink: 0;
}

/* ── Notes ───────────────────────────────────────────────────── */
.ls-notes {
  font-size: 12px;
  color: var(--text-muted);
  line-height: 1.5;
}
</style>

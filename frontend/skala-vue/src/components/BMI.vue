<template>
  <h1> BMI 계산기 🧮</h1>
  <div class="card">
    <!-- 1) 기본 입력 -->
    <div class="grid">
      <div class="field">
        <label>이름</label>
        <input v-model="name" type="text" placeholder="이름 입력" />
      </div>
      <div class="field">
        <label>나이(만, 년)</label>
        <input v-model.number="ageYears" type="number" min="0" step="1" placeholder="예: 15" />
      </div>
      <div class="field">
        <label>성별</label>
        <select v-model="sex">
          <option value="1">남자</option>
          <option value="2">여자</option>
        </select>
      </div>
      <div class="field">
        <label>키(cm)</label>
        <input v-model.number="height" type="number" min="0" step="0.1" placeholder="예: 170" />
      </div>
      <div class="field">
        <label>체중(kg)</label>
        <input v-model.number="weight" type="number" min="0" step="0.1" placeholder="예: 65" />
      </div>
    </div>

    <!-- 2) BMI 결과 -->
    <div class="result">
      <div><strong>BMI:</strong> <span>{{ bmi > 0 ? bmi.toFixed(2) : '-' }}</span></div>
      <div><strong>판정:</strong> <span>{{ judgement || '-' }}</span></div>
      <div v-if="warningMsg" class="warn">{{ warningMsg }}</div>
    </div>

    <!-- 3) 그래프 & 백분위 -->
    <div class="chart-area">
      <h3>연령대별 표준 몸무게 분포</h3>
      <p v-if="isAdult">
        현재 선택한 나이(≥20세)는 CDC 소아·청소년 표준(2~20세) 범위 밖입니다.
        분포 그래프/백분위는 표시하지 않고, BMI 정상 범위(18.5~24.9)에 따른
        체중 목표(약 {{ healthyMin.toFixed(1) }}~{{ healthyMax.toFixed(1) }} kg)만 안내합니다.
      </p>

      <div v-else>
        <canvas ref="chartEl" height="160"></canvas>
        <div class="percentile" v-if="userPercentile !== null">
          <strong>{{ name || '사용자' }}</strong> 님은
          <strong>동일 연령/성별</strong> 대비
          <strong>상위 {{ (100 - userPercentile).toFixed(1) }}%</strong>
          (백분위 {{ userPercentile.toFixed(1) }}‑th)에 위치합니다.
        </div>
        <small class="note">
          데이터 출처: CDC Growth Charts – Weight‑for‑Age (2–20y) CSV (LMS). 백분위는 LMS z‑score 기반 정규분포 누적확률로 계산했습니다.
        </small>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'

// ============== 상태 ==============
const name = ref('')
const ageYears = ref(15)     // 만 나이(년)
const sex = ref('1')         // 1=male, 2=female (CDC 표 규칙)
const height = ref(0)        // cm
const weight = ref(0)        // kg

const warningMsg = ref('')

// ============== BMI 계산/판정 ==============
const bmi = computed(() => (height.value > 0 ? weight.value / ((height.value / 100) ** 2) : 0))

const judgement = computed(() => {
  if (bmi.value === 0) return ''
  if (bmi.value < 18.5) return '저체중'
  if (bmi.value < 23.0) return '정상'
  if (bmi.value < 25.0) return '과체중'
  return '비만'
})

watch(bmi, (v) => {
  warningMsg.value = v >= 23.0 ? '다이어트 하세요!' : ''
})

// ============== 성인 BMI 기반 목표 체중(안내용) ==============
const healthyMin = computed(() => (height.value > 0 ? 18.5 * (height.value / 100) ** 2 : 0))
const healthyMax = computed(() => (height.value > 0 ? 24.9 * (height.value / 100) ** 2 : 0))
const isAdult = computed(() => ageYears.value >= 20)

// ============== CDC LMS 데이터 로드 (2~20세) ==============
/**
 * CDC wtage.csv: 열 예시
 *  Sex(1/2), Agemos(개월, 24~240), L, M, S, P3, P5, P10, P25, P50, P75, P90, P95, P97
 * 참고 및 수식: https://www.cdc.gov/growthcharts/cdc-data-files.htm
 */
const LMSRows = ref([]) // {sex:Number, agemos:Number, L:Number, M:Number, S:Number, PXX...}

async function fetchCDC() {
  const url = 'https://www.cdc.gov/growthcharts/data/zscore/wtage.csv'
  const res = await fetch(url)
  const text = await res.text()
  // 간단 CSV 파서 (쉼표 + 개행)
  const lines = text.trim().split(/\r?\n/)
  const header = lines[0].split(',')
  const idx = {
    Sex: header.indexOf('Sex'),
    Agemos: header.indexOf('Agemos'),
    L: header.indexOf('L'),
    M: header.indexOf('M'),
    S: header.indexOf('S'),
    P3: header.indexOf('P3'),
    P50: header.indexOf('P50'),
    P97: header.indexOf('P97'),
  }
  LMSRows.value = lines.slice(1).map((row) => {
    const c = row.split(',')
    return {
      sex: Number(c[idx.Sex]),
      agemos: Number(c[idx.Agemos]),
      L: Number(c[idx.L]),
      M: Number(c[idx.M]),
      S: Number(c[idx.S]),
      P3: Number(c[idx.P3]),
      P50: Number(c[idx.P50]),
      P97: Number(c[idx.P97]),
    }
  })
}

// ============== LMS 보간 & 백분위 ==============
// 나이를 개월로 변환(2~20세: 24~240개월)
const ageMonths = computed(() => Math.round(ageYears.value * 12))

function lerp(a, b, t) { return a + (b - a) * t }

// 해당 성별, 주변 두 개월 레코드로 선형보간해서 L/M/S 추정
function getLMSFor(age_mo, sexVal) {
  const rows = LMSRows.value.filter(r => r.sex === Number(sexVal)).sort((a,b)=>a.agemos-b.agemos)
  if (rows.length === 0) return null
  if (age_mo <= rows[0].agemos) return rows[0]
  if (age_mo >= rows[rows.length-1].agemos) return rows[rows.length-1]
  let lo=0, hi=rows.length-1
  while (lo <= hi) {
    const mid = (lo+hi)>>1
    if (rows[mid].agemos === age_mo) return rows[mid]
    if (rows[mid].agemos < age_mo) lo = mid+1
    else hi = mid-1
  }
  const i = Math.max(1, lo)
  const r1 = rows[i-1], r2 = rows[i]
  const t = (age_mo - r1.agemos) / (r2.agemos - r1.agemos)
  return {
    sex: r1.sex,
    agemos: age_mo,
    L: lerp(r1.L, r2.L, t),
    M: lerp(r1.M, r2.M, t),
    S: lerp(r1.S, r2.S, t),
    // 보조용 백분위 기준선(3/50/97)도 보간
    P3: lerp(r1.P3, r2.P3, t),
    P50: lerp(r1.P50, r2.P50, t),
    P97: lerp(r1.P97, r2.P97, t),
  }
}

// 정규 CDF 근사 (erf 기반)
function normCdf(z) {
  const t = 1 / (1 + 0.2316419 * Math.abs(z))
  const d = 0.3989423 * Math.exp(-z*z/2)
  let p = d * t * (0.3193815 + t*(-0.3565638 + t*(1.781478 + t*(-1.821256 + t*1.330274))))
  p = z > 0 ? 1 - p : p
  return p
}

// 체중 → z‑score (CDC 공식식)
function zFromLMS(x, L, M, S) {
  if (L !== 0) return (Math.pow(x / M, L) - 1) / (L * S)
  return Math.log(x / M) / S
}

const userPercentile = ref(null) // 0~100

watch([() => weight.value, ageMonths, sex], () => {
  if (isAdult.value || !weight.value || LMSRows.value.length === 0) {
    userPercentile.value = null
    renderChart() // 성인모드면 그래프 클리어
    return
  }
  const lms = getLMSFor(ageMonths.value, sex.value)
  if (!lms) { userPercentile.value = null; return }
  const z = zFromLMS(weight.value, lms.L, lms.M, lms.S)
  const p = normCdf(z) * 100
  userPercentile.value = Math.max(0, Math.min(100, p))
  renderChart(lms)
})

// ============== Chart.js ==============
let chart
const chartEl = ref(null)

function renderChart(lms = null) {
  if (!chartEl.value) return
  // Chart.js 동적 로드 (CDN)
  if (!window.Chart) {
    const s = document.createElement('script')
    s.src = 'https://cdn.jsdelivr.net/npm/chart.js'
    s.onload = () => renderChart(lms)
    document.head.appendChild(s)
    return
  }
  if (chart) { chart.destroy(); chart = null }

  if (isAdult.value || !lms) {
    // 성인 모드: 그래프 비우기
    const ctx = chartEl.value.getContext('2d')
    ctx.clearRect(0, 0, chartEl.value.width, chartEl.value.height)
    return
  }

  // 간단한 3개 기준선(3/50/97 백분위) + 사용자 위치 점
  const labels = ['P3', 'P50', 'P97', '나']
  const data = [lms.P3, lms.P50, lms.P97, weight.value]

  const ctx = chartEl.value.getContext('2d')
  chart = new window.Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: '체중(kg)',
        data,
      }],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: { enabled: true },
        title: {
          display: true,
          text: `연령 ${ageYears.value}세 / 성별 ${sex.value==='1'?'남':'여'} – 표준(kg)과 현재 체중`
        }
      },
      scales: {
        y: { beginAtZero: true }
      }
    }
  })
}

onMounted(async () => {
  await fetchCDC()
  renderChart()
})
</script>

<style scoped>
.card { border: 1px solid #e5e7eb; border-radius: 14px; padding: 16px; box-shadow: 0 1px 6px rgba(0,0,0,.04); }
.grid { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 12px; }
.field { display: flex; flex-direction: column; gap: 6px; }
.field label { font-size: 12px; color: #374151; }
.field input, .field select { padding: 8px 10px; border: 1px solid #d1d5db; border-radius: 8px; }

.result { display: flex; gap: 16px; align-items: center; margin: 12px 0; font-size: 15px; }
.warn { color: #c2410c; font-weight: 700; }

.chart-area { margin-top: 10px; }
.percentile { margin: 8px 0 0; font-size: 14px; }
.note { color: #6b7280; }
@media (max-width: 920px) {
  .grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
}
</style>

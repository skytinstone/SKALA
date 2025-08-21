<!-- Practice/Eatfood.vue -->
 <template>
  <div class="wrap">
    <!-- 1) 시작 전: 사용자 정보 입력 -->
    <form v-if="!started" class="card" @submit.prevent="start">
      <h2>사용자 기본정보 입력</h2>
      <div class="grid">
        <label>이름
          <input v-model.trim="name" placeholder="예: 홍길동" />
        </label>
        <label>나이
          <input v-model.number="age" type="number" min="1" placeholder="예: 29" />
        </label>
        <label>키 (cm)
          <input v-model.number="heightCm" type="number" min="50" step="0.1" placeholder="예: 170" />
        </label>
        <label>몸무게 (kg)
          <input v-model.number="weight" type="number" min="1" step="0.1" placeholder="예: 60" />
        </label>
      </div>

      <p class="hint">모든 값을 입력한 뒤 “시작하기”를 눌러주세요.</p>
      <button class="primary" :disabled="!isValid">시작하기</button>
    </form>

    <!-- 2) 시작 후: BMI 상태 + 자식 컴포넌트 동작 -->
    <div v-else class="card">
      <h1>{{ name }}의 BMI 상태</h1>
      <p><strong>나이:</strong> {{ age }}세</p>
      <p><strong>현재 체중:</strong> {{ weight.toFixed(1) }}kg</p>
      <p><strong>현재 키:</strong> {{ heightCm.toFixed(1) }}cm</p>
      <p><strong>BMI:</strong> {{ bmi.toFixed(1) }} ({{ bmiLabel }})</p>

      <section>
        <EatFood @eat="changeWeight" />
      </section>

      <section>
        <Practice @train="changeWeight" />
      </section>

      <div class="actions">
        <button @click="started = false">정보 수정</button>
        <button class="ghost" @click="reset">초기화</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import EatFood from './components/EatFood.vue'
import Practice from './components/Practice.vue'

// 입력값
const name = ref('')
const age = ref()
const heightCm = ref()
const weight = ref()

// 진행 상태
const started = ref(false)

// 유효성
const isValid = computed(() =>
  !!name.value &&
  Number.isFinite(age.value) && age.value > 0 &&
  Number.isFinite(heightCm.value) && heightCm.value > 0 &&
  Number.isFinite(weight.value) && weight.value > 0
)

// BMI
const bmi = computed(() => {
  if (!isValid.value) return 0
  const h = heightCm.value / 100
  return weight.value / (h * h)
})

const bmiLabel = computed(() => {
  const v = bmi.value
  if (v === 0) return '-'
  if (v < 18.5) return '저체중'
  if (v < 23)   return '정상'
  if (v < 25)   return '과체중'
  return '비만'
})

// 폼 제출
function start() {
  if (!isValid.value) return
  started.value = true
}

// 자식에서 주는 체중 증감(±kg)
function changeWeight(delta) {
  if (!started.value) return
  const next = (Number(weight.value) || 0) + delta
  weight.value = Math.max(0, Number(next.toFixed(1)))
}

// 초기화
function reset() {
  started.value = false
  name.value = ''
  age.value = undefined
  heightCm.value = undefined
  weight.value = undefined
}
</script>

<style scoped>
.wrap { max-width: 640px; margin: 24px; font-family: system-ui, -apple-system, Segoe UI, Roboto, 'Noto Sans KR', sans-serif; }
.card { border: 2px solid #222; padding: 16px 18px; border-radius: 12px; background: #fff; }
h1, h2 { margin: 6px 0 14px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
label { display: flex; flex-direction: column; gap: 6px; font-weight: 600; }
input { padding: 8px 10px; border-radius: 8px; border: 1px solid #ccc; }
.hint { color: #666; margin: 10px 0 14px; }
.primary { padding: 10px 14px; border-radius: 10px; border: 1px solid #111; background: #ffd400; cursor: pointer; }
.primary:disabled { opacity: .5; cursor: not-allowed; }
section { margin-top: 18px; }
.actions { margin-top: 16px; display: flex; gap: 8px; }
button { padding: 8px 12px; border-radius: 10px; border: 1px solid #ddd; background: #f7f7f7; cursor: pointer; }
button.ghost { background: #fff; }
button:hover { background: #f0f0f0; }
.actions {
  margin-top: 16px;
  display: flex;
  gap: 10px;
  justify-content: center;  /* ← 가운데 정렬 추가 */
}
</style>



<!-- BMI.vue -->
<!-- <template>
  <BMI></BMI>
</template>

<script setup>  
import BMI from './components/BMI.vue';
</script>

<style scoped>
.wrapper { max-width: 920px; margin: 24px auto; padding: 0 12px; }
h1 { text-align: center; margin-bottom: 16px; }
</style> -->

<!-- StrigifyAnything.vue -->
<!-- <template>
  <StrigifyAnything></StrigifyAnything>
</template>

<script setup>  
import StrigifyAnything from './components/StrigifyAnything.vue';
</script> -->

<!-- EventHandling -->
<!-- <template>
  <EventHandling></EventHandling>
</template>

<script setup>    
  import EventHandling from './components/EventHandling.vue';
</script> -->


<!-- EventCapture -->
 <!-- <template>
    <EventCapture>  

    </EventCapture>
 </template>

<script setup>
import EventCapture from './components/EventCapture.vue'; 
</script> -->


<!-- CommentMaker.vue template & Script -->
<!-- <template>
  <div id="app">
    <CommentMaker />
  </div>
</template>

<script setup>
import CommentMaker from './components/CommentMaker.vue'; // CommentMaker.vue를 import
</script> -->




<!-- looplist tmeplate & script -->
<!-- <template>
  <looplist></looplist>
</template>

<script setup>
import LoopList from './components/looplist.vue';
</script> -->



<!-- ShowBox template -->
<!-- <template>
  <ShowBox></ShowBox>
</template>

<script setup>
import ShowBox from './components/ShowBox.vue';
</script> -->


<!-- BoxStyle template -->
<!-- <template>
  <BoxStyle></BoxStyle>
</template>

<script setup>
import BoxStyle from './components/BoxStyle.vue';
</script> -->

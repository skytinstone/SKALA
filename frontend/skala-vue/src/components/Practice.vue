<template>
  <div>
    <div class="group-title">🏃 기술 연습</div>
    <div class="btns">
      <button @click="train(-1)">걷기 (-1kg)</button>
      <button @click="train(-2)">달리기 (-2kg)</button>
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['train'])
function train(delta) {
  emit('train', delta) // 부모(App)로 -kg 전달
}
</script>

<style scoped>
.group-title { 
  font-size: 18px; 
  margin: 8px 0 10px; 
  text-align: center;        /* ← 제목도 가운데 정렬 */
}
.btns { 
  display: flex; 
  gap: 8px; 
  flex-wrap: wrap; 
  justify-content: center;   /* ← 버튼 가운데 정렬 */
}
button { 
  padding: 8px 12px; 
  border: 1px solid #ddd; 
  border-radius: 8px; 
  background: #fff; 
  cursor: pointer; 
}
button:hover { background: #f5f5f5; }
</style>


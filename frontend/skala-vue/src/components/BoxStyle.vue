<template>
  <div>
    <!-- 색상과 사이즈 입력 받기 -->
    <input v-model="color" placeholder="색상 입력 (ex: orange)" />
    <input v-model="size" type="number" placeholder="사이즈 입력 (px)" />
    <button @click="applyStyle">적용</button>

    <!-- 스타일을 적용할 div 박스 -->
    <div :style="{ backgroundColor: color, width: size + 'px', height: size + 'px' }">
      스타일 미리보기 박스
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const color = ref('orange');  // 기본 색상
const size = ref(150);        // 기본 크기

// 스타일 적용 함수
const applyStyle = () => {
  // 색상과 사이즈는 v-model로 자동 반영되므로 추가적인 처리 없이 바로 적용됨
};
</script>

<style scoped>
div {
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  text-align: center;
  margin-top: 20px;
}
</style>

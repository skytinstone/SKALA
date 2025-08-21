<template>
  <div>
    <div
      class="box"
      @mousemove="updateMousePosition"
      @mouseleave="resetMousePosition"
      :style="{ width: '400px', height: '400px', backgroundColor: 'lightgray' }"
    >
      <p>마우스 좌표: X: {{ mouseX }}, Y: {{ mouseY }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const mouseX = ref(0);
const mouseY = ref(0);

// 마우스 좌표 갱신
const updateMousePosition = (event) => {
  mouseX.value = event.offsetX;
  mouseY.value = event.offsetY;
};

// 마우스가 박스를 벗어날 때 좌표 초기화
const resetMousePosition = () => {
  mouseX.value = 0;
  mouseY.value = 0;
};
</script>

<style scoped>
.box {
  margin: 0 auto;
  border: 1px solid #000;
  position: relative;
}
p {
  position: absolute;
  bottom: 10px;
  left: 10px;
  font-size: 14px;
  color: black;
}
</style>

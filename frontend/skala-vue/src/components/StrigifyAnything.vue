<template>
  <div>
    <h1>Vue 3에서 toJsonString 함수 예제</h1>
    <p>num: {{ toJsonString(num) }}</p>
    <p>obj: {{ toJsonString(obj) }}</p>
    <p>arr: {{ toJsonString(arr) }}</p>
    <p>r1: {{ toJsonString(r1) }}</p>
    <p>r2: {{ toJsonString(r2) }}</p>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';

// toJsonString 함수 작성
function toJsonString(value) {
  return JSON.stringify(value);
}

const num = 123;
const obj = { name: '홍길동', age: 30 };
const arr = [1, 2, 3];
const r1 = ref({ city: '서울' });
const r2 = reactive({ job: '개발자' });
</script>

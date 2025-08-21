<template>
    <button @click="doClick">버튼</button>
    <div>{{ message }}</div>
</template>

<script setup>
import { ref } from 'vue';

const message = ref('')
const doClick = () => {
    message.value = '버튼이 클릭되었습니다!'
}
</script>
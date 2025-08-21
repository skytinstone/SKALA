<template>
    <button @click=""></button>

    <template v-if="isVisible">
            <div>보입니다.</div>
    <p>나도 보여야해</p>
    </template>
    <div>안 보입니다.</div>

    <div v-show="isVisible">나는 보일까요?</div>
    <p>{{ message }}</p>
</template>

<script setup>  
import { ref } from 'vue';

const isVisible = ref(true);
const message = ref('');

function changeVisible()   {
    isVisible.value = !isVisible.value;
}
</script>
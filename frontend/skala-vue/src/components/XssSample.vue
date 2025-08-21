<template>
    <h1> XSS 예제 </h1>
    <input v-model="inputMessage"></input>
    <button> @click="showMessage"</button>
    <div> TEXT 출력 : {{outputMessage}}</div>
    <div> HTML 출력 : <p> v-html ="outputMessage"</p></div>
</template>

<script setup>
import { ref } from 'vue'

const inputMessage = ref()
const outputMessage = ref()

function showMessage() {
    outputMessage.value = inputMessage.value
}

</script>
<template>
    <ul>
        <li v-for="(fruit, index) in fruits">{{index}}.{{ fruit }}</li>
    </ul>
    <hr>
    </hr>
    <input v-model="inputFurit"></input> <button @click="addFruit">추가</button>
</template>

<script setup>
import { ref } from 'vue';


const fruits = ['사과', '바나나', '오렌지'];
const inputFruit = ref('');

function addFruit() {
    const inputFruit = document.getElementById('fruitInput').value;
    console.log(inputFruit.value);
    fruits.push(inputFruit.value);
    console.log(fruits);
}
</script>
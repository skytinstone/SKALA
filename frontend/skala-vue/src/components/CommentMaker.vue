<template>
  <div>
    <!-- 댓글 텍스트 입력창 -->
    <input v-model="newComment" placeholder="댓글을 입력하세요" />
    
    <!-- 등록 버튼 -->
    <button @click="addComment">등록</button>
    
    <!-- 댓글 목록 -->
    <ul>
      <li v-for="(comment, index) in comments" :key="index">{{ comment }}</li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const newComment = ref(''); // 새로운 댓글을 입력받을 텍스트
const comments = ref([]); // 댓글 목록을 저장할 배열

// 댓글 추가 함수
const addComment = () => {
  if (newComment.value.trim() !== '') {
    comments.value.push(newComment.value); // 댓글을 목록에 추가
    newComment.value = ''; // 입력창 초기화
  }
};
</script>

<style scoped>
/* 필요한 스타일 추가 */
input {
  margin-right: 10px;
}
button {
  padding: 5px 10px;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  margin: 5px 0;
}
</style>

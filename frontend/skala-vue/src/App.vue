<!-- src/App.vue -->
<template>
  <div id="app">
    <header class="header">
      <router-link class="home" to="/">둔갑술 선택 메뉴</router-link>
    </header>

    <!-- 현재 라우트 컴포넌트가 그려지는 자리 -->
    <router-view />
  </div>
</template>

<script setup>
// Vue 3 <script setup> 사용 — 별도 로직 없음
</script>

<style>
#app {
  max-width: 960px;
  margin: 40px auto;
  text-align: center;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, "Apple SD Gothic Neo", "Noto Sans KR", sans-serif;
}
.header {
  margin-bottom: 24px;
}
.home {
  text-decoration: none;
  font-weight: 700;
  font-size: 20px;
  color: #222;
}
.home:hover {
  text-decoration: underline;
}
</style>

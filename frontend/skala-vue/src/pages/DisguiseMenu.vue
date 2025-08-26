<template>
  <div>
    <h1>둔갑술 선택 메뉴</h1>

    <!-- 버튼 2개: 호랑이 / 도깨비 -->
    <button @click="goDisguise('호랑이')">호랑이로 둔갑</button>
    <button @click="goDisguise('도깨비')">도깨비로 둔갑</button>
  </div>
</template>

<script>
export default {
  name: 'DisguiseMenu',
  methods: {
    goDisguise(target) {
      // 결과 페이지로 이동 (query로 대상 전달)
      this.$router.push({ path: '/disguise', query: { target } })
    }
  }
}
</script>

<style scoped>
button {
  margin: 6px;
  padding: 10px 16px;
  border: none;
  background: #1976d2;
  color: #fff;
  border-radius: 8px;
  cursor: pointer;
}
button:hover { background: #1565c0; }
</style>

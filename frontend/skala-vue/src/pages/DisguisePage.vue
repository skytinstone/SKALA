<template>
  <div>
    <h1>둔갑술 시전!</h1>
    <p>
      신민석은 <strong>{{ target }}</strong>로 변신했습니다{{ ending }}
    </p>
  </div>
</template>

<script>
export default {
  name: 'DisguisePage',
  props: {
    target: { type: String, required: true }
  },
  computed: {
    // 요구사항: 도깨비 → 느낌표(!), 호랑이 → 마침표(.)
    ending() {
      return this.target === '도깨비' ? '!' : '.'
    }
  },
  created() {
    // URL에서 query를 숨기기: /disguise?target=호랑이  →  /disguise
    if (this.$route.query.target) {
      this.$router.replace({ path: '/disguise' })
    }
  }
}
</script>

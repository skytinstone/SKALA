<template>

    <h1>{{ target }}으로 변신했습니다.</h1>
</template>

<script setup>
    import {ref, onMounted} from 'vue';
    import {useRoute, useRouter} from 'vue-router';

    const route = useRoute();
    const router = useRouter();
    const target = ref('');

    onMounted(() => {
console.log(route)
target.value = route.query.target || '알 수 없는 존재';
router.replace({ path: '/disguise' });
    });

</script>
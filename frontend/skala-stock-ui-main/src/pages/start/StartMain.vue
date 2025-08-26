<script setup>
import { ref, reactive, computed } from 'vue';
import { useRouter } from 'vue-router';
import apiCall from '@/scripts/api-call';
import { storePlayer } from '@/scripts/store-player';
import { notifyInfo } from '@/scripts/store-popups';

const router = useRouter();

/* --- state --- */
const playerId = ref('');
const playerPassword = ref('');
const playerPasswordConfirm = ref('');
const playerMoney = ref('');
const isNewPlayer = ref(false); // false: 로그인 모드 / true: 회원가입 모드

const loading = ref(false);
const errors = reactive({ id: '', pw: '', pwConfirm: '', money: '' });

/* --- helpers --- */
function resetErrors() {
  errors.id = '';
  errors.pw = '';
  errors.pwConfirm = '';
  errors.money = '';
}

/** 비밀번호 규칙: 10자 이상 + 특수문자 1자 이상 */
function validatePasswordRule(pw) {
  const hasMinLen = typeof pw === 'string' && pw.length >= 10;
  const hasSpecial = /[^A-Za-z0-9]/.test(pw);
  return { hasMinLen, hasSpecial, ok: hasMinLen && hasSpecial };
}

/* 비밀번호 일치 여부 (둘 다 입력 시 즉시 반영) */
const pwFilled = computed(() => !!playerPassword.value && !!playerPasswordConfirm.value);
const pwEqual  = computed(() => pwFilled.value && playerPassword.value === playerPasswordConfirm.value);

/* --- validations --- */
function validateLogin() {
  resetErrors();
  if (!playerId.value.trim()) errors.id = '플레이어ID를 입력하세요.';
  if (!playerPassword.value) errors.pw = '비밀번호를 입력하세요.';
  return !(errors.id || errors.pw);
}

function validateSignup() {
  // 로그인 기본값 검사 먼저
  const okLogin = validateLogin();

  // 비밀번호 규칙
  const rule = validatePasswordRule(playerPassword.value);
  if (!rule.ok) {
    if (!rule.hasMinLen && !rule.hasSpecial) errors.pw = '비밀번호는 10자 이상이며 특수문자를 포함해야 합니다.';
    else if (!rule.hasMinLen) errors.pw = '비밀번호는 10자 이상이어야 합니다.';
    else if (!rule.hasSpecial) errors.pw = '비밀번호에 특수문자를 최소 1자 포함하세요.';
  }

  // 비밀번호 일치
  if (!pwEqual.value) {
    errors.pwConfirm = '비밀번호가 일치하지 않습니다.';
  }

  // 보유금액
  const n = Number(playerMoney.value);
  if (playerMoney.value === '' || Number.isNaN(n) || n < 0) {
    errors.money = '보유금액은 0 이상의 숫자여야 합니다.';
  }

  return okLogin && !errors.pw && !errors.pwConfirm && !errors.money;
}

/* --- API --- */
// 로그인: POST /api/players/login
const login = async () => {
  if (!validateLogin()) return;
  loading.value = true;
  try {
    const res = await apiCall('/api/players/login', {
      playerId: playerId.value.trim(),
      playerPassword: playerPassword.value,   // ← 필드명 교체
    }, 'POST', { 'Content-Type': 'application/json', Accept: 'application/json' });

    storePlayer(res?.data ?? res);
    router.push('/stock'); // 주식 거래 페이지
  } catch (e) {
    const status = e?.response?.status;
    const msg = e?.response?.data?.message || e?.message || '아이디/비밀번호를 확인하세요.';
    notifyInfo(`로그인 실패${status ? ` (HTTP ${status})` : ''}`, msg);

    // 실패 시: 회원가입 안내 및 가입모드로 전환
    isNewPlayer.value = true;
    console.error('[login:error]', { status, data: e?.response?.data });
  } finally {
    loading.value = false;
  }
};

// 회원가입: POST /api/players
const signup = async () => {
  // 가입모드 아니면 모드만 켜고 리턴 → 추가입력란 노출
  if (!isNewPlayer.value) {
    isNewPlayer.value = true;
    return;
  }
  if (!validateSignup()) return;

  loading.value = true;
  try {
    const payload = {
      playerId: playerId.value.trim(),
      playerPassword: playerPassword.value,   // ← 필드명 교체
      playerMoney: Number(playerMoney.value), // ← 필드명 교체
    };
    const res = await apiCall('/api/players', payload, 'POST', {
      'Content-Type': 'application/json',
      Accept: 'application/json',
    });

    // 성공 시 자동 로그인 처리
    storePlayer(res?.data ?? res);
    notifyInfo('가입 완료', '환영합니다! 자동으로 로그인됩니다.');
    router.push('/stock');
  } catch (e) {
    const status = e?.response?.status;
    const raw = e?.response?.data;
    console.error('[signup:error]', { status, raw });
    notifyInfo(`회원가입 실패${status ? ` (HTTP ${status})` : ''}`, 
               typeof raw === 'string' ? raw : JSON.stringify(raw));
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="container-sm mt-3 border border-2 p-1" style="max-width: 600px">
    <div class="bss-background p-1">
      <div class="mt-3 d-flex justify-content-center" style="height: 230px;">
        <span class="text-center text-danger fs-1 fw-bold mt-4">TOSS 증권</span>
      </div>

      <div class="row bg-info-subtle p-2 m-1" style="opacity: 95%;">
        <div class="col">
          <!-- ID -->
          <InlineInput
            v-model="playerId"
            label="플레이어ID"
            class="mb-1"
            type="text"
            placeholder="플레이어ID"
          />
          <small v-if="errors.id" class="text-danger">{{ errors.id }}</small>

          <!-- PW -->
          <InlineInput
            v-model="playerPassword"
            label="비밀번호"
            class="mb-1"
            type="password"
            placeholder="비밀번호"
          />
          <small v-if="errors.pw" class="text-danger d-block">{{ errors.pw }}</small>

          <!-- 주의사항 (가입 모드에서만 노출) -->
          <div v-if="isNewPlayer" class="form-text mt-1">
            <ul class="mb-2 ps-3">
              <li>비밀번호는 <strong>10자 이상</strong>이어야 합니다.</li>
              <li><strong>특수문자</strong>를 최소 1자 포함하세요. 예: <code>!@#$%^&*()_+-=</code></li>
              <li>공백 없이 영문 대/소문자, 숫자, 특수문자를 조합해 주세요.</li>
              <li>아이디/생일/연속문자(aaa111 등) 사용은 피하세요.</li>
            </ul>
          </div>

          <!-- PW 확인 (가입 모드 전용) -->
          <div v-if="isNewPlayer">
            <InlineInput
              v-model="playerPasswordConfirm"
              label="비밀번호 확인"
              class="mb-1"
              type="password"
              placeholder="비밀번호 확인"
            />

            <!-- 즉시 피드백 -->
            <small v-if="pwFilled && pwEqual" class="text-success">비밀번호가 일치합니다.</small>
            <small v-else-if="pwFilled && !pwEqual" class="text-danger">비밀번호가 일치하지 않습니다.</small>

            <!-- 제출 시 에러 표시 -->
            <small v-if="errors.pwConfirm" class="text-danger d-block">{{ errors.pwConfirm }}</small>
          </div>

          <!-- 초기 보유금액 (가입 모드 전용) -->
          <div v-if="isNewPlayer" class="mt-1">
            <InlineInput
              v-model="playerMoney"
              label="보유금액"
              class="mb-1"
              type="number"
              placeholder="예: 100000"
            />
            <small v-if="errors.money" class="text-danger">{{ errors.money }}</small>
          </div>
        </div>

        <!-- 버튼 -->
        <div class="d-flex justify-content-between align-items-center mt-2">
          <button class="btn btn-primary btn-sm" type="button" :disabled="loading" @click="login">
            <span v-if="loading" class="spinner-border spinner-border-sm me-1" />
            로그인
          </button>

          <button class="btn btn-outline-primary btn-sm" type="button" :disabled="loading" @click="signup">
            {{ isNewPlayer ? '회원가입 실행' : '회원가입' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.bss-background {
  width: 590px;
  height: 380px;
  background-image: url('/logo.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}
</style>

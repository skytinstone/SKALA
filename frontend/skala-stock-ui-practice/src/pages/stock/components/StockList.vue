<script setup>
  import { ref, reactive, watch, onMounted } from 'vue';
  import apiCall from '@/scripts/api-call';
import { get } from 'http';

  const stockName = ref('');
  const stockPrice = ref('');
  const table = reactive({
    headers:[
      { label : "주식ID", value: "id"},
      { label : "주식명", value: "stockName"},
      { label : "주식가격", value: "stockPrice"}
    ],
    items:[]
  })

  const page = reactive({
    count:10,
    current:1,
    total:0
  })

  const getStockList = async () => {
    table.items.length = 0

    const url = '/api/stock/list';
    const queryParams = {
      page: page.current,
      count: page.count
    }
    const { body: pagedList } = await apiCall.get(url, queryParams)
    if (pagedList) {
      page.current = pagedList.offset + 1;
      table.items = pagedList.list;
      page.total = pagedList.total;
    }

    const response = await apiCall.post(url, requestBody);
    if (response.result === apiCall.Response.SUCCESS){
      table.items = response.body.items;
      page.total = response.body.total;
    }
  }

  const addStock = async () => {
    const url = '/api/stock/add';
    const requestBody = {
      id: 0,
      stockName: stockName.value,
      stockPrice: stockPrice.value
    }
    await apiCall.post(url, null, requestBody);
    getStockList();
    stockName.value = '';
    stockPrice.value = '';
  }

  watch(() => page.current, () => {
    getStockList();
  })

  watch(() => page.count, () => {
    page.current = 1
    getStockList();
  })

  onMounted(() => {
    getStockList();
  })  
 
</script>

<template>
  <div class="row mt-2">
    <span class="fs-4"><i class="bi bi-graph-up m-2"></i>주식목록</span>
  </div>
  <div class="row border-bottom">
    <div class="col d-flex justify-content-end">
      <button class="btn btn-sm btn-primary m-1">
        <i class="bi bi-arrow-counterclockwise m-2"></i>갱신</button>
    </div>
  </div>
  <div class="row g-2 align-items-center m-2 mt-0">
    <div class="col">
      <ItemsTable :nosetting="true" />
      <PageNavigator />
    </div>
  </div>
  <div class="row g-2 m-2 border-top">
    <div class="col-2 d-flex justify-content-end">
      <label class="col-form-label form-control-sm p-1">주식정보</label>
    </div>
    <div class="col">
      <InlineInput placeholder="주식명" />
    </div>
    <div class="col">
      <InlineInput placeholder="주식가격" />
    </div>
    <div class="col d-flex justify-content-start">
      <button class="btn btn-sm btn-outline-primary me-2">주식 추가</button>
    </div>
  </div>
</template>

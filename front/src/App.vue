<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { init, dispose } from 'klinecharts'
import axios from 'axios'


const stocks = ref([])
const asymbol = ref('')
const chart = {}

function refresh() {
  axios.get("http://127.0.0.1:5000/api/fetch/kline/"+asymbol.value)
  .then(response => {
    console.log(response)
    loadStock(asymbol.value)
  })
  .catch(e => {
    this.errors.push(e)
  })
}

function loadStock(symbol) {
  if (symbol === '') {
    return
  }

  console.log(symbol)
  asymbol.value = symbol
  axios.get("http://127.0.0.1:5000/api/kline/"+symbol)
  .then(response => {
    

    const data = response.data.data
    const chartData = data.map(item => {
      return {
        timestamp: item[0],
        volume:    item[1],
        open:      item[2],
        high:      item[3],
        low:       item[4],
        close:     item[5]
      }
    })
    console.log(chartData)
    chart.chart.applyNewData(chartData)
  })
  .catch(e => {
    this.errors.push(e)
  })
}

onMounted(() => {
  chart.chart = init('chart')

  axios.get("http://127.0.0.1:5000/api/stock")
  .then(response => {
    console.log(response)
    stocks.value = response.data.data
    console.log(stocks)
  })
})

onUnmounted(() => {
  dispose('chart')
})
</script>

<template>
  <div>
    <h3>今日关注</h3>
    <div>
      <label v-for="stock in stocks" :key="stock.symbol">
        <button @click="loadStock(stock.symbol)">{{ stock.name }}</button>
      </label>
    </div>
  </div>
  <div>
    <input type="text" v-model="asymbol.symbol" />
    <button @click="loadStock">Load</button>
  </div>
  <div>
    <label>
      <button @click="refresh">{{ asymbol }} Refresh</button>
    </label>
    <div id="chart" style="width:600px;height:300px" />
  </div>
</template>
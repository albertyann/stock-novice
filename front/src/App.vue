<script setup>
import { onMounted, onUnmounted } from 'vue'
import { init, dispose } from 'klinecharts'
import axios from 'axios'

onMounted(() => {
  const chart = init('chart')

  axios.get("http://127.0.0.1:5000/api/kline")
  .then(response => {
    console.log(response)
    const data = response.data
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
    chart.applyNewData(chartData)
  })
  .catch(e => {
    this.errors.push(e)
  })
})

onUnmounted(() => {
  dispose('chart')
})
</script>

<template>
  <div id="chart" style="width:600px;height:300px" />
</template>
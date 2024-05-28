<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { init, dispose } from 'klinecharts'
import chartOption from './chart.config'
import hotkeys from "hotkeys-js"


import {
    request, unFavorite, fetchTodayRiseStock,
    stockSearch, downTodayRiseStock, 
    getStockKlineData, errors, tips
} from './Event.d'

const stocks = ref([])
const curStock = ref({
  symbol: '',
  name: ''
})
const searchValue = ref('')
const chart = {}
const klineLastDate = ref('')

hotkeys("j", () => {
  let stockIndex = 0
  for (let i = 0; i < stocks.value.length; i++) {
    if (stocks.value[i].symbol == curStock.value.symbol) {
      stockIndex = i
      break
    }
  }
  if (stockIndex == stocks.value.length - 1) {
	console.log('last')
	return false
  }
  if (stockIndex < stocks.value.length - 1) {
    stockIndex++
  }

  curStock.value = stocks.value[stockIndex]
  loadStock(curStock.value, null)
  nextViewPosition()
});

hotkeys("k", () => {
  let stockIndex = 0
  for (let i = 0; i < stocks.value.length; i++) {
    if (stocks.value[i].symbol == curStock.value.symbol) {
      stockIndex = i
      break
    }
  }
  if (stockIndex == 0) {
	console.log('first')
	return false
  }
  if (stockIndex > 0) {
    stockIndex--
  }
  curStock.value = stocks.value[stockIndex]
  loadStock(curStock.value, null)
  prevViewPosition()
});

hotkeys("r", () => {
  refresh(curStock.value)
});


function resetViewPosition() {
  let ele = document.getElementById('item-view')
  ele.style.top = 0 + 'px'
}

function nextViewPosition() {
  let ele = document.getElementById('item-view')
  let y = ele.offsetTop
  ele.style.top =  (y + 88) + 'px'

  let box_elem = document.getElementById('item-box')
  // 设置 box_elem 滚动条位置
  box_elem.scrollTop = y + 88
}

function prevViewPosition() {
  let ele = document.getElementById('item-view')
  let y = ele.offsetTop
  if (y <= 0) {
    ele.style.top = 0 + 'px'
  } else {
    ele.style.top = (y - 88) + 'px'
  }

  let box_elem = document.getElementById('item-box')
  // 设置 box_elem 滚动条位置
  box_elem.scrollTop = y - 88
}

function refresh(stock) {
	request("/api/fetch/kline/"+ stock.symbol)
	.then(res => {
		if (res.data.code == 0) {
			loadStock(stock, null)
		}
	})
	.catch(e => {
		console.log(e)
	})
}

function favorite(stock) {
    request("/api/stock/favorite/"+ stock.symbol)
    .then(response => {
        console.log(response)
    })
    .catch(e => {
        this.errors.push(e)
    })
}

function favoriteStockList() {
  request("/api/stock/favorite")
  .then(res => {
        stocks.value = res.data
        curStock.value = stocks.value[0]
        loadStock(curStock.value, null)
        resetViewPosition()
    })
    .catch(e => {
        this.errors.push(e)
    })
}


function loadStock(stock, event) {
	if (event) {
		const y = event.target.offsetTop
		let ele = document.getElementById('item-view')
		ele.style.top = y - 32 + 'px'
	}

	if (stock == null) {
		return
	}

  curStock.value = stock
  getStockKlineData(stock)
  .then((res) => {
    if (res.length > 0) {
		let stock = res.at(-1)
		let d = new Date(stock.timestamp)
		klineLastDate.value = (d.getMonth() + 1) + "-" + d.getDate()
    } else {
		klineLastDate.value = ''
	}
    chart.chart.applyNewData(res)
  })
}

function todayStockList() {
  request("/api/last/stock")
  .then(res => {
    stocks.value = res.data
    curStock.value = stocks.value[0]

    loadStock(curStock.value, null)
    resetViewPosition()
  })
  .catch(e => {
    errors.push(e)
  })
}

function onPageDown(e) {
  console.log(e)
}

onMounted(() => {
  chart.chart = init('chart')
  chart.chart.setStyles(chartOption)
  chart.chart.createIndicator('VOL')

  todayStockList()
})

onUnmounted(() => {
  dispose('chart')
})
</script>

<template>
  <div class="grid grid-cols-4 gap-px-4">
    <div class="py-4 col-start-1 col-end-1">
      <a class="btn-primary" href="javascript:void(0)" @click="downTodayRiseStock">Down</a>
      <a class="btn-primary" href="javascript:void(0)" @click="fetchTodayRiseStock">标注</a>
    </div>
    <div class="py-4 col-start-2 col-end-3">
      <a class="btn-primary" href="javascript:void(0)" @click="todayStockList">今日</a>
      <a class="btn-primary" href="javascript:void(0)" @click="favoriteStockList">关注</a>
      <a class="btn-primary" href="javascript:void(0)" @click="fetchTodayRiseStock">头部</a>
      <a class="btn-primary" href="javascript:void(0)" @click="fetchTodayRiseStock">长期</a>
    </div>
    <div class="py-4 col-start-3 col-end-5">
      <div class="group relative rounded-md dark:bg-slate-700 dark:highlight-white/10 dark:focus-within:bg-transparent">
        <svg width="20" height="20" fill="currentColor" class="absolute left-3 top-1/2 -mt-2.5 text-slate-400 pointer-events-none group-focus-within:text-blue-500 dark:text-slate-500">
          <path fill-rule="evenodd" clip-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"></path>
        </svg>
        <input type="text" class="input-search" v-model="searchValue" />
        <a class="btn-default pl-5" @click="stockSearch">确定</a>
        <span>{{ errors }}</span>
        <span>{{ tips }}</span>
      </div>
    </div>
  </div>

  <div class="grid grid-flow-col grid-cols-8 gap-2" @keyup.down="onPageDown">
    <div class="col-start-1 col-end-1 p-1">
      <h3>今日[{{ (new Date()).getUTCDate()  }}]</h3>
      <div class="item-box" id="item-box">
        <div class="item" v-for="stock in stocks" :key="stock.symbol">
            <div>
              <label>{{ stock.symbol }}</label>
            </div>
            <div @click="loadStock(stock, $event)">
              <a class="name" href="javascript:void(0)">{{ stock.name }}</a>
            </div>
            <div class="item-tags-box">
              <span class="stock_tag" v-for="tag in stock.tags" :key="tag"> {{ tag }}</span>
            </div>
        </div>
        <div id="item-view" class="item-view"></div>
      </div>
    </div>

    <div class="col-start-2 col-end-9 p-1">
      <div class="w-full">
        <a class="btn-stock-a" :href="'https://xueqiu.com/S/'+ curStock.symbol" target="_blank">{{ curStock.symbol }}</a>
        {{ curStock.name }}
        <a class="btn-default" @click="refresh(curStock)">更新K线</a>
        <a class="btn-default" @click="refresh(curStock)">生成TAG</a>
        <span v-if="curStock.favorite == 0">
          <a class="btn-default" @click="favorite(curStock)">关注</a>
        </span>
        <span v-if="curStock.favorite == 1">
          <a class="btn-default" @click="unFavorite(curStock)">取消关注</a>
        </span>
        <span>
          {{ klineLastDate }}
        </span>
      </div>
      <div>
        <div id="chart" style="width:700px;height:420px" />
      </div>
    </div>
  </div>
  
</template>

<style>
  .item-box {
    position: relative;
    float: left;
    flex-wrap: wrap;
    justify-content: flex-start;
    overflow: auto;
    height: calc(100vh - 200px);
    overflow-x: hidden;
  }
  .item-view {
    float: left;
    border: 1px solid #7293b1;
    width: calc(100% - 8px);
    height: 89px;
    position: absolute;
    z-index: -99;
    left: 0;
    top: 0;
    overflow: auto;
  }
  .item-tags-box {
    display: inline-block;
    overflow: hidden;
    content: normal;
    height: 22px;
  }
  .item {
    display: inline-block;
    margin: 1px;
    width: calc(100% - 10px);
    padding: 5px;
    background-color: aliceblue;
  }
  .item .stock_tag {
    margin: 0 5px 0 0 ;
    font-size: 0.9em;
    color: #d9896a;
    background-color: #fcefe3;
  }
  .chart-box {
    float: left;
    flex-direction: column;
    justify-content: flex-start;
    width: 600px;
    margin-left: 10px;
  }
  .chart-box label {
    margin-bottom: 10px;
  }
  .chart-box button {
    margin-left: 10px;
  }
</style>
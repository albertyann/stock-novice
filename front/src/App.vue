<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import { init, dispose } from 'klinecharts'
import axios from 'axios'

const stocks = ref([])
const curStock = ref({
  symbol: '',
  name: ''
})
const chart = {}

function refresh(stock) {
  axios.get("http://127.0.0.1:5000/api/fetch/kline/"+ stock.symbol)
  .then(response => {
    loadStock(stock, null)
  })
  .catch(e => {
    this.errors.push(e)
  })
}

function favorite(stock) {
  axios.get("http://127.0.0.1:5000/api/stock/favorite/"+ stock.symbol)
  .then(response => {
    console.log(response)
  })
  .catch(e => {
    this.errors.push(e)
  })
}

function unFavorite(stock) {
  axios.get("http://127.0.0.1:5000/api/stock/unfavorite/"+ stock.symbol)
  .then(response => {
    console.log(response)
  })
  .catch(e => {
    this.errors.push(e)
  })
}

function fetchTodayRiseStock() {
  axios.get("http://127.0.0.1:5000/api/stock/today/rise")
  .then(response => {
    stocks.value = response.data.data
    curStock.value = stocks.value[0]
    loadStock(curStock.value, null)
    resetViewPosition()
  })
  .catch(e => {
    this.errors.push(e)
  })
  .catch(e => {
    this.errors.push(e)
  })
}

function downTodayRiseStock() {
  axios.get("http://127.0.0.1:5000/api/stock/today/down")
  .then(response => {
    lastStockList()
  })
  .catch(e => {
    this.errors.push(e)
  })
  .catch(e => {
    this.errors.push(e)
  })
}

function fetchFavoriteStock() {
  axios.get("http://127.0.0.1:5000/api/stock/favorite")
  .then(response => {
    stocks.value = response.data.data
    curStock.value = stocks.value[0]
    loadStock(curStock.value, null)
    resetViewPosition()
  })
  .catch(e => {
    this.errors.push(e)
  })
}

function resetViewPosition() {
  let ele = document.getElementById('item-view')
  ele.style.top = 0 + 'px'
}

function loadStock(stock, event) {
  if (event) {
    const y = event.target.offsetTop
    let ele = document.getElementById('item-view')
    ele.style.top = y - 30 + 'px'
  }

  if (stock == null) {
    return
  }

  curStock.value = stock
  axios.get("http://127.0.0.1:5000/api/kline/"+ stock.symbol)
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
    chart.chart.applyNewData(chartData)
  })
  .catch(e => {
    this.errors.push(e)
  })
}

function lastStockList() {
  axios.get("http://127.0.0.1:5000/api/last/stock")
  .then(response => {
    stocks.value = response.data.data
    curStock.value = stocks.value[0]
    loadStock(curStock.value, null)
    resetViewPosition()
  })
  .catch(e => {
    this.errors.push(e)
  })
}

var options = {
  // 网格线
  grid: {
    show: true,
    horizontal: {
      show: true,
      size: 1,
      color: '#EDEDED',
      style: 'dashed',
      dashedValue: [2, 2]
    },
    vertical: {
      show: true,
      size: 1,
      color: '#EDEDED',
      style: 'dashed',
      dashedValue: [2, 2]
    }
  },
  // 蜡烛图
  candle: {
    // 蜡烛图类型 'candle_solid'|'candle_stroke'|'candle_up_stroke'|'candle_down_stroke'|'ohlc'|'area'
    type: 'candle_solid',
    // 蜡烛柱
    bar: {
      upColor: '#F92855',
      downColor: '#2DC08E',
      noChangeColor: '#888888',
      upBorderColor: '#F92855',
      downBorderColor: '#2DC08E',
      noChangeBorderColor: '#888888',
      upWickColor: '#F92855',
      downWickColor: '#2DC08E',
      noChangeWickColor: '#888888'
    },
    // 面积图
    area: {
      lineSize: 2,
      lineColor: '#2196F3',
      value: 'close',
      smooth: false,
      backgroundColor: [{
        offset: 0,
        color: 'rgba(33, 150, 243, 0.01)'
      }, {
        offset: 1,
        color: 'rgba(33, 150, 243, 0.2)'
      }],
      point: {
        show: true,
        radius: 4,
        rippleRadius: 8,
        animation: true,
        animationDuration: 1000
      }
    },
    priceMark: {
      show: true,
      // 最高价标记
      high: {
        show: true,
        color: '#D9D9D9',
        textOffset: 5,
        textSize: 10,
        textFamily: 'Helvetica Neue',
        textWeight: 'normal'
      },
      // 最低价标记
      low: {
        show: true,
        color: '#D9D9D9',
        textOffset: 5,
        textSize: 10,
        textFamily: 'Helvetica Neue',
        textWeight: 'normal',
      },
      // 最新价标记
      last: {
        show: true,
        upColor: '#2DC08E',
        downColor: '#F92855',
        noChangeColor: '#888888',
        line: {
          show: true,
          // 'solid' | 'dashed'
          style: 'dashed',
          dashedValue: [4, 4],
          size: 1
        },
        text: {
          show: true,
          // 'fill' | 'stroke' | 'stroke_fill'
          style: 'fill',
          size: 12,
          paddingLeft: 4,
          paddingTop: 4,
          paddingRight: 4,
          paddingBottom: 4,
          // 'solid' | 'dashed'
          borderStyle: 'solid',
          borderSize: 0,
          borderColor: 'transparent',
          borderDashedValue: [2, 2],
          color: '#FFFFFF',
          family: 'Helvetica Neue',
          weight: 'normal',
          borderRadius: 2
        }
      }
    },
    // 提示
    tooltip: {
      offsetLeft: 4,
      offsetTop: 6,
      offsetRight: 4,
      offsetBottom: 6,
      // 'always' | 'follow_cross' | 'none'
      showRule: 'always',
      // 'standard' | 'rect'
      showType: 'standard',
      // 自定义显示，可以是回调方法也可以是数组，当是一个方法时，需要返回一个数组
      // 数组的子项类型为 { title, value }
      // title和value可以是字符串或者对象，对象类型为 { text, color }
      // title 或者 title.text 可以是国际化的 key，
      // value 或者 value.text 支持字符串模版
      // 例如：想显示时间，开盘和收盘，配置[{ title: 'time', value: '{time}' }, { title: 'open', value: '{open}' }, { title: 'close', value: '{close}' }]
      custom: [
        { title: 'time', value: '{time}' },
        { title: 'open', value: '{open}' },
        { title: 'high', value: '{high}' },
        { title: 'low', value: '{low}' },
        { title: 'close', value: '{close}' },
        { title: 'volume', value: '{volume}' }
      ],
      defaultValue: 'n/a',
      rect: {
        // 'fixed' | 'pointer'
        position: 'fixed',
        paddingLeft: 4,
        paddingRight: 4,
        paddingTop: 4,
        paddingBottom: 4,
        offsetLeft: 4,
        offsetTop: 4,
        offsetRight: 4,
        offsetBottom: 4,
        borderRadius: 4,
        borderSize: 1,
        borderColor: '#f2f3f5',
        color: '#FEFEFE'
      },
      text: {
        size: 12,
        family: 'Helvetica Neue',
        weight: 'normal',
        color: '#D9D9D9',
        marginLeft: 8,
        marginTop: 4,
        marginRight: 8,
        marginBottom: 4
      },
      // 示例：
      // [{
      //   id: 'icon_id',
      //   position: 'left', // 类型有'left'，'middle'，'right'
      //   marginLeft: 8,
      //   marginTop: 6,
      //   marginRight: 0,
      //   marginBottom: 0,
      //   paddingLeft: 1,
      //   paddingTop: 1,
      //   paddingRight: 1,
      //   paddingBottom: 1,
      //   icon: '\ue900',
      //   fontFamily: 'iconfont',
      //   size: 12,
      //   color: '#76808F',
      //   backgroundColor: 'rgba(33, 150, 243, 0.2)',
      //   activeBackgroundColor: 'rgba(33, 150, 243, 0.4)'
      // }]
      icons: []
    }
  },
  // 技术指标
  indicator: {
    ohlc: {
      upColor: 'rgba(45, 192, 142, .7)',
      downColor: 'rgba(249, 40, 85, .7)',
      noChangeColor: '#888888'
    },
    bars: [{
      // 'fill' | 'stroke' | 'stroke_fill'
      style: 'fill',
      // 'solid' | 'dashed'
      borderStyle: 'solid',
      borderSize: 1,
      borderDashedValue: [2, 2],
      upColor: 'rgba(45, 192, 142, .7)',
      downColor: 'rgba(249, 40, 85, .7)',
      noChangeColor: '#888888'
    }],
    lines: [
      {
        // 'solid' | 'dashed'
        style: 'solid',
        smooth: false,
        size: 1,
        dashedValue: [2, 2],
        color: '#FF9600'
      }, {
        style: 'solid',
        smooth: false,
        size: 1,
        dashedValue: [2, 2],
        color: '#935EBD'
      }, {
        style: 'solid',
        smooth: false,
        size: 1,
        dashedValue: [2, 2],
        color: '#2196F3'
      }, {
        style: 'solid',
        smooth: false,
        size: 1,
        dashedValue: [2, 2],
        color: '#E11D74'
      }, {
        style: 'solid',
        smooth: false,
        size: 1,
        dashedValue: [2, 2],
        color: '#01C5C4'
      }
    ],
    circles: [{
      // 'fill' | 'stroke' | 'stroke_fill'
      style: 'fill',
      // 'solid' | 'dashed'
      borderStyle: 'solid',
      borderSize: 1,
      borderDashedValue: [2, 2],
      upColor: 'rgba(45, 192, 142, .7)',
      downColor: 'rgba(249, 40, 85, .7)',
      noChangeColor: '#888888'
    }],
    // 最新值标记
    lastValueMark: {
      show: false,
      text: {
        show: false,
        // 'fill' | 'stroke' | 'stroke_fill'
        style: 'fill',
        color: '#FFFFFF',
        size: 12,
        family: 'Helvetica Neue',
        weight: 'normal',
        // 'solid' | 'dashed'
        borderStyle: 'solid',
        borderSize: 1,
        borderDashedValue: [2, 2],
        paddingLeft: 4,
        paddingTop: 4,
        paddingRight: 4,
        paddingBottom: 4,
        borderRadius: 2
      }
    },
    // 提示
    tooltip: {
      offsetLeft: 4,
      offsetTop: 6,
      offsetRight: 4,
      offsetBottom: 6,
      // 'always' | 'follow_cross' | 'none'
      showRule: 'always',
      // 'standard' | 'rect'
      showType: 'standard',
      showName: true,
      showParams: true,
      defaultValue: 'n/a',
      text: {
        size: 12,
        family: 'Helvetica Neue',
        weight: 'normal',
        color: '#D9D9D9',
        marginTop: 4,
        marginRight: 8,
        marginBottom: 4,
        marginLeft: 8
      },
      // 示例：
      // [{
      //   id: 'icon_id',
      //   position: 'left', // 类型有'left'，'middle'，'right'
      //   marginLeft: 8,
      //   marginTop: 6,
      //   marginRight: 0,
      //   marginBottom: 0,
      //   paddingLeft: 1,
      //   paddingTop: 1,
      //   paddingRight: 1,
      //   paddingBottom: 1,
      //   icon: '\ue900',
      //   fontFamily: 'iconfont',
      //   size: 12,
      //   color: '#76808F',
      //   backgroundColor: 'rgba(33, 150, 243, 0.2)',
      //   activeBackgroundColor: 'rgba(33, 150, 243, 0.4)'
      // }]
      icons: []
    }
  },
  // x轴
  xAxis: {
    show: true,
    size: 'auto',
    // x轴线
    axisLine: {
      show: true,
      color: '#888888',
      size: 1
    },
    // x轴分割文字
    tickText: {
      show: true,
      color: '#D9D9D9',
      family: 'Helvetica Neue',
      weight: 'normal',
      size: 12,
      marginStart: 4,
      marginEnd: 4
    },
    // x轴分割线
    tickLine: {
      show: true,
      size: 1,
      length: 3,
      color: '#888888'
    }
  },
  // y轴
  yAxis: {
    show: true,
    size: 'auto',
    // 'left' | 'right'
    position: 'right',
    // 'normal' | 'percentage' | 'log'
    type: 'normal',
    inside: false,
    reverse: false,
    // y轴线
    axisLine: {
      show: true,
      color: '#888888',
      size: 1
    },
    // x轴分割文字
    tickText: {
      show: true,
      color: '#D9D9D9',
      family: 'Helvetica Neue',
      weight: 'normal',
      size: 12,
      marginStart: 4,
      marginEnd: 4
    },
    // x轴分割线
    tickLine: {
      show: true,
      size: 1,
      length: 3,
      color: '#888888'
    }
  },
  // 图表之间的分割线
  separator: {
    size: 1,
    color: '#888888',
    fill: true,
    activeBackgroundColor: 'rgba(230, 230, 230, .15)'
  },
  // 十字光标
  crosshair: {
    show: true,
    // 十字光标水平线及文字
    horizontal: {
      show: true,
      line: {
        show: true,
        // 'solid'|'dashed'
        style: 'dashed',
        dashedValue: [4, 2],
        size: 1,
        color: '#888888'
      },
      text: {
        show: true,
        // 'fill' | 'stroke' | 'stroke_fill'
        style: 'fill',
        color: '#FFFFFF',
        size: 12,
        family: 'Helvetica Neue',
        weight: 'normal',
        // 'solid' | 'dashed'
        borderStyle: 'solid',
        borderDashedValue: [2, 2],
        borderSize: 1,
        borderColor: '#686D76',
        borderRadius: 2,
        paddingLeft: 4,
        paddingRight: 4,
        paddingTop: 4,
        paddingBottom: 4,
        backgroundColor: '#686D76'
      }
    },
    // 十字光标垂直线及文字
    vertical: {
      show: true,
      line: {
        show: true,
        // 'solid'|'dashed'
        style: 'dashed',
        dashedValue: [4, 2],
        size: 1,
        color: '#888888'
      },
      text: {
        show: true,
        // 'fill' | 'stroke' | 'stroke_fill'
        style: 'fill',
        color: '#FFFFFF',
        size: 12,
        family: 'Helvetica Neue',
        weight: 'normal',
        // 'solid' | 'dashed'
        borderStyle: 'solid',
        borderDashedValue: [2, 2],
        borderSize: 1,
        borderColor: '#686D76',
        borderRadius: 2,
        paddingLeft: 4,
        paddingRight: 4,
        paddingTop: 4,
        paddingBottom: 4,
        backgroundColor: '#686D76'
      }
    }
  },
  // 覆盖物
  overlay: {
    point: {
      color: '#1677FF',
      borderColor: 'rgba(22, 119, 255, 0.35)',
      borderSize: 1,
      radius: 5,
      activeColor: '#1677FF',
      activeBorderColor: 'rgba(22, 119, 255, 0.35)',
      activeBorderSize: 3,
      activeRadius: 5
    },
    line: {
      // 'solid' | 'dashed'
      style: 'solid',
      smooth: false,
      color: '#1677FF',
      size: 1,
      dashedValue: [2, 2]
    },
    rect: {
      // 'fill' | 'stroke' | 'stroke_fill'
      style: 'fill',
      color: 'rgba(22, 119, 255, 0.25)',
      borderColor: '#1677FF',
      borderSize: 1,
      borderRadius: 0,
      // 'solid' | 'dashed'
      borderStyle: 'solid',
      borderDashedValue: [2, 2]
    },
    polygon: {
      // 'fill' | 'stroke' | 'stroke_fill'
      style: 'fill',
      color: '#1677FF',
      borderColor: '#1677FF',
      borderSize: 1,
      // 'solid' | 'dashed'
      borderStyle: 'solid',
      borderDashedValue: [2, 2]
    },
    circle: {
      // 'fill' | 'stroke' | 'stroke_fill'
      style: 'fill',
      color: 'rgba(22, 119, 255, 0.25)',
      borderColor: '#1677FF',
      borderSize: 1,
      // 'solid' | 'dashed'
      borderStyle: 'solid',
      borderDashedValue: [2, 2]
    },
    arc: {
      // 'solid' | 'dashed'
      style: 'solid',
      color: '#1677FF',
      size: 1,
      dashedValue: [2, 2]
    },
    text: {
      // 'fill' | 'stroke' | 'stroke_fill'
      style: 'fill',
      color: '#FFFFFF',
      size: 12,
      family: 'Helvetica Neue',
      weight: 'normal',
      // 'solid' | 'dashed'
      borderStyle: 'solid',
      borderDashedValue: [2, 2],
      borderSize: 0,
      borderRadius: 2,
      borderColor: '#1677FF',
      paddingLeft: 0,
      paddingRight: 0,
      paddingTop: 0,
      paddingBottom: 0,
      backgroundColor: 'transparent'
    },
    rectText: {
      // 'fill' | 'stroke' | 'stroke_fill'
      style: 'fill',
      color: '#FFFFFF',
      size: 12,
      family: 'Helvetica Neue',
      weight: 'normal',
      // 'solid' | 'dashed'
      borderStyle: 'solid',
      borderDashedValue: [2, 2],
      borderSize: 1,
      borderRadius: 2,
      borderColor: '#1677FF',
      paddingLeft: 4,
      paddingRight: 4,
      paddingTop: 4,
      paddingBottom: 4,
      backgroundColor: '#1677FF'
    }
  }
}

onMounted(() => {
  chart.chart = init('chart')
  chart.chart.setStyles(options)
  chart.chart.createIndicator('VOL')

  lastStockList()
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
      <a class="btn-primary" href="javascript:void(0)" @click="fetchTodayRiseStock">今日</a>
      <a class="btn-primary" href="javascript:void(0)" @click="fetchFavoriteStock">关注</a>
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
      </div>
    </div>
  </div>

  <div class="grid grid-flow-col grid-cols-8 gap-2">
    <div class="col-start-1 col-end-1 p-1">
      <h3>今日[{{ (new Date()).getUTCDate()  }}]</h3>
      <div class="item-box">
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
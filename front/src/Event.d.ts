import axios from 'axios'

const BASE_URL = 'http://127.0.0.1:5000'

interface ResponseData {
    status: number;
    data: any; // 或者定义更具体的类型
    message: string;
}

// 异步函数，使用 async/await
export async function request(url: string): Promise<ResponseData> {
    try {
        // 使用 axios 获取数据
        const response = await axios.get<ResponseData>(BASE_URL + url);

        // 从响应中返回数据
        return response.data.data;
    } catch (error) {
        // 错误处理，可以根据需要抛出错误或者返回错误信息
        console.error('请求失败:', error);
        throw error; // 或者返回一个错误对象
    }
}

export function refresh(stock) {
    axios.get(BASE_URL + "/api/fetch/kline/"+ stock.symbol)
    .then(response => {
        loadStock(stock, null)
    })
    .catch(e => {
        this.errors.push(e)
    })
}

export function favorite(stock) {
    axios.get(BASE_URL + "/api/stock/favorite/"+ stock.symbol)
    .then(response => {
        console.log(response)
    })
    .catch(e => {
        this.errors.push(e)
    })
}

export function unFavorite(stock) {
    axios.get(BASE_URL + "/api/stock/unfavorite/"+ stock.symbol)
    .then(response => {
        console.log(response)
    })
    .catch(e => {
        this.errors.push(e)
    })
}

export function fetchTodayRiseStock() {
    axios.get(BASE_URL + "/api/stock/today/rise")
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

export function stockSearch() {
    axios.get(BASE_URL + "/api/stock/search/"+searchValue.value)
    .then(response => {
        console.log(response)
        const retStock = response.data.data
        
        stocks.value.push(retStock)
        curStock.value = retStock
        loadStock(retStock, null)
    })
    .catch(e => {
        this.errors.push(e)
    })
    .catch(e => {
        this.errors.push(e)
    })
}

export function downTodayRiseStock() {
    axios.get(BASE_URL + "/api/stock/today/down")
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

export function fetchFavoriteStock() {
    axios.get(BASE_URL + "/api/stock/favorite")
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

export async function getStockKlineData(stock) {
    const chartData = [];

    const data = await request("/api/kline/"+ stock.symbol)
    data.forEach(item => {
        chartData.push({
            timestamp: item[0],
            volume:    item[1],
            open:      item[2],
            high:      item[3],
            low:       item[4],
            close:     item[5]
        })
    })

    return chartData
}

export default {}
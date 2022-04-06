<!--В общем тут творится адовая смесь-->
<template>
  <div class="main-container">
    <div class="choose-container">
      <select class="select-ticker" v-model="ticker" v-on:change="getData">
        <option
            v-for="item in tickers"
            :key="item">
          {{item}}
        </option>
      </select>
    </div>
    <div class="chart-container">
      <div class="data-settings">
        <form class="form-sett">
          <div class="form-row">
            <div style="width: 100px">
              <label for="start-dt">Начало</label>
            </div>
            <input id="start-dt" type="datetime-local" v-model="startDt" @change="getData">
          </div>
          <div class="form-row">
            <div style="width: 100px">
              <label for="end-dt">Конец</label>
            </div>
            <input id="end-dt" type="datetime-local" v-model="endDt" @change="getData">
          </div>
          <div class="form-row">
            <div style="width: 100px">
              <label for="end-dt">Лимит мин</label>
            </div>
            <select class="class-row" style="width: 50px; height: 20px" v-model="limit" v-on:change="getData">
                <option
                    v-for="item in limits"
                    :key="item">
                  {{item}}
                </option>
              </select>
          </div>
        </form>
      </div>
      <div class="chart" v-if="ready">
        <Bar
          :chart-options="chartOptions"
          :chart-data="chartData"
          :chart-id="chartId"
          :dataset-id-key="datasetIdKey"
          :plugins="plugins"
          :css-classes="cssClasses"
          :styles="styles"
          :width="width"
          :height="height"
        />
      </div>
    </div>
    <div class="history-container">
      <div class="rows">
        <table style="margin: 0 auto; width: 100%">
          <tbody>
            <tr class="row">
              <td>Date</td>
              <td>Trend</td>
              <td>Price</td>
            </tr>
            <tr v-for="item in datas"
             :key="item.changed_dt"
             v-bind:class="[item.price_trend===-1 ? 'minus' : 'plus']"
             class="row">
              <td style="min-width: 70%">{{item.changed_dt.replace('T', ' ')}}</td>
              <td>{{item.price_trend}}</td>
              <td>{{item.price}}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
// импортируем библиотеку vue-charts которая в свою очередь обертка над charts js
// потому что я не хочу писать логику отрисовки графиков самостоятельно
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
const axios = require('axios')

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
// тут константы
const chartColors = {
        red: "#ff0000",
        green: "#39ff00"
      }
const HOST = `${location.host}`
// const HOST = '192.168.0.105'

export default {
  name: 'HomeComponent',
  components: { Bar },
  // пропсы для графика, настройки, ширина высота
  props: {
    chartId: {
      type: String,
      default: 'bar-chart'
    },
    datasetIdKey: {
      type: String,
      default: 'label'
    },
    width: {
      type: Number,
      default: window.innerWidth*0.76
    },
    height: {
      type: Number,
      default: window.innerHeight*0.77
    },
    cssClasses: {
      default: '',
      type: String
    },
    styles: {
      type: Object,
      default: () => {

      }
    },
    plugins: {
      type: Object,
      default: () => {
      }
    }
  },
  data: function(){
    return {
      ready: false, // заглушка для отрисовки графика думал еше спиннер добавить, но руки не дошли
      tickers: [],  // список тикеров
      ticker: "", // активный тикер
      startDt: new Date().toISOString().split('.')[0], // начальная датавремя
      endDt: null,
      limits: [1,2,3,4,5,6,7,8,9,10], // выборы для лимитов в минутах
      limit: 1, // активный лимит
      connection: null, // коннкектион вебсокета
      datas: [], // данные для отрисовки истории
      inf: { // данные для отрисовки графика
        labels: [],
        datasets: [
          {
            label: '213',
            data: [],
            backgroundColor: []
          },
        ]
      },
      chartOptions: { // настройки для отрисовки графика
        scales: {
          y: {
            grid:{
              display: true
            },
            beginAtZero: false
          },
          x: {
            grid:{
              display: false
            },
          }
        },
        responsive: true
      }
    }
  },
  methods: {
    async initData () {

      // функция которая нам грузит тикеры
      let products = []
      await axios.get(`http://${HOST}/api/prices/tickers`).then(async function (response) {
          // console.log(await response.data)
          products = await response.data.products
          // this.tickers = await response.data.products
        }
      )
      for (let i = 0; i<products.length; i++){
        this.tickers.push(products[i])
      }
    },

    async getData () {
      // основная функция которая грузит данные, на каждое событие (выбор тикера, лимита, даты)

      // если у нас есть коннект то чистим его
      if (this.connection !== null ){
        console.log(this.connection)
        this.connection.send('close')
        this.connection.close()
        this.connection = null
      }

      // создание и указание локальных переменных под датам
      let startDt = ''
      let endDt = ''
      if (this.startDt !== null && this.startDt !== '') {
        startDt = this.startDt
      } else {
        let _ = new Date()
        _.setMinutes(_.getMinutes()-this.limit)
        startDt = `${_.getFullYear()}-${_.getUTCMonth()+1}-${_.getUTCDate()} ${_.getUTCHours()}:${_.getMinutes()}:${_.getSeconds()}`
        endDt = new Date().toISOString().split('.')[0].replace('T', ' ')
      }

      if (this.endDt !== null && this.endDt !== '') {
        endDt = this.endDt
      } else {
        let _ = new Date()
        _.setMinutes(_.getMinutes()-this.limit)
        startDt = `${_.getFullYear()}-${_.getUTCMonth()+1}-${_.getUTCDate()} ${_.getUTCHours()}:${_.getMinutes()}:${_.getSeconds()}`
        endDt = new Date().toISOString().split('.')[0].replace('T', ' ')
      }
      console.log(startDt, endDt)
      // указание лимитов строк для выгрузки
      let limit = this.limit * 60

      // чистим наши структуры для отрисовок истории и графиков
      this.datas = []
      this.inf = {
        labels: [],
        datasets: [
          {
            label: '',
            data: [],
            backgroundColor: []
          },
        ]
      }

      // устанавливаем ссылки
      let datas = this.datas
      let info = this.inf

      // собираем ендпоинт
      const endpoint = `http://${HOST}/api/prices/${this.ticker}?limit=${limit}&start_dt=${startDt}&end_dt=${endDt}`
      console.log(endpoint)
      // запрос на загрузку истории и заполнение структур
      await axios.get(endpoint).then(async function (response) {
          // datas = await response.data
          let _ = await response.data
          for (let i = 0; i < _.length; i++){
            datas.push(_[i])
            info.datasets[0].data.unshift([_[i].old_price, _[i].price])
            info.labels.unshift(_[i].changed_dt)
            info.datasets[0].backgroundColor.unshift(_[i].price_trend===-1 ? chartColors.red : chartColors.green)
          }
        }
      )

      this.ready = true
      // если у нас конечная дата не указана, мы считаем что хотим получать данные в реальном времени
      if (this.endDt === null || this.endDt === ''){
        // устанавливаем сокет
        this.connection = new WebSocket(`ws://${HOST}/api/ws/prices/${this.ticker}/`)
        // вешаем евенты
        this.connection.onmessage = function(event) {
          let i = JSON.parse(event.data)
          // каждое полученное сообщение добавляем в структуры для отрисовок
          info.labels.push(i.changed_dt)
          info.datasets[0].data.push([i.old_price, i.price])
          info.datasets[0].backgroundColor.push(i.price_trend===-1 ? chartColors.red : chartColors.green)
          datas.unshift(i)
          // если данные превышают лимит, чистим последние данные
          if (datas.length > limit){
            info.labels.shift()
            info.datasets[0].data.shift()
            info.datasets[0].backgroundColor.shift()
            datas.pop()
          }
        }
        this.connection.onopen = function(event){
          console.log(event)
          console.log("Success connected")
        }
      }
    }
  },
  computed: {
    chartData() {
      return this.inf
    }
  },
  beforeCreate: async function () {
    const _ = new Date()
    this.startDt = `${_.getFullYear()}-${_.getMonth()}-${_.getDate()}T${_.getHours()}:${_.getMinutes()}`
    console.log(_.toISOString().split('.')[0])
    },
  mounted: async function() {
  },
  updated: function() {

  },
  created: async function () {
    await this.initData()
    this.ticker = this.tickers[0]
    await this.getData()
    // let info = this.inf
    // let datas = this.datas
    console.log("Mounted component")
    console.log("Next work")
    },
  unmounted() {
    if (this.connection !== null ){
        this.connection.send('close')
        this.connection.close()
        this.connection = null
      }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .main-container{
    display: flex;
    /*width: 1000px;*/
    margin: 0;
  }

  .choose-container{
    display: flex;
    min-width: 150px;
    width: 3vw;
  }
  .select-ticker {
    width: 100%;
    height: 3vh;
    font-size: 16px;
    overflow: auto;
  }
  .chart-container {
    display: flex;
    flex-direction: column;
    width: 79vw;
  }
  .data-settings{
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    min-height: 100px;
    min-width: 100%;
  }
  .form-sett{
    display: flex;
    justify-items: flex-start;
    width: 100%;
    flex-wrap: wrap;
  }
  .form-row{
    margin-bottom: 5px;
    display: flex;
    width: 100%;
  }
  .chart{
    display: flex;
  }


  .history-container{
    display: flex;
    width: 14vw;
  }

  .rows{
    min-width: 100%;
    max-height: 84vh;
    overflow: auto;
  }
  .row{
    margin: 0 auto;
    min-width: 100%;
  }

  .minus {
    background-color: #ff7777;
  }
  .minus:hover{
    transition: 0.2s;
    background-color: #ff5151;
    cursor: pointer;
  }

  .plus {
    background-color: #97ff79;
  }
  .plus:hover{
    transition: 0.2s;
    background-color: #7cff56;
    cursor: pointer;
  }
</style>

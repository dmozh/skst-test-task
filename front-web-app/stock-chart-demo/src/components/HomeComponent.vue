<template>
  <div class="hello">
    <p>dqwdwww</p>
  </div>
</template>

<script>

export default {
  name: 'HomeComponent',
  props: {
    msg: String
  },
  deta: function(){
    return{
      connection: null
    }
  },
  methods: {
    sendMessage: function (message){
      console.log("send message", message)
      this.connection.send(message)
    }
  },
  created: function (){
      console.log("Mounted component")

      this.connection = new WebSocket(`ws://${location.host}/api/prices/ticker_00/ws`)
      this.connection.onmessage = function(event) {
        console.log(event)
      }
      this.connection.onopen = function(event){
        console.log(event)
        console.log("Success connected")
      }
    },
  unmounted() {
    this.connection.send('close')
    this.connection.close()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>

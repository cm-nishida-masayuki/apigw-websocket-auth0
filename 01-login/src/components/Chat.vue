<template>
  <div>
    <button v-if="!isConnected" @click="connect">接続</button>
    <div v-if="isConnected">
      <ul style="list-style: none" v-for="message in messages">
        <li>{{message}}</li>
      </ul>
      <input placeholder="Enter your message" style="width: 100%" v-model="inputMessage"/>
      <button @click="sendMessage">送信</button>
    </div>
  </div>
</template>

<script>
  export default {
    name: "Chat",
    data() {
      return {
        "inputMessage": "",
        "ws": null,
        "messages": [],
      }
    },
    computed: {
      isConnected() {
        return this.ws !== null
      }
    },
    methods: {
      async connect() {
        const token = await this.$auth.getTokenSilently()
        const ws = new WebSocket(`YOURWSSENDPOINT?token=${token}`)

        ws.onopen = () => {
          this.ws = ws
        }

        ws.onmessage = message => {
          const data = JSON.parse(message.data)
          this.messages.push(data.message)
        }
      },
      async sendMessage() {
        const data = {
          "action": "sendMessage",
          "data": {
            "message": this.inputMessage
          }
        }

        this.ws.send(JSON.stringify(data))

        this.inputMessage = ""
      }
    }
  }
</script>

<style scoped>

</style>

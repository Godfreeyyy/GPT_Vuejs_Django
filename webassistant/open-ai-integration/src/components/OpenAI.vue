<script setup>

import {ref, onMounted} from 'vue'
import axios from 'axios'

let messages = ref([])
let newMessage = ref('')
let isLoading = ref(true)

let isFirstRender = ref(true)

const fetchMessages = async () => {

}

const sendMessage = () => {
  try {

    const requestOptions = {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        "message": newMessage.value,
        "userId": 1
      })
    };

    fetch("http://127.0.0.1:8000/open-ai/message", requestOptions)
        .then(response => {
          return response.json()
        }).then(data => {
      var js = {
        "message": "Hello! How can I assist you today?",
        "users": {
          "id": 1,
          "avatar": "https://media.licdn.com/dms/image/D4E03AQHDH6P5jC9gJA/profile-displayphoto-shrink_800_800/0/1688393266395?e=2147483647&v=beta&t=pc_yPaWFZXKS3OrMdy1ZkK-WQZiT0MZf_vmdf-14czQ",
          "name": "Nguyen Huy"
        }
      }

      console.log(data)

      messages.value.push(
          {
            message: data.message,
            users: {
              id: data.users.id,
              avatar: data.users.avatar,
              name: data.users.name,
            }
          }
      )
    })
    console.log(messages)
  } catch (err) {
    console.error(err)
  }
  // Add logic to send a message to your server
}

onMounted(fetchMessages)

defineProps({
  msg: {
    type: {
      users: {
        type: {
          name: {
            type: String
          },
          avatar: {
            type: String
          }
        }
      },
      message: {
        type: String
      }
    },
    required: true
  }
})
</script>

<template>
  <div class="chat-container">

    <div v-for="msg in messages" :key="msg.users.id" class="message">
      <img :src="msg.users.avatar" :alt="msg.users.name"/>
      <div class="message-info">
        <h3>{{ msg.users.name }}</h3>
        <p>{{ msg.message }}</p>
      </div>
    </div>

    <div class="message-input">
      <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="Type your message here..."/>
      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>


<style scoped>
.message {
  display: flex;
  align-items: center;
}

.message img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 15px;
}

.chat-container {
  animation: slide-up 0.5s ease;
}

@keyframes slide-up {
  0% {
    transform: translateY(100%);
  }
  100% {
    transform: translateY(0);
  }
}
</style>
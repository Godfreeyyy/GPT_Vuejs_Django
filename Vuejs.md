
#Backend Design

## Library:

### Fake database (using json file):
Use `pydantic` for parsing json to python class structure:

consider `user_db.json`
```json
{
  "user": [
    {
      "id": 1,
      "avatar": "https://media.licdn.com/dms/image/D4E03AQHDH6P5jC9gJA/profile-displayphoto-shrink_800_800/0/1688393266395?e=2147483647&v=beta&t=pc_yPaWFZXKS3OrMdy1ZkK-WQZiT0MZf_vmdf-14czQ",
      "name": "Nguyen Huy"
    }
  ]
}
```

model type in python code:

```
class User(BaseModel):
    id: Optional[int]
    avatar: Optional[str]
    name: Optional[str]

    def getName(self):
        return self.Name

    def getAvatar(self):
        return self.Avatar

    def getID(self):
        return self.Id


class ClassLoader(BaseModel):
    user: List[User]

```

Use pydantic to transform json to `ClassLoader`

```
     master_data: ClassLoader = parse_file_as(path=helper.data_file, type_=ClassLoader)
```

where helper.data_file:

```
data_file = os.path.join(root_folder, "user_db.json")
```

### API Frame work:
Using fastapi:
FastAPI is a modern and fast web framework for building APIs with Python. It is designed to be easy to use, highly performant, 
and to take advantage of Python type hints for automatic data validation and documentation.

#### Setup:

```
def init_app() -> FastAPI:
    _app = FastAPI(title="CMS API", version="0.2.0")

    _app.add_middleware(
        CORSMiddleware,
        allow_origins="*",  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    _app.include_router(open_ai_router.OpenAIRouter().add_routesDr().router, prefix="/open-ai", tags=["project"])

    return _app


app = init_app()

```



- CORSMiddleware:
    Set `*` to allow cross origin -> make browser (vuejs client) be able to call api from backend server
- `_app.include_router(open_ai_router.OpenAIRouter().add_routesDr().router, prefix="/open-ai", tags=["project"])`
    For setup Router with prefix:  `open-ai`, this router including 1 api is `http://127.0.0.1:8000/open-ai/message`[method POST]
    Which request body(input) is the message of user send to open ai and response is the answer of the ai bot, including message and user information
- ` uvicorn.run(app, host="0.0.0.0", port=8000)`
    To start server with port 8000, front end will fetch data from api `http://127.0.0.1:8000/open-ai/message` to get the answer from chat bot
#### API Detail:

```
class OpenAIRouter:
    def __init__(self):
        self.router = APIRouter()
        self.db: FakeDB = FakeDB()

    def add_routesDr(self):

        @self.router.post("/message", response_model=AIResponse)
        async def getMessage(request: UserRequest):
            try:
                user = self.db.getUserRepo().getUserById(1)

                message = [{"role": "user", "content": request.message}]
                print(message)
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=message,
                    temperature=0.1,
                    max_tokens=1000,
                )
                # format the response
                formatted_response = response['choices'][0]['message']['content']

                response2: AIResponse = AIResponse()

                response2.users = user
                response2.message = formatted_response


                return response2
            except ValueError as e:
                print(f"An error occurred: {e}")
                return e

        return self
```

#Front end(VueJs):

## Setup step:

1. Install Node Js and following the [doc](https://vuejs.org/guide/quick-start.html)  from VueJs install project: 
    - ` npm init vue@latest`
    - After instalation, we have base structure of vueJS source code:
    

```shell
  ├── frontend/            # Frontend (Vue.js)
  │   ├── public/          # Public assets (index.html, images, etc.)
  │   ├── src/             # Vue.js source code
  │   │   ├── assets/      # Images, styles, etc.
  │   │   ├── components/  # Reusable Vue components
  │   │   ├── views/       # Vue components for different views/pages
  │   │   ├── services/    # Services to interact with backend APIs
  │   │   ├── router/      # Vue Router configuration
  │   │   └── main.js      # Main Vue.js application entry point
  │   └── ...              # Other frontend-related files
  │
```


2. Add Component named: `OpenAI.vue`

```js
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
          },
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
<div id="root"></div>
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
```


### Explaination:

Imports and reactive references:

```js
import {ref, onMounted} from 'vue'
import axios from 'axios'

let messages = ref([])
let newMessage = ref('')
let isLoading = ref(true)

let isFirstRender = ref(true)
```
It imports ref and onMounted from Vue and axios for making HTTP requests. 
It then sets up a few reactive references:

- messages is an array that will store the chat messages.
- newMessage is a string that will store the content of a new message being written by the user.
- isLoading is a boolean indicating whether the messages are currently being loaded.
- isFirstRender is a boolean to check if the component is initially rendered.

*Function*:

The sendMessage function is called when a user sends a new message. 
It makes a POST request to a specified URL, sending a JSON payload containing the new message and the user ID.
The response from the server is then added to the messages array (chat bot response).


The Vue template section creates a chat component. It iterates over the messages array using a `v-for` to display each message along with the sender's avatar and name. 
There's also an input field bound to newMessage
and a button that triggers sendMessage when clicked or when the Enter key is pressed in the input field.
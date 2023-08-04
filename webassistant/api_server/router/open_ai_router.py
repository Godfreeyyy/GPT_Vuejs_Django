from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from ..router import AIResponse, UserRequest, FakeDB
from fastapi import APIRouter, Depends, Query
import openai
API_KEY = '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'
# loading the API key from the secret_key file
openai.api_key = API_KEY


class OpenAIRouter:
    def __init__(self):
        self.router = APIRouter()
        self.db: FakeDB = FakeDB()

    def add_routesDr(self):

        @self.router.post("/message", response_model=AIResponse)
        async def getMessage(request: UserRequest):
            try:
                user = self.db.getUserRepo().getRootUser()

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

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel
import uvicorn
import asyncio
from utils.ai_utils import ollama_inference
import database

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    user_message = request.message
    
    # Save user message to DB
    database.save_message('user', user_message)
    
    # Get current history
    history = database.get_history()
    
    async def event_generator():
        # Call inference generator
        # Note: ollama_inference is synchronous generator, but we can iterate it.
        # Ideally, use async ollama client if available, but for now blocking code in thread or simple iteration is ok for local singleton usage.
        # To avoid blocking event loop, we should ideally use run_in_executor or async client.
        # But ollama python lib current version behaves synchronously or async? 
        # Most simple way for now with standard ollama lib:
        
        for chunk in ollama_inference(user_message, history=history):
            if chunk:
                yield {"data": chunk}
                await asyncio.sleep(0) # Yield control
        
        # End of stream
        yield {"data": "[DONE]"}

    return EventSourceResponse(event_generator())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

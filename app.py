from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from main import CollaborativeLearningSystem
import os

app = FastAPI()

# Initialize the system
system = CollaborativeLearningSystem()

class ChatRequest(BaseModel):
    message: str

@app.on_event("startup")
async def startup_event():
    print("Initializing Collaborative Learning System...")
    system.initialize()

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        if not request.message:
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        response = system.process_question(request.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse('static/index.html')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

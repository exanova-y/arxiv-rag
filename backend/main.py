from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from .chat import router as chat_router

app = FastAPI()
app.include_router(chat_router, prefix="/api")

origins = ["http://localhost", "http://localhost:5173", "http://127.0.0.1:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify allowed origins here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# http://127.0.0.1:8000/
@app.get("/")
def root():
    return {"status": "FastAPI server is running", "endpoints": ["/api/chat/"]}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.0", port=8000, reload=True)

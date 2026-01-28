from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from agent import agent_app

app = FastAPI()

# Serve UI
app.mount("/static", StaticFiles(directory="static"), name="static")

class Prompt(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("static/index.html") as f:
        return f.read()

@app.post("/chat")
def chat(prompt: Prompt):
    result = agent_app.invoke({
        "user_input": prompt.message
    })
    return {"answer": result["response"]}

from fastapi import FastAPI 

app = FastAPI()

@app.get("/")
def getMain():
    return "welcome to the main page"
from fastapi import FastAPI

app=FastAPI()
@app.get("/welcome")
def welecome():
    return{
        "message":"Hello world"
    }
    

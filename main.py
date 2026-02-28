from fastapi import FastAPI

app = FastAPI()

@app.get("/mul10/{num}")
def multiply_by_10(num: int):
    return {"result": num * 10}

@app.get("/getcode")
def get_code():
    return {"code": "Hello, TEST!"}
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from Lambda!"}

# This is the AWS Lambda handler
handler = Mangum(app)
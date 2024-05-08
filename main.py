from fastapi import FastAPI
from pydantic import BaseModel

# Create the FastAPI app
app = FastAPI()


class Example(BaseModel):
    name: str


@app.get("/", response_model=list[Example])
async def get_examples():
    return [Example(name="example")]

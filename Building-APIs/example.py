# Importing Dependencies
from fastapi import FastAPI
from pydantic import BaseModel

# Creating the app
app = FastAPI()

# Creating a simple model
class InputItem(BaseModel):
    name: str
    price: float
    discount: int

class OutputItem(BaseModel):
    name: str
    sellingPrice: float

# Creating a simple GET endpoint
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Creating a simple POST endpoint
@app.post("/items/", response_model=OutputItem)
def create_item(item: InputItem):
    sellingPrice = item.price - (item.price * item.discount / 100)
    return {"name": item.name, "sellingPrice": sellingPrice}



# To try it out, run the following command in the terminal:
# uvicorn main:app --reload         
# reload is for development purposes, it reloads the server on code changes

# To test the endpoint, open your browser and go to: http://link-to-your-api/
# For swagger UI: http://link-to-your-api/docs
# For redoc: http://link-to-your-api/redoc
# For openapi.json: http://link-to-your-api/openapi.json

# To test using Gunicorn, run the following command in the terminal:
# gunicorn service.main:app --workers 3 --worker-class uvicorn.workers.UvicornWorker
# It helps in scaling the application with multiple workers and threads for handling multiple requests simultaneously
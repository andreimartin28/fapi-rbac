from fastapi import FastAPI
from controllers.users import users
from controllers.auth import authentication
from controllers.products import products
from configs import db

# you can include inside things like :#$
# docs_url="/documentation", redoc_url=None
app = FastAPI()

app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(products.router)

db = db


@app.get("/")
def message_hello():
    return {
        "message": "hello"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)

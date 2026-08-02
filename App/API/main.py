from routes import health, sql_health
from fastapi import FastAPI

app = FastAPI(
    title="URL Shortener API",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Welcome to the URL Shortener API!"}

app.include_router(health.router)
app.include_router(sql_health.router)
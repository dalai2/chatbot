from fastapi import FastAPI
from routes import router

app = FastAPI()

# Include API routes
app.include_router(router)

# Root route
@app.get("/")
async def root():
    return {"message": "Chat API is tired!"}

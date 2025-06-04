from fastapi import FastAPI
from routers import search_router

app = FastAPI(
    title="Search Engine App",
    description="A basic search engine app",
    version="1.0.0"
)

app.include_router(search_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

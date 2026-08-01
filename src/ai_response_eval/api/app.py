from fastapi import FastAPI

from ai_response_eval.api.routes import router

app = FastAPI(
    title="AI Response Evaluation Framework",
    version="1.0.0",
)

app.include_router(router)

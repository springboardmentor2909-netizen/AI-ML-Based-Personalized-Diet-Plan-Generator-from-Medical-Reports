from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.routes.diet import router as diet_router
from app.routes.predict import router as predict_router

app = FastAPI(title="AI Diet Plan Generator")

app.include_router(upload_router)
app.include_router(diet_router)
app.include_router(predict_router)

@app.get("/")
def home():
    return {"message": "Backend is running successfully"}

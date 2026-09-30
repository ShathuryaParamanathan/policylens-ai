from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

from .database import db, check_database_connection
from .models.website import create_website_document


app = FastAPI(
    title="PolicyLens AI",
    description="AI-powered website policy and privacy analysis",
    version="0.1.0"
)


class WebsiteRequest(BaseModel):
    url: HttpUrl


@app.get("/")
def root():
    return {
        "message": "PolicyLens AI API is running"
    }


@app.get("/health")
def health():
    database_status = check_database_connection()

    return {
        "status": "healthy",
        "database": "connected" if database_status else "disconnected"
    }


@app.post("/websites")
def create_website(request: WebsiteRequest):

    url = str(request.url)

    domain = request.url.host

    website = create_website_document(
        url=url,
        domain=domain
    )

    result = db.websites.insert_one(website)

    return {
        "message": "Website created successfully",
        "website_id": str(result.inserted_id)
    }
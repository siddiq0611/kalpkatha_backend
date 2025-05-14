# """
# FastAPI application for the story generation service.
# """
# import os
# from fastapi import FastAPI, HTTPException, Depends
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel, Field
# from typing import Optional, Dict, Any

# from story_writer import StoryGenerator
# from config import get_settings, Settings
# from openai import OpenAI
# from contextlib import asynccontextmanager


# class StoryRequest(BaseModel):
#     prompt: str = Field(..., description="The story prompt from the user")


# class StoryResponse(BaseModel):
#     story: str = Field(..., description="The generated story")


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     settings = get_settings()
#     app.state.settings = settings
#     try:
#         app.state.openai_client = OpenAI(api_key=settings.openai_api_key)
#     except TypeError as e:
#         if "proxies" in str(e):
#             app.state.openai_client = OpenAI(
#                 api_key=settings.openai_api_key,
#             )
#         else:
#             raise
            
#     app.state.story_generator = StoryGenerator(app.state.openai_client)
    
#     yield

#     app.state.openai_client = None
#     app.state.story_generator = None


# # Initialize FastAPI app
# app = FastAPI(
#     title="Story Generator API",
#     description="An API for generating creative stories using AI",
#     version="1.0.0",
#     lifespan=lifespan
# )

# # Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Lock this down in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # Dependency for settings
# def get_app_settings():
#     return get_settings()


# @app.get("/health")
# async def health_check():
#     """Health check endpoint."""
#     return {"status": "healthy"}


# @app.post("/api/generate-story", response_model=StoryResponse)
# async def generate_story(request: StoryRequest):
#     try:
#         result = app.state.story_generator.generate_story(
#             user_prompt=request.prompt,
#         )
#         return result
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Story generation failed: {str(e)}")


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)











# ── backend/app.py ──
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from contextlib import asynccontextmanager
from openai import OpenAI, OpenAIError
import uuid

from config import get_settings
from story_writer import StoryGenerator

# Pydantic models
class StoryRequest(BaseModel):
    prompt: str = Field(..., description="The story prompt from the user")
    chapters: Optional[int] = Field(None, description="Number of chapters to generate; unlimited if omitted")
    chapter_length: Optional[int] = Field(None, description="Approximate length per chapter in words; unlimited if omitted")

class ContinueRequest(BaseModel):
    session_id: str = Field(..., description="ID of the story session to continue")
    next_chapters: Optional[int] = Field(1, description="How many more chapters to generate")
    chapter_length: Optional[int] = Field(None, description="Approximate length per chapter in words; leave blank to reuse original")

class StoryResponse(BaseModel):
    session_id: str
    chapters: List[str]

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.state.openai = OpenAI(api_key=settings.openai_api_key)
    app.state.generator = StoryGenerator(
        client=app.state.openai,
        model=settings.model_name,
        temperature=settings.default_temperature
    )
    yield

app = FastAPI(title="Enhanced Story Generator", version="2.2.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/generate-story", response_model=StoryResponse)
async def generate_story(request: StoryRequest):
    try:
        session_id, chapters = app.state.generator.start_story(
            prompt=request.prompt,
            num_chapters=request.chapters,
            chapter_length=request.chapter_length
        )
        return StoryResponse(session_id=session_id, chapters=chapters)
    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

@app.post("/api/continue-story", response_model=StoryResponse)
async def continue_story(request: ContinueRequest):
    try:
        chapters = app.state.generator.continue_story(
            session_id=request.session_id,
            next_chapters=request.next_chapters,
            chapter_length=request.chapter_length
        )
        return StoryResponse(session_id=request.session_id, chapters=chapters)
    except KeyError:
        raise HTTPException(status_code=404, detail="Session not found")
    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
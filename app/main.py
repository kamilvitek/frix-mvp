# FastAPI app instance & route includes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import meetup
from .routes import oauth, events

app = FastAPI(title="Frix MVP")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(meetup.router, tags=["auth"])
app.include_router(oauth.router)
app.include_router(events.router, prefix="/api", tags=["events"])

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}
"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import customers, products, revenue, sales
from app.db.database import Base, engine

# Create all tables on startup (SQLite file-based DB)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-Commerce Sales Intelligence API",
    description=(
        "Backend API powering Looker Studio dashboards for real-time "
        "e-commerce sales analytics."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sales.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(customers.router, prefix="/api/v1")
app.include_router(revenue.router, prefix="/api/v1")


@app.get("/", tags=["Health"])
def health_check() -> dict:
    """Basic health check endpoint."""
    return {"status": "ok", "service": "ecommerce_intelligence"}

"""
Vercel entrypoint for the FastAPI app.

Vercel's Python runtime looks for an `app` object in files like
`index.py`, `app.py`, or `server.py`. We simply re-export the
existing FastAPI application defined in `app/main.py`.
"""

from app.main import app


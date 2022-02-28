import uvicorn
from server.metadata import app

uvicorn.run(
    app,
    host="0.0.0.0",
    port=8000,
    debug=True,
)

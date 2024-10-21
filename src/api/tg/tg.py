from fastapi.responses import ORJSONResponse
from starlette.responses import JSONResponse

from src.api.tg.router import router

@router.get("/home")
async def home_post() -> JSONResponse:
    return ORJSONResponse({"message": "Hello"})
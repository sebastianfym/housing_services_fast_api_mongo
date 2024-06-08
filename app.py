from fastapi import FastAPI, HTTPException, BackgroundTasks, APIRouter
import uvicorn

from api.router import router
import api.houses
import api.apartments
import api.tariffs

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})


v1 = APIRouter(prefix="/api/v1")
v1.include_router(router)


app.include_router(v1)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
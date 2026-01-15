from fastapi import FastAPI,Request
from routers.user import router as userRouter
from routers.lesting import router as lestingRouter
from routers.category import router as categoryRouter
from routers.auth import router as authRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

apiKey="123456789apikeysecure"

app.add_middleware(CORSMiddleware, 
                   allow_origins=["http://localhost:5174","http://localhost:5173"],
                   allow_credentials = True, 
                   allow_methods = ["*"],
                   allow_headers=["*"]
                   )

@app.middleware("http")
async def middleware_apikey(request : Request, call_next):
    if request.method == "OPTIONS":
        return await call_next(request)
    if request.headers.get("apiKey") != apiKey:
       return JSONResponse(status_code=401, content="Invalid request, unauthorised")
    response = await call_next(request)
    return response

@app.get("/")
def getMain():
    return "welcome to the main page"

app.include_router(userRouter, prefix="/api/user", tags=["user"])
app.include_router(lestingRouter, prefix="/api/listing", tags=["listing"])
app.include_router(categoryRouter,prefix="/api/category", tags=["category"])
app.include_router(authRouter,prefix="/api/auth", tags=["auth"])


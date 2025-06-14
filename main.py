from fastapi import FastAPI, File, UploadFile, Form,  HTTPException
from fastapi.responses import PlainTextResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from services.client import generate_code_comments_and_docs

# ✅ Initialize FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load static data
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    return FileResponse("static/index.html")

# ✅ API route
@app.post("/generate-docs")
async def generate_docs(
    file: Optional[UploadFile] = File(None),
    code: Optional[str] = Form(None)
    ):
    try:
        if not file and not code:
            raise HTTPException(status_code=400, detail="You must provide either a file or raw code.")
        
        elif file and code:
            raise HTTPException(status_code=400, detail="Please provide only one of 'file' or 'code', not both.")

        elif code:
            response = generate_code_comments_and_docs(code)
            return response
        
        elif file:
            content = await file.read()
            code = content.decode("utf-8")
            response = generate_code_comments_and_docs(code)
            return response
        
        else:
            raise Exception("Invalid data")

    except Exception as ex:
        return PlainTextResponse(f"❌ Server error: {str(ex)}", status_code=500)

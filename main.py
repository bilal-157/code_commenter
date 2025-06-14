from fastapi import FastAPI, File, UploadFile
from services.client import generate_code_comments_and_docs

# ✅ Initialize FastAPI app
app = FastAPI()

@app.get("/")
def welcome():
    return {"messsage": "Welcome to server"}

# ✅ API route
@app.post("/generate-docs")
async def generate_docs(file: UploadFile = File(...)):
    try:
        content = await file.read()
        code = content.decode("utf-8")
        response = generate_code_comments_and_docs(code)
        return response

    except Exception as ex:
        return PlainTextResponse(f"❌ Server error: {str(ex)}", status_code=500)

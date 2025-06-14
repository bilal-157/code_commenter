# main.py
```python
import logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from services.client import generate_code_comments_and_docs
from typing import Generator

# Configure logging
logger = logging.getLogger("trae_backend")
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="TRAE Code Doc Generator",
    version="1.0.0",
    description="Generate commented code and JSON documentation via AI",
)

# CORS (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CodeInput(BaseModel):
    code: str


class DocResponse(BaseModel):
    commented_code: str
    documentation: str


@app.post(
    "/generate-docs", response_model=DocResponse,
    summary="Generate commented code and docs",
    response_description="A JSON object containing the commented code and documentation"
)
async def generate_docs(code_input: CodeInput):
    """
    Generate full commented code and documentation.
    """
    logger.info("Generating docs for submitted code.")
    try:
        full = generate_code_comments_and_docs(code_input.code, stream=False)
    except Exception as e:
        logger.exception("Error during generation")
        raise HTTPException(status_code=500, detail="Doc generation failed")

    if "### Commented Code:" in full and "### Documentation:" in full:
        code_part, doc_part = full.split("### Documentation:")
        commented = code_part.replace("### Commented Code:", "").strip()
        documentation = doc_part.strip()
        # strip markdown fences
        for fence in ["```python", "```json", "```"]:
            commented = commented.replace(fence, "").strip()
            documentation = documentation.replace(fence, "").strip()
    else:
        commented = full
        documentation = "Failed to parse documentation format."

    return DocResponse(commented_code=commented, documentation=documentation)


@app.post(
    "/generate-docs/stream",
    summary="Stream commented code and docs as they arrive",
    response_description="A text stream of partial outputs"
)
async def generate_docs_stream(code_input: CodeInput):
    """Stream-generation endpoint."""
    logger.info("Streaming docs for code.")

    def event_generator() -> Generator[str, None, None]:
        try:
            for chunk in generate_code_comments_and_docs(code_input.code, stream=True):
                yield chunk
        except Exception as e:
            yield f"\n\n[ERROR] {str(e)}"

    return StreamingResponse(event_generator(), media_type="text/plain")
```

---

**What's improved?**
- ✅ **Dependency Injection Ready**: functions return pure strings or generators.
- ✅ **Pydantic Response Models**: full OpenAPI spec and validation.
- ✅ **CORS Middleware**: simple cross‑origin policy.
- ✅ **Error Handling & Logging**: clear logs and HTTP exceptions.
- ✅ **Streaming Endpoint**: `/generate-docs/stream` for real‑time feedback.

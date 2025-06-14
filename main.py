from fastapi import FastAPI
from pydantic import BaseModel
from services.client import generate_code_comments_and_docs

# ✅ Initialize FastAPI app
app = FastAPI()

# ✅ Input model
class CodeInput(BaseModel):
    code: str

# ✅ API route
@app.post("/generate-docs")
async def generate_docs(code_input: CodeInput):
    chunks = generate_code_comments_and_docs(code_input.code, stream=True)
    full_result = ''.join([chunk for chunk in chunks if chunk])
    
    # Split the result
    commented_code = ""
    documentation = ""

    if "### Commented Code:" in full_result and "### Documentation:" in full_result:
        parts = full_result.split("### Documentation:")
        commented_code = parts[0].replace("### Commented Code:", "").strip()
        documentation = parts[1].strip()

        # ✅ Remove markdown code block formatting
        for tag in ["```python", "```json", "```"]:
            commented_code = commented_code.replace(tag, "").strip()
            documentation = documentation.replace(tag, "").strip()
    else:
        commented_code = full_result
        documentation = "Could not parse documentation."

    return {
        "commented_code": commented_code,
        "documentation": documentation
    }

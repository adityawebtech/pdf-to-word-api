from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import fitz  # PyMuPDF
from docx import Document

app = FastAPI()

# Allow frontend access (update this to your frontend domain for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/convert-pdf")
async def convert_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    pdf_path = f"converted/{uuid.uuid4()}.pdf"
    word_path = pdf_path.replace(".pdf", ".docx")

    # Save uploaded PDF
    with open(pdf_path, "wb") as f:
        f.write(contents)

    # Extract text and convert to Word
    doc = Document()
    pdf = fitz.open(pdf_path)
    for page in pdf:
        doc.add_paragraph(page.get_text())
    doc.save(word_path)
    pdf.close()

    return FileResponse(word_path, filename=os.path.basename(word_path), media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

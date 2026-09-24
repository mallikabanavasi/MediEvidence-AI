from pathlib import Path

from fastapi import APIRouter, UploadFile, File

from backend.services.ocr_service import extract_text_from_pdf_with_ocr
from backend.services.medical_extractor import extract_medical_information


router = APIRouter()

REPORTS_FOLDER = Path("data/reports")
REPORTS_FOLDER.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_report(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        return {
            "filename": file.filename,
            "message": "Only PDF files are supported right now."
        }

    safe_filename = Path(file.filename).name
    file_path = REPORTS_FOLDER / safe_filename

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Extract text automatically.
    # Normal PDF → PyMuPDF
    # Scanned PDF → Tesseract OCR
    extracted_text = extract_text_from_pdf_with_ocr(
        str(file_path)
    )

    # Extract structured medical information
    medical_information = extract_medical_information(
        extracted_text
    )

    return {
        "filename": safe_filename,
        "message": "Medical report uploaded and processed successfully!",

        "medical_information": {
            "patient_id": medical_information.patient_id,
            "patient_name": medical_information.patient_name,
            "age": medical_information.age,
            "gender": medical_information.gender,

            "symptoms": medical_information.symptoms,
            "diseases": medical_information.diseases,
            "medications": medical_information.medications,

            "laboratory_results": [
                {
                    "test_name": result.test_name,
                    "value": result.value,
                    "unit": result.unit,
                }
                for result in medical_information.laboratory_results
            ],

            "clinical_findings": medical_information.clinical_findings,
            "measurements": medical_information.measurements,
        },
    }
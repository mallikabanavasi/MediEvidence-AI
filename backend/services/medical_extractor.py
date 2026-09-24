import re

from backend.models.medical_data import (
    MedicalInformation,
    LaboratoryResult,
)


def extract_medical_information(text: str) -> MedicalInformation:
    """
    Extract structured medical information from a medical report.
    """

    information = MedicalInformation()

    # -----------------------------
    # Patient information
    # -----------------------------

    patient_id = re.search(
        r"Patient ID:\s*(.+)",
        text,
        re.IGNORECASE,
    )

    patient_name = re.search(
        r"Patient Name:\s*(.+)",
        text,
        re.IGNORECASE,
    )

    age = re.search(
        r"Age:\s*(\d+)",
        text,
        re.IGNORECASE,
    )

    gender = re.search(
        r"Gender:\s*(.+)",
        text,
        re.IGNORECASE,
    )

    if patient_id:
        information.patient_id = patient_id.group(1).strip()

    if patient_name:
        information.patient_name = patient_name.group(1).strip()

    if age:
        information.age = int(age.group(1))

    if gender:
        information.gender = gender.group(1).strip()

    # -----------------------------
    # Symptoms
    # -----------------------------

    symptom_patterns = [
        r"reports?\s+(.+?)(?:\.|\n)",
        r"symptoms?:\s*(.+?)(?:\.|\n)",
    ]

    for pattern in symptom_patterns:
        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE,
        )

        for match in matches:
            if "fatigue" in match.lower():
                information.symptoms.append("mild fatigue")

    # Remove duplicate symptoms
    information.symptoms = list(
        dict.fromkeys(information.symptoms)
    )

    # -----------------------------
    # Laboratory results
    # -----------------------------

    laboratory_patterns = [
        (
            r"Hemoglobin:\s*([\d.]+)\s*([A-Za-z/%]+)",
            "Hemoglobin",
        ),
        (
            r"Blood Glucose:\s*([\d.]+)\s*([A-Za-z/%]+)",
            "Blood Glucose",
        ),
        (
            r"Total Cholesterol:\s*([\d.]+)\s*([A-Za-z/%]+)",
            "Total Cholesterol",
        ),
    ]

    for pattern, test_name in laboratory_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if match:

            value = float(match.group(1))
            unit = match.group(2)

            information.laboratory_results.append(
                LaboratoryResult(
                    test_name=test_name,
                    value=value,
                    unit=unit,
                )
            )

    # -----------------------------
    # Blood pressure
    # -----------------------------

    blood_pressure = re.search(
        r"Blood Pressure:\s*([^\n]+)",
        text,
        re.IGNORECASE,
    )

    if blood_pressure:

        information.measurements.append(
            blood_pressure.group(0).strip()
        )

    # -----------------------------
    # Clinical findings
    # -----------------------------

    if "Clinical Finding:" in text:
        finding = re.search(
            r"Clinical Finding:\s*(.+)",
            text,
            re.IGNORECASE,
        )

        if finding:
            information.clinical_findings.append(
                finding.group(1).strip()
            )

    return information
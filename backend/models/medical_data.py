from dataclasses import dataclass, field
from typing import List


@dataclass
class LaboratoryResult:
    test_name: str = ""
    value: float | None = None
    unit: str = ""


@dataclass
class MedicalInformation:
    patient_id: str = ""
    patient_name: str = ""
    age: int | None = None
    gender: str = ""

    symptoms: List[str] = field(default_factory=list)
    diseases: List[str] = field(default_factory=list)
    medications: List[str] = field(default_factory=list)
    laboratory_results: List[LaboratoryResult] = field(default_factory=list)
    clinical_findings: List[str] = field(default_factory=list)
    measurements: List[str] = field(default_factory=list)
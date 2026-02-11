from export.base import PatientExporter

class FileExporter(PatientExporter):
    def __init__(self, filepath):
        self.filepath = filepath

    def export(self, patient):
        with open(self.filepath, "a") as f:
            f.write(f"{patient.patient_id},{patient.name}\n")
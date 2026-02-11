from export.base import PatientExporter

class ConsoleExporter(PatientExporter):
    def export(self, patient):
        print(
            f"[ID={patient.patient_id}] "
            f"[Name={patient.name}] "
            f"[DOB={patient.dob}] "
            f"[Gender={patient.gender}]"
        )

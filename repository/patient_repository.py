import sqlite3
from utils.logger import get_logger

logger = get_logger(__name__)


class PatientRepository:
    def __init__(self, db_path):
        self.db_path = db_path
        self._create_table()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        with self._get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS patients (
                    patient_id TEXT PRIMARY KEY,
                    name TEXT,
                    dob TEXT,
                    gender TEXT
                )
                """
            )

    def save(self, patient):
        try:
            with self._get_connection() as conn:
                conn.execute(
                    """
                    INSERT OR REPLACE INTO patients
                    VALUES (?, ?, ?, ?)
                    """,
                    (patient.patient_id, patient.name, patient.dob, patient.gender),
                )
                logger.info(f"Saved patient {patient.patient_id}")

        except sqlite3.DatabaseError:
            logger.exception("Database error while saving patient")

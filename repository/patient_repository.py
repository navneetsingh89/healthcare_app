"""SQLite repository for patient persistence."""

import sqlite3

from models.patient import Patient
from utils import get_logger

logger = get_logger(__name__)


class PatientRepository:
    """Handles create and save operations for patient records."""

    def __init__(self, db_path: str) -> None:
        """
        Initialize repository and ensure table exists.
        
        Args:
            db_path: File path to the SQLite database.
        
        Returns:
            None
        """
        self.db_path = db_path
        self._create_table()

    def _get_connection(self) -> sqlite3.Connection:
        """
        Return a database connection to the configured SQLite file.
        
        Args:
            None
        
        Returns:
            sqlite3.Connection: Open SQLite connection object.
        """
        return sqlite3.connect(self.db_path)

    def _create_table(self) -> None:
        """
        Create the patients table if it does not already exist.
        
        Args:
            None
        
        Returns:
            None
        """
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

    def save(self, patient: Patient) -> None:
        """
        Insert or replace a patient row in the database.
        
        Args:
            patient: Patient entity to persist.
        
        Returns:
            None
        """
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

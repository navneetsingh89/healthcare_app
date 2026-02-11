# Healthcare App (FHIR Patient Import)

Simple Python app that pulls patient data from a public FHIR server, parses it,
stores it in SQLite, and exports a summary to the console and a text file.

## What It Does
- Fetches patients from `https://r4.smarthealthit.org` (FHIR R4 demo server)
- Parses patient name, birth date, and gender
- Saves patients to `patients.db` (SQLite)
- Appends `patient_id,name` to `patients.txt`
- Prints patient summaries to the console

## Project Structure
- `main.py` - entry point
- `api/` - FHIR API client
- `parser/` - patient JSON parsing
- `models/` - patient model and validation
- `repository/` - SQLite storage
- `service/` - orchestration
- `export/` - console + file exporters

## Requirements
- Python 3.10+ (works with 3.13 too)
- `requests`

Install dependency:
```bash
pip install requests
```

## Setup (Recommended)
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run
```bash
python main.py
```

By default it fetches 10 patients. You can change this in `main.py`:
```python
service.process(count=10)
```

## Outputs
- `patients.db` - SQLite database with `patients` table
- `patients.txt` - appended lines of `patient_id,name`

## Notes
- The FHIR server is public and may rate-limit or change availability.
- Errors and retries are logged via the built-in `logging` module.

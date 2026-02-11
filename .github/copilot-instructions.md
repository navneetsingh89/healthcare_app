# Healthcare App - Copilot Instructions

## Architecture Overview

This is a FHIR healthcare data pipeline that fetches patient records, transforms them, persists them, and exports to multiple formats. The application follows a **layered architecture** with clear separation of concerns:

```
FHIR API → Parser → Service → Repository/Exporters
```

### Core Components

- **API Layer** ([api/fhir_client.py](api/fhir_client.py)): FHIR R4 client with resilient retry logic (exponential backoff, configurable timeouts) for HTTP 5xx errors and timeouts
- **Domain Model** ([models/patient.py](models/patient.py)): `Patient` class with defensive validation in constructor validates all fields against allowed values
- **Parser** ([parser/patient_parser.py](parser/patient_parser.py)): Transforms FHIR JSON to domain objects; gracefully degrades to "UNKNOWN" values on parse failures
- **Repository** ([repository/patient_repository.py](repository/patient_repository.py)): SQLite persistence layer with upsert semantics (`INSERT OR REPLACE`)
- **Service** ([service/patient_service.py](service/patient_service.py)): Orchestrator that chains API → Parse → Persist → Export in sequence
- **Exporters** ([export/](export/)): Plugin pattern with abstract `PatientExporter` base; `ConsoleExporter` and `FileExporter` implementations

## Key Patterns & Conventions

### Error Handling
- **API**: Log errors, catch exceptions (Timeout, HTTPError, general), return empty list as fallback
- **Parser**: Log exceptions, return Patient with all "UNKNOWN" fallback values on any failure
- **Repository**: Log DatabaseError, silently fail (no raise) to maintain pipeline continuity
- **Logging**: Always use `logging.info()` for save operations, `logging.exception()` for errors

### Data Validation
- `Patient` constructor validates each field via private `_validate_*()` methods
- Validation returns safe default ("UNKNOWN*") rather than raising exceptions
- Gender field is whitelist-validated against `{male, female, other, unknown}`

### Export Pattern
- All exporters inherit from `PatientExporter` base class with abstract `export()` method
- Multiple exporters can be chained in `PatientService.__init__()` and called sequentially per patient
- Exporters run *after* persistence (side effects happen after repository.save())

## Development Workflow

### Running the Application
```bash
python main.py
```

This will:
1. Fetch 10 patients from public FHIR server (r4.smarthealthit.org)
2. Parse each into `Patient` domain objects
3. Save to `patients.db` (SQLite)
4. Output to console
5. Append to `patients.txt`

### Adding New Features

- **New exporter**: Create class in [export/](export/) inheriting from `PatientExporter`, add to `main.py` instantiation
- **New data fields**: Extend `Patient` class with new `_validate_*()` method, update parser, repository schema, and exporters
- **Retry logic changes**: Modify `Retry()` params in [api/fhir_client.py](api/fhir_client.py) (status_forcelist, backoff_factor, etc.)
- **Database changes**: Update [repository/patient_repository.py](repository/patient_repository.py) schema in `_create_table()`

## File Structure

```
main.py              # Entry point; DI container for all components
api/                 # External API integration
parser/              # FHIR JSON → Patient transformation
models/              # Domain objects
repository/          # Persistence (SQLite)
service/             # Business logic orchestration
export/              # Output transformations (plugin pattern)
config/              # Reserved for future configuration (currently empty)
patients.db          # SQLite database (created on first run)
patients.txt         # CSV export output
```

## Important Implementation Details

- **Ambiguous FHIR data**: Parser extracts `names[0].given[0]` and `family` separately (prefers first entry)
- **Patient ID as PK**: Repository uses patient_id as SQLite PRIMARY KEY (enforces uniqueness)
- **Connection management**: Repository uses context manager (`with self._get_connection()`) for auto-commit
- **Timeout configuration**: API client has separate connect/read timeouts `(3.05, 10)` to handle slow FHIR servers

## External Dependencies

- `requests`: HTTP client library with urllib3 Retry adapter
- `sqlite3`: Standard library for local persistence
- No external healthcare libraries—FHIR parsing is done manually (educational project)

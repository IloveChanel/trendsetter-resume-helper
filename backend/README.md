# Backend API Documentation

## Trendsetter AI Resume Helper Backend

FastAPI-based backend for ATS-optimized resume analysis and optimization.

## Features

- 🤖 **ATS Compatibility Checker** - Identifies ATS-killer issues
- 🔑 **Keyword Extraction & Matching** - TF-IDF based matching with synonyms
- 📝 **Grammar & Style Checker** - Detects weak language and errors
- 📊 **Resume Parser** - Extracts structured data from resumes
- 💡 **Optimizer** - Provides actionable optimization suggestions
- 💾 **Database** - SQLite for jobs, resumes, keywords, and history

## Installation

```bash
cd backend
pip install -r requirements.txt
```

## Running the Server

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

API will be available at: `http://localhost:8000`
Documentation: `http://localhost:8000/docs`

## API Endpoints

### Health Check
- `GET /` - Root endpoint
- `GET /api/health` - Health check

### Resume Operations
- `POST /api/upload-resume` - Upload and parse resume (PDF/DOCX)
  - Form data: `file` (file upload)
  - Returns: parsed resume data

- `POST /api/analyze-resume` - Full resume analysis
  - Form data: `resume_text` (string), `filename` (optional string)
  - Returns: ATS score, grammar analysis, parsed data

- `POST /api/save-resume` - Save resume profile
  - Form data: `name`, `profile_type`, `content`, `file_path` (optional)
  - Returns: resume ID and details

- `GET /api/resumes` - Get all saved resume profiles
  - Returns: list of resume profiles

### Job Operations
- `POST /api/match-job` - Match resume against job description
  - Form data: `resume_text`, `job_description`, `job_title` (optional)
  - Returns: match score, ATS score, missing keywords, optimization suggestions

- `POST /api/save-job` - Save job description
  - Form data: `title`, `description`, `role_type`, `company` (optional)
  - Returns: job ID and keyword count

- `GET /api/jobs` - Get all saved jobs
  - Query params: `role_type` (optional)
  - Returns: list of jobs

- `GET /api/jobs/{role_type}` - Get jobs by role type
  - Path param: `role_type` (Full Stack, Frontend, Backend, Other)
  - Returns: filtered jobs

### Optimization
- `POST /api/optimize-resume` - Get optimization suggestions
  - Form data: `resume_text`, `job_description`
  - Returns: comprehensive optimization suggestions

### Keywords & History
- `GET /api/keyword-library/{role_type}` - Get keyword library
  - Path param: `role_type`
  - Returns: keywords with frequency and importance scores

- `GET /api/analysis-history` - Get past analyses
  - Query param: `limit` (default: 20)
  - Returns: analysis history

## Database Schema

### Tables

#### Jobs
- `id` - Primary key
- `title` - Job title
- `company` - Company name
- `description` - Job description text
- `role_type` - Full Stack, Frontend, Backend, Other
- `keywords` - JSON array of keywords
- `created_at` - Timestamp

#### Resumes
- `id` - Primary key
- `name` - Resume name
- `profile_type` - Profile type (Full Stack, Frontend, etc.)
- `content` - Resume text content
- `file_path` - Optional file path
- `created_at` - Timestamp

#### Keywords
- `id` - Primary key
- `keyword` - Keyword text
- `role_type` - Associated role type
- `frequency` - How often keyword appears
- `importance_score` - Calculated importance
- `created_at` - Timestamp

#### AnalysisHistory
- `id` - Primary key
- `resume_id` - Reference to resume
- `job_id` - Reference to job
- `resume_name` - Resume name
- `job_title` - Job title
- `score` - Match score
- `ats_score` - ATS compatibility score
- `missing_keywords` - JSON array
- `suggestions` - JSON array
- `created_at` - Timestamp

## Modules

### `database.py`
SQLAlchemy ORM models and database initialization.

### `ats_checker.py`
Checks resumes for ATS compatibility issues:
- Tables and complex formatting
- Non-standard section headers
- Special characters
- Contact information
- Quantifiable achievements

### `matcher.py`
Advanced keyword matching:
- TF-IDF scoring
- Synonym matching
- Keyword density calculation
- Match score calculation

### `resume_parser.py`
Extracts structured data:
- Contact information
- Work experience
- Education
- Skills
- Certifications
- Metrics and action verbs

### `grammar_checker.py`
Checks for grammar and style issues:
- Weak phrases
- Passive voice
- First person pronouns
- Spelling errors
- Readability score

### `optimizer.py`
Generates optimization suggestions:
- Section header improvements
- Keyword placement suggestions
- Formatting fixes
- Content enhancements
- Prioritized action items

## Example Usage

### Upload and Analyze Resume
```bash
curl -X POST http://localhost:8000/api/upload-resume \
  -F "file=@resume.pdf"
```

### Match Against Job
```bash
curl -X POST http://localhost:8000/api/match-job \
  -F "resume_text=..." \
  -F "job_description=..." \
  -F "job_title=Senior Developer"
```

### Save Job
```bash
curl -X POST http://localhost:8000/api/save-job \
  -F "title=Senior Full Stack Developer" \
  -F "description=..." \
  -F "role_type=Full Stack" \
  -F "company=Tech Corp"
```

## Error Handling

All endpoints return structured error responses:
```json
{
  "detail": "Error message here"
}
```

HTTP status codes:
- `200` - Success
- `400` - Bad request (invalid input)
- `500` - Server error

## Development

### Running Tests
```bash
pytest
```

### Code Style
```bash
black .
flake8 .
```

## License

MIT

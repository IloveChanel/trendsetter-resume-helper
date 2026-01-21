# Trendsetter AI Resume Helper

An AI-powered resume analyzer that matches resumes to job descriptions, helping candidates understand how well their resumes align with job requirements.

## 🎯 Project Purpose

This application helps job seekers by:
- Parsing resumes from PDF and DOCX formats
- Analyzing job descriptions
- Matching resumes against job requirements
- Providing a compatibility score and insights

## 📁 Directory Structure

```
trendsetter-resume-helper/
├── .gitignore              # Git ignore rules
├── .scripts/               # Utility scripts
│   └── find_duplicates.py  # Script to find duplicate files
├── backend/                # Backend API (FastAPI)
│   ├── app/
│   │   ├── app.py          # Main FastAPI application
│   │   └── matcher.py      # Resume-JD matching logic
│   └── requirements.txt    # Python dependencies
├── package.json            # Frontend dependencies (for future use)
├── package-lock.json       # Locked frontend dependencies
└── README.md               # This file
```

## 🚀 Setup Instructions

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn pdfplumber python-docx weasyprint jinja2
   ```
   
   Or create a `requirements.txt` with:
   ```
   fastapi
   uvicorn
   pdfplumber
   python-docx
   weasyprint
   jinja2
   ```
   
   And install with:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```bash
   cd app
   python app.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at `http://localhost:8000`

### Frontend Setup

Frontend is currently under development. Dependencies are tracked in `package.json`.

## 🔧 How to Use

### API Endpoints

#### 1. Root Endpoint
```
GET /
```
Returns a welcome message to verify the API is running.

#### 2. Parse Resume
```
POST /api/parse-resume
```
Upload a resume file (PDF or DOCX) to extract text content.

**Request:**
- Method: POST
- Content-Type: multipart/form-data
- Body: file (PDF or DOCX)

**Response:**
```json
{
  "resume": {
    "text": "Full resume text...",
    "lines": ["First 50 lines of the resume..."]
  }
}
```

#### 3. Match Resume to Job Description
```
POST /api/match-jd
```
Compare a resume against a job description to get a match score.

**Request:**
- Method: POST
- Content-Type: application/x-www-form-urlencoded
- Body:
  - `resume_text`: Full text of the resume
  - `jd_text`: Full text of the job description

**Response:**
```json
{
  "score": 75,
  "matching_keywords": ["python", "fastapi", "api"],
  "missing_keywords": ["kubernetes", "docker"]
}
```

## 🛠️ Development

### Running the Backend in Development Mode

```bash
cd backend/app
uvicorn app:app --reload
```

The `--reload` flag enables hot-reloading during development.

### API Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 🔍 Utilities

### Find Duplicates Script

The `.scripts/find_duplicates.py` script helps identify duplicate files in the repository:

```bash
python .scripts/find_duplicates.py
```

This generates a `duplicate_report.json` file (which is gitignored).

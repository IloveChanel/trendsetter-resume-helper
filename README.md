# 🚀 Trendsetter AI Resume Helper

Beat ATS bots and rank your resume at the top!

## Features

- 🤖 **ATS Compatibility Checker** - Identifies resume formatting issues that block ATS systems
- 🔑 **Keyword Extraction & Matching** - TF-IDF based matching with intelligent synonym recognition
- 📝 **Grammar & Error Scanner** - Detects weak language, passive voice, and spelling errors
- 💾 **Job Description Library** - Save and organize job postings by role type
- 👤 **Multiple Resume Profiles** - Maintain versions for Full Stack, Frontend, Backend roles
- 📊 **Match Score Analytics** - Visual dashboards with actionable optimization suggestions
- 💡 **Smart Optimizer** - Get specific placement suggestions for missing keywords

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn

### Local Development

#### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

#### Frontend Setup

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000`

#### Access the Application

Open your browser and navigate to: **http://localhost:3000**

### Quick Deploy with Docker

```bash
# One-command deployment
./deploy.sh

# Or manually with docker-compose
docker-compose up -d
```

Access at: **http://localhost:3000**

## Deployment

For production deployment options, see **[DEPLOYMENT.md](DEPLOYMENT.md)** for detailed guides on:

- 🚀 **Quick Deploy**: Vercel (Frontend) + Render (Backend) - Free tier available
- 🐳 **Docker Deployment**: Complete containerized setup
- ☁️ **Cloud Platforms**: AWS, DigitalOcean, Railway, Fly.io
- 🖥️ **VPS Deployment**: Ubuntu server with Nginx and PM2

**Recommended for Production:**
- Frontend: Vercel (Free tier or $20/mo Pro)
- Backend: Render ($7/mo) or Railway ($5/mo)
- Total cost: $0-30/month depending on tier

## Project Structure

```
trendsetter-resume-helper/
├── backend/
│   ├── app.py              # Main FastAPI application
│   ├── database.py         # SQLAlchemy models & DB setup
│   ├── ats_checker.py      # ATS compatibility checker
│   ├── matcher.py          # Keyword matching with TF-IDF
│   ├── resume_parser.py    # Resume data extraction
│   ├── grammar_checker.py  # Grammar and style checking
│   ├── optimizer.py        # Resume optimization suggestions
│   ├── requirements.txt    # Python dependencies
│   └── README.md          # Backend API documentation
│
├── frontend/
│   ├── app/
│   │   ├── layout.tsx      # Root layout
│   │   ├── page.tsx        # Landing page
│   │   └── globals.css     # Global styles
│   ├── components/
│   │   ├── ResumeUpload.tsx    # Drag-and-drop resume upload
│   │   ├── JobInput.tsx        # Job description input
│   │   └── Results.tsx         # Analysis results display
│   ├── package.json
│   └── tailwind.config.ts  # Tailwind configuration
│
└── README.md              # This file
```

## How It Works

### 1. Upload Your Resume
- Drag and drop your resume (PDF or DOCX)
- The parser extracts text and structured data

### 2. Enter Job Description
- Paste the job description
- Optionally add job title and role type
- System extracts keywords and requirements

### 3. Get Instant Analysis
- **ATS Compatibility Score (0-100%)** - Checks for formatting issues
- **Keyword Match Score (0-100%)** - Shows found and missing keywords
- **Grammar & Style Report** - Identifies weak language and errors
- **Optimization Suggestions** - Actionable improvements with examples

### 4. Optimize Your Resume
- Follow priority fixes
- Add missing keywords in suggested sections
- Improve formatting for ATS systems
- Re-analyze to track improvements

## API Endpoints

### Resume Operations
- `POST /api/upload-resume` - Upload and parse resume
- `POST /api/analyze-resume` - Full resume analysis
- `POST /api/save-resume` - Save resume profile
- `GET /api/resumes` - Get saved resumes

### Job Operations
- `POST /api/match-job` - Match resume against job description
- `POST /api/save-job` - Save job to library
- `GET /api/jobs` - Get all jobs
- `GET /api/jobs/{role_type}` - Filter by role

### Optimization
- `POST /api/optimize-resume` - Get optimization suggestions
- `GET /api/keyword-library/{role_type}` - Get keyword library
- `GET /api/analysis-history` - View past analyses

## Database

Uses SQLite for local storage (no external database needed):

- **Jobs** - Saved job descriptions with extracted keywords
- **Resumes** - Multiple resume profiles by type
- **Keywords** - Growing library of keywords by role
- **Analysis History** - Track all analyses and scores

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database
- **pdfplumber** - PDF text extraction
- **python-docx** - DOCX parsing
- **scikit-learn** - TF-IDF calculations

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **react-dropzone** - File upload
- **Framer Motion** - Animations
- **Recharts** - Data visualization

## Color Scheme

Modern, sophisticated design (NOT teal):

- **Primary**: Deep Purple (#6366f1)
- **Navy**: Sophisticated Navy (#1e293b)
- **Background**: Clean whites and grays (#f8fafc)
- **Success**: Emerald (#10b981)
- **Warning**: Amber (#f59e0b)
- **Error**: Rose (#f43f5e)

## Features in Detail

### ATS Compatibility Checker
Detects issues that cause ATS systems to fail:
- Tables and text boxes
- Images, graphics, charts
- Complex column layouts
- Non-standard section headers
- Special characters and symbols
- Missing contact information
- Lack of quantifiable achievements

### Keyword Matching
Advanced matching algorithm:
- TF-IDF scoring for keyword importance
- Synonym recognition (JavaScript = JS, React = React.js)
- Context-aware keyword extraction
- Keyword density calculation
- Missing keyword identification

### Grammar & Style Checker
Improves resume quality:
- Weak phrase detection
- Passive voice identification
- First-person pronoun checking
- Spelling error detection
- Readability scoring
- Action verb counting

### Resume Optimizer
Actionable suggestions:
- Section header improvements
- Keyword placement recommendations
- Formatting fixes
- Content enhancements
- Impact statement examples
- Priority-sorted action items

## Development

### Run Backend Tests
```bash
cd backend
pytest
```

### Run Frontend in Dev Mode
```bash
cd frontend
npm run dev
```

### Build for Production
```bash
cd frontend
npm run build
npm start
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Built with ❤️ to help you beat ATS bots and land your dream job!** 🚀

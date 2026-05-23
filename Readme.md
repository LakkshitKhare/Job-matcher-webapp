
# 🧠 AI-Powered Job Matcher Web App

A full-stack MVP project that helps users find the most relevant job listings and generate tailored CV summaries — powered by AI and your resume.

[🔗 Live Demo (Streamlit)](https://job-matcher-webapp-lakku.streamlit.app/)
[🧪 API Docs (FastAPI backend)](https://job-matcher-webapp.onrender.com/docs)

## 🚀 Features

### 📄 Resume Parsing
- Upload your resume (PDF).
- Automatically extract skills, experience, and other relevant data using `PyMuPDF` and `spaCy`.

### 🔍 Job Matching
- Fetches **real-time job listings** using the [JSearch API](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch).
- Matches jobs based on your resume content using a cosine similarity scoring system.

### ✨ AI-Based CV Summary Generation
- Uses the **Gemini Pro API** to generate customized CV paragraphs for each job listing.
- Tailored summaries boost your chances of selection in Applicant Tracking Systems (ATS).

### 🌐 Frontend & Backend
- **Frontend:** Built with Streamlit (lightweight and interactive UI).
- **Backend:** FastAPI handles parsing, matching, and AI integration logic.

---


## 🧰 Tech Stack

| Layer      | Tools Used                                    |
|------------|-----------------------------------------------|
| Frontend   | Streamlit                                     |
| Backend    | FastAPI, Pydantic, Uvicorn                    |
| AI API     | Gemini Pro (Google Generative AI)             |
| Resume Parsing | PyMuPDF, spaCy                           |
| Job API    | JSearch API via RapidAPI                      |
| Deployment | Render.com (Free tier for MVP)                |

---

## 🛠️ How It Works

1. **User uploads PDF resume** via Streamlit frontend.
2. **Backend parses** the resume → extracts data.
3. User **inputs a job description** or chooses from live job listings.
4. **Cosine similarity** is calculated between the resume and each job.
5. Top job matches are returned and **CV summaries are generated** for each.

---

## 💡 Future Enhancements

- Login/Signup with user dashboard
- Save multiple resumes and generated CVs
- Job alerts and application tracking
- Support for DOCX resumes and multi-language parsing

---

## 📦 Setup Instructions (Local)

```bash
# Clone the repo
git clone https://github.com/your-username/job-matcher-webapp.git
cd job-matcher-webapp

# Backend setup
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend setup
cd ../frontend
streamlit run app.py
````

---

## 📜 License

This project is open-sourced under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

Built with 💙 by [Lakkshit Khare](https://github.com/LakkshitKhare)
LinkedIn: [linkedin.com/in/lakkshitkhare](https://linkedin.com/in/lakkshitkhare)


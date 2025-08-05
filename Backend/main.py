from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PyPDF2 import PdfReader
from typing import List
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Keys
JSEARCH_API_KEY = os.getenv("JSEARCH_API_KEY") or "3dcc80e597mshcee82adce8002f7p1d6e5fjsn6f7270cd439e"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or "AIzaSyCOvZmYDqGP1CiIgvn7RqFWFYOwUNplAyw"

def extract_text_from_resume(uploaded_file: UploadFile) -> str:
    try:
        reader = PdfReader(uploaded_file.file)
        return " ".join(page.extract_text() or "" for page in reader.pages)
    except Exception:
        raise HTTPException(status_code=400, detail="Could not parse PDF.")

def generate_custom_cv(resume_text: str, job_role: str, location: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY,
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Given the resume text: \"{resume_text}\", generate a personalized CV summary tailored for a job as a {job_role} in {location}. Keep it professional, relevant, and impactful."
                    }
                ]
            }
        ]
    }

    response = requests.post(
        "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent",
        headers=headers,
        json=data,
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {response.text}")

    return response.json()["candidates"][0]["content"]["parts"][0]["text"]

def fetch_jobs_from_jsearch(job_role: str, location: str) -> List[dict]:
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": JSEARCH_API_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
    }

    # Enhanced location filtering
    params = {
        "query": f"{job_role} in {location}",
        "location": location,
        "page": "1"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"JSearch API error: {response.text}")

    jobs = response.json().get("data", [])
    
    # Enhanced output with job name, location, and link
    return [
        {
            "job_name": job.get("job_title", "Unknown"),
            "location": job.get("job_location", ""),
            "link": job.get("job_apply_link", ""),
            "company": job.get("employer_name", "Unknown")
        }
        for job in jobs
    ]

@app.post("/match-and-generate/")
async def match_and_generate(
    resume: UploadFile = File(...),
    job_role: str = Form(...),
    job_location: str = Form(...)
):
    resume_text = extract_text_from_resume(resume)
    custom_cv = generate_custom_cv(resume_text, job_role, job_location)
    matched_jobs = fetch_jobs_from_jsearch(job_role, job_location)

    return JSONResponse({
        "custom_cv": custom_cv,
        "matched_jobs": matched_jobs
    })

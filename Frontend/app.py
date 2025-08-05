import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="AI Job Matcher",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    .job-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .input-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="header"><h1>🎯 AI Job Matcher</h1><p>Upload your resume and get personalized job matches with custom CVs</p></div>', unsafe_allow_html=True)

# Input section
with st.container():
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📄 Upload Your Resume")
        resume_file = st.file_uploader("Choose a PDF file", type=["pdf"], help="Upload your resume in PDF format")
        
        st.markdown("### 🎯 Job Details")
        job_role = st.text_input("Job Role", placeholder="e.g. Machine Learning Engineer", help="Enter the job role you're applying for")
        job_location = st.text_input("Location", placeholder="e.g. Pune, India", help="Enter your preferred job location")
    
    with col2:
        st.markdown("### 🎨 Features")
        st.markdown("""
        - 📄 **Resume Analysis**: Extract text from PDF
        - 🎯 **Job Matching**: Find relevant positions
        - 📄 **Custom CV**: Personalized CV generation
        - 🔗 **Direct Links**: Apply directly to jobs
        """)

# Process button
if st.button("🚀 Generate Custom CV & Find Jobs", type="primary"):
    if resume_file and job_role and job_location:
        with st.spinner("🔄 Processing your resume and finding jobs..."):
            try:
                response = requests.post(
                    "https://jobmatcher-backend.onrender.com/match-and-generate/",
                    files={"resume": resume_file},
                    data={"job_role": job_role, "job_location": job_location},
                )

                if response.status_code == 200:
                    data = response.json()

                    # Custom CV Section
                    st.markdown("### 📄 Your Custom CV")
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.text_area("CV Preview", value=data["custom_cv"], height=200)
                    with col2:
                        st.download_button(
                            "📥 Download CV",
                            data["custom_cv"],
                            f"{job_role.replace(' ', '_')}_CV.txt",
                            "text/plain"
                        )

                    # Job Matches Section
                    st.markdown("### 🔍 Matching Jobs")
                    if data["matched_jobs"]:
                        for job in data["matched_jobs"]:
                            with st.container():
                                st.markdown(f"""
                                <div style="
                                    background-color: #ffffff;
                                    border-radius: 10px;
                                    padding: 1rem;
                                    margin: 0.5rem 0;
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
                                    color: #333333;
                                    font-family: Arial, sans-serif;
                                ">
                                    <h4 style="margin-bottom: 0.25rem; color: #2c3e50;">{job.get('job_name', 'Unknown Job')}</h4>
                                    <p style="margin: 0.1rem 0;"><strong>Company:</strong> {job.get('company', 'Unknown')}</p>
                                    <p style="margin: 0.1rem 0;"><strong>Location:</strong> {job.get('location', 'N/A')}</p>
                                    <a href="{job.get('link', '#')}" target="_blank" style="color: #2980b9; font-weight: bold; text-decoration: none;">Apply Now</a>
                                </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.info("No jobs found matching your criteria.")

                else:
                    st.error(f"Error: {response.status_code}")
            except Exception as e:
                st.error(f"Connection error: {e}")
    else:
        st.warning("Please complete all fields before proceeding.")

# Footer
st.markdown("---")
st.markdown("Made By Lakkshit Khare http://lakkshit-khare-nguezif.gamma.site", unsafe_allow_html=True)

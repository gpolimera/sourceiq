import streamlit as st
import urllib.parse
import google.generativeai as genai
from PyPDF2 import PdfReader

# --- 1. AI CONFIGURATION ---
# Get your key at: https://aistudio.google.com/
genai.configure(api_key="AIzaSyCimUFZ5xW_7Rw1uYu0L9kEmTS9THZMoDc")
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="SourceIQ", page_icon="🎯", layout="wide")

# Custom CSS for a professional "Unique" look
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main-header { color: #1E3A8A; font-size: 3rem; font-weight: bold; }
    .stButton>button { background-color: #1E3A8A; color: white; border-radius: 5px; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATA ---
locations = {
    "USA": ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"],
    "India": ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal", "Delhi", "Chandigarh", "Puducherry"]
}

# --- 4. HELPER FUNCTIONS ---
def extract_pdf_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# --- 5. UI LAYOUT ---
st.markdown('<div class="main-header">🎯 SourceIQ</div>', unsafe_allow_html=True)
st.subheader("Smart US & India IT Recruitment Suite")

menu = st.sidebar.selectbox("Navigate Features", ["Real LinkedIn Puller", "JD Analyser", "Resume Matcher"])

# --- FEATURE 1: LINKEDIN PULLER ---
if menu == "Real LinkedIn Puller":
    st.header("🔍 Real LinkedIn Profile Puller")
    col1, col2 = st.columns(2)
    with col1:
        country = st.selectbox("Select Country", ["USA", "India"])
    with col2:
        state = st.selectbox("Select State/UT", locations[country])
    
    job_title = st.text_input("Enter Job Title or Skills", placeholder="e.g. Senior Java Developer")
    
    if st.button("Generate X-Ray Search"):
        if job_title:
            query = f'site:linkedin.com/in/ "{job_title}" "{state}" -intitle:profiles -inurl:dir'
            encoded_query = urllib.parse.quote(query)
            google_url = f"https://www.google.com/search?q={encoded_query}"
            st.success(f"Success! Pulling profiles for {job_title}")
            st.code(query, language="markdown")
            st.link_button("🚀 Open Search Results on Google", google_url)
        else:
            st.error("Please enter a Job Title.")

# --- FEATURE 2: JD ANALYSER ---
elif menu == "JD Analyser":
    st.header("📝 Smart Job Description Analyser")
    jd_input = st.text_area("Paste Job Description Here", height=300)
    
    if st.button("Analyze as Professional Recruiter"):
        if jd_input:
            with st.spinner("Analyzing JD..."):
                prompt = f"Act as a Professional US IT Recruiter. Analyze this JD: {jd_input}. Provide: 1. A 3-sentence simple summary. 2. A list of 5 Must-Have Skills. 3. A high-quality Dice/LinkedIn Boolean String."
                response = model.generate_content(prompt)
                st.markdown("### 🤖 Recruiter Intelligence Output")
                st.write(response.text)
        else:
            st.error("Please paste a JD.")

# --- FEATURE 3: RESUME MATCHER ---
elif menu == "Resume Matcher":
    st.header("📄 Technical Resume Matcher (AI Scorer)")
    target_jd = st.text_area("Paste Target Job Description", height=200)
    uploaded_file = st.file_uploader("Upload Candidate Resume (PDF)", type="pdf")
    
    if st.button("Calculate Match Score"):
        if target_jd and uploaded_file:
            with st.spinner("Evaluating candidate..."):
                resume_text = extract_pdf_text(uploaded_file)
                prompt = f"""
                Compare this Resume to the JD. 
                Resume: {resume_text}
                JD: {target_jd}
                
                Provide:
                1. A Match Score from 0% to 100%.
                2. List of Matching Skills.
                3. List of Missing Skills (Gaps).
                4. Final Verdict (Hire/Reject).
                """
                response = model.generate_content(prompt)
                st.markdown("### 📊 Technical Match Report")
                st.write(response.text)
        else:
            st.error("Please provide both the JD and the Resume.") 
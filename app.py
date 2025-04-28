import streamlit as st
import spacy
from spacy.matcher import PhraseMatcher
import re
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import io

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    st.error("Please install the spaCy English language model by running: python -m spacy download en_core_web_sm")
    st.stop()

# Initialize phrase matcher
matcher = PhraseMatcher(nlp.vocab)

# Define skill categories and their patterns
SKILL_PATTERNS = {
    "PROGRAMMING": [
        r"python", r"java", r"javascript", r"c\+\+", r"c#", r"ruby", r"go", r"rust",
        r"swift", r"kotlin", r"typescript", r"php", r"perl", r"scala", r"r"
    ],
    "FRAMEWORK": [
        r"django", r"flask", r"spring", r"react", r"angular", r"vue", r"express",
        r"laravel", r"rails", r"tensorflow", r"pytorch", r"scikit-learn", r"node\.js"
    ],
    "TOOL": [
        r"git", r"docker", r"kubernetes", r"jenkins", r"ansible", r"terraform",
        r"aws", r"azure", r"gcp", r"jira", r"confluence", r"slack", r"trello"
    ],
    "METHODOLOGY": [
        r"agile", r"scrum", r"kanban", r"devops", r"ci/cd", r"tdd", r"bdd",
        r"pair programming", r"code review", r"version control"
    ],
    "SOFT_SKILL": [
        r"communication", r"leadership", r"teamwork", r"problem solving",
        r"time management", r"critical thinking", r"creativity", r"adaptability",
        r"emotional intelligence", r"conflict resolution"
    ],
    "DATABASE": [
        r"sql", r"mysql", r"postgresql", r"mongodb", r"redis", r"cassandra",
        r"oracle", r"sqlite", r"dynamodb", r"firebase"
    ]
}

# Compile patterns and add to matcher
for category, patterns in SKILL_PATTERNS.items():
    compiled_patterns = [nlp.make_doc(pattern) for pattern in patterns]
    matcher.add(category, compiled_patterns)

def load_skills():
    """Load the predefined skills list."""
    try:
        with open('skills_list.txt', 'r', encoding='utf-8') as file:
            skills = file.read()
            return [skill.strip().lower() for skill in skills.split('\n') if skill.strip()]
    except FileNotFoundError:
        st.error("Skills list file not found!")
        return []

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def extract_skills_with_spacy(text, skills_list):
    """Extract skills using spaCy NER, custom patterns, and pattern matching."""
    if not text:
        return set()
    
    # Process text with spaCy
    doc = nlp(text.lower())
    
    found_skills = set()
    
    # Extract skills using NER
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT", "LANGUAGE"]:
            skill = ent.text.lower()
            if skill in skills_list:
                found_skills.add(skill)
    
    # Extract skills using custom patterns
    matches = matcher(doc)
    for match_id, start, end in matches:
        category = nlp.vocab.strings[match_id]
        skill = doc[start:end].text.lower()
        if skill in skills_list:
            found_skills.add(skill)
    
    # Extract skills using pattern matching
    for skill in skills_list:
        # Create pattern for the skill
        pattern = re.compile(r'\b' + re.escape(skill) + r'\b', re.IGNORECASE)
        if pattern.search(text):
            found_skills.add(skill)
    
    return found_skills

def rank_missing_skills(job_description, missing_skills):
    """Rank missing skills using TF-IDF and frequency analysis."""
    if not missing_skills:
        return []
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        stop_words='english',
        token_pattern=r'(?u)\b\w+\b',
        ngram_range=(1, 3)
    )
    
    # Fit and transform the job description
    tfidf_matrix = vectorizer.fit_transform([job_description])
    feature_names = vectorizer.get_feature_names_out()
    
    # Get skill scores
    skill_scores = {}
    for skill in missing_skills:
        # Split skill into words for matching
        skill_words = skill.split()
        score = 0
        
        # Calculate TF-IDF score for the skill
        for word in skill_words:
            if word in feature_names:
                idx = np.where(feature_names == word)[0]
                if len(idx) > 0:
                    score += tfidf_matrix[0, idx[0]]
        
        # Add frequency bonus
        frequency = job_description.lower().count(skill.lower())
        score += frequency * 0.1
        
        skill_scores[skill] = score
    
    # Sort skills by score
    ranked_skills = sorted(skill_scores.items(), key=lambda x: x[1], reverse=True)
    return ranked_skills

def main():
    st.title("Resume Skills Enhancer")
    st.write("Upload your resume and paste the job description to analyze missing skills.")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=['pdf'])
    
    # Job description input
    job_description = st.text_area("Paste Job Description", height=200)
    
    # Analyze button
    if st.button("Analyze Skills"):
        if not uploaded_file:
            st.error("Please upload a resume file.")
            return
        
        if not job_description:
            st.error("Please enter a job description.")
            return
        
        # Load skills list
        skills_list = load_skills()
        if not skills_list:
            return
        
        # Extract text from resume
        resume_text = extract_text_from_pdf(uploaded_file)
        if not resume_text:
            return
        
        # Extract skills
        resume_skills = extract_skills_with_spacy(resume_text, skills_list)
        job_skills = extract_skills_with_spacy(job_description, skills_list)
        
        # Compare and suggest missing skills
        missing_skills = job_skills - resume_skills
        
        # Rank missing skills
        ranked_missing_skills = rank_missing_skills(job_description, missing_skills)
        
        # Display results
        st.subheader("Analysis Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Skills in Your Resume")
            if resume_skills:
                for skill in sorted(resume_skills):
                    st.write(f"- {skill}")
            else:
                st.write("No skills found in resume.")
        
        with col2:
            st.write("### Required Skills")
            if job_skills:
                for skill in sorted(job_skills):
                    st.write(f"- {skill}")
            else:
                st.write("No skills found in job description.")
        
        st.write("### Suggested Skills to Add")
        if ranked_missing_skills:
            for skill, score in ranked_missing_skills:
                st.write(f"- {skill} (importance score: {score:.2f})")
        else:
            st.write("No missing skills found!")

if __name__ == "__main__":
    main() 
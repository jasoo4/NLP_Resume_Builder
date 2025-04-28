import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import PyPDF2
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import spacy
from spacy.matcher import PhraseMatcher
import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy English language model...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

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

def load_pdf(filename):
    """Load and extract text from a PDF file."""
    try:
        with open(filename, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
    except Exception as e:
        messagebox.showerror("Error", f"Error reading PDF: {e}")
        return None

def load_file(filename):
    """Load and return the contents of a text file or PDF."""
    if filename.lower().endswith('.pdf'):
        return load_pdf(filename)
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found: {filename}")
        return None

def load_skills():
    """Load the predefined skills list."""
    skills = load_file('skills_list.txt')
    if skills:
        return [skill.strip().lower() for skill in skills.split('\n') if skill.strip()]
    return []

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
        ngram_range=(1, 3)  # Consider 1-3 word phrases
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
        score += frequency * 0.1  # Weight for frequency
        
        skill_scores[skill] = score
    
    # Sort skills by score
    ranked_skills = sorted(skill_scores.items(), key=lambda x: x[1], reverse=True)
    return ranked_skills

def compare_skills(resume_skills, job_skills):
    """Compare skills and return missing skills."""
    return job_skills - resume_skills

class ResumeSkillsEnhancer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Resume Skills Enhancer")
        self.root.geometry("800x600")
        
        # Create main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Resume upload section
        self.resume_frame = tk.Frame(self.main_frame)
        self.resume_frame.pack(fill=tk.X, pady=10)
        
        self.upload_btn = tk.Button(self.resume_frame, text="Upload Resume", command=self.upload_resume)
        self.upload_btn.pack(side=tk.LEFT)
        
        self.resume_path_label = tk.Label(self.resume_frame, text="No resume selected")
        self.resume_path_label.pack(side=tk.LEFT, padx=10)
        
        # Job description section
        self.job_desc_frame = tk.Frame(self.main_frame)
        self.job_desc_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(self.job_desc_frame, text="Paste Job Description:").pack(anchor=tk.W)
        self.job_desc_text = scrolledtext.ScrolledText(self.job_desc_frame, height=10)
        self.job_desc_text.pack(fill=tk.BOTH, expand=True)
        
        # Analyze button
        self.analyze_btn = tk.Button(self.main_frame, text="Analyze Skills", command=self.analyze_skills)
        self.analyze_btn.pack(pady=10)
        
        # Results section
        self.results_frame = tk.Frame(self.main_frame)
        self.results_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = scrolledtext.ScrolledText(self.results_frame, height=10)
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        self.resume_path = None

    def upload_resume(self):
        filetypes = [
            ("PDF files", "*.pdf"),
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
        filename = filedialog.askopenfilename(
            title="Select Resume",
            filetypes=filetypes
        )
        if filename:
            self.resume_path = filename
            self.resume_path_label.config(text=os.path.basename(filename))

    def analyze_skills(self):
        if not self.resume_path:
            messagebox.showerror("Error", "Please upload a resume first")
            return
        
        job_description = self.job_desc_text.get("1.0", tk.END).strip()
        if not job_description:
            messagebox.showerror("Error", "Please enter a job description")
            return
        
        # Load skills list
        skills_list = load_skills()
        if not skills_list:
            messagebox.showerror("Error", "Could not load skills list")
            return
        
        # Extract skills
        resume_text = load_file(self.resume_path)
        if not resume_text:
            return
        
        resume_skills = extract_skills_with_spacy(resume_text, skills_list)
        job_skills = extract_skills_with_spacy(job_description, skills_list)
        
        # Compare and suggest missing skills
        missing_skills = compare_skills(resume_skills, job_skills)
        
        # Rank missing skills
        ranked_missing_skills = rank_missing_skills(job_description, missing_skills)
        
        # Display results
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert(tk.END, "Skills Analysis Results:\n\n")
        self.results_text.insert(tk.END, f"Skills found in your resume: {', '.join(resume_skills)}\n\n")
        self.results_text.insert(tk.END, f"Skills required in job description: {', '.join(job_skills)}\n\n")
        
        if ranked_missing_skills:
            self.results_text.insert(tk.END, "Suggested skills to add (ranked by importance):\n")
            for skill, score in ranked_missing_skills:
                self.results_text.insert(tk.END, f"- {skill} (importance score: {score:.2f})\n")
        else:
            self.results_text.insert(tk.END, "No missing skills found!")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ResumeSkillsEnhancer()
    app.run() 
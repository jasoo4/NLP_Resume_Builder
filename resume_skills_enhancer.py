import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import PyPDF2
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

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

def extract_skills(text, skills_list):
    """Extract skills from text using the skills list."""
    if not text:
        return set()
    
    # Tokenize and clean the text
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words and token not in string.punctuation]
    
    # Find matching skills
    found_skills = set()
    for skill in skills_list:
        if skill in ' '.join(tokens):
            found_skills.add(skill)
    
    return found_skills

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
        
        resume_skills = extract_skills(resume_text, skills_list)
        job_skills = extract_skills(job_description, skills_list)
        
        # Compare and suggest missing skills
        missing_skills = compare_skills(resume_skills, job_skills)
        
        # Display results
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert(tk.END, "Skills Analysis Results:\n\n")
        self.results_text.insert(tk.END, f"Skills found in your resume: {', '.join(resume_skills)}\n\n")
        self.results_text.insert(tk.END, f"Skills required in job description: {', '.join(job_skills)}\n\n")
        self.results_text.insert(tk.END, f"Suggested skills to add: {', '.join(missing_skills)}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ResumeSkillsEnhancer()
    app.run() 
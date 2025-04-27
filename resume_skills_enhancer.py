import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

def load_file(filename):
    """Load and return the contents of a text file."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
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

def main():
    # Load the files
    resume_text = load_file('resume.txt')
    job_description_text = load_file('job_description.txt')
    skills_list = load_skills()
    
    if not all([resume_text, job_description_text, skills_list]):
        return
    
    # Extract skills
    resume_skills = extract_skills(resume_text, skills_list)
    job_skills = extract_skills(job_description_text, skills_list)
    
    # Compare and suggest missing skills
    missing_skills = compare_skills(resume_skills, job_skills)
    
    # Print results
    print("\nSkills Analysis Results:")
    print(f"\nSkills found in your resume: {', '.join(resume_skills)}")
    print(f"\nSkills required in job description: {', '.join(job_skills)}")
    print(f"\nSuggested skills to add: {', '.join(missing_skills)}")

if __name__ == "__main__":
    main() 
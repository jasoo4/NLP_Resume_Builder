# Smart Resume Skills Enhancer

This project helps job seekers identify missing skills in their resume compared to job descriptions.

## Features
- Load and parse resume and job description text files
- Extract skills using a predefined skills list
- Compare skills between resume and job description
- Generate suggestions for missing skills

## Setup
1. Install Python 3.8 or higher
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Download NLTK data:
   ```
   python -c "import nltk; nltk.download('punkt')"
   ```

## Usage
1. Place your resume in `resume.txt`
2. Place the job description in `job_description.txt`
3. Run the script:
   ```
   python resume_skills_enhancer.py
   ```

## File Structure
- `resume_skills_enhancer.py`: Main script
- `skills_list.txt`: Predefined list of skills
- `resume.txt`: Sample resume text file
- `job_description.txt`: Sample job description text file 
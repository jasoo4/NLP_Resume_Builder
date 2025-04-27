# Smart Resume Skills Enhancer

This project helps job seekers identify missing skills in their resume compared to job descriptions.

## Features
- GUI interface for easy use
- Support for PDF and text file resumes via file upload
- Direct job description input via text box
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
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

## Usage
1. Run the script:
   ```
   python resume_skills_enhancer.py
   ```
2. Click "Upload Resume" to select your resume file (PDF or text)
3. Paste the job description in the text box
4. Click "Analyze Skills" to see the results
5. View the analysis results in the results section

## File Structure
- `resume_skills_enhancer.py`: Main script with GUI interface
- `skills_list.txt`: Predefined list of skills
- `requirements.txt`: Required Python packages 
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)

user_data = {}
interview_state = {}
training_data = {
    'questions': [],
    'templates': []
}

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

RESUME_TEMPLATES = {
    'professional': {
        'name': 'Professional',
        'style': 'traditional',
        'color': "#040608"
    },
    'modern': {
        'name': 'Modern',
        'style': 'contemporary',
        'color': '#667eea'
    },
    'creative': {
        'name': 'Creative',
        'style': 'bold',
        'color': "#51496d"
    },
    'minimal': {
        'name': 'Minimal',
        'style': 'simple',
        'color': '#34495e'
    }
}

@app.route('/get-templates', methods=['GET'])
def get_templates():
    return jsonify({'templates': RESUME_TEMPLATES})

@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    data = request.json
    
    name = data.get('name', '')
    role = data.get('role', '')
    skills = data.get('skills', '')
    achievements = data.get('achievements', '')
    education = data.get('education', '')
    experience = data.get('experience', '')
    projects = data.get('projects', '')
    contact = data.get('contact', '')
    template = data.get('template', 'modern')
    user_data['resume'] = data
    objective = generate_career_objective(role, skills, experience)
    template_info = RESUME_TEMPLATES.get(template, RESUME_TEMPLATES['modern'])
    color = template_info['color']
    if template == 'professional':
        resume_html = generate_professional_template(name, role, contact, objective, skills, experience, education, achievements, projects, color)
    elif template == 'creative':
        resume_html = generate_creative_template(name, role, contact, objective, skills, experience, education, achievements, projects, color)
    elif template == 'minimal':
        resume_html = generate_minimal_template(name, role, contact, objective, skills, experience, education, achievements, projects, color)
    else:
        resume_html = generate_modern_template(name, role, contact, objective, skills, experience, education, achievements, projects, color)
    
    return jsonify({'resume': resume_html, 'success': True})

def generate_career_objective(role, skills, experience):
    
    skill_list = [s.strip() for s in skills.split(',')[:3]] 
    skills_text = ', '.join(skill_list) if skill_list else 'relevant technical skills'
    years = ''
    if 'year' in experience.lower():
        import re
        year_match = re.search(r'(\d+)\s*(?:\+)?\s*year', experience.lower())
        if year_match:
            years = year_match.group(1) + '+ years of '
    role_lower = role.lower()
    
    if 'software' in role_lower or 'developer' in role_lower or 'engineer' in role_lower:
        objective = f"Motivated {role} with {years}experience seeking to leverage expertise in {skills_text} to build innovative solutions and contribute to organizational success. Committed to writing clean, efficient code and staying current with emerging technologies."
    
    elif 'data' in role_lower and ('scientist' in role_lower or 'analyst' in role_lower):
        objective = f"A highly motivated and research-driven individual seeking the position of {role} with {years} expertise in {skills_text} Committed to continuous learning and utilizing advanced analytical techniques to deliver impactful, data-driven solutions."
    
    elif 'marketing' in role_lower or 'digital' in role_lower:
        objective = f"Creative and strategic {role} with {years}experience in {skills_text} seeking to drive brand growth and customer engagement. Dedicated to delivering impactful campaigns and measurable results."
    
    elif 'design' in role_lower or 'ui' in role_lower or 'ux' in role_lower:
        objective = f"A creative and user-focused professional seeking the role of {role} with {years} proficiency in {skills_text} seeking to create user-centered designs that enhance digital experiences. Passionate about combining aesthetics with functionality."
    
    elif 'manager' in role_lower or 'lead' in role_lower:
        objective = f"A dedicated and result-oriented professional seeking the role of {role} with {years} experience in {skills_text} Committed to leading teams effectively, improving operational efficiency, and ensuring smooth project execution. Driven to contribute to organizational growth through strategic planning, problem-solving, and collaboration. Eager to take on responsibilities that support business success and long-term goals."
    
    elif 'business' in role_lower and 'analyst' in role_lower:
        objective = f"A detail-oriented and analytical professional seeking the role of {role} with {years} expertise in {skills_text} Committed to understanding business needs, analyzing data, and delivering actionable insights that support strategic decision-making. Dedicated to improving processes, enhancing operational efficiency, and collaborating with cross-functional teams. Eager to contribute to organizational growth through effective problem-solving and data-driven recommendations."
    
    elif 'qa' in role_lower or 'quality' in role_lower or 'test' in role_lower:
        objective = f"A detail-oriented and process-driven professional seeking the role of {role} with {years} experience in {skills_text}Committed to ensuring product quality, identifying defects, and optimizing testing processes to meet industry standards. Dedicated to improving system reliability through thorough analysis, documentation, and collaboration with development teams. Eager to contribute to organizational excellence by delivering consistent, high-quality outcomes."
    elif 'devops' in role_lower or 'cloud' in role_lower:
        objective = f"A highly motivated and solution-oriented professional seeking the role of {role} with {years} expertise in {skills_text} Committed to improving deployment pipelines, automating workflows, and ensuring seamless integration and delivery across environments. Dedicated to enhancing system reliability, performance, and scalability through collaborative problem-solving and continuous improvement. Eager to contribute to organizational growth by building efficient, stable, and secure DevOps practices."
    
    elif 'product' in role_lower:
        objective = f"A strategic and user-focused professional seeking the role of {role} with {years} experience in {skills_text} Committed to driving product vision, translating user needs into actionable requirements, and collaborating with cross-functional teams to deliver high-impact solutions. Dedicated to improving product performance through data-driven decision-making, continuous iteration, and customer-centric thinking. Eager to contribute to the organizations growth by building products that create meaningful value."
    
    elif 'cyber' in role_lower or 'security' in role_lower:
        objective = f"A highly vigilant and security-focused professional seeking the role of {role} with {years} equipped with strong expertise in {skills_text} Committed to safeguarding systems, identifying vulnerabilities, and implementing effective security measures to protect organizational assets. Dedicated to strengthening security posture through proactive monitoring, incident response, and compliance with industry standards. Eager to contribute to a safer, resilient, and threat-resistant digital environment."
    
    else:
        objective = f"Motivated and skilled {role} with {years} expertise in {skills_text} seeking to contribute to organizational success through dedication, innovation, and continuous learning. Committed to delivering excellence and driving positive outcomes."
    
    return objective

def generate_modern_template(name, role, contact, objective, skills, experience, education, achievements, projects, color):
    return f"""
    <div class="resume-container modern-template" style="--theme-color: {color}">
        <div class="resume-header">
            <h1>{name}</h1>
            <p class="role-title">{role}</p>
            <p class="contact-info">{contact}</p>
        </div>
        
        <div class="resume-section">
            <h2>Professional Summary</h2>
            <p>Results-driven {role} with proven expertise in delivering high-quality solutions. 
            Passionate about leveraging technical skills to solve complex problems and drive business success.</p>
        </div>
        
        <div class="resume-section">
            <h2>Skills</h2>
            <div class="skills-list">
                {format_skills(skills)}
            </div>
        </div>
        
        <div class="resume-section">
            <h2>Professional Experience</h2>
            {format_experience(experience)}
        </div>
        
        <div class="resume-section">
            <h2>Education</h2>
            {format_education(education)}
        </div>
        
        <div class="resume-section">
            <h2>Key Achievements</h2>
            {format_achievements(achievements)}
        </div>
        
        <div class="resume-section">
            <h2>Projects</h2>
            {format_projects(projects)}
        </div>
    </div>
    """

def generate_professional_template(name, role, contact, objective, skills, experience, education, achievements, projects, color):
    return f"""
    <div class="resume-container professional-template" style="--theme-color: {color}">
        <div class="resume-header-pro">
            <div class="header-content">
                <h1>{name}</h1>
                <h3>{role}</h3>
            </div>
            <div class="contact-info-pro">{contact}</div>
        </div>
        
        <div class="two-column">
            <div class="left-column">
                <div class="resume-section">
                    <h2>Objective</h2>
                    <p>{objective}</p>
                </div>
                
                <div class="resume-section">
                    <h2>Skills</h2>
                    {format_skills_list(skills)}
                </div>
                
                <div class="resume-section">
                    <h2>Education</h2>
                    {format_education(education)}
                </div>
            </div>
            
            <div class="right-column">
                <div class="resume-section">
                    <h2>Experience</h2>
                    {format_experience(experience)}
                </div>
                
                <div class="resume-section">
                    <h2>Achievements</h2>
                    {format_achievements(achievements)}
                </div>
                
                <div class="resume-section">
                    <h2>Projects</h2>
                    {format_projects(projects)}
                </div>
            </div>
        </div>
    </div>
    """

def generate_creative_template(name, role, contact, objective, skills, experience, education, achievements, projects, color):
    return f"""
    <div class="resume-container creative-template" style="--theme-color: {color}">
        <div class="creative-header">
            <div class="name-section">
                <h1>{name}</h1>
                <div class="role-badge">{role}</div>
            </div>
            <div class="contact-creative">{contact}</div>
        </div>
        
        <div class="creative-grid">
            <div class="resume-section full-width">
                <h2>Career Objective</h2>
                <p>{objective}</p>
            </div>
            
            <div class="resume-section full-width">
                <h2>Core Skills</h2>
                {format_skills_creative(skills)}
            </div>
            
            <div class="resume-section full-width">
                <h2>Experience</h2>
                {format_experience(experience)}
            </div>
            
            <div class="resume-section">
                <h2>Education</h2>
                {format_education(education)}
            </div>
            
            <div class="resume-section">
                <h2>Achievements</h2>
                {format_achievements(achievements)}
            </div>
            
            <div class="resume-section full-width">
                <h2>Featured Projects</h2>
                {format_projects(projects)}
            </div>
        </div>
    </div>
    """

def generate_minimal_template(name, role, contact, objective, skills, experience, education, achievements, projects, color):
    return f"""
    <div class="resume-container minimal-template" style="--theme-color: {color}">
        <div class="minimal-header">
            <h1>{name}</h1>
            <p>{role} | {contact}</p>
        </div>
        
        <div class="resume-section">
            <h2>Objective</h2>
            <p>{objective}</p>
        </div>
        
        <div class="resume-section">
            <h2>Skills</h2>
            <p>{skills}</p>
        </div>
        
        <div class="resume-section">
            <h2>Experience</h2>
            {format_experience(experience)}
        </div>
        
        <div class="resume-section">
            <h2>Education</h2>
            {format_education(education)}
        </div>
        
        <div class="resume-section">
            <h2>Achievements</h2>
            {format_achievements(achievements)}
        </div>
        
        <div class="resume-section">
            <h2>Projects</h2>
            {format_projects(projects)}
        </div>
    </div>
    """

def format_skills(skills):
    skill_list = [s.strip() for s in skills.split(',')]
    html = '<ul class="skill-items">'
    for skill in skill_list:
        if skill:
            html += f'<li>{skill}</li>'
    html += '</ul>'
    return html

def format_skills_list(skills):
    skill_list = [s.strip() for s in skills.split(',')]
    html = '<ul class="skill-list-simple">'
    for skill in skill_list:
        if skill:
            html += f'<li>{skill}</li>'
    html += '</ul>'
    return html

def format_skills_creative(skills):
    skill_list = [s.strip() for s in skills.split(',')]
    html = '<div class="skill-tags">'
    for skill in skill_list:
        if skill:
            html += f'<span class="skill-tag">{skill}</span>'
    html += '</div>'
    return html

def format_experience(experience):
    exp_items = experience.split('\n')
    html = '<div class="experience-list">'
    for item in exp_items:
        if item.strip():
            html += f'<p>• {item.strip()}</p>'
    html += '</div>'
    return html

def format_education(education):
    edu_items = education.split('\n')
    html = '<div class="education-list">'
    for item in edu_items:
        if item.strip():
            html += f'<p>{item.strip()}</p>'
    html += '</div>'
    return html

def format_achievements(achievements):
    ach_items = achievements.split('\n')
    html = '<ul class="achievement-list">'
    for item in ach_items:
        if item.strip():
            html += f'<li>{item.strip()}</li>'
    html += '</ul>'
    return html

def format_projects(projects):
    proj_items = projects.split('\n')
    html = '<div class="project-list">'
    for item in proj_items:
        if item.strip():
            html += f'<p>• {item.strip()}</p>'
    html += '</div>'
    return html

QUESTION_BANK = {
    'hr': [
        'Tell me about yourself and your background.',
        'Why do you want to work for our company?',
        'What are your greatest strengths?',
        'What is your biggest weakness?',
        'Where do you see yourself in 5 years?',
        'Why should we hire you?',
        'Tell me about a time you faced a challenge at work.',
        'How do you handle stress and pressure?',
        'What motivates you?',
        'Describe your ideal work environment.'
    ],
    'technical': [
        'Explain your experience with the main technologies in your resume.',
        'Describe a complex technical problem you solved.',
        'How do you stay updated with new technologies?',
        'Walk me through your development process for a project.',
        'What testing strategies do you use?',
        'How do you handle technical debt?',
        'Explain a time you optimized performance.',
        'How do you approach debugging difficult issues?',
        'What version control practices do you follow?',
        'Describe your experience with Agile/Scrum.'
    ],
    'behavioral': [
        'Tell me about a time you worked in a team.',
        'Describe a situation where you had a conflict with a colleague.',
        'Give an example of when you showed leadership.',
        'Tell me about a time you failed and what you learned.',
        'How do you prioritize multiple tasks?',
        'Describe a time you had to meet a tight deadline.',
        'Tell me about a time you received criticism.',
        'Give an example of when you went above and beyond.',
        'Describe a time you had to learn something new quickly.',
        'Tell me about a time you disagreed with a decision.'
    ],
    'situational': [
        'What would you do if you disagreed with your manager?',
        'How would you handle an angry customer?',
        'What if you missed a critical deadline?',
        'How would you deal with a difficult team member?',
        'What if you found a bug in production?',
        'How would you handle multiple urgent requests?',
        'What if you had to work with outdated technology?',
        'How would you approach learning a new framework quickly?',
        'What if your project requirements changed suddenly?',
        'How would you handle working remotely with a distributed team?'
    ]
}

@app.route('/get-training-questions', methods=['GET'])
def get_training_questions():
    return jsonify({'questions': QUESTION_BANK})

@app.route('/practice-question', methods=['POST'])
def practice_question():
    data = request.json
    category = data.get('category', 'hr')
    
    questions = QUESTION_BANK.get(category, QUESTION_BANK['hr'])
    question = random.choice(questions)
    
    return jsonify({
        'question': question,
        'category': category,
        'tips': get_answer_tips(category)
    })

def get_answer_tips(category):
    tips = {
        'hr': [
            'Be honest and authentic',
            'Use specific examples from your experience',
            'Show enthusiasm and positive attitude',
            'Keep answers concise (1-2 minutes)'
        ],
        'technical': [
            'Explain your thought process clearly',
            'Use technical terms appropriately',
            'Mention trade-offs and alternatives',
            'Be ready to discuss implementation details'
        ],
        'behavioral': [
            'Use the STAR method (Situation, Task, Action, Result)',
            'Focus on your specific role and actions',
            'Quantify results when possible',
            'Show what you learned from the experience'
        ],
        'situational': [
            'Think through the problem systematically',
            'Consider multiple perspectives',
            'Explain your reasoning clearly',
            'Show problem-solving skills'
        ]
    }
    return tips.get(category, tips['hr'])

@app.route('/evaluate-practice-answer', methods=['POST'])
def evaluate_practice_answer():
    data = request.json
    answer = data.get('answer', '')
    category = data.get('category', 'hr')
    
    word_count = len(answer.split())
    feedback = {
        'length_score': evaluate_length(word_count),
        'detail_score': evaluate_detail(answer),
        'structure_score': evaluate_structure(answer, category),
        'overall_rating': '',
        'suggestions': []
    }
    avg_score = (feedback['length_score'] + feedback['detail_score'] + feedback['structure_score']) / 3
    
    if avg_score >= 8:
        feedback['overall_rating'] = 'Excellent'
        feedback['suggestions'].append('Great answer! You demonstrated strong understanding.')
    elif avg_score >= 6:
        feedback['overall_rating'] = 'Good'
        feedback['suggestions'].append('Solid answer. Consider adding more specific examples.')
    else:
        feedback['overall_rating'] = 'Needs Improvement'
        feedback['suggestions'].append('Try to provide more details and structure your answer better.')
    if word_count < 50:
        feedback['suggestions'].append('Your answer is quite brief. Aim for 50-150 words.')
    
    if category == 'behavioral' and 'situation' not in answer.lower():
        feedback['suggestions'].append('For behavioral questions, use the STAR method.')
    
    return jsonify(feedback)

def evaluate_length(word_count):
    if 50 <= word_count <= 150:
        return 10
    elif 30 <= word_count < 50 or 150 < word_count <= 200:
        return 7
    else:
        return 4

def evaluate_detail(answer):
    indicators = ['example', 'specifically', 'result', 'achieved', 'implemented', 'improved']
    count = sum(1 for word in indicators if word in answer.lower())
    return min(10, count * 2 + 4)

def evaluate_structure(answer, category):
    if category == 'behavioral':
        star_elements = ['situation', 'task', 'action', 'result']
        count = sum(1 for element in star_elements if element in answer.lower())
        return min(10, count * 2.5)
    else:
        sentences = answer.split('.')
        if 3 <= len(sentences) <= 6:
            return 10
        elif 2 <= len(sentences) < 3 or 6 < len(sentences) <= 8:
            return 7
        else:
            return 5

@app.route('/start-interview', methods=['POST'])
def start_interview():
    if 'resume' not in user_data:
        return jsonify({'error': 'Please generate resume first'}), 400
    
    role = user_data['resume'].get('role', 'Professional')
    
    questions = generate_questions(role, user_data['resume'])
    
    interview_state['questions'] = questions
    interview_state['current'] = 0
    interview_state['answers'] = []
    
    return jsonify({
        'question': questions[0],
        'question_number': 1,
        'total_questions': len(questions)
    })

def generate_questions(role, resume):
    skills = resume.get('skills', '')
    experience = resume.get('experience', '')
    questions = []
    
    hr_questions = random.sample(QUESTION_BANK['hr'], 2)
    for q in hr_questions:
        questions.append({'type': 'HR', 'question': q})
   
    tech_questions = random.sample(QUESTION_BANK['technical'], 3)
    for q in tech_questions:
        questions.append({'type': 'Technical', 'question': q})

    behavioral = random.choice(QUESTION_BANK['behavioral'])
    questions.append({'type': 'Behavioral', 'question': behavioral})
    
    situational = random.choice(QUESTION_BANK['situational'])
    questions.append({'type': 'Situational', 'question': situational})
    
    return questions

@app.route('/submit-answer', methods=['POST'])
def submit_answer():
    data = request.json
    answer = data.get('answer', '')
    
    if 'questions' not in interview_state:
        return jsonify({'error': 'Interview not started'}), 400
    
    current = interview_state['current']
    
    feedback = generate_feedback(answer, interview_state['questions'][current])
    
    interview_state['answers'].append({
        'question': interview_state['questions'][current],
        'answer': answer,
        'feedback': feedback
    })
    
    interview_state['current'] += 1
    
    if interview_state['current'] < len(interview_state['questions']):
        next_question = interview_state['questions'][interview_state['current']]
        return jsonify({
            'feedback': feedback,
            'next_question': next_question,
            'question_number': interview_state['current'] + 1,
            'total_questions': len(interview_state['questions']),
            'completed': False
        })
    else:
        return jsonify({
            'feedback': feedback,
            'completed': True,
            'summary': 'Interview completed! You answered all questions.'
        })

def generate_feedback(answer, question):
    word_count = len(answer.split())
    q_type = question['type'].lower()
    
    if q_type == 'behavioral':
        star_check = sum(1 for word in ['situation', 'task', 'action', 'result'] 
                        if word in answer.lower())
        if star_check >= 2 and word_count >= 60:
            return {
                'rating': 'Excellent',
                'comment': 'Great use of the STAR method! Your answer was well-structured and detailed.'
            }
        elif word_count >= 40:
            return {
                'rating': 'Good',
                'comment': 'Good answer! For behavioral questions, try using STAR format: Situation, Task, Action, Result.'
            }
        else:
            return {
                'rating': 'Needs Improvement',
                'comment': 'Your answer needs more detail. Use STAR method and provide specific examples.'
            }
    else:
        if word_count < 30:
            return {
                'rating': 'Needs Improvement',
                'comment': 'Your answer is too brief. Provide more details and examples.'
            }
        elif word_count < 60:
            return {
                'rating': 'Good',
                'comment': 'Good response! Consider adding more specific examples to strengthen your answer.'
            }
        else:
            return {
                'rating': 'Excellent',
                'comment': 'Excellent answer! You provided detailed information and demonstrated strong understanding.'
            }

@app.route('/get-summary', methods=['GET'])
def get_summary():
    if 'answers' not in interview_state:
        return jsonify({'error': 'No interview data'}), 400
    
    return jsonify({
        'answers': interview_state['answers'],
        'total': len(interview_state['answers'])
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
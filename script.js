const API_URL = 'http://localhost:5000';

let currentQuestionData = null;
let selectedTemplate = 'modern';
let currentPracticeCategory = '';

function showTab(tabName) {
    const tabs = document.querySelectorAll('.tab-content');
    const buttons = document.querySelectorAll('.tab-btn');
    
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });
    
    buttons.forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.getElementById(tabName + '-tab').classList.add('active');
    event.target.classList.add('active');
}

function selectTemplate(template) {
    selectedTemplate = template;
    document.getElementById('selected-template').value = template;
    
    
    const options = document.querySelectorAll('.template-option');
    options.forEach(opt => {
        opt.classList.remove('selected');
    });
    event.currentTarget.classList.add('selected');
}


document.getElementById('resume-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('name').value,
        role: document.getElementById('role').value,
        contact: document.getElementById('contact').value,
        skills: document.getElementById('skills').value,
        education: document.getElementById('education').value,
        experience: document.getElementById('experience').value,
        achievements: document.getElementById('achievements').value,
        projects: document.getElementById('projects').value,
        template: selectedTemplate
    };
    
    try {
        const response = await fetch(API_URL + '/generate-resume', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('resume-content').innerHTML = data.resume;
            document.getElementById('resume-output').style.display = 'block';

            document.getElementById('resume-output').scrollIntoView({ 
                behavior: 'smooth' 
            });
        }
    } catch (error) {
        alert('Error generating resume. Make sure the backend server is running on port 5000.');
        console.error('Error:', error);
    }
});

async function downloadResume() {
    const element = document.getElementById('resume-content');
    const userName = document.getElementById('name').value || 'Resume';
    const button = event.target;
    
    if (typeof html2canvas === 'undefined' || typeof jspdf === 'undefined') {
        alert('PDF library is still loading. Please wait a few seconds and try again.');
        console.error('Required libraries not loaded yet');
        return;
    }
    
    
    const originalText = button.textContent;
    button.textContent = 'Generating PDF...';
    button.disabled = true;
    
    try {
       
        const canvas = await html2canvas(element, {
            scale: 2,
            useCORS: true,
            logging: false,
            backgroundColor: '#ffffff'
        });
        
       
        const imgData = canvas.toDataURL('image/png');
        
       
        const { jsPDF } = jspdf;
        const pdf = new jsPDF({
            orientation: 'portrait',
            unit: 'mm',
            format: 'a4'
        });
        
        const imgWidth = 210; 
        const pageHeight = 297; 
        const imgHeight = (canvas.height * imgWidth) / canvas.width;
        let heightLeft = imgHeight;
        let position = 0;
         
        pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
        heightLeft -= pageHeight;
        
        while (heightLeft > 0) {
            position = heightLeft - imgHeight;
            pdf.addPage();
            pdf.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
            heightLeft -= pageHeight;
        }
        
      
        const filename = userName.replace(/\s+/g, '_') + '_Resume.pdf';
        pdf.save(filename);
        
        button.textContent = originalText;
        button.disabled = false;
        
    } catch (error) {
        console.error('PDF generation error:', error);
        alert('Error generating PDF. Using print dialog instead...');
        window.print();
        button.textContent = originalText;
        button.disabled = false;
    }
}


async function practiceCategory(category) {
    currentPracticeCategory = category;
    
    document.getElementById('practice-area').style.display = 'block';
    
    const categoryTitles = {
        'hr': 'HR Questions Practice',
        'technical': 'Technical Questions Practice',
        'behavioral': 'Behavioral Questions Practice',
        'situational': 'Situational Questions Practice'
    };
    
    document.getElementById('practice-category-title').textContent = categoryTitles[category];
    
    await loadPracticeQuestion(category);
}

async function loadPracticeQuestion(category) {
    try {
        const response = await fetch(API_URL + '/practice-question', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ category: category })
        });
        
        const data = await response.json();
        
        document.getElementById('practice-question').textContent = data.question;
        document.getElementById('practice-answer').value = '';
        document.getElementById('practice-feedback').style.display = 'none';
        
        const tipsList = document.getElementById('answer-tips');
        tipsList.innerHTML = '';
        data.tips.forEach(tip => {
            const li = document.createElement('li');
            li.textContent = tip;
            tipsList.appendChild(li);
        });
        
    } catch (error) {
        alert('Error loading question. Make sure the backend server is running.');
        console.error('Error:', error);
    }
}

function newPracticeQuestion() {
    loadPracticeQuestion(currentPracticeCategory);
}


document.addEventListener('DOMContentLoaded', function() {
    const practiceAnswer = document.getElementById('practice-answer');
    if (practiceAnswer) {
        practiceAnswer.addEventListener('input', function() {
            const words = this.value.trim().split(/\s+/).filter(word => word.length > 0);
            document.getElementById('word-count').textContent = words.length + ' words';
        });
    }
});

async function evaluatePracticeAnswer() {
    const answer = document.getElementById('practice-answer').value.trim();
    
    if (!answer) {
        alert('Please provide an answer before getting feedback!');
        return;
    }
    
    try {
        const response = await fetch(API_URL + '/evaluate-practice-answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                answer: answer,
                category: currentPracticeCategory
            })
        });
        
        const data = await response.json();
        
      
        document.getElementById('length-score').textContent = data.length_score + '/10';
        document.getElementById('detail-score').textContent = data.detail_score + '/10';
        document.getElementById('structure-score').textContent = data.structure_score + '/10';
        document.getElementById('practice-rating').textContent = data.overall_rating;
        
     
        const suggestionsList = document.getElementById('practice-suggestions');
        suggestionsList.innerHTML = '';
        data.suggestions.forEach(suggestion => {
            const li = document.createElement('li');
            li.textContent = suggestion;
            suggestionsList.appendChild(li);
        });
        
        document.getElementById('practice-feedback').style.display = 'block';
        
        
        document.getElementById('practice-feedback').scrollIntoView({ 
            behavior: 'smooth' 
        });
        
    } catch (error) {
        alert('Error evaluating answer. Make sure the backend server is running.');
        console.error('Error:', error);
    }
}

async function startInterview() {
    try {
        const response = await fetch(API_URL + '/start-interview', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.error) {
            alert('Please generate a resume first before starting the interview!');
            return;
        }
        
        currentQuestionData = data;
        
        document.getElementById('interview-start').style.display = 'none';
        document.getElementById('interview-active').style.display = 'block';
        
        displayQuestion(data);
        
    } catch (error) {
        alert('Error starting interview. Make sure the backend server is running.');
        console.error('Error:', error);
    }
}


function displayQuestion(data) {
    document.getElementById('question-counter').textContent = 
        `Question ${data.question_number} of ${data.total_questions}`;
    
    document.getElementById('question-type').textContent = data.question.type;
    document.getElementById('current-question').textContent = data.question.question;
    
    document.getElementById('answer-input').value = '';
    document.getElementById('feedback-box').style.display = 'none';
}


async function submitAnswer() {
    const answer = document.getElementById('answer-input').value.trim();
    
    if (!answer) {
        alert('Please provide an answer before submitting!');
        return;
    }
    
    try {
        const response = await fetch(API_URL + '/submit-answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ answer: answer })
        });
        
        const data = await response.json();
        
    
        document.getElementById('feedback-rating').textContent = data.feedback.rating;
        document.getElementById('feedback-comment').textContent = data.feedback.comment;
        document.getElementById('feedback-box').style.display = 'block';
        
        if (!data.completed) {
            currentQuestionData = {
                question: data.next_question,
                question_number: data.question_number,
                total_questions: data.total_questions
            };
        } else {
            
            setTimeout(() => {
                showInterviewComplete();
            }, 2000);
        }
        
    } catch (error) {
        alert('Error submitting answer.');
        console.error('Error:', error);
    }
}


function nextQuestion() {
    if (currentQuestionData) {
        displayQuestion(currentQuestionData);
    }
}


async function showInterviewComplete() {
    document.getElementById('interview-active').style.display = 'none';
    document.getElementById('interview-complete').style.display = 'block';
    
    try {
        const response = await fetch(API_URL + '/get-summary');
        const data = await response.json();
        
        let summaryHTML = '<h3>Your Performance Summary</h3>';
        
        data.answers.forEach((item, index) => {
            summaryHTML += `
                <div class="summary-item">
                    <h4>Question ${index + 1}: ${item.question.type}</h4>
                    <p><strong>Q:</strong> ${item.question.question}</p>
                    <p><strong>Your Answer:</strong> ${item.answer.substring(0, 100)}...</p>
                    <span class="rating">${item.feedback.rating}</span>
                    <p>${item.feedback.comment}</p>
                </div>
            `;
        });
        
        document.getElementById('interview-summary').innerHTML = summaryHTML;
        
    } catch (error) {
        console.error('Error fetching summary:', error);
    }
}

function restartInterview() {
    document.getElementById('interview-complete').style.display = 'none';
    document.getElementById('interview-start').style.display = 'block';
    currentQuestionData = null;
}
document.addEventListener('DOMContentLoaded', function() {
    const firstTemplate = document.querySelector('.template-option');
    if (firstTemplate) {
        firstTemplate.classList.add('selected');
    }
});

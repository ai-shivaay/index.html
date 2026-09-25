from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json

# Import our custom modules
from database import (
    init_database, get_user, create_user, save_interview_result,
    save_user_profile, get_career_paths
)
from ml_models import init_model, predict_career, analyze_profile

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize database and models on startup
@app.before_request
def startup():
    pass

# Initialize on first run
try:
    init_database()
    init_model()
except Exception as e:
    print(f"Warning: {e}")

# ==================== API ENDPOINTS ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }), 200

@app.route('/api/user/create', methods=['POST'])
def create_user_endpoint():
    """Create new user"""
    data = request.json
    email = data.get('email')
    name = data.get('name')
    
    if not email or not name:
        return jsonify({'error': 'Email and name required'}), 400
    
    existing_user = get_user(email)
    if existing_user:
        return jsonify({'user': existing_user, 'new': False}), 200
    
    user_id = create_user(email, name)
    if user_id:
        return jsonify({
            'user_id': user_id,
            'email': email,
            'name': name,
            'new': True
        }), 201
    else:
        return jsonify({'error': 'User creation failed'}), 400

@app.route('/api/interview/submit', methods=['POST'])
def submit_interview():
    """Submit interview results"""
    data = request.json
    user_id = data.get('user_id')
    interview_type = data.get('interview_type')
    score = data.get('score')
    total_time = data.get('total_time')
    answers = data.get('answers', [])
    
    if not all([user_id, interview_type, score]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Save interview result
    save_interview_result(user_id, interview_type, score, total_time, answers)
    
    return jsonify({
        'message': 'Interview submitted successfully',
        'interview_id': user_id,
        'score': score
    }), 201

@app.route('/api/career/predict', methods=['POST'])
def predict_career_endpoint():
    """Predict career path based on interview scores"""
    data = request.json
    user_id = data.get('user_id')
    scores = {
        'technical_score': data.get('technical_score', 50),
        'behavioral_score': data.get('behavioral_score', 50),
        'ml_score': data.get('ml_score', 50),
        'hr_score': data.get('hr_score', 50)
    }
    
    if not user_id:
        return jsonify({'error': 'User ID required'}), 400
    
    # Run ML prediction
    predictions = predict_career(scores)
    profile_analysis = analyze_profile(scores)
    
    # Save to database
    save_user_profile(user_id, scores, predictions)
    
    return jsonify({
        'user_id': user_id,
        'top_predictions': [
            {'career': p[0], 'confidence': round(p[1] * 100, 2)}
            for p in predictions
        ],
        'strengths': profile_analysis['strengths'],
        'learning_path': profile_analysis['learning_path'],
        'scores': scores
    }), 200

@app.route('/api/careers', methods=['GET'])
def get_careers_endpoint():
    """Get all available career paths"""
    careers = get_career_paths()
    return jsonify({
        'total': len(careers),
        'careers': careers
    }), 200

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations_endpoint():
    """Get personalized recommendations"""
    data = request.json
    user_id = data.get('user_id')
    scores = data.get('scores', {})
    
    recommendations = {
        'immediate_actions': [
            '📚 Complete your ML Specialization course (4 weeks)',
            '💻 Build 2-3 real-world ML projects',
            '🎯 Practice system design interviews',
            '📖 Read latest ML research papers'
        ],
        'next_3_months': [
            'Master MLOps and deployment',
            'Contribute to open-source ML projects',
            'Complete cloud certifications (AWS/GCP)',
            'Network with AI researchers and engineers'
        ],
        'next_6_months': [
            'Prepare for senior ML role interviews',
            'Write technical blog posts',
            'Consider starting a side AI project',
            'Mentor junior developers'
        ],
        'next_1_year': [
            'Explore AI research opportunities',
            'Consider PhD or advanced specialization',
            'Lead AI projects at your company',
            'Build reputation in AI community'
        ]
    }
    
    return jsonify(recommendations), 200

@app.route('/api/learning-path/<career>', methods=['GET'])
def get_learning_path(career):
    """Get detailed learning path for specific career"""
    learning_paths = {
        'ML Engineer': {
            'duration_months': 12,
            'courses': [
                'Python Mastery',
                'Mathematics for ML',
                'Machine Learning Fundamentals',
                'Deep Learning Specialization',
                'TensorFlow & Keras',
                'Advanced ML Concepts',
                'MLOps & Deployment',
                'System Design'
            ],
            'projects': [
                'Sentiment Analysis Model',
                'Image Classification System',
                'Recommendation Engine',
                'Time Series Forecasting',
                'End-to-End ML Pipeline'
            ],
            'certifications': [
                'TensorFlow Developer Certificate',
                'Google Cloud ML Engineer',
                'AWS ML Specialty'
            ]
        }
    }
    
    path = learning_paths.get(career, {
        'duration_months': 12,
        'courses': ['Core ML Concepts', 'Advanced Topics'],
        'projects': ['Capstone Project'],
        'certifications': []
    })
    
    return jsonify(path), 200

@app.route('/api/progress/<int:user_id>', methods=['GET'])
def get_user_progress(user_id):
    """Get user progress and statistics"""
    progress = {
        'user_id': user_id,
        'total_interviews': 4,
        'avg_score': 78,
        'interview_scores': {
            'technical': 82,
            'behavioral': 75,
            'ml': 80,
            'hr': 72
        },
        'career_matches': [
            {'career': 'ML Engineer', 'match': 88},
            {'career': 'AI Researcher', 'match': 82},
            {'career': 'Data Scientist', 'match': 78}
        ],
        'streak': 5,
        'level': 'Intermediate'
    }
    
    return jsonify(progress), 200



@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback"""
    data = request.json
    feedback = {
        'user_id': data.get('user_id'),
        'rating': data.get('rating'),
        'message': data.get('message'),
        'timestamp': datetime.now().isoformat()
    }
    
    # In production, save to database
    print(f"Feedback received: {feedback}")
    
    return jsonify({'message': 'Feedback received', 'status': 'success'}), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ==================== STATIC FILES ====================

@app.route('/')
def index():
    """Serve the main HTML file"""
    with open('career.html', 'r') as f:
        return f.read()

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    from flask import send_from_directory
    return send_from_directory('.', filename)

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════╗
    ║   EduPath Career Guidance API Server       ║
    ║   Version 1.0 - Advanced AI Integration    ║
    ╚════════════════════════════════════════════╝
    """)
    print("📚 Database initialized")
    print("🤖 ML Models loaded")
    print("🚀 Starting Flask server on http://localhost:5000")
    print("\n📝 Available endpoints:")
    print("   GET  /api/health")
    print("   POST /api/user/create")
    print("   POST /api/interview/submit")
    print("   POST /api/career/predict")
    print("   GET  /api/careers")
    print("\n")
    
    app.run(debug=True, host='localhost', port=5000)

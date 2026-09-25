import sqlite3
import os
from datetime import datetime

DATABASE_PATH = 'career_guidance.db'

def init_database():
    """Initialize SQLite database with required tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Interview results table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interview_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            interview_type TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_time INTEGER,
            answers TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Career paths table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS career_paths (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            avg_salary INTEGER,
            demand_level TEXT,
            required_skills TEXT,
            learning_time_months INTEGER
        )
    ''')
    
    # User profiles table (for ML analysis)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            technical_score REAL,
            behavioral_score REAL,
            ml_score REAL,
            hr_score REAL,
            predicted_career_1 TEXT,
            predicted_career_2 TEXT,
            predicted_career_3 TEXT,
            confidence_scores TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Skill assessments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skill_assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            skill_name TEXT NOT NULL,
            proficiency_level TEXT,
            score REAL,
            last_assessed TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Career recommendations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            career_path TEXT NOT NULL,
            match_percentage REAL,
            reasoning TEXT,
            next_steps TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Populate career paths
    career_data = [
        ('ML Engineer', 'Develops machine learning models and systems', 180000, 'Very High', 'Python,ML,Math,Cloud', 12),
        ('Data Scientist', 'Analyzes data and builds predictive models', 140000, 'High', 'Python,SQL,Statistics,ML', 12),
        ('AI Researcher', 'Conducts research in AI and deep learning', 160000, 'High', 'Python,Math,Research,ML', 18),
        ('NLP Specialist', 'Works with natural language processing', 150000, 'High', 'Python,NLP,ML,Linguistics', 12),
        ('AI Architect', 'Designs AI-powered systems at scale', 200000, 'High', 'System Design,Cloud,ML,Leadership', 24),
        ('Data Engineer', 'Builds data pipelines and infrastructure', 160000, 'High', 'Python,SQL,Cloud,Big Data', 12),
        ('AI Ethics Officer', 'Ensures responsible AI development', 130000, 'Medium', 'AI,Ethics,Policy,Communication', 9),
        ('Product Manager', 'Manages AI-powered products', 170000, 'High', 'Leadership,Communication,AI', 12),
    ]
    
    cursor.execute('SELECT COUNT(*) FROM career_paths')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
            INSERT INTO career_paths 
            (name, description, avg_salary, demand_level, required_skills, learning_time_months) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', career_data)
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

def get_user(email):
    """Get user by email"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def create_user(email, name):
    """Create new user"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (email, name) VALUES (?, ?)', (email, name))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def save_interview_result(user_id, interview_type, score, total_time, answers):
    """Save interview results"""
    import json
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO interview_results 
        (user_id, interview_type, score, total_time, answers) 
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, interview_type, score, total_time, json.dumps(answers)))
    conn.commit()
    conn.close()

def save_user_profile(user_id, scores, predictions):
    """Save user profile with ML predictions"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    import json
    cursor.execute('''
        INSERT INTO user_profiles 
        (user_id, technical_score, behavioral_score, ml_score, hr_score, 
         predicted_career_1, predicted_career_2, predicted_career_3, confidence_scores) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id,
          scores.get('technical_score'),
          scores.get('behavioral_score'),
          scores.get('ml_score'),
          scores.get('hr_score'),
          predictions[0][0],
          predictions[1][0],
          predictions[2][0],
          json.dumps([p[1] for p in predictions])))
    conn.commit()
    conn.close()

def get_career_paths():
    """Get all career paths"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM career_paths')
    careers = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return careers

if __name__ == '__main__':
    init_database()

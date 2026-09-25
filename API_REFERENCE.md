# 📡 API Reference - EduPath Backend

## Base URL
```
http://localhost:5000
```

---

## Authentication
Currently, no authentication required. Future versions will include JWT tokens.

---

## 1. Health Check Endpoint

### GET /api/health
**Purpose:** Verify server is running and healthy

**No authentication required**

**Request:**
```bash
curl http://localhost:5000/api/health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2024-02-14T10:30:00Z",
  "version": "1.0.0",
  "components": {
    "database": "connected",
    "ml_models": "loaded"
  }
}
```

---

## 2. User Management

### POST /api/user/create
**Purpose:** Create or retrieve user account

**No authentication required**

**Request Body:**
```json
{
  "email": "student@example.com",
  "name": "John Doe"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/api/user/create \
  -H "Content-Type: application/json" \
  -d '{"email":"student@example.com","name":"John Doe"}'
```

**Response (200/201 OK):**
```json
{
  "user_id": 1,
  "email": "student@example.com",
  "name": "John Doe",
  "new": true,
  "created_at": "2024-02-14T10:30:00Z"
}
```

**Error Response (400):**
```json
{
  "error": "Email is required",
  "code": "INVALID_REQUEST",
  "status": 400
}
```

**Fields:**
- `email` (required): Valid email address
- `name` (required): User's full name

---

## 3. Interview Management

### POST /api/interview/submit
**Purpose:** Submit completed interview with answers and scores

**No authentication required (include user_id in body)**

**Request Body:**
```json
{
  "user_id": 1,
  "interview_type": "technical",
  "score": 82,
  "total_time": 1200,
  "answers": [
    {
      "question": "What is machine learning?",
      "answer": "Machine learning is ...",
      "time_taken": 120,
      "word_count": 85
    }
  ]
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/api/interview/submit \
  -H "Content-Type: application/json" \
  -d '{
    "user_id":1,
    "interview_type":"technical",
    "score":82,
    "total_time":1200,
    "answers":[]
  }'
```

**Response (201 CREATED):**
```json
{
  "success": true,
  "interview_id": 5,
  "user_id": 1,
  "interview_type": "technical",
  "score": 82,
  "saved_at": "2024-02-14T10:35:00Z"
}
```

**Fields:**
- `user_id` (required): User ID from /api/user/create
- `interview_type` (required): "technical", "behavioral", "hr", or "ml"
- `score` (required): Interview score 0-100
- `total_time` (required): Total time in seconds
- `answers` (optional): Array of answer objects

---

## 4. Career Prediction

### POST /api/career/predict
**Purpose:** Get ML-based career predictions based on interview scores

**No authentication required**

**Request Body:**
```json
{
  "user_id": 1,
  "technical_score": 82,
  "behavioral_score": 75,
  "ml_score": 80,
  "hr_score": 72
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/api/career/predict \
  -H "Content-Type: application/json" \
  -d '{
    "user_id":1,
    "technical_score":82,
    "behavioral_score":75,
    "ml_score":80,
    "hr_score":72
  }'
```

**Response (200 OK):**
```json
{
  "user_id": 1,
  "top_predictions": [
    {
      "career": "ML Engineer",
      "confidence": 88.5,
      "avg_salary": "$180,000",
      "demand_level": "Very High"
    },
    {
      "career": "Data Scientist",
      "confidence": 84.2,
      "avg_salary": "$165,000",
      "demand_level": "Very High"
    },
    {
      "career": "AI Researcher",
      "confidence": 79.8,
      "avg_salary": "$175,000",
      "demand_level": "High"
    }
  ],
  "strengths": [
    "Strong technical foundation",
    "Excellent ML knowledge",
    "Good behavioral skills"
  ],
  "learning_path": [
    "Advanced Deep Learning",
    "Distributed Computing",
    "MLOps and Production"
  ],
  "scores": {
    "technical_score": 82,
    "behavioral_score": 75,
    "ml_score": 80,
    "hr_score": 72
  },
  "predicted_at": "2024-02-14T10:40:00Z"
}
```

**Fields Required:**
- `user_id`: Existing user ID
- `technical_score`: 0-100
- `behavioral_score`: 0-100
- `ml_score`: 0-100
- `hr_score`: 0-100

**Scoring Guide:**
- 90-100: Outstanding
- 80-90: Excellent
- 70-80: Good
- 60-70: Average
- <60: Needs Improvement

---

## 5. Career Paths

### GET /api/careers
**Purpose:** Get all available career paths with details

**No parameters required**

**Request:**
```bash
curl http://localhost:5000/api/careers
```

**Response (200 OK):**
```json
{
  "total": 8,
  "careers": [
    {
      "id": 1,
      "name": "ML Engineer",
      "description": "Builds and deploys machine learning models...",
      "avg_salary": "$180,000",
      "demand_level": "Very High",
      "required_skills": ["Python", "PyTorch", "TensorFlow", "MLOps"],
      "learning_time_months": 12
    },
    {
      "id": 2,
      "name": "Data Scientist",
      "description": "Analyzes complex data to drive business insights...",
      "avg_salary": "$165,000",
      "demand_level": "Very High",
      "required_skills": ["Python", "SQL", "Statistics", "ML"],
      "learning_time_months": 10
    }
  ],
  "retrieved_at": "2024-02-14T10:45:00Z"
}
```

**Available Careers:**
1. ML Engineer
2. Data Scientist
3. AI Researcher
4. NLP Specialist
5. AI Architect
6. Data Engineer
7. AI Ethics Officer
8. Product Manager

---

## 6. Recommendations

### POST /api/recommendations
**Purpose:** Get 4-tier recommendations for career development

**No authentication required**

**Request Body:**
```json
{
  "user_id": 1,
  "career_preference": "ML Engineer"
}
```

**Response (200 OK):**
```json
{
  "user_id": 1,
  "career": "ML Engineer",
  "recommendations": {
    "immediate": [
      "Start Andrew Ng's Deep Learning Specialization",
      "Practice coding ML algorithms from scratch",
      "Join Kaggle competitions"
    ],
    "3_months": [
      "Build 2-3 portfolio projects",
      "Learn MLOps basics",
      "Study system design for ML"
    ],
    "6_months": [
      "Complete advanced ML courses",
      "Contribute to open-source ML projects",
      "Practice technical interviews"
    ],
    "1_year": [
      "Build production ML system",
      "Prepare for senior roles",
      "Mentor junior developers"
    ]
  },
  "generated_at": "2024-02-14T10:50:00Z"
}
```

---

## 7. Learning Paths

### GET /api/learning-path/{career}
**Purpose:** Get detailed learning path for specific career

**URL Prefix:** `/api/learning-path/`

**Request:**
```bash
curl http://localhost:5000/api/learning-path/ML%20Engineer
```

**Response (200 OK):**
```json
{
  "career": "ML Engineer",
  "overview": "Comprehensive path to becoming an ML Engineer",
  "duration_months": 12,
  "difficulty": "Intermediate to Advanced",
  "prerequisites": [
    "Python basics",
    "Linear algebra fundamentals",
    "Statistics basics"
  ],
  "courses": [
    {
      "level": 1,
      "name": "Machine Learning Fundamentals",
      "provider": "Coursera",
      "duration_weeks": 4,
      "skills": ["ML Basics", "Algorithms", "Evaluation Metrics"]
    },
    {
      "level": 2,
      "name": "Deep Learning Specialization",
      "provider": "Coursera",
      "duration_weeks": 8,
      "skills": ["Neural Networks", "CNN", "RNN"]
    }
  ],
  "projects": [
    {
      "name": "House Price Prediction",
      "description": "Build regression model",
      "skills_used": ["Pandas", "Scikit-learn"],
      "difficulty": "Easy"
    },
    {
      "name": "Image Classification",
      "description": "CNN with PyTorch",
      "skills_used": ["PyTorch", "CNN", "Transfer Learning"],
      "difficulty": "Medium"
    }
  ],
  "certifications": [
    "Google Cloud Professional Data Engineer",
    "AWS ML Specialty"
  ]
}
```

---

## 8. User Progress

### GET /api/progress/{user_id}
**Purpose:** Get user's progress dashboard

**Request:**
```bash
curl http://localhost:5000/api/progress/1
```

**Response (200 OK):**
```json
{
  "user_id": 1,
  "user_name": "John Doe",
  "dashboard": {
    "interviews_completed": 3,
    "average_score": 79.3,
    "preferred_career": "ML Engineer",
    "profile": {
      "technical_score": 82,
      "behavioral_score": 75,
      "ml_score": 80,
      "hr_score": 72
    },
    "interview_history": [
      {
        "interview_type": "technical",
        "score": 82,
        "date": "2024-02-12",
        "duration_minutes": 20
      },
      {
        "interview_type": "ml",
        "score": 80,
        "date": "2024-02-13",
        "duration_minutes": 22
      }
    ],
    "predicted_careers": [
      "ML Engineer",
      "Data Scientist",
      "AI Researcher"
    ],
    "next_recommendations": [
      "Complete behavioral interview",
      "Join online ML community",
      "Start portfolio project"
    ]
  },
  "progress_percentage": 60
}
```

---

## 9. Market Analytics

### GET /api/analytics/trends
**Purpose:** Get market trends and job forecasts

**Request:**
```bash
curl http://localhost:5000/api/analytics/trends
```

**Response (200 OK):**
```json
{
  "report_date": "2024-02-14",
  "trends": {
    "job_growth": {
      "ml_engineer": "25% YoY",
      "data_scientist": "22% YoY",
      "ai_researcher": "18% YoY",
      "nlp_specialist": "28% YoY"
    },
    "salary_trends": {
      "ml_engineer": {
        "entry_level": "$120,000-$140,000",
        "mid_level": "$160,000-$200,000",
        "senior": "$200,000-$300,000"
      },
      "data_scientist": {
        "entry_level": "$100,000-$120,000",
        "mid_level": "$140,000-$180,000",
        "senior": "$180,000-$250,000"
      }
    },
    "in_demand_skills": [
      "Large Language Models",
      "Prompt Engineering",
      "Cloud ML Platforms",
      "MLOps/DevOps",
      "Transformers",
      "Distributed Computing",
      "Data Engineering",
      "System Design"
    ],
    "top_companies": [
      "Google",
      "Meta",
      "OpenAI",
      "Microsoft",
      "Amazon",
      "Apple",
      "NVIDIA",
      "Anthropic"
    ]
  },
  "forecast_period": "2024-2025"
}
```

---

## 10. Feedback Submission

### POST /api/feedback
**Purpose:** Submit user feedback or ratings

**Request Body:**
```json
{
  "user_id": 1,
  "rating": 4.5,
  "feedback": "Great platform! Very helpful interview simulator.",
  "category": "interview",
  "improvements": ["Add more question variety", "Include AI explanations"]
}
```

**Response (201 CREATED):**
```json
{
  "feedback_id": 123,
  "user_id": 1,
  "status": "received",
  "timestamp": "2024-02-14T10:55:00Z",
  "message": "Thank you for your feedback!"
}
```

---

## 11. Static Files

### GET /
**Purpose:** Serve main HTML and static files

**Request:**
```bash
curl http://localhost:5000/
```

**Response:**
- Serves career.html as main page
- Access static CSS/JS files

---

## HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Successful GET/POST request |
| 201 | Created | New user/interview created |
| 400 | Bad Request | Missing required fields |
| 404 | Not Found | User/career not found |
| 500 | Server Error | Internal server error |

---

## Error Response Handling

**Standard Error Format:**
```json
{
  "error": "Invalid interview type",
  "code": "INVALID_REQUEST",
  "status": 400,
  "details": {
    "field": "interview_type",
    "provided": "invalid",
    "valid_options": ["technical", "behavioral", "hr", "ml"]
  }
}
```

---

## Rate Limiting

Currently: No rate limiting
Future: 100 requests/minute per IP

---

## API Response Headers

```
Content-Type: application/json
Access-Control-Allow-Origin: *
X-API-Version: 1.0.0
X-Request-ID: unique-request-id
```

---

## Testing Examples

### Test 1: Complete User Journey
```bash
# 1. Create user
curl -X POST http://localhost:5000/api/user/create \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","name":"Test User"}'

# 2. Submit interview (use user_id from step 1)
curl -X POST http://localhost:5000/api/interview/submit \
  -H "Content-Type: application/json" \
  -d '{
    "user_id":1,
    "interview_type":"technical",
    "score":85,
    "total_time":1200,
    "answers":[]
  }'

# 3. Predict career
curl -X POST http://localhost:5000/api/career/predict \
  -H "Content-Type: application/json" \
  -d '{
    "user_id":1,
    "technical_score":85,
    "behavioral_score":80,
    "ml_score":82,
    "hr_score":78
  }'

# 4. Get progress
curl http://localhost:5000/api/progress/1
```

---

## Documentation Version

- **API Version:** 1.0.0
- **Last Updated:** February 14, 2024
- **Status:** Production Ready

---

**For more help, see README.md or QUICKSTART.md**

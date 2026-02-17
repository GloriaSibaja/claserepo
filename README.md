# Employee Wellbeing & Security Analytics Platform

A comprehensive AI-powered system for predicting employee stress levels, calculating burnout scores, assessing phishing vulnerability, and generating executive insights.

## 🎯 Features

1. **RandomForest Model** - Predicts employee stress levels based on work metrics
2. **Burnout Score Engine** - Mathematical calculation of burnout risk across multiple dimensions
3. **Phishing Vulnerability Index** - Risk assessment for security vulnerabilities
4. **LLM Executive Summaries** - AI-generated personalized explanations and recommendations
5. **Professional Dashboard** - Interactive web interface with real-time analytics

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Train the model (first time only)
python stress_predictor.py

# Start the web application
python app.py
```

The dashboard will be available at `http://localhost:5000`

## 📊 System Components

### 1. Stress Level Predictor (RandomForest)
- **File**: `stress_predictor.py`
- **Model**: RandomForest Classifier with 100 estimators
- **Features**: Work hours, sleep, meetings, emails, deadline pressure, task complexity, team support, work-life balance
- **Output**: Stress level (Low/Medium/High/Critical) with confidence scores

### 2. Burnout Engine (Mathematical)
- **File**: `burnout_engine.py`
- **Components**:
  - Emotional Exhaustion (35%)
  - Depersonalization (25%)
  - Personal Accomplishment (20%)
  - Work Overload (20%)
- **Output**: Burnout score 0-100 with risk categorization

### 3. Phishing Risk Engine
- **File**: `phishing_risk.py`
- **Factors**:
  - Stress level contribution (25%)
  - Burnout score contribution (30%)
  - Cognitive load (25%)
  - Awareness level (20%)
- **Output**: Vulnerability index with attack success probability

### 4. LLM Explainer
- **File**: `llm_explainer.py`
- **Modes**: OpenAI GPT (if API key provided) or template-based
- **Output**: Personalized executive summary with recommendations

### 5. Web Dashboard
- **File**: `app.py` (Flask backend)
- **Templates**: `templates/dashboard.html`
- **Features**:
  - Interactive data input forms
  - Real-time risk analysis
  - Visualizations with Plotly
  - Executive summaries

## 🔧 Configuration

### Optional: OpenAI API
To enable AI-powered explanations:

1. Copy `.env.example` to `.env`
2. Add your OpenAI API key
3. System will automatically use GPT for summaries

Without API key, the system uses high-quality template-based explanations.

## 📈 Usage Example

```python
from stress_predictor import StressLevelPredictor
from burnout_engine import BurnoutEngine
from phishing_risk import PhishingRiskEngine

# Initialize engines
predictor = StressLevelPredictor()
burnout_engine = BurnoutEngine()
phishing_engine = PhishingRiskEngine()

# Employee data
data = {
    'work_hours_per_week': 50,
    'sleep_hours_per_day': 6,
    'meetings_per_week': 20,
    'emails_per_day': 100,
    'deadline_pressure': 8,
    'task_complexity': 7,
    'team_support': 5,
    'work_life_balance': 4
}

# Run analysis
stress = predictor.predict(data)
burnout = burnout_engine.calculate_burnout_score({**data, 'stress_level': stress['stress_level']})
phishing = phishing_engine.calculate_vulnerability_index(data, stress, burnout)

print(f"Stress: {stress['stress_level']}")
print(f"Burnout: {burnout['total_score']}/100")
print(f"Phishing Risk: {phishing['vulnerability_index']}/100")
```

## 🧪 Testing Individual Components

```bash
# Test stress predictor
python stress_predictor.py

# Test burnout engine
python burnout_engine.py

# Test phishing risk
python phishing_risk.py

# Test LLM explainer
python llm_explainer.py
```

## 📁 Project Structure

```
claserepo/
├── app.py                    # Flask web application
├── stress_predictor.py       # RandomForest ML model
├── burnout_engine.py         # Mathematical burnout calculator
├── phishing_risk.py          # Security risk engine
├── llm_explainer.py          # AI explanation generator
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── models/                  # Trained ML models (auto-generated)
├── templates/
│   └── dashboard.html       # Web dashboard UI
├── static/
│   ├── css/
│   │   └── dashboard.css    # Dashboard styling
│   └── js/
│       └── dashboard.js     # Dashboard interactivity
└── data/                    # Data storage (optional)
```

## 🛡️ Security & Privacy

- All analysis is performed locally
- No employee data is stored or transmitted (except OpenAI API if enabled)
- API keys should be kept secure in `.env` file
- `.env` is excluded from git via `.gitignore`

## 📊 Metrics Interpretation

### Stress Levels
- **Low**: Healthy stress levels, normal productivity
- **Medium**: Elevated stress, monitor situation
- **High**: Concerning stress levels, intervention recommended
- **Critical**: Severe stress, immediate action required

### Burnout Score
- **0-30**: Low risk, healthy state
- **30-50**: Moderate risk, preventive measures
- **50-70**: High risk, active intervention needed
- **70-100**: Critical risk, urgent support required

### Phishing Vulnerability
- **0-30**: Low vulnerability, good security awareness
- **30-50**: Moderate vulnerability, schedule training
- **50-70**: High vulnerability, immediate training needed
- **70-100**: Critical vulnerability, urgent intervention

## 🤝 Contributing

This is a demonstration project showcasing integrated ML, mathematical engines, and LLM capabilities.

## 📄 License

Educational/Demonstration Project

---

**Built with**: Python, Flask, Scikit-learn, Plotly, OpenAI API
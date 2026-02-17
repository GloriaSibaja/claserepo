"""
Module 5: Professional Dashboard Frontend
Flask web application with comprehensive analytics dashboard
"""
from flask import Flask, render_template, request, jsonify
import json
from stress_predictor import StressLevelPredictor
from burnout_engine import BurnoutEngine
from phishing_risk import PhishingRiskEngine
from llm_explainer import LLMExplainer

app = Flask(__name__)

# Initialize all engines
stress_predictor = StressLevelPredictor()
burnout_engine = BurnoutEngine()
phishing_engine = PhishingRiskEngine()
llm_explainer = LLMExplainer(dataset_file='employee_dataset.csv')

# Train model if not exists
try:
    stress_predictor.load_model()
    print("✓ Model loaded successfully")
except:
    print("Training new model...")
    accuracy = stress_predictor.train()
    print(f"✓ Model trained with {accuracy:.1%} accuracy")


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    Main analysis endpoint
    Processes employee data through all engines
    """
    try:
        data = request.json
        
        # Extract employee info
        employee_name = data.get('employee_name', 'Employee')
        
        # Prepare features for stress prediction
        stress_features = {
            'work_hours_per_week': float(data.get('work_hours_per_week', 40)),
            'sleep_hours_per_day': float(data.get('sleep_hours_per_day', 7)),
            'meetings_per_week': int(data.get('meetings_per_week', 15)),
            'emails_per_day': int(data.get('emails_per_day', 75)),
            'deadline_pressure': int(data.get('deadline_pressure', 5)),
            'task_complexity': int(data.get('task_complexity', 5)),
            'team_support': int(data.get('team_support', 5)),
            'work_life_balance': int(data.get('work_life_balance', 5))
        }
        
        # 1. Predict stress level
        stress_result = stress_predictor.predict(stress_features)
        
        # 2. Calculate burnout score
        burnout_data = {**stress_features, 'stress_level': stress_result['stress_level']}
        burnout_result = burnout_engine.calculate_burnout_score(burnout_data)
        
        # 3. Calculate phishing vulnerability
        phishing_result = phishing_engine.calculate_vulnerability_index(
            stress_features,
            stress_result,
            burnout_result
        )
        
        # 4. Generate executive explanation
        combined_results = {
            'stress': stress_result,
            'burnout': burnout_result,
            'phishing': phishing_result,
            'inputs': stress_features
        }
        
        explanation = llm_explainer.generate_explanation(employee_name, combined_results)
        
        # Prepare response
        response = {
            'success': True,
            'employee_name': employee_name,
            'stress': stress_result,
            'burnout': burnout_result,
            'phishing': phishing_result,
            'explanation': explanation,
            'inputs': stress_features
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': stress_predictor.model is not None,
        'engines_ready': True
    })


@app.route('/api/dataset/info', methods=['GET'])
def dataset_info():
    """Get dataset statistics"""
    stats = llm_explainer.dataset_loader.get_stats()
    return jsonify({
        'dataset_loaded': llm_explainer.dataset_loader.dataset is not None,
        'stats': stats
    })


if __name__ == '__main__':
    import os
    # Only enable debug mode in development
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)

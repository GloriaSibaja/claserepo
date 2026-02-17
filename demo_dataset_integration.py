"""
Demo script showing dataset integration features
Run this to see how the dataset enhances LLM explanations
"""
from dataset_loader import DatasetLoader
from llm_explainer import LLMExplainer

print("=" * 70)
print("DATASET INTEGRATION DEMO")
print("=" * 70)

# 1. Load Dataset
print("\n1️⃣ Loading Employee Dataset...")
loader = DatasetLoader()
dataset = loader.load_dataset('employee_dataset.csv')
stats = loader.get_stats()

print(f"✓ Loaded {stats['total_employees']} employee records")
print(f"  - Average Burnout Score: {stats['avg_burnout']:.1f}/100")
print(f"  - High Risk Employees: {stats['high_risk_count']}")
print(f"  - Stress Distribution: {stats['avg_stress_score']}")

# 2. Find Similar Cases
print("\n2️⃣ Finding Similar Employee Cases...")
test_employee = {
    'work_hours_per_week': 58,
    'sleep_hours_per_day': 5.5,
    'meetings_per_week': 24,
    'emails_per_day': 130,
    'deadline_pressure': 9,
    'task_complexity': 8,
    'team_support': 3,
    'work_life_balance': 2
}

similar = loader.find_similar_cases(test_employee, n=3)
print(f"✓ Found {len(similar)} similar cases:")
for i, case in enumerate(similar, 1):
    print(f"  {i}. Similarity: {case['similarity_score']:.0%}")
    print(f"     Stress: {case['stress_level']}, Burnout: {case['burnout_score']:.1f}/100")
    print(f"     Outcome: {case['outcome']}")

# 3. Generate LLM Explanation with Dataset Context
print("\n3️⃣ Generating LLM Explanation with Dataset Context...")
explainer = LLMExplainer(dataset_file='employee_dataset.csv')

# Simulate full analysis results
test_results = {
    'stress': {
        'stress_level': 'High',
        'confidence': 0.844
    },
    'burnout': {
        'total_score': 59.09,
        'level': 'High Risk',
        'components': {
            'emotional_exhaustion': 65,
            'depersonalization': 60,
            'personal_accomplishment': 50,
            'work_overload': 62
        }
    },
    'phishing': {
        'vulnerability_index': 61.5,
        'risk_level': 'High Vulnerability',
        'attack_success_probability': 42.68
    },
    'inputs': test_employee
}

explanation = explainer.generate_explanation("Demo Employee", test_results)

print("\n" + "=" * 70)
print("EXECUTIVE SUMMARY (WITH DATASET CONTEXT)")
print("=" * 70)
print(explanation)

# 4. Show Dataset Context
print("\n" + "=" * 70)
print("DATASET CONTEXT FOR LLM")
print("=" * 70)
context = loader.get_context_for_llm(test_employee)
print(context)

print("\n" + "=" * 70)
print("✅ Dataset integration successfully demonstrated!")
print("=" * 70)
print("\nKey Benefits:")
print("• Similar case analysis provides real-world context")
print("• Historical outcomes inform recommendations")
print("• Benchmarking against organizational data")
print("• More personalized and data-driven insights")

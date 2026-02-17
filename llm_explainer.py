"""
Module 4: LLM Module for Executive Explanations
Generates personalized executive summaries using AI with dataset context
"""
import os
from typing import Dict, Any, Optional
from dataset_loader import DatasetLoader


class LLMExplainer:
    def __init__(self, api_key=None, dataset_file: Optional[str] = None):
        """
        Initialize LLM Explainer
        
        Args:
            api_key: OpenAI API key (optional, can use environment variable)
            dataset_file: Optional dataset file for context
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.use_openai = self.api_key is not None
        
        # Initialize dataset loader
        self.dataset_loader = DatasetLoader()
        if dataset_file and os.path.exists(os.path.join('data', dataset_file)):
            try:
                self.dataset_loader.load_dataset(dataset_file)
                print(f"✓ Dataset loaded: {dataset_file}")
            except Exception as e:
                print(f"Warning: Could not load dataset - {e}")
        
        if self.use_openai:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except ImportError:
                print("OpenAI package not available, using template-based explanations")
                self.use_openai = False
    
    def generate_explanation_openai(self, employee_name: str, results: Dict[str, Any]) -> str:
        """Generate explanation using OpenAI API with dataset context"""
        
        # Get dataset context if available
        dataset_context = ""
        if self.dataset_loader.dataset is not None:
            dataset_context = self.dataset_loader.get_context_for_llm(results['inputs'])
            dataset_context = f"\n\n{dataset_context}\n"
        
        prompt = f"""As an executive HR consultant, provide a professional summary for {employee_name}.

Analysis Results:
- Stress Level: {results['stress']['stress_level']} (Confidence: {results['stress']['confidence']:.1%})
- Burnout Score: {results['burnout']['total_score']}/100 ({results['burnout']['level']})
- Phishing Vulnerability: {results['phishing']['vulnerability_index']}/100 ({results['phishing']['risk_level']})
- Attack Success Probability: {results['phishing']['attack_success_probability']}%

Component Breakdown:
- Emotional Exhaustion: {results['burnout']['components']['emotional_exhaustion']}/100
- Depersonalization: {results['burnout']['components']['depersonalization']}/100
- Work Overload: {results['burnout']['components']['work_overload']}/100

Key Metrics:
- Work Hours/Week: {results['inputs']['work_hours_per_week']}
- Sleep Hours/Day: {results['inputs']['sleep_hours_per_day']}
- Meetings/Week: {results['inputs']['meetings_per_week']}
- Emails/Day: {results['inputs']['emails_per_day']}
{dataset_context}
Provide a 2-3 paragraph executive summary that:
1. Summarizes the employee's current state
2. Identifies key risk factors
3. Provides actionable recommendations
Be professional, empathetic, and data-driven."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert HR consultant specializing in employee wellbeing and security risk assessment."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self.generate_explanation_template(employee_name, results)
    
    def generate_explanation_template(self, employee_name: str, results: Dict[str, Any]) -> str:
        """Generate explanation using templates (fallback) with dataset context"""
        stress_level = results['stress']['stress_level']
        burnout_score = results['burnout']['total_score']
        burnout_level = results['burnout']['level']
        phishing_risk = results['phishing']['risk_level']
        vulnerability_index = results['phishing']['vulnerability_index']
        
        # Get similar cases from dataset if available
        similar_cases = []
        dataset_stats_text = ""
        if self.dataset_loader.dataset is not None:
            similar_cases = self.dataset_loader.find_similar_cases(results['inputs'], n=2)
            stats = self.dataset_loader.get_stats()
            if stats:
                dataset_stats_text = f" Based on analysis of {stats['total_employees']} employees in our database, "
        
        # Opening based on risk level
        if burnout_score >= 70 or stress_level == 'Critical':
            opening = f"{employee_name} is currently experiencing **{stress_level.lower()} stress levels** with a burnout score of **{burnout_score}/100** ({burnout_level}).{dataset_stats_text} This situation requires immediate attention."
        elif burnout_score >= 50 or stress_level == 'High':
            opening = f"{employee_name} shows **{stress_level.lower()} stress levels** and a burnout score of **{burnout_score}/100** ({burnout_level}), indicating elevated risk that should be addressed proactively."
        else:
            opening = f"{employee_name} currently maintains **{stress_level.lower()} stress levels** with a burnout score of **{burnout_score}/100** ({burnout_level}), showing relatively healthy work patterns."
        
        # Key factors analysis
        inputs = results['inputs']
        factors = []
        
        if inputs['work_hours_per_week'] > 50:
            factors.append(f"working **{inputs['work_hours_per_week']} hours/week** (above recommended levels)")
        
        if inputs['sleep_hours_per_day'] < 6.5:
            factors.append(f"averaging only **{inputs['sleep_hours_per_day']} hours of sleep** (below optimal)")
        
        if inputs['meetings_per_week'] > 20:
            factors.append(f"attending **{inputs['meetings_per_week']} meetings/week** (high meeting load)")
        
        if inputs['emails_per_day'] > 100:
            factors.append(f"processing **{inputs['emails_per_day']} emails/day** (significant communication overhead)")
        
        if factors:
            factor_text = f"Key contributing factors include {', '.join(factors)}."
        else:
            factor_text = "Work metrics are within normal ranges."
        
        # Security risk assessment
        security_text = f"From a security perspective, the **Phishing Vulnerability Index** stands at **{vulnerability_index}/100** ({phishing_risk}), with an estimated **{results['phishing']['attack_success_probability']}% attack success probability**. "
        
        if vulnerability_index >= 70:
            security_text += "This elevated vulnerability requires urgent security awareness training and workload management."
        elif vulnerability_index >= 50:
            security_text += "This moderate vulnerability suggests scheduling a security awareness refresher while addressing workload concerns."
        else:
            security_text += "This relatively low vulnerability indicates good security awareness, though continuous monitoring is recommended."
        
        # Recommendations
        recommendations = []
        
        if burnout_score >= 70:
            recommendations.append("**Immediate workload review** and potential redistribution")
            recommendations.append("Schedule **wellness consultation** within 48 hours")
        elif burnout_score >= 50:
            recommendations.append("**Schedule a check-in** to discuss workload and support needs")
            recommendations.append("Consider **flexible work arrangements** if feasible")
        
        if inputs['sleep_hours_per_day'] < 6.5:
            recommendations.append("Encourage **better sleep hygiene** and time management")
        
        if inputs['meetings_per_week'] > 20:
            recommendations.append("**Audit meeting necessity** and reduce where possible")
        
        if vulnerability_index >= 50:
            recommendations.append("Provide **targeted security awareness training**")
            recommendations.append("Implement **email filtering** and additional safeguards")
        
        if not recommendations:
            recommendations.append("Continue **monitoring** these metrics monthly")
            recommendations.append("Maintain current **support structures**")
        
        rec_text = "**Recommended Actions:**\n" + "\n".join(f"• {rec}" for rec in recommendations)
        
        # Add similar cases context if available
        similar_cases_text = ""
        if similar_cases:
            similar_cases_text = "\n\n**Similar Cases Analysis:**\n"
            for i, case in enumerate(similar_cases, 1):
                outcome = case.get('outcome', 'No outcome data')
                similar_cases_text += f"• Employee with similar profile (Burnout: {case.get('burnout_score', 0):.0f}/100): {outcome}\n"
        
        # Combine all parts
        explanation = f"""{opening} {factor_text}

{security_text}

{rec_text}{similar_cases_text}"""
        
        return explanation
    
    def generate_explanation(self, employee_name: str, results: Dict[str, Any]) -> str:
        """
        Generate executive explanation
        
        Args:
            employee_name: Name of the employee
            results: Combined results from all engines
        
        Returns:
            Professional executive summary
        """
        if self.use_openai:
            return self.generate_explanation_openai(employee_name, results)
        else:
            return self.generate_explanation_template(employee_name, results)


if __name__ == '__main__':
    # Test explanation generation with dataset
    explainer = LLMExplainer(dataset_file='employee_dataset.csv')
    
    test_results = {
        'stress': {
            'stress_level': 'High',
            'confidence': 0.85
        },
        'burnout': {
            'total_score': 68,
            'level': 'High Risk',
            'components': {
                'emotional_exhaustion': 72,
                'depersonalization': 65,
                'work_overload': 70,
                'personal_accomplishment': 60
            }
        },
        'phishing': {
            'vulnerability_index': 64,
            'risk_level': 'High Vulnerability',
            'attack_success_probability': 42
        },
        'inputs': {
            'work_hours_per_week': 55,
            'sleep_hours_per_day': 6,
            'meetings_per_week': 25,
            'emails_per_day': 120,
            'deadline_pressure': 9,
            'task_complexity': 8,
            'team_support': 4,
            'work_life_balance': 3
        }
    }
    
    explanation = explainer.generate_explanation("John Doe", test_results)
    print("Executive Summary (with dataset context):")
    print("=" * 60)
    print(explanation)

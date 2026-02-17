"""
Module 3: Risk Engine for Phishing Vulnerability Index
Calculates employee vulnerability to phishing attacks based on stress and burnout
"""
import numpy as np


class PhishingRiskEngine:
    def __init__(self):
        # Risk factors and their weights
        self.risk_factors = {
            'stress_level': 0.25,
            'burnout_score': 0.30,
            'cognitive_load': 0.25,
            'awareness_level': 0.20
        }
    
    def calculate_cognitive_load(self, emails_per_day, meetings_per_week, task_complexity):
        """
        Calculate cognitive load score
        High cognitive load = more likely to make mistakes
        
        Args:
            emails_per_day: number of emails
            meetings_per_week: number of meetings
            task_complexity: 1-10 scale
        
        Returns:
            score 0-100
        """
        # Email overload
        email_factor = min(100, (emails_per_day - 30) * 0.7)
        email_factor = max(0, email_factor)
        
        # Meeting fatigue
        meeting_factor = min(100, (meetings_per_week - 5) * 3)
        meeting_factor = max(0, meeting_factor)
        
        # Task complexity
        complexity_factor = task_complexity * 10
        
        # Combined cognitive load
        score = (email_factor * 0.4 + meeting_factor * 0.3 + complexity_factor * 0.3)
        
        return min(100, max(0, score))
    
    def estimate_awareness_level(self, work_hours, sleep_hours, work_life_balance):
        """
        Estimate security awareness level (inverse)
        Low awareness = higher vulnerability
        
        Args:
            work_hours: hours per week
            sleep_hours: hours per day
            work_life_balance: 1-10 scale
        
        Returns:
            score 0-100 (higher = less aware/more vulnerable)
        """
        # Overwork reduces attention to security
        overwork_factor = min(100, max(0, (work_hours - 40) * 2))
        
        # Sleep deprivation impairs judgment
        sleep_factor = max(0, (7.5 - sleep_hours) * 12)
        sleep_factor = min(100, sleep_factor)
        
        # Poor work-life balance reduces security mindfulness
        balance_factor = (10 - work_life_balance) * 10
        
        score = (overwork_factor * 0.35 + sleep_factor * 0.35 + balance_factor * 0.30)
        
        return min(100, max(0, score))
    
    def calculate_vulnerability_index(self, employee_data, stress_result, burnout_result):
        """
        Calculate comprehensive phishing vulnerability index
        
        Args:
            employee_data: dict with employee metrics
            stress_result: result from StressLevelPredictor
            burnout_result: result from BurnoutEngine
        
        Returns:
            dict with vulnerability index and risk factors
        """
        # Map stress level to score
        stress_map = {'Low': 20, 'Medium': 45, 'High': 70, 'Critical': 95}
        stress_score = stress_map.get(stress_result.get('stress_level', 'Medium'), 50)
        
        # Get burnout score
        burnout_score = burnout_result.get('total_score', 50)
        
        # Calculate cognitive load
        cognitive_load = self.calculate_cognitive_load(
            employee_data.get('emails_per_day', 75),
            employee_data.get('meetings_per_week', 15),
            employee_data.get('task_complexity', 5)
        )
        
        # Calculate awareness level (vulnerability)
        awareness_vulnerability = self.estimate_awareness_level(
            employee_data.get('work_hours_per_week', 40),
            employee_data.get('sleep_hours_per_day', 7),
            employee_data.get('work_life_balance', 5)
        )
        
        # Calculate weighted total
        vulnerability_index = (
            stress_score * self.risk_factors['stress_level'] +
            burnout_score * self.risk_factors['burnout_score'] +
            cognitive_load * self.risk_factors['cognitive_load'] +
            awareness_vulnerability * self.risk_factors['awareness_level']
        )
        
        # Categorize risk
        if vulnerability_index < 30:
            risk_level = 'Low Vulnerability'
            color = 'green'
            recommendation = 'Maintain current security practices'
        elif vulnerability_index < 50:
            risk_level = 'Moderate Vulnerability'
            color = 'yellow'
            recommendation = 'Schedule security awareness refresher'
        elif vulnerability_index < 70:
            risk_level = 'High Vulnerability'
            color = 'orange'
            recommendation = 'Immediate security training required'
        else:
            risk_level = 'Critical Vulnerability'
            color = 'red'
            recommendation = 'Urgent intervention needed - high phishing risk'
        
        # Calculate attack success probability
        # Based on industry research: stressed employees 4x more likely to fall for phishing
        base_rate = 0.15  # 15% baseline click rate
        multiplier = 1 + (vulnerability_index / 100) * 3  # Up to 4x increase
        attack_success_probability = min(0.95, base_rate * multiplier)
        
        return {
            'vulnerability_index': round(vulnerability_index, 2),
            'risk_level': risk_level,
            'color': color,
            'attack_success_probability': round(attack_success_probability * 100, 2),
            'recommendation': recommendation,
            'risk_factors': {
                'stress_contribution': round(stress_score * self.risk_factors['stress_level'], 2),
                'burnout_contribution': round(burnout_score * self.risk_factors['burnout_score'], 2),
                'cognitive_load': round(cognitive_load, 2),
                'awareness_vulnerability': round(awareness_vulnerability, 2)
            },
            'factor_weights': self.risk_factors
        }


if __name__ == '__main__':
    # Test phishing risk calculation
    engine = PhishingRiskEngine()
    
    employee_data = {
        'work_hours_per_week': 55,
        'sleep_hours_per_day': 6,
        'emails_per_day': 120,
        'meetings_per_week': 25,
        'task_complexity': 8,
        'work_life_balance': 3
    }
    
    # Mock stress and burnout results
    stress_result = {'stress_level': 'High'}
    burnout_result = {'total_score': 68}
    
    result = engine.calculate_vulnerability_index(employee_data, stress_result, burnout_result)
    
    print(f"Phishing Vulnerability Index: {result['vulnerability_index']}/100")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Attack Success Probability: {result['attack_success_probability']}%")
    print(f"Recommendation: {result['recommendation']}")
    print(f"\nRisk Factor Breakdown:")
    for factor, value in result['risk_factors'].items():
        print(f"  {factor}: {value}")

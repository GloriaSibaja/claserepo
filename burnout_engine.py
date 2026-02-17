"""
Module 2: Mathematical Engine for Burnout Score Calculation
Calculates comprehensive burnout score based on multiple factors
"""
import numpy as np


class BurnoutEngine:
    def __init__(self):
        # Weights for different burnout dimensions
        self.weights = {
            'emotional_exhaustion': 0.35,
            'depersonalization': 0.25,
            'personal_accomplishment': 0.20,
            'work_overload': 0.20
        }
    
    def calculate_emotional_exhaustion(self, work_hours, sleep_hours, stress_level_score):
        """
        Calculate emotional exhaustion component
        
        Args:
            work_hours: hours worked per week
            sleep_hours: average sleep hours per day
            stress_level_score: stress level from predictor (0-100)
        
        Returns:
            score 0-100 (higher = more exhaustion)
        """
        # Normalize work hours (40 is baseline, 60+ is critical)
        work_factor = min(100, max(0, (work_hours - 40) * 5))
        
        # Sleep deprivation (7-8 hours is ideal)
        sleep_factor = max(0, (7.5 - sleep_hours) * 15)
        sleep_factor = min(100, sleep_factor)
        
        # Combine factors
        score = (work_factor * 0.4 + sleep_factor * 0.3 + stress_level_score * 0.3)
        
        return min(100, max(0, score))
    
    def calculate_depersonalization(self, team_support, work_life_balance, meetings_per_week):
        """
        Calculate depersonalization component (cynicism, detachment)
        
        Args:
            team_support: 1-10 scale
            work_life_balance: 1-10 scale
            meetings_per_week: number of meetings
        
        Returns:
            score 0-100 (higher = more depersonalization)
        """
        # Inverse of support (low support = high depersonalization)
        support_factor = (10 - team_support) * 10
        
        # Poor work-life balance increases depersonalization
        balance_factor = (10 - work_life_balance) * 10
        
        # Too many meetings can lead to meeting fatigue
        meeting_factor = min(100, (meetings_per_week - 10) * 3)
        meeting_factor = max(0, meeting_factor)
        
        score = (support_factor * 0.4 + balance_factor * 0.4 + meeting_factor * 0.2)
        
        return min(100, max(0, score))
    
    def calculate_personal_accomplishment(self, task_complexity, deadline_pressure):
        """
        Calculate reduced personal accomplishment
        
        Args:
            task_complexity: 1-10 scale
            deadline_pressure: 1-10 scale
        
        Returns:
            score 0-100 (higher = less accomplishment)
        """
        # High complexity with high pressure reduces sense of accomplishment
        complexity_factor = task_complexity * 5
        pressure_factor = deadline_pressure * 5
        
        # Combined effect (synergistic)
        synergy = (task_complexity * deadline_pressure) * 0.5
        
        score = complexity_factor * 0.3 + pressure_factor * 0.4 + synergy * 0.3
        
        return min(100, max(0, score))
    
    def calculate_work_overload(self, work_hours, emails_per_day, meetings_per_week):
        """
        Calculate work overload component
        
        Args:
            work_hours: hours per week
            emails_per_day: number of emails
            meetings_per_week: number of meetings
        
        Returns:
            score 0-100 (higher = more overload)
        """
        # Normalize to 0-100 scale
        hours_factor = min(100, max(0, (work_hours - 40) * 3))
        email_factor = min(100, (emails_per_day - 50) * 0.5)
        meeting_factor = min(100, (meetings_per_week - 10) * 4)
        
        score = (hours_factor * 0.5 + email_factor * 0.25 + meeting_factor * 0.25)
        
        return min(100, max(0, score))
    
    def calculate_burnout_score(self, employee_data):
        """
        Calculate comprehensive burnout score
        
        Args:
            employee_data: dict with employee metrics
        
        Returns:
            dict with burnout score and breakdown
        """
        # Map stress level to score
        stress_map = {'Low': 25, 'Medium': 50, 'High': 75, 'Critical': 100}
        stress_score = stress_map.get(employee_data.get('stress_level', 'Medium'), 50)
        
        # Calculate components
        emotional_exhaustion = self.calculate_emotional_exhaustion(
            employee_data.get('work_hours_per_week', 40),
            employee_data.get('sleep_hours_per_day', 7),
            stress_score
        )
        
        depersonalization = self.calculate_depersonalization(
            employee_data.get('team_support', 5),
            employee_data.get('work_life_balance', 5),
            employee_data.get('meetings_per_week', 15)
        )
        
        personal_accomplishment = self.calculate_personal_accomplishment(
            employee_data.get('task_complexity', 5),
            employee_data.get('deadline_pressure', 5)
        )
        
        work_overload = self.calculate_work_overload(
            employee_data.get('work_hours_per_week', 40),
            employee_data.get('emails_per_day', 75),
            employee_data.get('meetings_per_week', 15)
        )
        
        # Calculate weighted total
        total_score = (
            emotional_exhaustion * self.weights['emotional_exhaustion'] +
            depersonalization * self.weights['depersonalization'] +
            personal_accomplishment * self.weights['personal_accomplishment'] +
            work_overload * self.weights['work_overload']
        )
        
        # Categorize burnout level
        if total_score < 30:
            level = 'Low Risk'
            color = 'green'
        elif total_score < 50:
            level = 'Moderate Risk'
            color = 'yellow'
        elif total_score < 70:
            level = 'High Risk'
            color = 'orange'
        else:
            level = 'Critical Risk'
            color = 'red'
        
        return {
            'total_score': round(total_score, 2),
            'level': level,
            'color': color,
            'components': {
                'emotional_exhaustion': round(emotional_exhaustion, 2),
                'depersonalization': round(depersonalization, 2),
                'personal_accomplishment': round(personal_accomplishment, 2),
                'work_overload': round(work_overload, 2)
            },
            'weights': self.weights
        }


if __name__ == '__main__':
    # Test burnout calculation
    engine = BurnoutEngine()
    
    test_data = {
        'work_hours_per_week': 55,
        'sleep_hours_per_day': 6,
        'stress_level': 'High',
        'team_support': 4,
        'work_life_balance': 3,
        'meetings_per_week': 25,
        'task_complexity': 8,
        'deadline_pressure': 9,
        'emails_per_day': 120
    }
    
    result = engine.calculate_burnout_score(test_data)
    print(f"Burnout Score: {result['total_score']}/100")
    print(f"Risk Level: {result['level']}")
    print(f"\nComponent Breakdown:")
    for component, score in result['components'].items():
        print(f"  {component}: {score}/100")

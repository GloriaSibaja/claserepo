"""
Dataset Loader Module
Loads and manages employee datasets for enhanced LLM context
"""
import pandas as pd
import json
import os
from typing import Dict, List, Any, Optional
import numpy as np


class DatasetLoader:
    def __init__(self, data_dir='data'):
        """
        Initialize Dataset Loader
        
        Args:
            data_dir: Directory containing dataset files
        """
        self.data_dir = data_dir
        self.dataset = None
        self.dataset_stats = None
        
    def load_dataset(self, filename: str) -> pd.DataFrame:
        """
        Load dataset from CSV or JSON file
        
        Args:
            filename: Name of the dataset file
            
        Returns:
            pandas DataFrame with employee data
        """
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Dataset not found: {filepath}")
        
        # Load based on file extension
        if filename.endswith('.csv'):
            self.dataset = pd.read_csv(filepath)
        elif filename.endswith('.json'):
            self.dataset = pd.read_json(filepath)
        else:
            raise ValueError(f"Unsupported file format. Use .csv or .json")
        
        # Calculate statistics
        self._calculate_stats()
        
        return self.dataset
    
    def _calculate_stats(self):
        """Calculate dataset statistics"""
        if self.dataset is None:
            return
        
        self.dataset_stats = {
            'total_employees': len(self.dataset),
            'avg_stress_score': self.dataset.get('stress_level', pd.Series()).value_counts().to_dict(),
            'avg_burnout': self.dataset.get('burnout_score', pd.Series()).mean() if 'burnout_score' in self.dataset else None,
            'high_risk_count': len(self.dataset[self.dataset.get('burnout_score', 0) > 70]) if 'burnout_score' in self.dataset else 0,
            'columns': list(self.dataset.columns)
        }
    
    def find_similar_cases(self, employee_data: Dict[str, Any], n: int = 3) -> List[Dict[str, Any]]:
        """
        Find similar employee cases from the dataset
        
        Args:
            employee_data: Current employee metrics
            n: Number of similar cases to return
            
        Returns:
            List of similar employee records
        """
        if self.dataset is None or len(self.dataset) == 0:
            return []
        
        # Calculate similarity based on key metrics
        similarity_scores = []
        
        for idx, row in self.dataset.iterrows():
            score = 0
            count = 0
            
            # Compare numeric fields
            for field in ['work_hours_per_week', 'sleep_hours_per_day', 'meetings_per_week', 
                         'emails_per_day', 'deadline_pressure', 'task_complexity']:
                if field in employee_data and field in row:
                    # Calculate normalized difference
                    diff = abs(float(employee_data[field]) - float(row[field]))
                    max_val = max(float(employee_data[field]), float(row[field]), 1)
                    score += (1 - diff / max_val)
                    count += 1
            
            avg_similarity = score / count if count > 0 else 0
            similarity_scores.append((idx, avg_similarity))
        
        # Sort by similarity and get top N
        similarity_scores.sort(key=lambda x: x[1], reverse=True)
        top_cases = similarity_scores[:n]
        
        # Return the similar cases
        similar = []
        for idx, similarity in top_cases:
            case = self.dataset.iloc[idx].to_dict()
            case['similarity_score'] = similarity
            similar.append(case)
        
        return similar
    
    def get_context_for_llm(self, employee_data: Dict[str, Any]) -> str:
        """
        Generate context string for LLM from dataset
        
        Args:
            employee_data: Current employee metrics
            
        Returns:
            Formatted context string
        """
        if self.dataset is None:
            return ""
        
        context_parts = []
        
        # Add dataset statistics
        if self.dataset_stats:
            context_parts.append(f"Dataset Context: {self.dataset_stats['total_employees']} employees analyzed")
            
            if self.dataset_stats['avg_burnout']:
                context_parts.append(f"Average burnout score: {self.dataset_stats['avg_burnout']:.1f}/100")
        
        # Add similar cases
        similar_cases = self.find_similar_cases(employee_data, n=3)
        if similar_cases:
            context_parts.append("\nSimilar Employee Cases:")
            for i, case in enumerate(similar_cases, 1):
                summary = f"  Case {i} (Similarity: {case['similarity_score']:.0%}): "
                details = []
                
                if 'stress_level' in case:
                    details.append(f"Stress: {case['stress_level']}")
                if 'burnout_score' in case:
                    details.append(f"Burnout: {case['burnout_score']:.1f}/100")
                if 'outcome' in case:
                    details.append(f"Outcome: {case['outcome']}")
                
                summary += ", ".join(details)
                context_parts.append(summary)
        
        return "\n".join(context_parts)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get dataset statistics"""
        return self.dataset_stats or {}
    
    def save_dataset(self, data: pd.DataFrame, filename: str):
        """
        Save dataset to file
        
        Args:
            data: DataFrame to save
            filename: Output filename
        """
        filepath = os.path.join(self.data_dir, filename)
        os.makedirs(self.data_dir, exist_ok=True)
        
        if filename.endswith('.csv'):
            data.to_csv(filepath, index=False)
        elif filename.endswith('.json'):
            data.to_json(filepath, orient='records', indent=2)
        else:
            raise ValueError("Unsupported file format. Use .csv or .json")


def generate_sample_dataset(n_samples: int = 100, output_file: str = 'data/employee_dataset.csv'):
    """
    Generate a sample employee dataset for testing
    
    Args:
        n_samples: Number of employee records to generate
        output_file: Output file path
    """
    np.random.seed(42)
    
    # Generate synthetic employee data
    data = {
        'employee_id': [f'EMP{i:04d}' for i in range(1, n_samples + 1)],
        'work_hours_per_week': np.random.normal(45, 10, n_samples).clip(20, 80),
        'sleep_hours_per_day': np.random.normal(7, 1.5, n_samples).clip(3, 12),
        'meetings_per_week': np.random.randint(5, 35, n_samples),
        'emails_per_day': np.random.randint(20, 200, n_samples),
        'deadline_pressure': np.random.randint(1, 11, n_samples),
        'task_complexity': np.random.randint(1, 11, n_samples),
        'team_support': np.random.randint(1, 11, n_samples),
        'work_life_balance': np.random.randint(1, 11, n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Calculate derived metrics
    # Stress score
    stress_score = (
        (df['work_hours_per_week'] - 40) * 0.5 +
        (8 - df['sleep_hours_per_day']) * 5 +
        df['meetings_per_week'] * 0.3 +
        df['emails_per_day'] * 0.05 +
        df['deadline_pressure'] * 3 +
        df['task_complexity'] * 2 -
        df['team_support'] * 2 -
        df['work_life_balance'] * 2
    )
    
    df['stress_level'] = pd.cut(
        stress_score, 
        bins=[-np.inf, 20, 40, 60, np.inf],
        labels=['Low', 'Medium', 'High', 'Critical']
    )
    
    # Burnout score (simplified calculation)
    df['burnout_score'] = (
        (df['work_hours_per_week'] - 40) * 0.8 +
        (8 - df['sleep_hours_per_day']) * 6 +
        df['deadline_pressure'] * 4 +
        (10 - df['team_support']) * 3 +
        (10 - df['work_life_balance']) * 3
    ).clip(0, 100)
    
    # Add outcomes (simulated interventions and results)
    outcomes = []
    for _, row in df.iterrows():
        if row['burnout_score'] > 70:
            outcomes.append('Intervention: Workload reduced, improved after 3 months')
        elif row['burnout_score'] > 50:
            outcomes.append('Monitoring: Regular check-ins scheduled')
        else:
            outcomes.append('Healthy: Continuing normal work pattern')
    
    df['outcome'] = outcomes
    
    # Save dataset
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)
    
    print(f"Generated sample dataset with {n_samples} employees")
    print(f"Saved to: {output_file}")
    print(f"\nDataset Statistics:")
    print(f"  Stress Levels: {df['stress_level'].value_counts().to_dict()}")
    print(f"  Avg Burnout Score: {df['burnout_score'].mean():.1f}/100")
    print(f"  High Risk (>70): {len(df[df['burnout_score'] > 70])} employees")
    
    return df


if __name__ == '__main__':
    # Generate sample dataset
    df = generate_sample_dataset(100, 'data/employee_dataset.csv')
    
    # Test dataset loader
    loader = DatasetLoader()
    dataset = loader.load_dataset('employee_dataset.csv')
    
    print(f"\nLoaded dataset: {len(dataset)} records")
    print(f"Columns: {list(dataset.columns)}")
    
    # Test finding similar cases
    test_employee = {
        'work_hours_per_week': 55,
        'sleep_hours_per_day': 6,
        'meetings_per_week': 22,
        'emails_per_day': 110,
        'deadline_pressure': 8,
        'task_complexity': 7,
        'team_support': 4,
        'work_life_balance': 3
    }
    
    similar = loader.find_similar_cases(test_employee, n=3)
    print(f"\nFound {len(similar)} similar cases")
    for i, case in enumerate(similar, 1):
        print(f"  {i}. Similarity: {case['similarity_score']:.0%}, "
              f"Stress: {case['stress_level']}, Burnout: {case['burnout_score']:.1f}")

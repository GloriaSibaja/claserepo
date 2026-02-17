# Employee Dataset Documentation

## Overview

This dataset contains anonymized employee wellbeing and productivity metrics used to enhance the LLM module's ability to provide contextual recommendations.

## Dataset: employee_dataset.csv

### Description
A synthetic dataset of 100 employee records with comprehensive work metrics, stress levels, burnout scores, and intervention outcomes.

### Columns

| Column | Type | Range | Description |
|--------|------|-------|-------------|
| `employee_id` | string | EMP0001-EMP0100 | Unique employee identifier |
| `work_hours_per_week` | float | 20-80 | Average weekly work hours |
| `sleep_hours_per_day` | float | 3-12 | Average daily sleep hours |
| `meetings_per_week` | integer | 5-35 | Number of meetings attended weekly |
| `emails_per_day` | integer | 20-200 | Number of emails processed daily |
| `deadline_pressure` | integer | 1-10 | Self-reported deadline pressure (1=low, 10=high) |
| `task_complexity` | integer | 1-10 | Self-reported task complexity (1=simple, 10=complex) |
| `team_support` | integer | 1-10 | Perceived team support level (1=low, 10=high) |
| `work_life_balance` | integer | 1-10 | Self-reported work-life balance (1=poor, 10=excellent) |
| `stress_level` | category | Low/Medium/High/Critical | Calculated stress level category |
| `burnout_score` | float | 0-100 | Calculated burnout risk score |
| `outcome` | string | - | Intervention outcome or current status |

### Statistics

- **Total Records**: 100 employees
- **Stress Distribution**:
  - Low: 35%
  - Medium: 51%
  - High: 14%
  - Critical: 0%
- **Average Burnout Score**: 59.1/100
- **High Risk Employees (>70)**: 31%

### Use Cases

1. **Similar Case Analysis**: Find employees with similar profiles to provide relevant recommendations
2. **Outcome Prediction**: Learn from historical intervention outcomes
3. **Benchmarking**: Compare individual employees against organizational averages
4. **LLM Context**: Provide the LLM with real-world examples for better explanations

### Data Generation

This dataset was synthetically generated using:
- Normal distributions for continuous variables (work hours, sleep)
- Uniform distributions for discrete variables (meetings, emails, scales)
- Calculated stress and burnout scores based on weighted formulas
- Simulated intervention outcomes based on risk levels

### Privacy & Ethics

- **No Real Data**: This is 100% synthetic data
- **No PII**: No personally identifiable information
- **Educational Purpose**: Created for demonstration and development

## How to Use

### Loading the Dataset

```python
from dataset_loader import DatasetLoader

loader = DatasetLoader()
dataset = loader.load_dataset('employee_dataset.csv')
print(f"Loaded {len(dataset)} records")
```

### Finding Similar Cases

```python
employee_data = {
    'work_hours_per_week': 55,
    'sleep_hours_per_day': 6,
    'meetings_per_week': 22,
    'emails_per_day': 110,
    'deadline_pressure': 8,
    'task_complexity': 7,
    'team_support': 4,
    'work_life_balance': 3
}

similar = loader.find_similar_cases(employee_data, n=3)
for case in similar:
    print(f"Similar employee: Burnout {case['burnout_score']:.1f}, "
          f"Outcome: {case['outcome']}")
```

### Using with LLM

```python
from llm_explainer import LLMExplainer

explainer = LLMExplainer(dataset_file='employee_dataset.csv')
# The explainer will automatically use the dataset for context
```

## Adding Your Own Dataset

You can replace `employee_dataset.csv` with your own data:

1. **CSV Format**: Ensure your CSV has the required columns
2. **Column Names**: Match the expected column names
3. **Data Types**: Follow the type specifications above
4. **Location**: Place in the `data/` directory
5. **Privacy**: Ensure data is anonymized and compliant with regulations

### Example Custom Dataset

```csv
employee_id,work_hours_per_week,sleep_hours_per_day,...
CUSTOM001,48,7.5,...
CUSTOM002,52,6.0,...
```

Then load it:

```python
explainer = LLMExplainer(dataset_file='my_custom_dataset.csv')
```

## API Endpoints

### Get Dataset Info

```bash
curl http://localhost:5000/api/dataset/info
```

Response:
```json
{
  "dataset_loaded": true,
  "stats": {
    "total_employees": 100,
    "avg_burnout": 59.1,
    "high_risk_count": 31,
    "columns": ["employee_id", "work_hours_per_week", ...]
  }
}
```

## Future Enhancements

- [ ] Support for time-series data (tracking employees over time)
- [ ] Department/team segmentation
- [ ] External dataset upload via web interface
- [ ] Data validation and quality checks
- [ ] Automated dataset updates

## License

This synthetic dataset is provided for educational purposes. Feel free to modify and extend it for your needs.

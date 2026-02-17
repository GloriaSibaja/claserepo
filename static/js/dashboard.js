// Dashboard JavaScript - handles form submission and visualization

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('analysisForm');
    const loading = document.getElementById('loading');
    const results = document.getElementById('results');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading
        loading.style.display = 'flex';
        results.style.display = 'none';

        // Collect form data
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            // Convert numeric fields
            if (key !== 'employee_name') {
                data[key] = parseFloat(value);
            } else {
                data[key] = value;
            }
        }

        try {
            // Call API
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error('Analysis failed');
            }

            const result = await response.json();
            
            // Hide loading
            loading.style.display = 'none';
            
            // Display results
            displayResults(result);
            
        } catch (error) {
            loading.style.display = 'none';
            alert('Error: ' + error.message);
        }
    });
});

function displayResults(data) {
    const results = document.getElementById('results');
    results.style.display = 'block';
    
    // Smooth scroll to results
    results.scrollIntoView({ behavior: 'smooth', block: 'start' });

    // Update Stress Card
    updateStressCard(data.stress);
    
    // Update Burnout Card
    updateBurnoutCard(data.burnout);
    
    // Update Phishing Card
    updatePhishingCard(data.phishing);
    
    // Update Probability Card
    updateProbabilityCard(data.phishing);
    
    // Create Charts
    createBurnoutChart(data.burnout);
    createRiskChart(data.phishing);
    
    // Update Executive Summary
    updateExecutiveSummary(data.explanation);
}

function updateStressCard(stress) {
    const card = document.getElementById('stressCard');
    const value = document.getElementById('stressValue');
    const confidence = document.getElementById('stressConfidence');
    
    value.textContent = stress.stress_level;
    confidence.textContent = `${(stress.confidence * 100).toFixed(0)}% confidence`;
    
    // Update card color
    card.className = 'metric-card';
    if (stress.stress_level === 'Low') {
        card.classList.add('low-risk');
    } else if (stress.stress_level === 'Medium') {
        card.classList.add('medium-risk');
    } else {
        card.classList.add('high-risk');
    }
}

function updateBurnoutCard(burnout) {
    const card = document.getElementById('burnoutCard');
    const value = document.getElementById('burnoutValue');
    const level = document.getElementById('burnoutLevel');
    
    value.textContent = `${burnout.total_score}/100`;
    level.textContent = burnout.level;
    
    // Update card color
    card.className = 'metric-card';
    if (burnout.total_score < 30) {
        card.classList.add('low-risk');
    } else if (burnout.total_score < 60) {
        card.classList.add('medium-risk');
    } else {
        card.classList.add('high-risk');
    }
}

function updatePhishingCard(phishing) {
    const card = document.getElementById('phishingCard');
    const value = document.getElementById('phishingValue');
    const level = document.getElementById('phishingLevel');
    
    value.textContent = `${phishing.vulnerability_index}/100`;
    level.textContent = phishing.risk_level;
    
    // Update card color
    card.className = 'metric-card';
    if (phishing.vulnerability_index < 30) {
        card.classList.add('low-risk');
    } else if (phishing.vulnerability_index < 60) {
        card.classList.add('medium-risk');
    } else {
        card.classList.add('high-risk');
    }
}

function updateProbabilityCard(phishing) {
    const card = document.getElementById('probabilityCard');
    const value = document.getElementById('probabilityValue');
    
    value.textContent = `${phishing.attack_success_probability}%`;
    
    // Update card color
    card.className = 'metric-card';
    if (phishing.attack_success_probability < 20) {
        card.classList.add('low-risk');
    } else if (phishing.attack_success_probability < 40) {
        card.classList.add('medium-risk');
    } else {
        card.classList.add('high-risk');
    }
}

function createBurnoutChart(burnout) {
    const components = burnout.components;
    
    const data = [{
        type: 'bar',
        x: Object.keys(components).map(k => k.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())),
        y: Object.values(components),
        marker: {
            color: Object.values(components).map(v => {
                if (v < 30) return '#10b981';
                if (v < 60) return '#f59e0b';
                return '#ef4444';
            })
        },
        text: Object.values(components).map(v => `${v.toFixed(1)}`),
        textposition: 'auto'
    }];
    
    const layout = {
        margin: { t: 20, r: 20, b: 80, l: 60 },
        yaxis: { 
            title: 'Score (0-100)',
            range: [0, 100]
        },
        xaxis: {
            tickangle: -45
        },
        height: 350,
        plot_bgcolor: '#f8fafc',
        paper_bgcolor: 'transparent'
    };
    
    Plotly.newPlot('burnoutChart', data, layout, {responsive: true, displayModeBar: false});
}

function createRiskChart(phishing) {
    const riskFactors = phishing.risk_factors;
    
    const data = [{
        type: 'bar',
        x: Object.keys(riskFactors).map(k => k.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())),
        y: Object.values(riskFactors),
        marker: {
            color: '#7c3aed',
            line: {
                color: '#5b21b6',
                width: 1
            }
        },
        text: Object.values(riskFactors).map(v => `${v.toFixed(1)}`),
        textposition: 'auto'
    }];
    
    const layout = {
        margin: { t: 20, r: 20, b: 80, l: 60 },
        yaxis: { 
            title: 'Risk Contribution',
            range: [0, Math.max(...Object.values(riskFactors)) * 1.2]
        },
        xaxis: {
            tickangle: -45
        },
        height: 350,
        plot_bgcolor: '#f8fafc',
        paper_bgcolor: 'transparent'
    };
    
    Plotly.newPlot('riskChart', data, layout, {responsive: true, displayModeBar: false});
}

function updateExecutiveSummary(explanation) {
    const summaryDiv = document.getElementById('executiveSummary');
    
    // Convert markdown-style bold to HTML
    let html = explanation
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n•/g, '<br>•');
    
    summaryDiv.innerHTML = `<p>${html}</p>`;
}

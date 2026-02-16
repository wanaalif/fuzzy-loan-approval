# Fuzzy Logic Loan Approval System

A sophisticated fuzzy logic controller implementation for automated loan approval decisions, combining multiple financial indicators to provide nuanced risk assessment and interest rate recommendations.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-complete-success.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Input Variables](#input-variables)
- [Output Variables](#output-variables)
- [Fuzzy Rules](#fuzzy-rules)
- [Examples](#examples)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## 🎯 Overview

This project implements a **Fuzzy Logic Controller (FLC)** for loan approval decisions, developed as part of the Computational Intelligence (SAIA 1193) course at Universiti Teknologi Malaysia. Unlike traditional binary decision systems, this fuzzy logic approach handles uncertainty and provides human-like reasoning for complex financial evaluations.

### Why Fuzzy Logic?

- **Handles Uncertainty**: Loan decisions involve imprecise information and multiple gray areas
- **Human-like Reasoning**: Mimics how loan officers evaluate applications using linguistic terms
- **Smooth Transitions**: Provides gradual transitions between approval categories
- **Multi-criteria Analysis**: Effectively manages multiple conflicting criteria

## ✨ Features

- **4 Input Variables**: Credit Score, Debt-to-Income Ratio, Annual Income, Employment Duration
- **2 Output Variables**: Approval Score (0-100) and Recommended Interest Rate (3-25%)
- **8 Expert-Derived Rules**: Based on banking industry best practices
- **Comprehensive Visualizations**: 
  - All membership functions
  - Complete inference process
  - Rule activation strengths
  - Defuzzification results
- **Three Decision Categories**: Approve, Review, Reject
- **Risk-Based Pricing**: Interest rates automatically adjusted based on risk profile

## 🏗️ System Architecture

The system follows a standard four-component fuzzy logic architecture:

```
Input Variables → Fuzzification → Inference Engine → Defuzzification → Output
                      ↓               ↓
                 Membership      Fuzzy Rules
                  Functions
```

### Components:

1. **Fuzzification**: Converts crisp input values into fuzzy membership degrees
2. **Rule Base**: 8 IF-THEN rules encoding banking expertise
3. **Inference Engine**: Mamdani inference with min-max operations
4. **Defuzzification**: Centroid method for crisp output generation

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/fuzzy-loan-approval.git
cd fuzzy-loan-approval
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the example:
```bash
python fuzzy_loan_controller.py
```

## 🚀 Usage

### Basic Usage

```python
from fuzzy_loan_controller import FuzzyLoanController

# Initialize the controller
flc = FuzzyLoanController()

# Define applicant data
applicant = {
    'credit_score': 720,
    'debt_ratio': 30,        # percentage
    'income': 75000,         # annual income in dollars
    'employment_duration': 5  # years
}

# Evaluate the application
result = flc.evaluate_loan_application(applicant)

# Display results
print(f"Decision: {result['decision']}")
print(f"Approval Score: {result['approval_score']}/100")
print(f"Interest Rate: {result['interest_rate']}%")
```

### Visualization

```python
# Visualize all membership functions
flc.visualize_all_membership_functions()

# Visualize complete inference process for an applicant
result = flc.evaluate_loan_application(applicant)
flc.visualize_inference_process(result, "John Doe")
```

## 📊 Input Variables

| Variable | Range | Linguistic Terms | Description |
|----------|-------|------------------|-------------|
| **Credit Score** | 300-850 | Poor, Fair, Good, Excellent | FICO score indicating creditworthiness |
| **Debt Ratio** | 0-100% | Low, Medium, High | Debt-to-Income ratio |
| **Annual Income** | $0-$200,000 | Low, Medium, High | Yearly earnings |
| **Employment Duration** | 0-40 years | Short, Medium, Long | Length of continuous employment |

## 📈 Output Variables

| Variable | Range | Linguistic Terms | Description |
|----------|-------|------------------|-------------|
| **Approval Score** | 0-100 | Reject, Review, Approve | Continuous approval likelihood |
| **Interest Rate** | 3-25% | Low, Medium, High | Recommended APR based on risk |

### Decision Mapping:
- **Score 0-35**: REJECTED
- **Score 35-70**: REQUIRES REVIEW
- **Score 70-100**: APPROVED

## 📜 Fuzzy Rules

The system uses 8 expert-derived rules:

1. **Rule 1**: IF Credit Score is Excellent AND Debt Ratio is Low → Approve + Low Interest
2. **Rule 2**: IF Credit Score is Good AND Debt Ratio is Low AND Income is High → Approve + Low Interest
3. **Rule 3**: IF Credit Score is Good AND Debt Ratio is Medium AND Income is Medium/High → Approve + Medium Interest
4. **Rule 4**: IF Credit Score is Fair AND Debt Ratio is Low AND Employment is Long → Review + Medium Interest
5. **Rule 5**: IF Credit Score is Fair AND Debt Ratio is Medium → Review + Medium Interest
6. **Rule 6**: IF Credit Score is Poor OR Debt Ratio is High → Reject + High Interest
7. **Rule 7**: IF Income is Low AND Employment is Short → Reject + High Interest
8. **Rule 8**: IF Credit Score is Excellent AND Debt Ratio is Medium → Approve + Medium Interest

## 💡 Examples

### Example 1: High-Quality Applicant
```python
inputs = {
    'credit_score': 780,
    'debt_ratio': 15,
    'income': 85000,
    'employment_duration': 8
}
# Result: APPROVED, Score: 85.88/100, Interest: 5.49%
```

### Example 2: Medium-Quality Applicant
```python
inputs = {
    'credit_score': 650,
    'debt_ratio': 35,
    'income': 50000,
    'employment_duration': 3
}
# Result: REQUIRES REVIEW, Score: 52.75/100, Interest: 12.87%
```

### Example 3: Poor-Quality Applicant
```python
inputs = {
    'credit_score': 450,
    'debt_ratio': 60,
    'income': 25000,
    'employment_duration': 1
}
# Result: REJECTED, Score: 18.23/100, Interest: 21.05%
```

## 📁 Project Structure

```
fuzzy-loan-approval/
│
├── fuzzy_loan_controller.py    # Main fuzzy logic implementation
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── LICENSE                      # MIT License
├── .gitignore                   # Git ignore rules
│
├── docs/                        # Documentation
│   └── LOAN_APPROVAL_SYSTEM_REPORT.pdf  # Detailed technical report
│
└── examples/                    # Example scripts
    └── demo.py                  # Demonstration script
```

## 🔧 Technical Details

### Membership Functions

The system uses both triangular and trapezoidal membership functions:

- **Trapezoidal**: Used for boundary categories (e.g., "Poor" credit, "Excellent" credit)
- **Triangular**: Used for middle categories with clear peaks

### Inference Method

- **Type**: Mamdani fuzzy inference
- **AND operator**: min() function
- **OR operator**: max() function
- **Aggregation**: Maximum composition
- **Defuzzification**: Centroid method (center of gravity)

### Key Algorithms

**Centroid Defuzzification Formula**:
```
centroid = Σ(x × μ(x)) / Σμ(x)
```

Where:
- x = values in the universe of discourse
- μ(x) = aggregated membership function value at x

## 🔮 Future Enhancements

- [ ] **Expanded Rule Base**: Add more sophisticated scenarios and edge cases
- [ ] **Adaptive Learning**: Implement ANFIS for automatic rule optimization
- [ ] **Weighted Rules**: Allow different rules to have varying importance
- [ ] **Additional Inputs**: Include loan amount, collateral value, payment history
- [ ] **Web Interface**: Build a user-friendly web application
- [ ] **API Development**: Create RESTful API for integration
- [ ] **Database Integration**: Store and analyze historical decisions
- [ ] **Explainability Dashboard**: Enhanced visualization of decision reasoning

## 🤝 Contributing

This is an academic project, but suggestions and improvements are welcome! Feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

**Course**: SAIA 1193 - Computational Intelligence  
**Institution**: Universiti Teknologi Malaysia (UTM)  
**Faculty**: Faculty of Artificial Intelligence  
**Semester**: 2024/2025-2

**Group Members**:
- Amina Asyiffa Binti Aspiyah Mahyus (A24AI0015)
- Farin Batrisyia Binti Saipul Nizam (A24AI0030)
- Le Yong Xiang (A24AI0045)
- Muhammad Danish Iqbal Bin Mohamad Hassan (A24AI0052)
- Wan Alif Danial Bin Wan Kamarulfarid (A24AI0093)

### References

- Angraini, N., Rosalina, K., & Kosasih, A. (2024). Optimizing Loan Approval Processes with Support Vector Machines (SVM)
- Sope, D. R., & Fujio, M. (2023). On fuzzification and optimization problems of clustering indices
- Kgatwe, C., et al. (2023). Fuzzy Inference Engine in Condition Monitoring of Industrial Equipment
- Mitsuishi, T. (2022). Definition of Centroid Method as Defuzzification

---

**⭐ If you found this project helpful, please consider giving it a star!**

For questions or feedback, please open an issue on GitHub.

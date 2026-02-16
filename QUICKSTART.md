# Quick Start Guide

## Getting Started in 5 Minutes

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/fuzzy-loan-approval.git
cd fuzzy-loan-approval

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Demo

```bash
python examples/demo.py
```

This will show you three example loan applications with visualizations.

### 3. Try Your Own Example

Create a new Python file (e.g., `my_test.py`):

```python
from fuzzy_loan_controller import FuzzyLoanController

# Create controller
flc = FuzzyLoanController()

# Define your applicant
my_applicant = {
    'credit_score': 700,      # FICO score (300-850)
    'debt_ratio': 25,          # Percentage (0-100)
    'income': 60000,           # Annual income in dollars
    'employment_duration': 4   # Years of employment
}

# Evaluate
result = flc.evaluate_loan_application(my_applicant)

# Print results
print(f"Decision: {result['decision']}")
print(f"Approval Score: {result['approval_score']}/100")
print(f"Recommended Interest Rate: {result['interest_rate']}%")

# Visualize (optional)
flc.visualize_inference_process(result, "My Application")
```

### 4. Understanding the Inputs

| Input | Valid Range | What It Means |
|-------|-------------|---------------|
| **credit_score** | 300-850 | Your FICO credit score. Higher = better |
| **debt_ratio** | 0-100 | Percentage of monthly income that goes to debt payments |
| **income** | 0-200000 | Your annual income in dollars |
| **employment_duration** | 0-40 | How many years you've been employed |

### 5. Understanding the Outputs

**Decision Types:**
- `APPROVED`: Loan is approved (score ≥ 70)
- `REQUIRES REVIEW`: Borderline case, needs manual review (score 35-70)
- `REJECTED`: Loan is denied (score < 35)

**Approval Score:** A number from 0-100 indicating approval likelihood

**Interest Rate:** Recommended rate from 3% to 25% based on risk

### 6. Tips for Good Results

✅ **What helps approval:**
- High credit score (720+)
- Low debt ratio (<30%)
- Higher income
- Longer employment (5+ years)

❌ **What hurts approval:**
- Poor credit score (<580)
- High debt ratio (>45%)
- Low income
- Short employment (<2 years)

### 7. Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check the technical report in `docs/` folder
- Modify the fuzzy rules in `fuzzy_loan_controller.py` to experiment
- Create custom test cases

### Need Help?

- Open an issue on GitHub
- Check the examples folder for more use cases
- Review the inline code documentation

---

**Happy coding!** 🎉

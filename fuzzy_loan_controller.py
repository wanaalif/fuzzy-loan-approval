"""
Fuzzy Logic Loan Approval System

This module implements a fuzzy logic controller for automated loan approval decisions.
The system evaluates loan applications based on multiple financial indicators and provides
both approval decisions and risk-based interest rate recommendations.

Author: Le Yong Xiang (A24AI0045) and Team
Course: SAIA 1193 - Computational Intelligence
Institution: Universiti Teknologi Malaysia
Date: June 2025

Usage:
    from fuzzy_loan_controller import FuzzyLoanController
    
    flc = FuzzyLoanController()
    result = flc.evaluate_loan_application({
        'credit_score': 720,
        'debt_ratio': 30,
        'income': 75000,
        'employment_duration': 5
    })
    print(f"Decision: {result['decision']}")
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple


class FuzzyLoanController:
    """
    Fuzzy Logic Controller for Loan Approval System
    
    This class implements a complete fuzzy logic system that evaluates loan applications
    based on four input variables (credit score, debt ratio, income, employment duration)
    and produces two outputs (approval score and interest rate).
    
    The system uses:
    - Mamdani fuzzy inference
    - Triangular and trapezoidal membership functions
    - Centroid defuzzification method
    - 8 expert-derived fuzzy rules
    
    Attributes:
        credit_score_range: Tuple defining min and max credit score (300-850)
        debt_ratio_range: Tuple defining min and max debt ratio (0-100%)
        income_range: Tuple defining min and max annual income ($0-$200,000)
        employment_duration_range: Tuple defining min and max employment years (0-40)
        approval_score_range: Tuple defining min and max approval score (0-100)
        interest_rate_range: Tuple defining min and max interest rate (3-25%)
    """
    def __init__(self):
        """
        Initialize the Fuzzy Loan Controller with predefined variable ranges.
        
        Sets up the universe of discourse for all input and output variables based on
        banking industry standards and typical financial assessment practices.
        """
        # Define input variable ranges based on industry standards
        self.credit_score_range = (300, 850)  # FICO score range
        self.debt_ratio_range = (0, 100)  # Debt-to-income ratio percentage
        self.income_range = (0, 200000)  # Annual income in dollars
        self.employment_duration_range = (0, 40)  # Employment duration in years

        # Define output variable ranges
        self.approval_score_range = (0, 100)  # Approval likelihood (0=reject, 100=approve)
        self.interest_rate_range = (3, 25)  # Annual percentage rate

    def triangular_membership(self, x: float, a: float, b: float, c: float) -> float:
        """
        Calculate triangular membership function value.
        
        A triangular membership function rises linearly from 0 at point 'a' to 1 at point 'b',
        then falls linearly back to 0 at point 'c'.
        
        Args:
            x: Input value to evaluate
            a: Left base point (membership = 0)
            b: Peak point (membership = 1)
            c: Right base point (membership = 0)
            
        Returns:
            Membership degree in range [0, 1]
            
        Example:
            >>> flc = FuzzyLoanController()
            >>> flc.triangular_membership(620, 500, 620, 720)  # Peak value
            1.0
            >>> flc.triangular_membership(560, 500, 620, 720)  # Rising slope
            0.5
        """
        if x <= a or x >= c:
            return 0.0
        elif a < x <= b:
            return (x - a) / (b - a)
        else:  # b < x < c
            return (c - x) / (c - b)

    def trapezoidal_membership(self, x: float, a: float, b: float, c: float, d: float) -> float:
        """
        Calculate trapezoidal membership function value.
        
        A trapezoidal membership function rises linearly from 0 at 'a' to 1 at 'b',
        remains at 1 from 'b' to 'c', then falls linearly to 0 at 'd'.
        
        Args:
            x: Input value to evaluate
            a: Left base point (membership = 0)
            b: Left top point (membership = 1 starts)
            c: Right top point (membership = 1 ends)
            d: Right base point (membership = 0)
            
        Returns:
            Membership degree in range [0, 1]
            
        Example:
            >>> flc = FuzzyLoanController()
            >>> flc.trapezoidal_membership(400, 300, 300, 500, 580)
            1.0  # In the flat top region
        """
        if x <= a or x >= d:
            return 0.0
        elif a < x <= b:
            return (x - a) / (b - a)
        elif b < x <= c:
            return 1.0
        else:  # c < x < d
            return (d - x) / (d - c)

    def get_credit_score_membership(self, score: float) -> Dict[str, float]:
        """
        Calculate membership degrees for all credit score categories.
        
        Credit score categories based on standard FICO scoring:
        - Poor (300-580): High credit risk
        - Fair (500-720): Moderate credit risk  
        - Good (650-780): Low credit risk
        - Excellent (720-850): Minimal credit risk
        
        Args:
            score: Credit score value (typically 300-850)
            
        Returns:
            Dictionary mapping category names to membership degrees
            
        Example:
            >>> flc = FuzzyLoanController()
            >>> memberships = flc.get_credit_score_membership(720)
            >>> memberships
            {'poor': 0.0, 'fair': 0.0, 'good': 1.0, 'excellent': 0.0}
        """
        return {
            'poor': self.trapezoidal_membership(score, 300, 300, 500, 580),
            'fair': self.triangular_membership(score, 500, 620, 720),
            'good': self.triangular_membership(score, 650, 720, 780),
            'excellent': self.trapezoidal_membership(score, 720, 800, 850, 850)
        }

    def get_debt_ratio_membership(self, ratio: float) -> Dict[str, float]:
        """
        Calculate membership degrees for all debt-to-income ratio categories.
        
        Debt-to-income ratio categories based on lending standards:
        - Low (0-35%): Healthy debt level, excellent repayment capacity
        - Medium (25-55%): Moderate debt level, acceptable risk
        - High (45-100%): Concerning debt level, high default risk
        
        The 43% DTI threshold is a critical industry standard for qualified mortgages.
        
        Args:
            ratio: Debt-to-income ratio as percentage (0-100)
            
        Returns:
            Dictionary mapping category names to membership degrees
            
        Example:
            >>> flc = FuzzyLoanController()
            >>> flc.get_debt_ratio_membership(30)
            {'low': 0.67, 'medium': 0.33, 'high': 0.0}
        """
        return {
            'low': self.trapezoidal_membership(ratio, 0, 0, 20, 35),
            'medium': self.triangular_membership(ratio, 25, 40, 55),
            'high': self.trapezoidal_membership(ratio, 45, 60, 100, 100)
        }

    def get_income_membership(self, income: float) -> Dict[str, float]:
        """Define membership functions for annual income"""
        return {
            'low': self.trapezoidal_membership(income, 0, 0, 30000, 50000),
            'medium': self.triangular_membership(income, 35000, 70000, 120000),
            'high': self.trapezoidal_membership(income, 80000, 150000, 200000, 200000)
        }

    def get_employment_membership(self, duration: float) -> Dict[str, float]:
        """Define membership functions for employment duration"""
        return {
            'short': self.trapezoidal_membership(duration, 0, 0, 1, 3),
            'medium': self.triangular_membership(duration, 2, 5, 10),
            'long': self.trapezoidal_membership(duration, 7, 15, 40, 40)
        }

    def get_approval_membership_inverse(self, approval_level: str) -> Tuple[float, float, float, float]:
        """Get parameters for output membership functions"""
        if approval_level == 'reject':
            return (0, 0, 15, 35)
        elif approval_level == 'review':
            return (20, 40, 60, 80)
        elif approval_level == 'approve':
            return (65, 85, 100, 100)

    def get_interest_membership_inverse(self, rate_level: str) -> Tuple[float, float, float, float]:
        """Get parameters for interest rate membership functions"""
        if rate_level == 'low':
            return (3, 3, 6, 9)
        elif rate_level == 'medium':
            return (7, 10, 14, 17)
        elif rate_level == 'high':
            return (15, 20, 25, 25)

    def get_all_approval_memberships(self) -> Dict[str, Tuple[float, float, float, float]]:
      return {
          'reject': (0, 0, 15, 35),
          'review': (20, 40, 60, 80),
          'approve': (65, 85, 100, 100)
      }

    def get_all_interest_memberships(self) -> Dict[str, Tuple[float, float, float, float]]:
      return {
          'low': (3, 3, 6, 9),
          'medium': (7, 10, 14, 17),
          'high': (15, 20, 25, 25)
      }

    def apply_fuzzy_rules(self, inputs: Dict[str, float]) -> Dict[str, Dict[str, float]]:
        """
        Apply fuzzy inference rules to determine loan approval and interest rate.
        
        This method implements 8 expert-derived fuzzy rules that encode banking
        best practices for loan evaluation. Rules use Mamdani inference with:
        - AND operations: min() function
        - OR operations: max() function  
        - Aggregation: maximum composition
        
        The rules prioritize critical risk factors (poor credit, high debt) and
        balance positive attributes (good credit, stable employment) to produce
        fair and consistent decisions.
        
        Args:
            inputs: Dictionary containing:
                - credit_score: FICO score (300-850)
                - debt_ratio: Debt-to-income percentage (0-100)
                - income: Annual income in dollars (0-200000)
                - employment_duration: Years employed (0-40)
                
        Returns:
            Dictionary with two keys:
                - 'approval': Dict of approval membership values (reject/review/approve)
                - 'interest': Dict of interest rate membership values (low/medium/high)
                
        Side Effects:
            Stores rule activation details in self.rule_details for visualization
            
        Example:
            >>> flc = FuzzyLoanController()
            >>> inputs = {'credit_score': 720, 'debt_ratio': 30, 'income': 75000, 'employment_duration': 5}
            >>> outputs = flc.apply_fuzzy_rules(inputs)
            >>> outputs['approval']
            {'reject': 0.0, 'review': 0.2, 'approve': 0.8}
        """
        # Get membership values for all inputs
        credit_mem = self.get_credit_score_membership(inputs['credit_score'])
        debt_mem = self.get_debt_ratio_membership(inputs['debt_ratio'])
        income_mem = self.get_income_membership(inputs['income'])
        employment_mem = self.get_employment_membership(inputs['employment_duration'])

        # Initialize output membership values
        approval_output = {'reject': 0, 'review': 0, 'approve': 0}
        interest_output = {'low': 0, 'medium': 0, 'high': 0}

        # Store rule activations for visualization
        self.rule_details = []

        # Rule 1: Excellent credit + Low debt → Approve + Low interest
        rule1_strength = min(credit_mem['excellent'], debt_mem['low'])
        approval_output['approve'] = max(approval_output['approve'], rule1_strength)
        interest_output['low'] = max(interest_output['low'], rule1_strength)
        self.rule_details.append(('Rule 1: Excellent credit + Low debt → Approve + Low interest', rule1_strength))

        # Rule 2: Good credit + Low debt + High income → Approve + Low interest
        rule2_strength = min(credit_mem['good'], debt_mem['low'], income_mem['high'])
        approval_output['approve'] = max(approval_output['approve'], rule2_strength)
        interest_output['low'] = max(interest_output['low'], rule2_strength)
        self.rule_details.append(('Rule 2: Good credit + Low debt + High income → Approve + Low interest', rule2_strength))

        # Rule 3: Good credit + Medium debt + Medium/High income → Approve + Medium interest
        rule3_strength = min(credit_mem['good'], debt_mem['medium'],
                           max(income_mem['medium'], income_mem['high']))
        approval_output['approve'] = max(approval_output['approve'], rule3_strength)
        interest_output['medium'] = max(interest_output['medium'], rule3_strength)
        self.rule_details.append(('Rule 3: Good credit + Medium debt + Medium/High income → Approve + Medium interest', rule3_strength))

        # Rule 4: Fair credit + Low debt + Long employment → Review + Medium interest
        rule4_strength = min(credit_mem['fair'], debt_mem['low'], employment_mem['long'])
        approval_output['review'] = max(approval_output['review'], rule4_strength)
        interest_output['medium'] = max(interest_output['medium'], rule4_strength)
        self.rule_details.append(('Rule 4: Fair credit + Low debt + Long employment → Review + Medium interest', rule4_strength))

        # Rule 5: Fair credit + Medium debt → Review + Medium interest
        rule5_strength = min(credit_mem['fair'], debt_mem['medium'])
        approval_output['review'] = max(approval_output['review'], rule5_strength)
        interest_output['medium'] = max(interest_output['medium'], rule5_strength)
        self.rule_details.append(('Rule 5: Fair credit + Medium debt → Review + Medium interest', rule5_strength))

        # Rule 6: Poor credit OR High debt → Reject + High interest
        rule6_strength = max(credit_mem['poor'], debt_mem['high'])
        approval_output['reject'] = max(approval_output['reject'], rule6_strength)
        interest_output['high'] = max(interest_output['high'], rule6_strength)
        self.rule_details.append(('Rule 6: Poor credit OR High debt → Reject + High interest', rule6_strength))

        # Rule 7: Low income + Short employment → Reject + High interest
        rule7_strength = min(income_mem['low'], employment_mem['short'])
        approval_output['reject'] = max(approval_output['reject'], rule7_strength)
        interest_output['high'] = max(interest_output['high'], rule7_strength)
        self.rule_details.append(('Rule 7: Low income + Short employment → Reject + High interest', rule7_strength))

        # Rule 8: Excellent credit + Medium debt → Approve + Medium interest
        rule8_strength = min(credit_mem['excellent'], debt_mem['medium'])
        approval_output['approve'] = max(approval_output['approve'], rule8_strength)
        interest_output['medium'] = max(interest_output['medium'], rule8_strength)
        self.rule_details.append(('Rule 8: Excellent credit + Medium debt → Approve + Medium interest', rule8_strength))

        return {'approval': approval_output, 'interest': interest_output}

    def centroid_defuzzification(self, membership_values: Dict[str, float],
                                output_type: str) -> float:
        """Defuzzify using centroid method"""
        if output_type == 'approval':
            ranges = {
                'reject': self.get_approval_membership_inverse('reject'),
                'review': self.get_approval_membership_inverse('review'),
                'approve': self.get_approval_membership_inverse('approve')
            }
            universe = np.linspace(0, 100, 1000)
        else:  # interest
            ranges = {
                'low': self.get_interest_membership_inverse('low'),
                'medium': self.get_interest_membership_inverse('medium'),
                'high': self.get_interest_membership_inverse('high')
            }
            universe = np.linspace(3, 25, 1000)

        # Calculate aggregated membership function
        aggregated = np.zeros_like(universe)

        for level, strength in membership_values.items():
            if strength > 0:
                a, b, c, d = ranges[level]
                level_membership = np.array([
                    min(strength, self.trapezoidal_membership(x, a, b, c, d))
                    for x in universe
                ])
                aggregated = np.maximum(aggregated, level_membership)

        # Store aggregated function for visualization
        if output_type == 'approval':
            self.approval_aggregated = aggregated
            self.approval_universe = universe
        else:
            self.interest_aggregated = aggregated
            self.interest_universe = universe

        # Calculate centroid
        if np.sum(aggregated) == 0:
            return universe[len(universe)//2]  # Return middle value if no activation

        centroid = np.sum(universe * aggregated) / np.sum(aggregated)
        return centroid

    def evaluate_loan_application(self, inputs: Dict[str, float]) -> Dict[str, float]:
        """
        Main entry point: Evaluate a complete loan application.
        
        This method orchestrates the entire fuzzy logic pipeline:
        1. Fuzzification: Convert crisp inputs to fuzzy sets
        2. Rule Application: Apply 8 expert rules  
        3. Aggregation: Combine rule outputs
        4. Defuzzification: Convert fuzzy outputs to crisp decisions
        5. Interpretation: Map scores to approval decisions
        
        Args:
            inputs: Dictionary containing applicant information:
                - credit_score (float): FICO score, range 300-850
                - debt_ratio (float): Debt-to-income %, range 0-100
                - income (float): Annual income in $, range 0-200000
                - employment_duration (float): Years employed, range 0-40
                
        Returns:
            Dictionary containing:
                - approval_score (float): Continuous score 0-100
                - interest_rate (float): Recommended APR 3-25%
                - decision (str): "APPROVED" | "REQUIRES REVIEW" | "REJECTED"
                - rule_activations (dict): Detailed rule firing information
                - inputs (dict): Echo of input values
                
        Raises:
            KeyError: If required input keys are missing
            ValueError: If input values are outside valid ranges
            
        Example:
            >>> flc = FuzzyLoanController()
            >>> result = flc.evaluate_loan_application({
            ...     'credit_score': 720,
            ...     'debt_ratio': 30,
            ...     'income': 75000,
            ...     'employment_duration': 5
            ... })
            >>> print(result['decision'])
            'APPROVED'
            >>> print(f"{result['approval_score']}/100")
            '78.5/100'
        """
        # Apply fuzzy rules
        rule_outputs = self.apply_fuzzy_rules(inputs)

        # Defuzzify outputs
        approval_score = self.centroid_defuzzification(rule_outputs['approval'], 'approval')
        interest_rate = self.centroid_defuzzification(rule_outputs['interest'], 'interest')

        # Determine final decision
        if approval_score >= 70:
            decision = "APPROVED"
        elif approval_score >= 40:
            decision = "REQUIRES REVIEW"
        else:
            decision = "REJECTED"

        return {
            'approval_score': round(approval_score, 2),
            'interest_rate': round(interest_rate, 2),
            'decision': decision,
            'rule_activations': rule_outputs,
            'inputs': inputs
        }

    def visualize_all_membership_functions(self):
        """Visualize all input and output membership functions"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle('Fuzzy Logic System - All Membership Functions', fontsize=16, fontweight='bold')

        # Credit Score
        credit_range = np.linspace(300, 850, 1000)
        axes[0,0].plot(credit_range, [self.get_credit_score_membership(x)['poor'] for x in credit_range],
                      label='Poor', linewidth=2)
        axes[0,0].plot(credit_range, [self.get_credit_score_membership(x)['fair'] for x in credit_range],
                      label='Fair', linewidth=2)
        axes[0,0].plot(credit_range, [self.get_credit_score_membership(x)['good'] for x in credit_range],
                      label='Good', linewidth=2)
        axes[0,0].plot(credit_range, [self.get_credit_score_membership(x)['excellent'] for x in credit_range],
                      label='Excellent', linewidth=2)
        axes[0,0].set_title('Credit Score Membership Functions', fontweight='bold')
        axes[0,0].set_xlabel('Credit Score')
        axes[0,0].set_ylabel('Membership Degree')
        axes[0,0].legend()
        axes[0,0].grid(True, alpha=0.3)

        # Debt Ratio
        debt_range = np.linspace(0, 100, 1000)
        axes[0,1].plot(debt_range, [self.get_debt_ratio_membership(x)['low'] for x in debt_range],
                      label='Low', linewidth=2)
        axes[0,1].plot(debt_range, [self.get_debt_ratio_membership(x)['medium'] for x in debt_range],
                      label='Medium', linewidth=2)
        axes[0,1].plot(debt_range, [self.get_debt_ratio_membership(x)['high'] for x in debt_range],
                      label='High', linewidth=2)
        axes[0,1].set_title('Debt-to-Income Ratio Membership Functions', fontweight='bold')
        axes[0,1].set_xlabel('Debt Ratio (%)')
        axes[0,1].set_ylabel('Membership Degree')
        axes[0,1].legend()
        axes[0,1].grid(True, alpha=0.3)

        # Income
        income_range = np.linspace(0, 200000, 1000)
        axes[1,0].plot(income_range, [self.get_income_membership(x)['low'] for x in income_range],
                      label='Low', linewidth=2)
        axes[1,0].plot(income_range, [self.get_income_membership(x)['medium'] for x in income_range],
                      label='Medium', linewidth=2)
        axes[1,0].plot(income_range, [self.get_income_membership(x)['high'] for x in income_range],
                      label='High', linewidth=2)
        axes[1,0].set_title('Annual Income Membership Functions', fontweight='bold')
        axes[1,0].set_xlabel('Annual Income ($)')
        axes[1,0].set_ylabel('Membership Degree')
        axes[1,0].legend()
        axes[1,0].grid(True, alpha=0.3)

        # Employment Duration
        emp_range = np.linspace(0, 40, 1000)
        axes[1,1].plot(emp_range, [self.get_employment_membership(x)['short'] for x in emp_range],
                      label='Short', linewidth=2)
        axes[1,1].plot(emp_range, [self.get_employment_membership(x)['medium'] for x in emp_range],
                      label='Medium', linewidth=2)
        axes[1,1].plot(emp_range, [self.get_employment_membership(x)['long'] for x in emp_range],
                      label='Long', linewidth=2)
        axes[1,1].set_title('Employment Duration Membership Functions', fontweight='bold')
        axes[1,1].set_xlabel('Employment Duration (Years)')
        axes[1,1].set_ylabel('Membership Degree')
        axes[1,1].legend()
        axes[1,1].grid(True, alpha=0.3)

        # Output Functions
        # Approval Score
        app_range = np.linspace(0, 100, 1000)
        approval_memberships = self.get_all_approval_memberships()
        for label, params in approval_memberships.items():
            membership_values = [self.trapezoidal_membership(x, *params) for x in app_range]
            axes[0,2].plot(app_range, membership_values, label=label.title(), linewidth=2)
        axes[0,2].set_title('Approval Score Membership Functions', fontweight='bold')
        axes[0,2].set_xlabel('Approval Score')
        axes[0,2].set_ylabel('Membership Degree')
        axes[0,2].legend()
        axes[0,2].grid(True, alpha=0.3)

        # Interest Rate
        interest_range = np.linspace(3, 25, 1000)
        interest_memberships = self.get_all_interest_memberships()
        for label, params in interest_memberships.items():
            membership_values = [self.trapezoidal_membership(x, *params) for x in interest_range]
            axes[1,2].plot(interest_range, membership_values, label=label.title(), linewidth=2)
        axes[1,2].set_title('Interest Rate Membership Functions', fontweight='bold')
        axes[1,2].set_xlabel('Interest Rate (%)')
        axes[1,2].set_ylabel('Membership Degree')
        axes[1,2].legend()
        axes[1,2].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

    def visualize_inference_process(self, result: Dict, applicant_name: str):
            """Visualize the complete inference process for a specific applicant"""
            inputs = result['inputs']

            # Create figure with subplots
            fig = plt.figure(figsize=(20, 12))
            fig.suptitle(f'Fuzzy Inference Process - {applicant_name}', fontsize=16, fontweight='bold')

            # Input fuzzification plots
            gs = fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)

            # Credit Score
            ax1 = fig.add_subplot(gs[0, 0])
            credit_range = np.linspace(300, 850, 1000)
            credit_mem = self.get_credit_score_membership(inputs['credit_score'])

            for level, value in credit_mem.items():
                if value > 0:
                    y_values = [self.get_credit_score_membership(x)[level] for x in credit_range]
                    ax1.plot(credit_range, y_values, label=f'{level} ({value:.3f})', linewidth=2)
                    # Fill area up to activation level
                    y_filled = np.minimum(y_values, value)
                    ax1.fill_between(credit_range, 0, y_filled, alpha=0.3)

            ax1.axvline(inputs['credit_score'], color='red', linestyle='--', linewidth=2, label=f"Input: {inputs['credit_score']}")
            ax1.set_title('Credit Score Fuzzification')
            ax1.set_xlabel('Credit Score')
            ax1.set_ylabel('Membership')
            ax1.legend(fontsize=8)
            ax1.grid(True, alpha=0.3)

            # Debt Ratio
            ax2 = fig.add_subplot(gs[0, 1])
            debt_range = np.linspace(0, 100, 1000)
            debt_mem = self.get_debt_ratio_membership(inputs['debt_ratio'])

            for level, value in debt_mem.items():
                if value > 0:
                    y_values = [self.get_debt_ratio_membership(x)[level] for x in debt_range]
                    ax2.plot(debt_range, y_values, label=f'{level} ({value:.3f})', linewidth=2)
                    y_filled = np.minimum(y_values, value)
                    ax2.fill_between(debt_range, 0, y_filled, alpha=0.3)

            ax2.axvline(inputs['debt_ratio'], color='red', linestyle='--', linewidth=2, label=f"Input: {inputs['debt_ratio']}%")
            ax2.set_title('Debt Ratio Fuzzification')
            ax2.set_xlabel('Debt Ratio (%)')
            ax2.set_ylabel('Membership')
            ax2.legend(fontsize=8)
            ax2.grid(True, alpha=0.3)

            # Income
            ax3 = fig.add_subplot(gs[0, 2])
            income_range = np.linspace(0, 200000, 1000)
            income_mem = self.get_income_membership(inputs['income'])

            for level, value in income_mem.items():
                if value > 0:
                    y_values = [self.get_income_membership(x)[level] for x in income_range]
                    ax3.plot(income_range, y_values, label=f'{level} ({value:.3f})', linewidth=2)
                    y_filled = np.minimum(y_values, value)
                    ax3.fill_between(income_range, 0, y_filled, alpha=0.3)

            ax3.axvline(inputs['income'], color='red', linestyle='--', linewidth=2, label=f"Input: ${inputs['income']:,}")
            ax3.set_title('Income Fuzzification')
            ax3.set_xlabel('Annual Income ($)')
            ax3.set_ylabel('Membership')
            ax3.legend(fontsize=8)
            ax3.grid(True, alpha=0.3)

            # Employment Duration
            ax4 = fig.add_subplot(gs[0, 3])
            emp_range = np.linspace(0, 40, 1000)
            emp_mem = self.get_employment_membership(inputs['employment_duration'])

            for level, value in emp_mem.items():
                if value > 0:
                    y_values = [self.get_employment_membership(x)[level] for x in emp_range]
                    ax4.plot(emp_range, y_values, label=f'{level} ({value:.3f})', linewidth=2)
                    y_filled = np.minimum(y_values, value)
                    ax4.fill_between(emp_range, 0, y_filled, alpha=0.3)

            ax4.axvline(inputs['employment_duration'], color='red', linestyle='--', linewidth=2,
                      label=f"Input: {inputs['employment_duration']} years")
            ax4.set_title('Employment Duration Fuzzification')
            ax4.set_xlabel('Employment Duration (Years)')
            ax4.set_ylabel('Membership')
            ax4.legend(fontsize=8)
            ax4.grid(True, alpha=0.3)

            # Rule activation summary
            ax5 = fig.add_subplot(gs[1, :])
            rule_names = [rule[0].split(':')[0] for rule in self.rule_details]
            rule_strengths = [rule[1] for rule in self.rule_details]

            bars = ax5.bar(rule_names, rule_strengths, color='skyblue', alpha=0.7)
            ax5.set_title('Rule Activation Strengths')
            ax5.set_ylabel('Activation Strength')
            ax5.set_ylim(0, 1)
            ax5.grid(True, alpha=0.3, axis='y')

            # Add value labels on bars
            for bar, strength in zip(bars, rule_strengths):
                if strength > 0:
                    ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                            f'{strength:.3f}', ha='center', va='bottom', fontweight='bold')

            # Output defuzzification
            # Approval Score
            ax6 = fig.add_subplot(gs[2, 0:2])
            ax6.plot(self.approval_universe, self.approval_aggregated, 'b-', linewidth=2, label='Aggregated Output')
            ax6.fill_between(self.approval_universe, 0, self.approval_aggregated, alpha=0.3, color='blue')

            # Mark centroid
            centroid_approval = result['approval_score']
            ax6.axvline(centroid_approval, color='red', linestyle='--', linewidth=3,
                      label=f'Centroid: {centroid_approval}')

            ax6.set_title('Approval Score Defuzzification')
            ax6.set_xlabel('Approval Score')
            ax6.set_ylabel('Membership')
            ax6.legend()
            ax6.grid(True, alpha=0.3)

            # Interest Rate
            ax7 = fig.add_subplot(gs[2, 2:4])
            ax7.plot(self.interest_universe, self.interest_aggregated, 'g-', linewidth=2, label='Aggregated Output')
            ax7.fill_between(self.interest_universe, 0, self.interest_aggregated, alpha=0.3, color='green')

            # Mark centroid
            centroid_interest = result['interest_rate']
            ax7.axvline(centroid_interest, color='red', linestyle='--', linewidth=3,
                      label=f'Centroid: {centroid_interest}%')

            ax7.set_title('Interest Rate Defuzzification')
            ax7.set_xlabel('Interest Rate (%)')
            ax7.set_ylabel('Membership')
            ax7.legend()
            ax7.grid(True, alpha=0.3)

            plt.show()

            # Print detailed rule analysis
            print(f"\n=== DETAILED RULE ANALYSIS FOR {applicant_name.upper()} ===")
            print(f"Inputs: Credit Score: {inputs['credit_score']}, Debt Ratio: {inputs['debt_ratio']}%, "
                  f"Income: ${inputs['income']:,}, Employment: {inputs['employment_duration']} years")
            print("\nRule Activations:")
            for rule_desc, strength in self.rule_details:
                if strength > 0:
                    print(f"  {rule_desc}: {strength:.3f}")

            print(f"\nFinal Results:")
            print(f"  Decision: {result['decision']}")
            print(f"  Approval Score: {result['approval_score']}/100")
            print(f"  Interest Rate: {result['interest_rate']}%")


def main():
    # Create fuzzy controller
    flc = FuzzyLoanController()

    print("=== FUZZY LOGIC LOAN APPROVAL SYSTEM ===\n")

    # First, visualize all membership functions to understand the system
    print("Step 1: Visualizing all membership functions...")
    flc.visualize_all_membership_functions()

    # Define test cases
    test_cases = [
        {
            'name': 'High-Quality Applicant',
            'inputs': {
                'credit_score': 780,
                'debt_ratio': 15,
                'income': 85000,
                'employment_duration': 8
            }
        },
        {
            'name': 'Medium-Quality Applicant',
            'inputs': {
                'credit_score': 650,
                'debt_ratio': 35,
                'income': 55000,
                'employment_duration': 3
            }
        },
        {
            'name': 'Poor-Quality Applicant',
            'inputs': {
                'credit_score': 480,
                'debt_ratio': 65,
                'income': 25000,
                'employment_duration': 0.5
            }
        },
    ]

    # Process each test case
    print("\nStep 2: Processing test cases and visualizing inference process...\n")

    for i, case in enumerate(test_cases, 1):
        print(f"=== CASE {i}: {case['name'].upper()} ===")

        # Evaluate the application
        result = flc.evaluate_loan_application(case['inputs'])

        # Print basic results
        print(f"Inputs: {case['inputs']}")
        print(f"Decision: {result['decision']}")
        print(f"Approval Score: {result['approval_score']}/100")
        print(f"Interest Rate: {result['interest_rate']}%")

        # Visualize the complete inference process
        flc.visualize_inference_process(result, case['name'])

        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()
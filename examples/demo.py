"""
Demo Script for Fuzzy Logic Loan Approval System

This script demonstrates the usage of the FuzzyLoanController with three
different applicant profiles: high-quality, medium-quality, and poor-quality.

Run this script to see how the fuzzy logic system evaluates different loan applications.
"""

import sys
import os

# Add parent directory to path to import the module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fuzzy_loan_controller import FuzzyLoanController


def print_separator():
    """Print a visual separator for better readability."""
    print("\n" + "=" * 80 + "\n")


def display_result(result: dict, applicant_name: str):
    """
    Display the evaluation result in a formatted way.
    
    Args:
        result: Dictionary containing evaluation results
        applicant_name: Name of the applicant for display
    """
    print(f"{'Decision:':<20} {result['decision']}")
    print(f"{'Approval Score:':<20} {result['approval_score']}/100")
    print(f"{'Interest Rate:':<20} {result['interest_rate']}%")
    
    # Add interpretation
    if result['decision'] == 'APPROVED':
        print(f"\n✓ {applicant_name} meets the approval criteria with a strong financial profile.")
    elif result['decision'] == 'REQUIRES REVIEW':
        print(f"\n⚠ {applicant_name}'s application requires manual review by a loan officer.")
    else:
        print(f"\n✗ {applicant_name}'s application does not meet current approval criteria.")


def main():
    """Run the demonstration with three example applicants."""
    
    print("=" * 80)
    print(" " * 20 + "FUZZY LOGIC LOAN APPROVAL SYSTEM")
    print(" " * 25 + "Demonstration Script")
    print("=" * 80)
    
    # Create fuzzy controller instance
    flc = FuzzyLoanController()
    
    # Visualize all membership functions first
    print("\nStep 1: Visualizing all membership functions...")
    print("(Close the plot window to continue)")
    flc.visualize_all_membership_functions()
    
    print_separator()
    
    # =========================================================================
    # Example 1: High-Quality Applicant
    # =========================================================================
    print("EXAMPLE 1: High-Quality Applicant")
    print("-" * 80)
    
    applicant_1 = {
        'credit_score': 780,
        'debt_ratio': 15,
        'income': 85000,
        'employment_duration': 8
    }
    
    print(f"{'Credit Score:':<25} {applicant_1['credit_score']}")
    print(f"{'Debt-to-Income Ratio:':<25} {applicant_1['debt_ratio']}%")
    print(f"{'Annual Income:':<25} ${applicant_1['income']:,}")
    print(f"{'Employment Duration:':<25} {applicant_1['employment_duration']} years")
    print()
    
    result_1 = flc.evaluate_loan_application(applicant_1)
    display_result(result_1, "This applicant")
    
    print("\nStep 2: Visualizing inference process...")
    print("(Close the plot window to continue)")
    flc.visualize_inference_process(result_1, "High-Quality Applicant")
    
    print_separator()
    
    # =========================================================================
    # Example 2: Medium-Quality Applicant
    # =========================================================================
    print("EXAMPLE 2: Medium-Quality Applicant")
    print("-" * 80)
    
    applicant_2 = {
        'credit_score': 650,
        'debt_ratio': 35,
        'income': 50000,
        'employment_duration': 3
    }
    
    print(f"{'Credit Score:':<25} {applicant_2['credit_score']}")
    print(f"{'Debt-to-Income Ratio:':<25} {applicant_2['debt_ratio']}%")
    print(f"{'Annual Income:':<25} ${applicant_2['income']:,}")
    print(f"{'Employment Duration:':<25} {applicant_2['employment_duration']} years")
    print()
    
    result_2 = flc.evaluate_loan_application(applicant_2)
    display_result(result_2, "This applicant")
    
    print("\nVisualizing inference process...")
    print("(Close the plot window to continue)")
    flc.visualize_inference_process(result_2, "Medium-Quality Applicant")
    
    print_separator()
    
    # =========================================================================
    # Example 3: Poor-Quality Applicant
    # =========================================================================
    print("EXAMPLE 3: Poor-Quality Applicant")
    print("-" * 80)
    
    applicant_3 = {
        'credit_score': 450,
        'debt_ratio': 60,
        'income': 25000,
        'employment_duration': 1
    }
    
    print(f"{'Credit Score:':<25} {applicant_3['credit_score']}")
    print(f"{'Debt-to-Income Ratio:':<25} {applicant_3['debt_ratio']}%")
    print(f"{'Annual Income:':<25} ${applicant_3['income']:,}")
    print(f"{'Employment Duration:':<25} {applicant_3['employment_duration']} year")
    print()
    
    result_3 = flc.evaluate_loan_application(applicant_3)
    display_result(result_3, "This applicant")
    
    print("\nVisualizing inference process...")
    print("(Close the plot window to continue)")
    flc.visualize_inference_process(result_3, "Poor-Quality Applicant")
    
    print_separator()
    
    # =========================================================================
    # Summary Comparison
    # =========================================================================
    print("SUMMARY: Comparison of All Applicants")
    print("-" * 80)
    print(f"{'Applicant':<25} {'Decision':<20} {'Score':<15} {'Interest Rate':<15}")
    print("-" * 80)
    print(f"{'High-Quality':<25} {result_1['decision']:<20} {result_1['approval_score']:<15} {result_1['interest_rate']}%")
    print(f"{'Medium-Quality':<25} {result_2['decision']:<20} {result_2['approval_score']:<15} {result_2['interest_rate']}%")
    print(f"{'Poor-Quality':<25} {result_3['decision']:<20} {result_3['approval_score']:<15} {result_3['interest_rate']}%")
    
    print_separator()
    print("Demonstration complete! Try modifying the applicant data or creating your own examples.")
    print("=" * 80)


if __name__ == "__main__":
    main()

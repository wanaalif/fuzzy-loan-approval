"""
Simple tests for the Fuzzy Logic Loan Approval System

Run these basic tests to verify the system is working correctly.
This is not a comprehensive test suite, but covers basic functionality.

Usage:
    python examples/test_basic.py
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fuzzy_loan_controller import FuzzyLoanController


def test_controller_initialization():
    """Test that the controller initializes correctly."""
    print("Test 1: Controller Initialization... ", end="")
    try:
        flc = FuzzyLoanController()
        assert flc.credit_score_range == (300, 850)
        assert flc.debt_ratio_range == (0, 100)
        assert flc.income_range == (0, 200000)
        assert flc.employment_duration_range == (0, 40)
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def test_membership_functions():
    """Test membership function calculations."""
    print("Test 2: Membership Functions... ", end="")
    try:
        flc = FuzzyLoanController()
        
        # Test triangular at peak
        result = flc.triangular_membership(620, 500, 620, 720)
        assert abs(result - 1.0) < 0.01, f"Expected 1.0, got {result}"
        
        # Test trapezoidal in flat region
        result = flc.trapezoidal_membership(400, 300, 300, 500, 580)
        assert abs(result - 1.0) < 0.01, f"Expected 1.0, got {result}"
        
        # Test membership outside range
        result = flc.triangular_membership(100, 500, 620, 720)
        assert abs(result - 0.0) < 0.01, f"Expected 0.0, got {result}"
        
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def test_excellent_applicant():
    """Test evaluation of an excellent applicant."""
    print("Test 3: Excellent Applicant Evaluation... ", end="")
    try:
        flc = FuzzyLoanController()
        result = flc.evaluate_loan_application({
            'credit_score': 800,
            'debt_ratio': 10,
            'income': 100000,
            'employment_duration': 10
        })
        
        assert result['decision'] == 'APPROVED', f"Expected APPROVED, got {result['decision']}"
        assert result['approval_score'] > 70, f"Expected score > 70, got {result['approval_score']}"
        assert result['interest_rate'] < 10, f"Expected rate < 10%, got {result['interest_rate']}"
        
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def test_poor_applicant():
    """Test evaluation of a poor applicant."""
    print("Test 4: Poor Applicant Evaluation... ", end="")
    try:
        flc = FuzzyLoanController()
        result = flc.evaluate_loan_application({
            'credit_score': 400,
            'debt_ratio': 70,
            'income': 20000,
            'employment_duration': 0.5
        })
        
        assert result['decision'] == 'REJECTED', f"Expected REJECTED, got {result['decision']}"
        assert result['approval_score'] < 40, f"Expected score < 40, got {result['approval_score']}"
        assert result['interest_rate'] > 15, f"Expected rate > 15%, got {result['interest_rate']}"
        
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def test_borderline_applicant():
    """Test evaluation of a borderline applicant."""
    print("Test 5: Borderline Applicant Evaluation... ", end="")
    try:
        flc = FuzzyLoanController()
        result = flc.evaluate_loan_application({
            'credit_score': 650,
            'debt_ratio': 35,
            'income': 50000,
            'employment_duration': 3
        })
        
        # Borderline cases should require review
        assert result['decision'] in ['REQUIRES REVIEW', 'APPROVED'], \
            f"Expected REQUIRES REVIEW or APPROVED, got {result['decision']}"
        assert 30 < result['approval_score'] < 80, \
            f"Expected score between 30-80, got {result['approval_score']}"
        
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def test_output_format():
    """Test that output has correct format."""
    print("Test 6: Output Format Validation... ", end="")
    try:
        flc = FuzzyLoanController()
        result = flc.evaluate_loan_application({
            'credit_score': 700,
            'debt_ratio': 30,
            'income': 60000,
            'employment_duration': 4
        })
        
        # Check all required keys exist
        required_keys = ['approval_score', 'interest_rate', 'decision', 'rule_activations', 'inputs']
        for key in required_keys:
            assert key in result, f"Missing key: {key}"
        
        # Check data types
        assert isinstance(result['approval_score'], (int, float))
        assert isinstance(result['interest_rate'], (int, float))
        assert isinstance(result['decision'], str)
        assert isinstance(result['rule_activations'], dict)
        
        # Check value ranges
        assert 0 <= result['approval_score'] <= 100
        assert 3 <= result['interest_rate'] <= 25
        assert result['decision'] in ['APPROVED', 'REQUIRES REVIEW', 'REJECTED']
        
        print("✓ PASSED")
        return True
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False


def run_all_tests():
    """Run all tests and report results."""
    print("=" * 70)
    print(" " * 15 + "FUZZY LOAN APPROVAL SYSTEM - BASIC TESTS")
    print("=" * 70)
    print()
    
    tests = [
        test_controller_initialization,
        test_membership_functions,
        test_excellent_applicant,
        test_poor_applicant,
        test_borderline_applicant,
        test_output_format
    ]
    
    results = [test() for test in tests]
    
    print()
    print("=" * 70)
    print(f"RESULTS: {sum(results)}/{len(results)} tests passed")
    print("=" * 70)
    
    if all(results):
        print("\n✓ All tests passed! The system is working correctly.")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the implementation.")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)

from decimal import Decimal
from typing import Dict

def calculate_score(
    test_cases_passed: int,
    total_test_cases: int,
    execution_time_ms: int,
    problem_points: int = 100,
    time_limit_ms: int = 2000
) -> Decimal:
    """
    Calculate score based on:
    1. Correctness (percentage of test cases passed)
    2. Execution time (faster = higher score)
    """
    # Factor 1: Correctness (0-100% of problem points)
    correctness_score = (test_cases_passed / total_test_cases) * problem_points if total_test_cases > 0 else 0
    
    # Factor 2: Execution time bonus (up to 10% bonus for fast execution)
    # Faster execution gets a bonus, normalized by time limit
    time_bonus = 0
    if execution_time_ms > 0 and time_limit_ms > 0:
        time_ratio = execution_time_ms / time_limit_ms
        # If execution is faster than 50% of time limit, give bonus
        if time_ratio < 0.5:
            time_bonus = (0.5 - time_ratio) * 0.2 * problem_points  # Up to 10% bonus
    
    total_score = Decimal(str(correctness_score + time_bonus))
    return total_score.quantize(Decimal('0.01'))


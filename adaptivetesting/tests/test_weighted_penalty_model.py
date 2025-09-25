"""
Comprehensive test suite for the weighted penalty model functions used in content balancing.

This module tests all functions related to content balancing penalty calculations,
including proportion calculations, penalty computations, standardization functions,
and weighted penalty value calculations.
"""

import unittest
import numpy as np
from unittest.mock import patch, MagicMock

from adaptivetesting.models import TestItem, ItemSelectionException
from adaptivetesting.math.content_balancing.__constraint import Constraint
from adaptivetesting.math.content_balancing.__functions import (
    compute_prop,
    compute_expected_difference,
    compute_penalty_value,
    compute_total_content_penalty_value_for_item,
    standardize_total_content_constraint_penalty_value,
    standardize_item_information,
    compute_information_penalty_value,
    compute_weighted_penalty_value
)


class TestWeightedPenaltyModel(unittest.TestCase):
    """
    Comprehensive test suite for weighted penalty model functions.
    
    This test class is organized into several test groups:
    1. Basic utility functions (proportion, expected difference)
    2. Penalty value calculations
    3. Standardization functions
    4. Integration and workflow tests
    """

    def setUp(self):
        """Set up comprehensive test fixtures for all test scenarios."""
        # Create diverse test items with different parameters
        self.item_math_algebra = self._create_test_item(
            item_id=1,
            a=1.5, b=-0.5, c=0.2, d=0.9,
            categories=["Math", "Algebra"]
        )

        self.item_english = self._create_test_item(
            item_id=2,
            a=1.2, b=0.3, c=0.1, d=1.0,
            categories=["English"]
        )

        self.item_science = self._create_test_item(
            item_id=3,
            a=2.0, b=0.0, c=0.15, d=1.0,
            categories=["Science"]
        )

        self.item_multiple_categories = self._create_test_item(
            item_id=4,
            a=1.8, b=-1.0, c=0.25, d=0.8,
            categories=["Math", "Science", "Advanced"]
        )

        # Create comprehensive constraint set
        self.constraint_math = Constraint(
            name="Math",
            weight=0.8,
            proportion=0.6,
            lower=0.4,
            upper=0.7
        )

        self.constraint_algebra = Constraint(
            name="Algebra",
            weight=0.5,
            proportion=0.3,
            lower=0.2,
            upper=0.4
        )

        self.constraint_english = Constraint(
            name="English",
            weight=1.0,
            proportion=0.8,
            lower=0.3,
            upper=0.9
        )

        self.constraint_science = Constraint(
            name="Science",
            weight=0.7,
            proportion=0.25,
            lower=0.1,
            upper=0.4
        )

        self.constraint_advanced = Constraint(
            name="Advanced",
            weight=1.2,
            proportion=0.15,
            lower=0.05,
            upper=0.25
        )

        self.all_constraints = [
            self.constraint_math,
            self.constraint_algebra, 
            self.constraint_english,
            self.constraint_science,
            self.constraint_advanced
        ]

    def _create_test_item(self, item_id: int, a: float, b: float, c: float, d: float, categories: list[str]) -> TestItem:
        """Helper method to create test items with consistent setup."""
        item = TestItem()
        item.id = item_id
        item.a = a
        item.b = b
        item.c = c
        item.d = d
        item.additional_properties = {"category": categories}
        return item

    # ===================================================================
    # GROUP 1: Basic Utility Function Tests
    # ===================================================================

    def test_compute_prop_standard_cases(self):
        """Test basic proportion calculation with standard scenarios."""
        # Standard case with some administered items
        result = compute_prop(n_administered=5, prevalence=0.3, n_remaining=10, test_length=20)
        expected = (5 + 0.3 * 10) / 20  # (5 + 3) / 20 = 0.4
        self.assertAlmostEqual(result, expected, places=6)

        # Different values to ensure calculation is correct
        result = compute_prop(n_administered=3, prevalence=0.5, n_remaining=12, test_length=15)
        expected = (3 + 0.5 * 12) / 15  # (3 + 6) / 15 = 0.6
        self.assertAlmostEqual(result, expected, places=6)

    def test_compute_prop_edge_cases(self):
        """Test proportion calculation with edge cases and boundary conditions."""
        # No items administered yet
        result = compute_prop(n_administered=0, prevalence=0.5, n_remaining=20, test_length=20)
        expected = (0 + 0.5 * 20) / 20  # 0.5
        self.assertAlmostEqual(result, expected)

        # All items administered (no remaining items)
        result = compute_prop(n_administered=20, prevalence=0.5, n_remaining=0, test_length=20)
        expected = (20 + 0.5 * 0) / 20  # 1.0
        self.assertAlmostEqual(result, expected)

        # Zero prevalence
        result = compute_prop(n_administered=5, prevalence=0.0, n_remaining=15, test_length=20)
        expected = (5 + 0.0 * 15) / 20  # 0.25
        self.assertAlmostEqual(result, expected)

        # Full prevalence (all remaining items have the constraint)
        result = compute_prop(n_administered=2, prevalence=1.0, n_remaining=8, test_length=10)
        expected = (2 + 1.0 * 8) / 10  # 1.0
        self.assertAlmostEqual(result, expected)

    def test_compute_prop_extreme_cases(self):
        """Test proportion calculation with extreme but valid inputs."""
        # Very small test
        result = compute_prop(n_administered=1, prevalence=0.5, n_remaining=1, test_length=2)
        expected = (1 + 0.5 * 1) / 2  # 0.75
        self.assertAlmostEqual(result, expected)

        # Very large test
        result = compute_prop(n_administered=500, prevalence=0.3, n_remaining=1500, test_length=2000)
        expected = (500 + 0.3 * 1500) / 2000  # (500 + 450) / 2000 = 0.475
        self.assertAlmostEqual(result, expected)

    def test_compute_expected_difference_standard_cases(self):
        """Test expected difference calculation with various scenarios."""
        # Positive difference (proportion exceeds target)
        result = compute_expected_difference(proportion=0.6, constraint_target=0.5)
        self.assertAlmostEqual(result, 0.1)

        # Negative difference (proportion below target)
        result = compute_expected_difference(proportion=0.3, constraint_target=0.7)
        self.assertAlmostEqual(result, -0.4)

        # Zero difference (exactly at target)
        result = compute_expected_difference(proportion=0.5, constraint_target=0.5)
        self.assertAlmostEqual(result, 0.0)

    def test_compute_expected_difference_extreme_cases(self):
        """Test expected difference calculation with extreme values."""
        # Maximum positive difference
        result = compute_expected_difference(proportion=1.0, constraint_target=0.0)
        self.assertAlmostEqual(result, 1.0)

        # Maximum negative difference
        result = compute_expected_difference(proportion=0.0, constraint_target=1.0)
        self.assertAlmostEqual(result, -1.0)

        # Very small differences (precision test)
        result = compute_expected_difference(proportion=0.501, constraint_target=0.5)
        self.assertAlmostEqual(result, 0.001, places=6)

    # ===================================================================
    # GROUP 2: Penalty Value Calculation Tests
    # ===================================================================

    def test_compute_penalty_value_within_bounds(self):
        """Test penalty value calculation when proportion is within acceptable bounds."""
        lower, upper = 0.3, 0.7
        mid = (upper + lower) / 2  # 0.5
        
        # Exactly at midpoint
        result = compute_penalty_value(prop=0.5, lower=lower, upper=upper)
        expected = 0.5 - mid  # 0.0
        self.assertAlmostEqual(result, expected, places=6)

        # Slightly above midpoint
        result = compute_penalty_value(prop=0.6, lower=lower, upper=upper)
        expected = 0.6 - mid  # 0.1
        self.assertAlmostEqual(result, expected, places=6)

        # Slightly below midpoint
        result = compute_penalty_value(prop=0.4, lower=lower, upper=upper)
        expected = 0.4 - mid  # -0.1
        self.assertAlmostEqual(result, expected, places=6)

    def test_compute_penalty_value_at_boundaries(self):
        """Test penalty value calculation exactly at boundary conditions."""
        lower, upper = 0.3, 0.7
        mid = (upper + lower) / 2  # 0.5

        # At lower bound (should be treated as within bounds)
        result = compute_penalty_value(prop=0.3, lower=lower, upper=upper)
        expected = 0.3 - mid  # -0.2
        self.assertAlmostEqual(result, expected, places=6)

        # Just above lower bound
        result = compute_penalty_value(prop=0.300001, lower=lower, upper=upper)
        expected = 0.300001 - mid
        self.assertAlmostEqual(result, expected, places=6)

    def test_compute_penalty_value_below_lower_bound(self):
        """Test penalty value calculation when proportion is below lower bound."""
        lower, upper = 0.3, 0.7
        prop = 0.2  # Below lower bound
        
        mid = (upper + lower) / 2  # 0.5
        d = lower - mid  # 0.3 - 0.5 = -0.2
        k = 2
        expected_diff = prop - mid  # 0.2 - 0.5 = -0.3
        
        # Based on actual implementation: (1 / (k * d)) * expected_diff^2 + (d / k)
        expected = (1 / (k * d)) * (expected_diff ** 2) + (d / k)
        # expected = (1 / (2 * -0.2)) * (-0.3)^2 + (-0.2 / 2)
        # expected = (1 / -0.4) * 0.09 + (-0.1)
        # expected = -2.5 * 0.09 - 0.1 = -0.225 - 0.1 = -0.325
        
        result = compute_penalty_value(prop=prop, lower=lower, upper=upper)
        self.assertAlmostEqual(result, expected, places=6)

    def test_compute_penalty_value_above_upper_bound(self):
        """Test penalty value calculation when proportion is above upper bound."""
        lower, upper = 0.3, 0.7
        prop = 0.8  # Above upper bound
        
        mid = (upper + lower) / 2  # 0.5
        a = upper - mid  # 0.7 - 0.5 = 0.2
        k = 2
        expected_diff = prop - mid  # 0.8 - 0.5 = 0.3
        
        # Based on actual implementation: (1 / (k * a)) * expected_diff^2 + (a / k)
        expected = (1 / (k * a)) * (expected_diff ** 2) + (a / k)
        # expected = (1 / (2 * 0.2)) * (0.3)^2 + (0.2 / 2)
        # expected = (1 / 0.4) * 0.09 + 0.1
        # expected = 2.5 * 0.09 + 0.1 = 0.225 + 0.1 = 0.325
        
        result = compute_penalty_value(prop=prop, lower=lower, upper=upper)
        self.assertAlmostEqual(result, expected, places=6)

    def test_compute_penalty_value_extreme_violations(self):
        """Test penalty value calculation with extreme constraint violations."""
        lower, upper = 0.4, 0.6
        
        # Very far below lower bound
        result = compute_penalty_value(prop=0.1, lower=lower, upper=upper)
        self.assertIsInstance(result, float)
        self.assertFalse(np.isnan(result))
        self.assertLess(result, 0)  # Should be negative penalty for being below

        # Very far above upper bound  
        result = compute_penalty_value(prop=0.9, lower=lower, upper=upper)
        self.assertIsInstance(result, float)
        self.assertFalse(np.isnan(result))
        self.assertGreater(result, 0)  # Should be positive penalty for being above

    def test_compute_penalty_value_narrow_bounds(self):
        """Test penalty value calculation with very narrow acceptable bounds."""
        lower, upper = 0.49, 0.51
        mid = (upper + lower) / 2  # 0.5
        
        # Within narrow bounds
        result = compute_penalty_value(prop=0.5, lower=lower, upper=upper)
        expected = 0.5 - mid  # 0.0
        self.assertAlmostEqual(result, expected, places=6)

        # Just outside narrow bounds (below)
        result = compute_penalty_value(prop=0.48, lower=lower, upper=upper)
        self.assertIsInstance(result, float)
        self.assertFalse(np.isnan(result))

    # ===================================================================
    # GROUP 3: Total Content Penalty Tests
    # ===================================================================

    def test_compute_total_content_penalty_value_single_constraint(self):
        """Test total content penalty calculation for items with single constraint."""
        # Mock penalty calculation to focus on the aggregation logic
        with patch('adaptivetesting.math.content_balancing.__functions.compute_penalty_value') as mock_penalty:
            mock_penalty.return_value = 0.15
            
            result = compute_total_content_penalty_value_for_item(
                item=self.item_english,  # Has only "English" category
                constraints=self.all_constraints
            )
            
            # Should only match English constraint with weight 1.0
            expected = 0.15 * 1.0
            self.assertAlmostEqual(result, expected, places=6)
            mock_penalty.assert_called_once()

    def test_compute_total_content_penalty_value_multiple_constraints(self):
        """Test total content penalty calculation for items with multiple constraints."""
        with patch('adaptivetesting.math.content_balancing.__functions.compute_penalty_value') as mock_penalty:
            # Return different penalty values for different constraints
            mock_penalty.side_effect = [0.1, 0.2]  # Math=0.1, Algebra=0.2
            
            result = compute_total_content_penalty_value_for_item(
                item=self.item_math_algebra,  # Has ["Math", "Algebra"] categories
                constraints=self.all_constraints
            )
            
            # Math: penalty=0.1, weight=0.8 -> 0.08
            # Algebra: penalty=0.2, weight=0.5 -> 0.10
            # Total: 0.08 + 0.10 = 0.18
            expected = 0.1 * 0.8 + 0.2 * 0.5
            self.assertAlmostEqual(result, expected, places=6)
            self.assertEqual(mock_penalty.call_count, 2)

    def test_compute_total_content_penalty_value_many_constraints(self):
        """Test total content penalty calculation for items with many constraints."""
        with patch('adaptivetesting.math.content_balancing.__functions.compute_penalty_value') as mock_penalty:
            # Return different penalty values for Math, Science, and Advanced
            mock_penalty.side_effect = [0.3, 0.1, 0.4]
            
            result = compute_total_content_penalty_value_for_item(
                item=self.item_multiple_categories,  # Has ["Math", "Science", "Advanced"]
                constraints=self.all_constraints
            )
            
            # Math: penalty=0.3, weight=0.8 -> 0.24
            # Science: penalty=0.1, weight=0.7 -> 0.07  
            # Advanced: penalty=0.4, weight=1.2 -> 0.48
            # Total: 0.24 + 0.07 + 0.48 = 0.79
            expected = 0.3 * 0.8 + 0.1 * 0.7 + 0.4 * 1.2
            self.assertAlmostEqual(result, expected, places=6)
            self.assertEqual(mock_penalty.call_count, 3)

    def test_compute_total_content_penalty_value_no_matching_constraints(self):
        """Test total content penalty calculation with no matching constraints."""
        # Create item with category not in any constraint
        item_orphan = self._create_test_item(
            item_id=99, a=1.0, b=0.0, c=0.0, d=1.0, 
            categories=["Unmatched", "Category"]
        )
        
        result = compute_total_content_penalty_value_for_item(
            item=item_orphan,
            constraints=self.all_constraints
        )
        
        # No matching constraints should result in zero penalty
        self.assertEqual(result, 0.0)

    def test_compute_total_content_penalty_value_constraint_bounds_validation(self):
        """Test that function validates constraint bounds are not None."""
        # Create constraint with None bounds
        invalid_constraint = Constraint(
            name="Math", weight=1.0, proportion=0.5, 
            lower=None, upper=0.7  # lower is None
        )
        
        with self.assertRaises(ValueError) as context:
            compute_total_content_penalty_value_for_item(
                item=self.item_math_algebra,
                constraints=[invalid_constraint]
            )
        self.assertIn("lower cannot be None", str(context.exception))

        # Test upper bound None
        invalid_constraint_upper = Constraint(
            name="Math", weight=1.0, proportion=0.5,
            lower=0.3, upper=None  # upper is None
        )
        
        with self.assertRaises(ValueError) as context:
            compute_total_content_penalty_value_for_item(
                item=self.item_math_algebra,
                constraints=[invalid_constraint_upper]
            )
        self.assertIn("upper cannot be None", str(context.exception))

    # ===================================================================
    # GROUP 4: Standardization Function Tests
    # ===================================================================

    def test_standardize_total_content_constraint_penalty_value_normal_cases(self):
        """Test standardization of content constraint penalty values in normal scenarios."""
        # Standard case: value in middle of range
        result = standardize_total_content_constraint_penalty_value(
            item_penality_value=0.6,
            min=0.2,
            max=1.0
        )
        expected = (0.6 - 0.2) / (1.0 - 0.2)  # 0.4 / 0.8 = 0.5
        self.assertAlmostEqual(result, expected, places=6)

        # Different range
        result = standardize_total_content_constraint_penalty_value(
            item_penality_value=0.75,
            min=0.5,
            max=1.5
        )
        expected = (0.75 - 0.5) / (1.5 - 0.5)  # 0.25 / 1.0 = 0.25
        self.assertAlmostEqual(result, expected, places=6)

    def test_standardize_total_content_constraint_penalty_value_boundary_cases(self):
        """Test standardization at boundary conditions."""
        # At minimum value
        result = standardize_total_content_constraint_penalty_value(
            item_penality_value=0.2,
            min=0.2,
            max=1.0
        )
        self.assertAlmostEqual(result, 0.0, places=6)

        # At maximum value
        result = standardize_total_content_constraint_penalty_value(
            item_penality_value=1.0,
            min=0.2,
            max=1.0
        )
        self.assertAlmostEqual(result, 1.0, places=6)

    def test_standardize_total_content_constraint_penalty_value_edge_cases(self):
        """Test standardization with edge cases and error conditions."""
        # Zero range (min == max) should cause division by zero
        with self.assertRaises(ZeroDivisionError):
            standardize_total_content_constraint_penalty_value(
                item_penality_value=0.5,
                min=0.5,
                max=0.5
            )

        # Negative values (valid mathematically)
        result = standardize_total_content_constraint_penalty_value(
            item_penality_value=-0.5,
            min=-1.0,
            max=0.0
        )
        expected = (-0.5 - (-1.0)) / (0.0 - (-1.0))  # 0.5 / 1.0 = 0.5
        self.assertAlmostEqual(result, expected, places=6)

        # Value outside range (above max)
        result = standardize_total_content_constraint_penalty_value(
            item_penality_value=1.5,
            min=0.2,
            max=1.0
        )
        expected = (1.5 - 0.2) / (1.0 - 0.2)  # 1.3 / 0.8 = 1.625
        self.assertAlmostEqual(result, expected, places=6)

        # Value outside range (below min)
        result = standardize_total_content_constraint_penalty_value(
            item_penality_value=0.1,
            min=0.2,
            max=1.0
        )
        expected = (0.1 - 0.2) / (1.0 - 0.2)  # -0.1 / 0.8 = -0.125
        self.assertAlmostEqual(result, expected, places=6)

    def test_standardize_item_information_normal_cases(self):
        """Test item information standardization in normal scenarios."""
        # Standard case
        result = standardize_item_information(item_information=0.8, max=2.0)
        expected = 0.8 / 2.0  # 0.4
        self.assertAlmostEqual(result, expected, places=6)

        # Different values
        result = standardize_item_information(item_information=1.5, max=3.0)
        expected = 1.5 / 3.0  # 0.5
        self.assertAlmostEqual(result, expected, places=6)

    def test_standardize_item_information_boundary_cases(self):
        """Test item information standardization at boundaries."""
        # Zero information
        result = standardize_item_information(item_information=0.0, max=2.0)
        self.assertAlmostEqual(result, 0.0, places=6)

        # Maximum information
        result = standardize_item_information(item_information=2.0, max=2.0)
        self.assertAlmostEqual(result, 1.0, places=6)

        # Information exceeds maximum (mathematically valid)
        result = standardize_item_information(item_information=3.0, max=2.0)
        self.assertAlmostEqual(result, 1.5, places=6)

    def test_standardize_item_information_error_cases(self):
        """Test item information standardization error conditions."""
        # Division by zero when max is zero
        with self.assertRaises(ZeroDivisionError):
            standardize_item_information(item_information=1.0, max=0.0)

        # Negative maximum (mathematically valid but unusual)
        result = standardize_item_information(item_information=1.0, max=-2.0)
        expected = 1.0 / -2.0  # -0.5
        self.assertAlmostEqual(result, expected, places=6)

    # ===================================================================
    # GROUP 5: Information Penalty Function Tests  
    # ===================================================================

    def test_compute_information_penalty_value_standard_cases(self):
        """Test information penalty value computation with standard inputs."""
        # Mid-range value
        result = compute_information_penalty_value(standardized_item_information=0.8)
        expected = -(0.8 ** 2)  # -0.64
        self.assertAlmostEqual(result, expected, places=6)

        # Different value
        result = compute_information_penalty_value(standardized_item_information=0.5)
        expected = -(0.5 ** 2)  # -0.25
        self.assertAlmostEqual(result, expected, places=6)

    def test_compute_information_penalty_value_boundary_cases(self):
        """Test information penalty value at boundary conditions."""
        # Zero information (no penalty)
        result = compute_information_penalty_value(standardized_item_information=0.0)
        self.assertAlmostEqual(result, 0.0, places=6)

        # Perfect information (maximum penalty)
        result = compute_information_penalty_value(standardized_item_information=1.0)
        self.assertAlmostEqual(result, -1.0, places=6)

    def test_compute_information_penalty_value_extreme_cases(self):
        """Test information penalty value with extreme inputs."""
        # Information above 1.0 (possible due to standardization issues)
        result = compute_information_penalty_value(standardized_item_information=1.5)
        expected = -(1.5 ** 2)  # -2.25
        self.assertAlmostEqual(result, expected, places=6)

        # Very small positive information
        result = compute_information_penalty_value(standardized_item_information=0.001)
        expected = -(0.001 ** 2)  # -0.000001
        self.assertAlmostEqual(result, expected, places=9)

        # Negative information (mathematically unusual but handled)
        result = compute_information_penalty_value(standardized_item_information=-0.5)
        expected = -((-0.5) ** 2)  # -0.25
        self.assertAlmostEqual(result, expected, places=6)

    # ===================================================================
    # GROUP 6: Weighted Penalty Function Tests
    # ===================================================================

    def test_compute_weighted_penalty_value_balanced_weights(self):
        """Test weighted penalty value computation with balanced weights."""
        result = compute_weighted_penalty_value(
            constraint_weight=0.5,
            standardized_constraint_penalty_value=0.4,
            information_weight=0.5,
            information_penalty_value=-0.6
        )
        expected = 0.5 * 0.4 + 0.5 * (-0.6)  # 0.2 - 0.3 = -0.1
        self.assertAlmostEqual(result, expected, places=6)

    def test_compute_weighted_penalty_value_constraint_focused(self):
        """Test weighted penalty value computation favoring constraint penalties."""
        result = compute_weighted_penalty_value(
            constraint_weight=0.8,
            standardized_constraint_penalty_value=0.6,
            information_weight=0.2,
            information_penalty_value=-0.8
        )
        expected = 0.8 * 0.6 + 0.2 * (-0.8)  # 0.48 - 0.16 = 0.32
        self.assertAlmostEqual(result, expected, places=6)

    def test_compute_weighted_penalty_value_information_focused(self):
        """Test weighted penalty value computation favoring information penalties."""
        result = compute_weighted_penalty_value(
            constraint_weight=0.2,
            standardized_constraint_penalty_value=0.7,
            information_weight=0.8,
            information_penalty_value=-0.9
        )
        expected = 0.2 * 0.7 + 0.8 * (-0.9)  # 0.14 - 0.72 = -0.58
        self.assertAlmostEqual(result, expected, places=6)

    def test_compute_weighted_penalty_value_extreme_weights(self):
        """Test weighted penalty value computation with extreme weight distributions."""
        # Only constraint weight (information weight = 0)
        result = compute_weighted_penalty_value(
            constraint_weight=1.0,
            standardized_constraint_penalty_value=0.5,
            information_weight=0.0,
            information_penalty_value=-0.8
        )
        self.assertAlmostEqual(result, 0.5, places=6)

        # Only information weight (constraint weight = 0)
        result = compute_weighted_penalty_value(
            constraint_weight=0.0,
            standardized_constraint_penalty_value=0.5,
            information_weight=1.0,
            information_penalty_value=-0.8
        )
        self.assertAlmostEqual(result, -0.8, places=6)

        # Both weights zero
        result = compute_weighted_penalty_value(
            constraint_weight=0.0,
            standardized_constraint_penalty_value=0.5,
            information_weight=0.0,
            information_penalty_value=-0.8
        )
        self.assertAlmostEqual(result, 0.0, places=6)

    def test_compute_weighted_penalty_value_negative_penalties(self):
        """Test weighted penalty value computation with negative penalty values."""
        result = compute_weighted_penalty_value(
            constraint_weight=0.6,
            standardized_constraint_penalty_value=-0.3,  # Negative constraint penalty
            information_weight=0.4,
            information_penalty_value=-0.7  # Negative information penalty
        )
        expected = 0.6 * (-0.3) + 0.4 * (-0.7)  # -0.18 - 0.28 = -0.46
        self.assertAlmostEqual(result, expected, places=6)

    def test_compute_weighted_penalty_value_weights_exceeding_one(self):
        """Test weighted penalty value computation with weights that sum to more than 1."""
        # Weights summing to more than 1.0 (mathematically valid)
        result = compute_weighted_penalty_value(
            constraint_weight=0.8,
            standardized_constraint_penalty_value=0.5,
            information_weight=0.7,  # Total weight = 1.5
            information_penalty_value=-0.4
        )
        expected = 0.8 * 0.5 + 0.7 * (-0.4)  # 0.4 - 0.28 = 0.12
        self.assertAlmostEqual(result, expected, places=6)

    # ===================================================================
    # GROUP 7: Integration and Workflow Tests
    # ===================================================================

    def test_complete_penalty_calculation_workflow(self):
        """Integration test for the complete weighted penalty calculation workflow."""
        # This test simulates a realistic end-to-end penalty calculation
        
        # Step 1: Calculate total content penalty using actual function (not mocked)
        # We'll use constraint with known bounds to get predictable results
        test_constraint = Constraint(
            name="Math",
            weight=0.8,
            proportion=0.4,  # This will be used in penalty calculation
            lower=0.3,
            upper=0.7
        )
        
        content_penalty = compute_total_content_penalty_value_for_item(
            item=self.item_math_algebra,
            constraints=[test_constraint]
        )
        
        # Step 2: Standardize content penalty (using realistic min/max)
        standardized_content_penalty = standardize_total_content_constraint_penalty_value(
            item_penality_value=content_penalty,
            min=-0.5,  # Realistic minimum penalty
            max=0.8    # Realistic maximum penalty
        )
        
        # Step 3: Calculate and standardize item information
        mock_item_information = 1.2  # Realistic information value
        standardized_information = standardize_item_information(
            item_information=mock_item_information,
            max=2.5  # Realistic maximum information
        )
        
        # Step 4: Calculate information penalty
        information_penalty = compute_information_penalty_value(standardized_information)
        
        # Step 5: Calculate weighted penalty
        weighted_penalty = compute_weighted_penalty_value(
            constraint_weight=0.6,
            standardized_constraint_penalty_value=standardized_content_penalty,
            information_weight=0.4,
            information_penalty_value=information_penalty
        )
        
        # Verify the result is mathematically valid
        self.assertIsInstance(weighted_penalty, float)
        self.assertFalse(np.isnan(weighted_penalty))
        self.assertFalse(np.isinf(weighted_penalty))

    def test_penalty_calculation_with_multiple_items_and_constraints(self):
        """Integration test comparing penalty calculations across multiple items."""
        penalties = {}
        
        # Calculate penalties for different items using the same constraints
        test_items = [
            self.item_math_algebra,
            self.item_english,
            self.item_science,
            self.item_multiple_categories
        ]
        
        # Use a subset of constraints for predictable results
        test_constraints = [self.constraint_math, self.constraint_english, self.constraint_science]
        
        for item in test_items:
            content_penalty = compute_total_content_penalty_value_for_item(
                item=item,
                constraints=test_constraints
            )
            penalties[item.id] = content_penalty
        
        # Verify all penalties are valid numbers
        for item_id, penalty in penalties.items():
            self.assertIsInstance(penalty, float)
            self.assertFalse(np.isnan(penalty))
            self.assertFalse(np.isinf(penalty))
        
        # Items with no matching constraints should have zero penalty
        # (item_science doesn't match any of our test constraints initially)
        # This assumes our test setup doesn't include Science in the first three constraints

    def test_standardization_workflow_robustness(self):
        """Test that standardization functions handle various realistic scenarios."""
        # Test various penalty value ranges
        penalty_values = [-0.8, -0.2, 0.0, 0.3, 0.9, 1.5]
        information_values = [0.0, 0.2, 0.8, 1.0, 1.3, 2.0]
        
        # Test content penalty standardization
        for penalty in penalty_values:
            result = standardize_total_content_constraint_penalty_value(
                item_penality_value=penalty,
                min=-1.0,
                max=2.0
            )
            self.assertIsInstance(result, float)
            self.assertFalse(np.isnan(result))
        
        # Test information standardization
        for info in information_values:
            result = standardize_item_information(
                item_information=info,
                max=2.5
            )
            self.assertIsInstance(result, float)
            self.assertFalse(np.isnan(result))
            
            # Test information penalty calculation
            info_penalty = compute_information_penalty_value(result)
            self.assertIsInstance(info_penalty, float)
            self.assertFalse(np.isnan(info_penalty))
            self.assertLessEqual(info_penalty, 0.0)  # Should always be negative or zero

    def test_edge_case_combinations(self):
        """Test combinations of edge cases that might occur in practice."""
        # Scenario 1: Item with constraints at exact boundaries
        boundary_constraint = Constraint(
            name="Math",
            weight=1.0,
            proportion=0.5,  # Exactly at midpoint
            lower=0.3,
            upper=0.7
        )
        
        penalty = compute_total_content_penalty_value_for_item(
            item=self.item_math_algebra,
            constraints=[boundary_constraint]
        )
        
        # Should be zero since proportion is at midpoint
        self.assertAlmostEqual(penalty, 0.0, places=6)
        
        # Scenario 2: Very narrow constraint bounds
        narrow_constraint = Constraint(
            name="Math",
            weight=0.5,
            proportion=0.501,  # Just above midpoint
            lower=0.499,
            upper=0.502
        )
        
        penalty = compute_total_content_penalty_value_for_item(
            item=self.item_math_algebra,
            constraints=[narrow_constraint]
        )
        
        self.assertIsInstance(penalty, float)
        self.assertFalse(np.isnan(penalty))


if __name__ == '__main__':
    unittest.main()
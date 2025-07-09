# Gamma Control Analysis Report

**Experiment:** gamma_experiment_20250702_113820
**Date:** 2025-07-02 11:38:27
**Mode:** Demonstration

## Executive Summary

- **Gamma range tested:** 1.0 - 800.0
- **Total tests:** 7
- **Total violations detected:** 23
- **Maximum penalty cost:** 800
- **Optimal gamma (min violations):** 200.0

## Gamma Control Effect

The gamma penalty mechanism demonstrates clear control over violation behavior:

- **γ = 1.0:** 8 violations, 15 total flow, penalty cost: 15
- **γ = 10.0:** 7 violations, 9 total flow, penalty cost: 90
- **γ = 50.0:** 3 violations, 3 total flow, penalty cost: 150
- **γ = 100.0:** 3 violations, 4 total flow, penalty cost: 400
- **γ = 200.0:** 0 violations, 0 total flow, penalty cost: 0
- **γ = 400.0:** 1 violations, 0 total flow, penalty cost: 0
- **γ = 800.0:** 1 violations, 1 total flow, penalty cost: 800

## Key Insights

1. **Low gamma values** lead to more violations as the penalty is 'cheaper' than compliance
2. **Medium gamma values** provide balanced trade-off between efficiency and compliance
3. **High gamma values** enforce strict compliance with zero or minimal violations
4. **Escape edges** serve as safety valves allowing controlled violations when necessary

## Flow Value Explanation

Flow values can exceed AGV count because:
- Multiple AGVs may violate the same restriction
- Single AGV may violate multiple times in different time windows
- Flow represents cumulative violation intensity across time and space

## Technical Details

- **Escape edge detection:** Identifies artificial edges with gamma costs
- **Flow analysis:** Measures actual usage of escape edges
- **Violation calculation:** Flow × Gamma = Penalty cost
- **Control mechanism:** Higher gamma → higher penalty → fewer violations

## Conclusion

Gamma control provides effective 'knob' for balancing operational efficiency with rule compliance. System designers can tune gamma values to achieve desired balance between strict adherence and practical flexibility.

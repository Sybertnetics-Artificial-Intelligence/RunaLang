# Fixed Income Module

The fixed income module provides comprehensive bond analysis capabilities including bond pricing, yield calculations, duration and convexity analysis, yield curve construction, term structure models, and credit risk assessment essential for fixed income investment and risk management.

## Overview

Fixed income securities represent debt instruments with predetermined cash flows. This module provides sophisticated mathematical tools for pricing bonds, analyzing interest rate sensitivity, constructing yield curves, and managing fixed income portfolios across various market conditions.

## Mathematical Foundation

### Bond Pricing Theory

The fundamental bond pricing equation discounts future cash flows:

**P = Σᵢ₌₁ⁿ CFᵢ/(1+y)ⁱ + FV/(1+y)ⁿ**

Where:
- P = Bond price
- CFᵢ = Coupon payment at time i
- FV = Face value
- y = Yield to maturity
- n = Number of periods

### Interest Rate Risk Measures

- **Duration**: Price sensitivity to yield changes (∂P/∂y × 1/P)
- **Modified Duration**: Duration/(1+y) for small yield changes
- **Convexity**: Second-order price sensitivity (∂²P/∂y² × 1/P)
- **DV01**: Dollar value of a basis point change

## Core Data Structures

### BondContract

Represents a bond with all relevant characteristics:

```runa
Type called "BondContract":
    bond_id as String                     Note: Unique bond identifier
    issuer as String                      Note: Bond issuer name
    coupon_rate as Float                  Note: Annual coupon rate (e.g., 0.05 for 5%)
    face_value as Float                   Note: Par value of the bond
    maturity_date as Integer              Note: Bond maturity timestamp
    issue_date as Integer                 Note: Bond issuance timestamp
    bond_type as String                   Note: "government", "corporate", "municipal"
    payment_frequency as Integer          Note: Payments per year (1, 2, 4, 12)
    credit_rating as String               Note: Credit rating (AAA, AA, A, BBB, etc.)
    callable as Boolean                   Note: Whether bond is callable
    putable as Boolean                    Note: Whether bond is putable
    call_schedules as List[CallSchedule]  Note: Call option details
    put_schedules as List[PutSchedule]    Note: Put option details
```

### YieldCurve

Represents the term structure of interest rates:

```runa
Type called "YieldCurve":
    curve_id as String                    Note: Yield curve identifier
    curve_date as Integer                 Note: Observation date
    curve_type as String                  Note: "government", "corporate", "swap"
    maturities as List[Float]             Note: Time to maturity (in years)
    yields as List[Float]                 Note: Corresponding yields
    interpolation_method as String        Note: "linear", "spline", "nelson_siegel"
    currency as String                    Note: Currency of the curve
    data_source as String                 Note: Source of yield data
```

## Basic Usage

### Bond Pricing and Yield Calculation

```runa
Use math.financial.fixed_income as FixedIncome

Note: Create a bond contract
Let corporate_bond be FixedIncome.create_bond_contract()
corporate_bond.coupon_rate = 0.045  Note: 4.5% annual coupon
corporate_bond.face_value = 1000.0
corporate_bond.payment_frequency = 2  Note: Semi-annual payments
corporate_bond.maturity_date = FixedIncome.add_years_to_date(FixedIncome.current_date(), 5)

Note: Calculate bond price given yield
Let market_yield be 0.04  Note: 4% yield to maturity
let bond_price be FixedIncome.calculate_bond_price(corporate_bond, market_yield)

Note: Calculate yield given price
Let market_price be 1050.0
Let yield_to_maturity be FixedIncome.calculate_yield_to_maturity(corporate_bond, market_price)
```

### Duration and Convexity Analysis

```runa
Note: Calculate risk measures
Let duration_measures be FixedIncome.calculate_duration_and_convexity(corporate_bond, market_yield)

Let macaulay_duration be duration_measures["macaulay_duration"]
Let modified_duration be duration_measures["modified_duration"]
Let convexity be duration_measures["convexity"]
Let dv01 be duration_measures["dv01"]
```

## Advanced Bond Pricing

### Present Value Calculation

```runa
Note: Comprehensive bond present value calculation
Process called "calculate_bond_present_value" that takes bond as BondContract, discount_yield as Float, settlement_date as Integer returns Dictionary[String, Float]:
    Let pricing_results be Dictionary[String, Float].create()
    
    Note: Calculate cash flow schedule
    Let cash_flows be FixedIncome.generate_cash_flow_schedule(bond)
    Let present_value be 0.0
    Let accrued_interest be 0.0
    
    Note: Handle settlement date and accrued interest
    Let days_since_last_payment be FixedIncome.days_between_dates(bond.last_payment_date, settlement_date)
    let days_in_period be 365 / bond.payment_frequency
    Let accrual_factor be Float.from_integer(days_since_last_payment) / Float.from_integer(days_in_period)
    
    If accrual_factor > 0.0:
        accrued_interest = bond.coupon_rate * bond.face_value * accrual_factor / Float.from_integer(bond.payment_frequency)
    
    Note: Discount each cash flow
    For cash_flow in cash_flows:
        Let payment_date be cash_flow["payment_date"]
        let payment_amount be cash_flow["payment_amount"]
        let years_to_payment be FixedIncome.years_between_dates(settlement_date, payment_date)
        
        Note: Calculate discount factor
        Let discount_factor be 1.0 / FixedIncome.power(1.0 + discount_yield / Float.from_integer(bond.payment_frequency), years_to_payment * Float.from_integer(bond.payment_frequency))
        
        present_value = present_value + payment_amount * discount_factor
    
    pricing_results["present_value"] = present_value
    pricing_results["accrued_interest"] = accrued_interest
    pricing_results["clean_price"] = present_value - accrued_interest
    pricing_results["dirty_price"] = present_value
    
    Return pricing_results
```

### Yield to Maturity Calculation

```runa
Note: Calculate yield to maturity using Newton-Raphson method
Process called "calculate_ytm_newton_raphson" that takes bond as BondContract, market_price as Float returns Float:
    Let tolerance be 1e-8
    Let max_iterations be 100
    Let initial_yield be 0.05  Note: Start with 5% yield estimate
    
    let current_yield be initial_yield
    
    For iteration from 1 to max_iterations:
        Note: Calculate price and price derivative at current yield
        Let calculated_price be FixedIncome.calculate_bond_price_internal(bond, current_yield)
        Let price_derivative be FixedIncome.calculate_price_derivative(bond, current_yield)
        
        Let price_difference be calculated_price - market_price
        
        If FixedIncome.abs(price_difference) < tolerance:
            Return current_yield
        
        If FixedIncome.abs(price_derivative) < 1e-10:
            Return -1.0  Note: Derivative too small, convergence issues
        
        Note: Newton-Raphson update
        current_yield = current_yield - price_difference / price_derivative
        
        Note: Keep yield positive and reasonable
        current_yield = FixedIncome.max(0.0001, FixedIncome.min(current_yield, 1.0))
    
    Return -1.0  Note: Failed to converge
```

### Duration Calculation

```runa
Note: Calculate Macaulay and modified duration
Process called "calculate_comprehensive_duration" that takes bond as BondContract, yield as Float returns Dictionary[String, Float]:
    Let duration_results be Dictionary[String, Float].create()
    
    Note: Generate cash flow schedule with timing
    Let cash_flows be FixedIncome.generate_detailed_cash_flow_schedule(bond)
    Let bond_price be FixedIncome.calculate_bond_price_internal(bond, yield)
    
    Let weighted_time_sum be 0.0
    Let present_value_sum be 0.0
    
    Note: Calculate present value weighted average time
    For cash_flow in cash_flows:
        Let payment_time be cash_flow["time_to_payment"]  Note: In years
        Let payment_amount be cash_flow["payment_amount"]
        
        let discount_factor be 1.0 / FixedIncome.power(1.0 + yield / Float.from_integer(bond.payment_frequency), payment_time * Float.from_integer(bond.payment_frequency))
        Let present_value be payment_amount * discount_factor
        
        weighted_time_sum = weighted_time_sum + payment_time * present_value
        present_value_sum = present_value_sum + present_value
    
    Note: Macaulay duration
    let macaulay_duration be weighted_time_sum / present_value_sum
    duration_results["macaulay_duration"] = macaulay_duration
    
    Note: Modified duration
    Let periods_per_year be Float.from_integer(bond.payment_frequency)
    Let modified_duration be macaulay_duration / (1.0 + yield / periods_per_year)
    duration_results["modified_duration"] = modified_duration
    
    Note: Approximate percentage price change for 1% yield change
    duration_results["price_sensitivity_1pct"] = -modified_duration * 0.01
    
    Return duration_results
```

### Convexity Analysis

```runa
Note: Calculate bond convexity for second-order price sensitivity
Process called "calculate_bond_convexity" that takes bond as BondContract, yield as Float returns Float:
    Let cash_flows be FixedIncome.generate_detailed_cash_flow_schedule(bond)
    Let bond_price be FixedIncome.calculate_bond_price_internal(bond, yield)
    
    Let convexity_sum be 0.0
    Let periods_per_year be Float.from_integer(bond.payment_frequency)
    
    For cash_flow in cash_flows:
        Let payment_time be cash_flow["time_to_payment"]
        Let payment_amount be cash_flow["payment_amount"]
        Let periods_to_payment be payment_time * periods_per_year
        
        Let discount_factor be 1.0 / FixedIncome.power(1.0 + yield / periods_per_year, periods_to_payment)
        let present_value be payment_amount * discount_factor
        
        Note: Convexity formula component: t(t+1) * PV / (1+y)²
        Let time_factor be periods_to_payment * (periods_to_payment + 1.0)
        convexity_sum = convexity_sum + time_factor * present_value
    
    Note: Normalize by bond price and adjust for compounding frequency
    let convexity be convexity_sum / (bond_price * FixedIncome.power(1.0 + yield / periods_per_year, 2.0)) / (periods_per_year * periods_per_year)
    
    Return convexity
```

## Callable and Putable Bonds

### Option-Adjusted Duration

```runa
Note: Calculate option-adjusted duration for callable bonds
Process called "calculate_option_adjusted_duration" that takes bond as BondContract, yield as Float, volatility as Float returns Dictionary[String, Float]:
    Let oad_results be Dictionary[String, Float].create()
    
    Note: Use binomial tree for option valuation
    Let tree_steps be 100
    Let time_to_maturity be FixedIncome.years_to_maturity(bond)
    Let dt be time_to_maturity / Float.from_integer(tree_steps)
    
    Note: Build interest rate tree
    Let rate_tree be FixedIncome.build_interest_rate_tree(yield, volatility, tree_steps, dt)
    
    Note: Calculate bond values at each node (working backwards)
    Let bond_values_tree be FixedIncome.price_callable_bond_tree(bond, rate_tree, dt)
    
    Note: Calculate price sensitivity using finite differences
    Let yield_shift be 0.0001  Note: 1 basis point
    Let rate_tree_up be FixedIncome.build_interest_rate_tree(yield + yield_shift, volatility, tree_steps, dt)
    let rate_tree_down be FixedIncome.build_interest_rate_tree(yield - yield_shift, volatility, tree_steps, dt)
    
    Let price_base be bond_values_tree[0][0]
    Let price_up be FixedIncome.price_callable_bond_tree(bond, rate_tree_up, dt)[0][0]
    Let price_down be FixedIncome.price_callable_bond_tree(bond, rate_tree_down, dt)[0][0]
    
    Note: Option-adjusted duration calculation
    Let oad be -(price_up - price_down) / (2.0 * yield_shift * price_base)
    oad_results["option_adjusted_duration"] = oad
    
    Note: Negative convexity check for callable bonds
    Let convexity be (price_up + price_down - 2.0 * price_base) / (yield_shift * yield_shift * price_base)
    oad_results["option_adjusted_convexity"] = convexity
    
    Note: Option value
    Let straight_bond_price be FixedIncome.calculate_bond_price_internal(bond, yield)
    oad_results["option_value"] = straight_bond_price - price_base
    
    Return oad_results
```

### Call Option Valuation in Bonds

```runa
Note: Value embedded call option using binomial tree
Process called "value_embedded_call_option" that takes bond as BondContract, spot_rate as Float, volatility as Float returns Float:
    If not bond.callable:
        Return 0.0  Note: No call option to value
    
    Let tree_steps be 100
    let time_to_maturity be FixedIncome.years_to_maturity(bond)
    Let dt be time_to_maturity / Float.from_integer(tree_steps)
    
    Note: Build interest rate tree using CIR or other model
    Let rate_tree be FixedIncome.build_cir_rate_tree(spot_rate, volatility, tree_steps, dt)
    
    Note: Initialize bond value tree at maturity
    Let num_final_nodes be tree_steps + 1
    Let bond_value_tree be List[List[Float]].create()
    
    Note: Work backwards from maturity
    For step from tree_steps down to 0:
        Let step_values be List[Float].create()
        let num_nodes be step + 1
        
        If step == tree_steps:
            Note: At maturity, bond worth face value
            For node from 0 to num_nodes:
                step_values.add(bond.face_value)
        Otherwise:
            Note: Calculate bond value at each node
            For node from 0 to num_nodes:
                Let current_rate be rate_tree[step][node]
                
                Note: Calculate continuation value (expected discounted future value)
                Let up_prob be 0.5  Note: Risk-neutral probability
                Let down_prob be 0.5
                let discount_factor be 1.0 / (1.0 + current_rate * dt)
                
                Let continuation_value be discount_factor * (up_prob * bond_value_tree[0][node] + down_prob * bond_value_tree[0][node + 1])
                
                Note: Add coupon payment if applicable
                If FixedIncome.is_coupon_payment_date(step, dt, bond):
                    Let coupon_payment be bond.coupon_rate * bond.face_value / Float.from_integer(bond.payment_frequency)
                    continuation_value = continuation_value + coupon_payment
                
                Note: Check if bond is callable at this node
                Let call_price be FixedIncome.get_call_price_at_time(bond, step * dt)
                If call_price > 0.0 and continuation_value > call_price:
                    step_values.add(call_price)  Note: Bond called away
                Otherwise:
                    step_values.add(continuation_value)
        
        bond_value_tree.add_front(step_values)
    
    Note: Option value = Straight bond value - Callable bond value
    Let straight_bond_value be FixedIncome.calculate_bond_price_internal(bond, spot_rate)
    Let callable_bond_value be bond_value_tree[0][0]
    
    Return straight_bond_value - callable_bond_value
```

## Yield Curve Construction

### Nelson-Siegel Model

```runa
Note: Fit Nelson-Siegel yield curve model
Process called "fit_nelson_siegel_curve" that takes market_yields as Dictionary[Float, Float] returns Dictionary[String, Float]:
    Let ns_parameters be Dictionary[String, Float].create()
    
    Note: Nelson-Siegel formula: y(τ) = β₀ + β₁((1-e^(-τ/λ))/(τ/λ)) + β₂((1-e^(-τ/λ))/(τ/λ) - e^(-τ/λ))
    Note: where τ is time to maturity, λ is decay parameter
    
    Note: Set up optimization problem
    Let maturities be market_yields.keys()
    let yields be market_yields.values()
    
    Note: Initial parameter guesses
    Let initial_beta0 be FixedIncome.calculate_mean(yields)  Note: Long-term rate
    Let initial_beta1 be yields[0] - initial_beta0  Note: Short-term component
    Let initial_beta2 be 0.0  Note: Hump component
    Let initial_lambda be 2.0  Note: Decay parameter
    
    Let initial_params be [initial_beta0, initial_beta1, initial_beta2, initial_lambda]
    
    Note: Minimize sum of squared errors
    Let optimization_result be FixedIncome.minimize_yield_curve_error(initial_params, maturities, yields, "nelson_siegel")
    
    ns_parameters["beta_0"] = optimization_result.parameters[0]
    ns_parameters["beta_1"] = optimization_result.parameters[1]
    ns_parameters["beta_2"] = optimization_result.parameters[2]
    ns_parameters["lambda"] = optimization_result.parameters[3]
    ns_parameters["rmse"] = optimization_result.rmse
    
    Return ns_parameters
```

### Spline Interpolation for Yield Curves

```runa
Note: Construct smooth yield curve using cubic splines
Process called "construct_spline_yield_curve" that takes market_data as Dictionary[Float, Float] returns Dictionary[String, List[Float]]:
    Let spline_curve be Dictionary[String, List[Float]].create()
    
    Let maturities be FixedIncome.sort_ascending(market_data.keys())
    Let yields be List[Float].create()
    
    For maturity in maturities:
        yields.add(market_data[maturity])
    
    Note: Fit natural cubic spline
    Let spline_coefficients be FixedIncome.fit_natural_cubic_spline(maturities, yields)
    
    Note: Generate interpolated curve at standard maturities
    Let standard_maturities be [0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 15.0, 20.0, 30.0]
    Let interpolated_yields be List[Float].create()
    
    For target_maturity in standard_maturities:
        If target_maturity <= maturities[0]:
            Note: Extrapolate flat before first point
            interpolated_yields.add(yields[0])
        Otherwise If target_maturity >= maturities[maturities.size - 1]:
            Note: Extrapolate flat after last point
            interpolated_yields.add(yields[yields.size - 1])
        Otherwise:
            Note: Interpolate using spline
            Let interpolated_yield be FixedIncome.evaluate_cubic_spline(spline_coefficients, maturities, target_maturity)
            interpolated_yields.add(interpolated_yield)
    
    spline_curve["maturities"] = standard_maturities
    spline_curve["yields"] = interpolated_yields
    spline_curve["spline_coefficients"] = FixedIncome.coefficients_to_list(spline_coefficients)
    
    Return spline_curve
```

## Credit Risk Analysis

### Credit Spread Analysis

```runa
Note: Analyze credit spreads and default probabilities
Process called "analyze_credit_spreads" that takes corporate_yields as Dictionary[String, Float], government_yields as Dictionary[String, Float], recovery_rate as Float returns Dictionary[String, Float]:
    Let credit_analysis be Dictionary[String, Float].create()
    
    Note: Calculate credit spreads
    Let credit_spreads be Dictionary[String, Float].create()
    For rating in corporate_yields.keys():
        If government_yields.contains_key("benchmark"):
            let spread be corporate_yields[rating] - government_yields["benchmark"]
            credit_spreads[rating] = spread
    
    Note: Estimate default probabilities using simplified approach
    For rating in credit_spreads.keys():
        Let spread be credit_spreads[rating]
        
        Note: Default probability ≈ Credit Spread / (1 - Recovery Rate)
        Let implied_default_prob be spread / (1.0 - recovery_rate)
        credit_analysis[rating + "_default_prob"] = implied_default_prob
        credit_analysis[rating + "_spread"] = spread
    
    Note: Calculate credit duration (sensitivity to spread changes)
    For rating in corporate_yields.keys():
        Let modified_duration be 5.0  Note: Simplified assumption, would calculate properly
        let credit_duration be modified_duration * credit_spreads[rating] / corporate_yields[rating]
        credit_analysis[rating + "_credit_duration"] = credit_duration
    
    Return credit_analysis
```

### Merton Model for Credit Risk

```runa
Note: Merton structural model for corporate bond pricing
Process called "merton_model_bond_pricing" that takes firm_value as Float, debt_face_value as Float, risk_free_rate as Float, volatility as Float, time_to_maturity as Float returns Dictionary[String, Float]:
    Let merton_results be Dictionary[String, Float].create()
    
    Note: Calculate d1 and d2 parameters
    let d1 be (FixedIncome.log(firm_value / debt_face_value) + (risk_free_rate + 0.5 * volatility * volatility) * time_to_maturity) / (volatility * FixedIncome.sqrt(time_to_maturity))
    Let d2 be d1 - volatility * FixedIncome.sqrt(time_to_maturity)
    
    Note: Calculate normal cumulative distribution values
    Let N_d1 be FixedIncome.normal_cdf(d1)
    Let N_d2 be FixedIncome.normal_cdf(d2)
    Let N_minus_d2 be FixedIncome.normal_cdf(-d2)
    
    Note: Equity value (call option on firm value)
    Let equity_value be firm_value * N_d1 - debt_face_value * FixedIncome.exp(-risk_free_rate * time_to_maturity) * N_d2
    
    Note: Debt value
    Let risk_free_bond_value be debt_face_value * FixedIncome.exp(-risk_free_rate * time_to_maturity)
    Let debt_value be risk_free_bond_value * N_d2 + firm_value * FixedIncome.normal_cdf(-d1)
    
    Note: Default probability
    Let default_probability be N_minus_d2
    
    Note: Credit spread
    Let corporate_bond_yield be -FixedIncome.log(debt_value / debt_face_value) / time_to_maturity
    let credit_spread be corporate_bond_yield - risk_free_rate
    
    merton_results["equity_value"] = equity_value
    merton_results["debt_value"] = debt_value
    merton_results["default_probability"] = default_probability
    merton_results["credit_spread"] = credit_spread
    merton_results["corporate_yield"] = corporate_bond_yield
    
    Return merton_results
```

## Term Structure Models

### Vasicek Interest Rate Model

```runa
Note: Simulate Vasicek interest rate paths
Process called "simulate_vasicek_rates" that takes initial_rate as Float, mean_reversion_speed as Float, long_term_rate as Float, volatility as Float, time_horizon as Float, time_steps as Integer, num_simulations as Integer returns List[List[Float]]:
    Let rate_paths be List[List[Float]].create()
    
    Let dt be time_horizon / Float.from_integer(time_steps)
    Let sqrt_dt be FixedIncome.sqrt(dt)
    
    For simulation from 1 to num_simulations:
        Let rate_path be List[Float].create()
        Let current_rate be initial_rate
        rate_path.add(current_rate)
        
        For step from 1 to time_steps:
            Note: Vasicek SDE: dr = κ(θ - r)dt + σdW
            Let drift be mean_reversion_speed * (long_term_rate - current_rate) * dt
            Let diffusion be volatility * sqrt_dt * FixedIncome.generate_standard_normal()
            
            current_rate = current_rate + drift + diffusion
            
            Note: Ensure rates don't go negative (optional floor)
            current_rate = FixedIncome.max(0.0, current_rate)
            
            rate_path.add(current_rate)
        
        rate_paths.add(rate_path)
    
    Return rate_paths
```

### Cox-Ingersoll-Ross Model

```runa
Note: Simulate CIR interest rate model with mean reversion
Process called "simulate_cir_rates" that takes initial_rate as Float, mean_reversion_speed as Float, long_term_rate as Float, volatility as Float, time_horizon as Float, time_steps as Integer, num_simulations as Integer returns List[List[Float]]:
    let rate_paths be List[List[Float]].create()
    
    Let dt be time_horizon / Float.from_integer(time_steps)
    let sqrt_dt be FixedIncome.sqrt(dt)
    
    Note: Check Feller condition: 2κθ ≥ σ²
    Let feller_condition be 2.0 * mean_reversion_speed * long_term_rate >= volatility * volatility
    
    For simulation from 1 to num_simulations:
        Let rate_path be List[Float].create()
        Let current_rate be initial_rate
        rate_path.add(current_rate)
        
        For step from 1 to time_steps:
            Note: CIR SDE: dr = κ(θ - r)dt + σ√r dW
            Let drift be mean_reversion_speed * (long_term_rate - current_rate) * dt
            let diffusion be volatility * FixedIncome.sqrt(FixedIncome.max(0.0, current_rate)) * sqrt_dt * FixedIncome.generate_standard_normal()
            
            current_rate = current_rate + drift + diffusion
            
            Note: CIR model naturally keeps rates non-negative if Feller condition satisfied
            If not feller_condition:
                current_rate = FixedIncome.max(0.001, current_rate)  Note: Small positive floor
            
            rate_path.add(current_rate)
        
        rate_paths.add(rate_path)
    
    Return rate_paths
```

## Bond Portfolio Analysis

### Portfolio Duration and Convexity

```runa
Note: Calculate portfolio-level duration and convexity
Process called "calculate_portfolio_duration" that takes bond_portfolio as List[Dictionary[String, String]], portfolio_weights as List[Float] returns Dictionary[String, Float]:
    Let portfolio_metrics be Dictionary[String, Float].create()
    
    Let weighted_duration be 0.0
    Let weighted_convexity be 0.0
    Let portfolio_yield be 0.0
    
    For i from 0 to bond_portfolio.size:
        Let bond_data be bond_portfolio[i]
        Let weight be portfolio_weights[i]
        
        Let bond be FixedIncome.parse_bond_from_data(bond_data)
        Let bond_yield be Float.parse(bond_data["yield"])
        Let duration be FixedIncome.calculate_modified_duration(bond, bond_yield)
        Let convexity be FixedIncome.calculate_bond_convexity(bond, bond_yield)
        
        weighted_duration = weighted_duration + weight * duration
        weighted_convexity = weighted_convexity + weight * convexity
        portfolio_yield = portfolio_yield + weight * bond_yield
    
    portfolio_metrics["portfolio_duration"] = weighted_duration
    portfolio_metrics["portfolio_convexity"] = weighted_convexity
    portfolio_metrics["portfolio_yield"] = portfolio_yield
    
    Note: Portfolio price sensitivity to yield changes
    portfolio_metrics["price_sensitivity_100bp"] = -weighted_duration * 0.01 + 0.5 * weighted_convexity * 0.01 * 0.01
    
    Return portfolio_metrics
```

## Error Handling and Validation

### Bond Parameter Validation

```runa
Note: Comprehensive bond parameter validation
Process called "validate_bond_parameters" that takes bond as BondContract returns Dictionary[String, Boolean]:
    Let validation_results be Dictionary[String, Boolean].create()
    
    Note: Basic parameter checks
    validation_results["positive_coupon_rate"] = bond.coupon_rate >= 0.0 and bond.coupon_rate <= 1.0
    validation_results["positive_face_value"] = bond.face_value > 0.0
    validation_results["valid_maturity"] = bond.maturity_date > bond.issue_date
    validation_results["valid_payment_frequency"] = bond.payment_frequency > 0 and bond.payment_frequency <= 12
    
    Note: Logical consistency checks
    Let years_to_maturity be FixedIncome.years_between_dates(FixedIncome.current_date(), bond.maturity_date)
    validation_results["reasonable_maturity"] = years_to_maturity > 0.0 and years_to_maturity <= 100.0
    
    Note: Credit rating validation
    Let valid_ratings be ["AAA", "AA+", "AA", "AA-", "A+", "A", "A-", "BBB+", "BBB", "BBB-", "BB+", "BB", "BB-", "B+", "B", "B-", "CCC", "CC", "C", "D"]
    validation_results["valid_credit_rating"] = FixedIncome.list_contains(valid_ratings, bond.credit_rating)
    
    Note: Call/put option consistency
    If bond.callable and bond.call_schedules.size == 0:
        validation_results["call_schedule_consistency"] = false
    Otherwise:
        validation_results["call_schedule_consistency"] = true
    
    validation_results["overall_valid"] = validation_results["positive_coupon_rate"] and
                                         validation_results["positive_face_value"] and
                                         validation_results["valid_maturity"] and
                                         validation_results["valid_payment_frequency"] and
                                         validation_results["reasonable_maturity"] and
                                         validation_results["valid_credit_rating"] and
                                         validation_results["call_schedule_consistency"]
    
    Return validation_results
```

### Yield Curve Validation

```runa
Note: Validate yield curve for reasonable shape and absence of arbitrage
Process called "validate_yield_curve" that takes curve as YieldCurve returns Dictionary[String, Boolean]:
    Let validation be Dictionary[String, Boolean].create()
    
    Note: Check data completeness
    validation["matching_data_lengths"] = curve.maturities.size == curve.yields.size
    validation["sufficient_points"] = curve.maturities.size >= 3
    
    Note: Check for monotonic maturities
    Let monotonic_maturities be true
    For i from 1 to curve.maturities.size:
        If curve.maturities[i] <= curve.maturities[i - 1]:
            monotonic_maturities = false
            Break
    validation["monotonic_maturities"] = monotonic_maturities
    
    Note: Check for reasonable yield levels
    Let unreasonable_yields be false
    For yield_value in curve.yields:
        If yield_value < -0.05 or yield_value > 0.25:  Note: -5% to 25% reasonable range
            unreasonable_yields = true
            Break
    validation["reasonable_yield_levels"] = not unreasonable_yields
    
    Note: Check for excessive yield curve inversions
    Let inversion_count be 0
    For i from 1 to curve.yields.size:
        If curve.yields[i] < curve.yields[i - 1]:
            inversion_count = inversion_count + 1
    validation["reasonable_inversions"] = inversion_count <= 2  Note: Allow some inversions
    
    validation["overall_valid"] = validation["matching_data_lengths"] and
                                 validation["sufficient_points"] and
                                 validation["monotonic_maturities"] and
                                 validation["reasonable_yield_levels"] and
                                 validation["reasonable_inversions"]
    
    Return validation
```

## Related Documentation

- **[Risk](risk.md)** - Interest rate risk management and bond portfolio risk
- **[Options](options.md)** - Bond options and embedded option valuation
- **[Portfolio](portfolio.md)** - Fixed income portfolio optimization
- **[Time Series](time_series.md)** - Interest rate modeling and term structure evolution
- **[Derivatives](derivatives.md)** - Interest rate derivatives and bond futures
# Options Module

The options module provides comprehensive options pricing and valuation models essential for derivatives trading, risk management, and quantitative finance applications. This module implements industry-standard pricing models, Greeks calculation, and advanced options strategies.

## Overview

Options are financial derivatives that give the holder the right, but not the obligation, to buy or sell an underlying asset at a specified price within a certain time period. This module provides the mathematical tools for accurate options pricing, risk assessment, and strategic trading decisions.

## Mathematical Foundation

### Options Pricing Theory

The module implements several foundational pricing models:

- **Black-Scholes Model**: Analytical solution for European options under constant volatility
- **Black-Scholes-Merton**: Extension including dividend yield
- **Binomial Trees**: Discrete-time model for American and exotic options
- **Monte Carlo Methods**: Numerical pricing for complex path-dependent options

### Core Pricing Equation

The Black-Scholes partial differential equation:
**∂V/∂t + ½σ²S²∂²V/∂S² + rS∂V/∂S - rV = 0**

Where:
- V = Option value
- S = Stock price
- σ = Volatility
- r = Risk-free rate
- t = Time

## Core Data Structures

### OptionContract

Represents an options contract with all relevant parameters:

```runa
Type called "OptionContract":
    contract_id as String                 Note: Unique contract identifier
    underlying_asset as String           Note: Underlying stock/asset symbol
    option_type as String                 Note: "call" or "put"
    strike_price as Float                 Note: Exercise price
    expiration_date as Integer           Note: Contract expiration timestamp
    premium as Float                      Note: Option premium/price
    contract_size as Integer             Note: Number of shares per contract
    exercise_style as String             Note: "European" or "American"
    option_status as String              Note: "open", "exercised", "expired"
```

### BlackScholesParameters

Configuration for Black-Scholes pricing model:

```runa
Type called "BlackScholesParameters":
    spot_price as Float                  Note: Current underlying price
    strike_price as Float                Note: Option strike price
    time_to_expiration as Float          Note: Time until expiry (in years)
    risk_free_rate as Float              Note: Risk-free interest rate
    volatility as Float                  Note: Implied/historical volatility
    dividend_yield as Float              Note: Continuous dividend yield
    option_type as String                Note: "call" or "put"
```

## Basic Usage

### Black-Scholes Pricing

```runa
Use math.financial.options as Options

Note: Price a European call option
Let bs_params be Options.create_black_scholes_parameters()
bs_params.spot_price = 100.0
bs_params.strike_price = 105.0
bs_params.time_to_expiration = 0.25  Note: 3 months
bs_params.risk_free_rate = 0.05
bs_params.volatility = 0.20
bs_params.dividend_yield = 0.02
bs_params.option_type = "call"

Let option_price be Options.black_scholes_price(bs_params)
Let greeks be Options.calculate_greeks(bs_params)
```

### Binomial Tree Pricing

```runa
Note: Price an American option using binomial tree
Let american_option be Options.create_option_contract()
american_option.underlying_asset = "AAPL"
american_option.option_type = "put"
american_option.strike_price = 150.0
american_option.exercise_style = "American"

Let tree_steps be 100
Let option_value be Options.binomial_tree_pricing(american_option, bs_params, tree_steps)
```

## Advanced Pricing Models

### Black-Scholes Formula Implementation

```runa
Note: Complete Black-Scholes analytical solution
Process called "black_scholes_analytical" that takes params as BlackScholesParameters returns Float:
    Let S be params.spot_price
    Let K be params.strike_price
    Let T be params.time_to_expiration
    Let r be params.risk_free_rate
    let sigma be params.volatility
    Let q be params.dividend_yield
    
    Note: Calculate d1 and d2 parameters
    Let ln_SK be Options.natural_log(S / K)
    Let variance_term be (r - q + 0.5 * sigma * sigma) * T
    Let d1 be (ln_SK + variance_term) / (sigma * Options.sqrt(T))
    Let d2 be d1 - sigma * Options.sqrt(T)
    
    Note: Calculate normal cumulative distribution values
    Let N_d1 be Options.normal_cdf(d1)
    Let N_d2 be Options.normal_cdf(d2)
    Let N_minus_d1 be Options.normal_cdf(-d1)
    Let N_minus_d2 be Options.normal_cdf(-d2)
    
    Note: Apply discount factors
    Let discount_factor be Options.exp(-r * T)
    Let dividend_discount be Options.exp(-q * T)
    
    Match params.option_type:
        Case "call":
            Let call_value be S * dividend_discount * N_d1 - K * discount_factor * N_d2
            Return call_value
        Case "put":
            Let put_value be K * discount_factor * N_minus_d2 - S * dividend_discount * N_minus_d1
            Return put_value
        Otherwise:
            Return 0.0
```

### American Options with Binomial Trees

```runa
Note: American option pricing with early exercise capability
Process called "american_binomial_pricing" that takes option as OptionContract, params as BlackScholesParameters, steps as Integer returns Float:
    Let dt be params.time_to_expiration / Float.from_integer(steps)
    Let r be params.risk_free_rate
    let sigma be params.volatility
    Let q be params.dividend_yield
    
    Note: Calculate binomial tree parameters
    Let u be Options.exp(sigma * Options.sqrt(dt))  Note: Up factor
    let d be 1.0 / u  Note: Down factor
    let risk_neutral_prob be (Options.exp((r - q) * dt) - d) / (u - d)
    
    Note: Initialize asset price tree
    Let price_tree be List[List[Float]].create_matrix(steps + 1, steps + 1)
    Let option_tree be List[List[Float]].create_matrix(steps + 1, steps + 1)
    
    Note: Fill forward asset prices
    For i from 0 to steps:
        For j from 0 to i:
            Let up_moves be j
            Let down_moves be i - j
            price_tree[i][j] = params.spot_price * Options.power(u, Float.from_integer(up_moves)) * Options.power(d, Float.from_integer(down_moves))
    
    Note: Calculate terminal option values
    For j from 0 to steps:
        Let terminal_price be price_tree[steps][j]
        Match option.option_type:
            Case "call":
                option_tree[steps][j] = Options.max(terminal_price - option.strike_price, 0.0)
            Case "put":
                option_tree[steps][j] = Options.max(option.strike_price - terminal_price, 0.0)
    
    Note: Backward induction with early exercise check
    let discount_factor be Options.exp(-r * dt)
    
    For i from (steps - 1) down to 0:
        For j from 0 to i:
            Note: Calculate continuation value
            Let continuation_value be discount_factor * (risk_neutral_prob * option_tree[i + 1][j + 1] + (1.0 - risk_neutral_prob) * option_tree[i + 1][j])
            
            Note: Calculate intrinsic value for early exercise
            Let current_price be price_tree[i][j]
            Let intrinsic_value be 0.0
            Match option.option_type:
                Case "call":
                    intrinsic_value = Options.max(current_price - option.strike_price, 0.0)
                Case "put":
                    intrinsic_value = Options.max(option.strike_price - current_price, 0.0)
            
            Note: American option can be exercised early
            option_tree[i][j] = Options.max(continuation_value, intrinsic_value)
    
    Return option_tree[0][0]
```

### Monte Carlo Option Pricing

```runa
Note: Monte Carlo simulation for path-dependent options
Process called "monte_carlo_option_pricing" that takes option as OptionContract, params as BlackScholesParameters, simulations as Integer returns Float:
    Let S0 be params.spot_price
    Let K be option.strike_price
    Let T be params.time_to_expiration
    Let r be params.risk_free_rate
    Let sigma be params.volatility
    Let q be params.dividend_yield
    
    Let payoff_sum be 0.0
    Let time_steps be 252  Note: Daily steps for one year
    Let dt be T / Float.from_integer(time_steps)
    
    Note: Risk-neutral drift
    Let mu be r - q - 0.5 * sigma * sigma
    
    For simulation from 1 to simulations:
        Let current_price be S0
        Let path_dependent_value be 0.0
        
        Note: Generate one price path
        For step from 1 to time_steps:
            Let random_normal be Options.generate_standard_normal()
            Let price_change be mu * dt + sigma * Options.sqrt(dt) * random_normal
            current_price = current_price * Options.exp(price_change)
        
        Note: Calculate payoff at expiration
        Let final_payoff be 0.0
        Match option.option_type:
            Case "call":
                final_payoff = Options.max(current_price - K, 0.0)
            Case "put":
                final_payoff = Options.max(K - current_price, 0.0)
        
        payoff_sum = payoff_sum + final_payoff
    
    Note: Discount average payoff to present value
    Let average_payoff be payoff_sum / Float.from_integer(simulations)
    let present_value be average_payoff * Options.exp(-r * T)
    
    Return present_value
```

## Greeks Calculation

### The Greeks - Risk Sensitivities

```runa
Note: Calculate all option Greeks for risk management
Process called "calculate_comprehensive_greeks" that takes params as BlackScholesParameters returns Dictionary[String, Float]:
    Let greeks be Dictionary[String, Float].create()
    
    Note: Delta - sensitivity to underlying price
    Let delta be Options.calculate_delta(params)
    greeks["delta"] = delta
    
    Note: Gamma - rate of change of delta
    Let gamma be Options.calculate_gamma(params)
    greeks["gamma"] = gamma
    
    Note: Theta - time decay
    Let theta be Options.calculate_theta(params)
    greeks["theta"] = theta
    
    Note: Vega - volatility sensitivity
    Let vega be Options.calculate_vega(params)
    greeks["vega"] = vega
    
    Note: Rho - interest rate sensitivity
    Let rho be Options.calculate_rho(params)
    greeks["rho"] = rho
    
    Note: Higher-order Greeks
    greeks["vanna"] = Options.calculate_vanna(params)  Note: ∂Delta/∂σ
    greeks["charm"] = Options.calculate_charm(params)  Note: ∂Delta/∂t
    greeks["volga"] = Options.calculate_volga(params)  Note: ∂Vega/∂σ
    
    Return greeks
```

### Delta Calculation

```runa
Note: Delta calculation using Black-Scholes formula
Process called "calculate_delta_analytical" that takes params as BlackScholesParameters returns Float:
    Let S be params.spot_price
    Let K be params.strike_price
    Let T be params.time_to_expiration
    Let r be params.risk_free_rate
    Let sigma be params.volatility
    Let q be params.dividend_yield
    
    Note: Calculate d1 parameter
    Let ln_SK be Options.natural_log(S / K)
    Let d1 be (ln_SK + (r - q + 0.5 * sigma * sigma) * T) / (sigma * Options.sqrt(T))
    
    Note: Apply dividend adjustment
    Let dividend_discount be Options.exp(-q * T)
    
    Match params.option_type:
        Case "call":
            Return dividend_discount * Options.normal_cdf(d1)
        Case "put":
            Return -dividend_discount * Options.normal_cdf(-d1)
        Otherwise:
            Return 0.0
```

## Implied Volatility Calculation

### Newton-Raphson Method for Implied Volatility

```runa
Note: Calculate implied volatility from market price
Process called "calculate_implied_volatility" that takes market_price as Float, params as BlackScholesParameters returns Float:
    Let tolerance be 1e-6
    Let max_iterations be 100
    Let initial_guess be 0.20  Note: Start with 20% volatility
    
    Let sigma be initial_guess
    
    For iteration from 1 to max_iterations:
        Note: Calculate theoretical price and vega
        let temp_params be Options.copy_parameters(params)
        temp_params.volatility = sigma
        
        Let theoretical_price be Options.black_scholes_analytical(temp_params)
        Let vega be Options.calculate_vega(temp_params)
        
        Let price_difference be theoretical_price - market_price
        
        If Options.abs(price_difference) < tolerance:
            Return sigma
        
        If vega == 0.0:
            Return -1.0  Note: Error - cannot calculate
        
        Note: Newton-Raphson update
        sigma = sigma - price_difference / vega
        
        Note: Keep volatility positive and reasonable
        sigma = Options.max(0.001, Options.min(sigma, 5.0))
    
    Return -1.0  Note: Failed to converge
```

## Exotic Options

### Asian Options (Average Price)

```runa
Note: Asian option pricing using Monte Carlo
Process called "price_asian_option" that takes option_params as BlackScholesParameters, averaging_type as String, simulations as Integer returns Float:
    Let S0 be option_params.spot_price
    Let K be option_params.strike_price
    Let T be option_params.time_to_expiration
    Let r be option_params.risk_free_rate
    Let sigma be option_params.volatility
    
    Let payoff_sum be 0.0
    let observation_points be 252  Note: Daily observations
    Let dt be T / Float.from_integer(observation_points)
    Let mu be r - 0.5 * sigma * sigma
    
    For simulation from 1 to simulations:
        Let price_path be List[Float].create()
        Let current_price be S0
        price_path.add(current_price)
        
        Note: Generate price path
        For step from 1 to observation_points:
            Let random_normal be Options.generate_standard_normal()
            current_price = current_price * Options.exp(mu * dt + sigma * Options.sqrt(dt) * random_normal)
            price_path.add(current_price)
        
        Note: Calculate average price
        Let average_price be 0.0
        Match averaging_type:
            Case "arithmetic":
                For price in price_path:
                    average_price = average_price + price
                average_price = average_price / Float.from_integer(price_path.size)
            Case "geometric":
                Let log_sum be 0.0
                For price in price_path:
                    log_sum = log_sum + Options.natural_log(price)
                average_price = Options.exp(log_sum / Float.from_integer(price_path.size))
        
        Note: Calculate payoff
        Let payoff be 0.0
        Match option_params.option_type:
            Case "call":
                payoff = Options.max(average_price - K, 0.0)
            Case "put":
                payoff = Options.max(K - average_price, 0.0)
        
        payoff_sum = payoff_sum + payoff
    
    Note: Discount to present value
    Let average_payoff be payoff_sum / Float.from_integer(simulations)
    Return average_payoff * Options.exp(-r * T)
```

### Barrier Options

```runa
Note: Barrier option pricing with knock-out/knock-in features
Process called "price_barrier_option" that takes params as BlackScholesParameters, barrier_level as Float, barrier_type as String returns Float:
    Let S be params.spot_price
    Let K be params.strike_price
    let B be barrier_level
    Let T be params.time_to_expiration
    Let r be params.risk_free_rate
    Let sigma be params.volatility
    
    Note: Analytical solution for down-and-out call
    Match barrier_type:
        Case "down_and_out_call":
            If S <= B:
                Return 0.0  Note: Already knocked out
            
            Let lambda_val be (r + 0.5 * sigma * sigma) / (sigma * sigma)
            Let y1 be (Options.natural_log(B * B / (S * K)) + lambda_val * sigma * sigma * T) / (sigma * Options.sqrt(T))
            
            Let regular_call be Options.black_scholes_analytical(params)
            Let barrier_adjustment be Options.power(B / S, 2.0 * lambda_val) * Options.black_scholes_analytical_modified(B * B / S, K, params)
            
            Return regular_call - barrier_adjustment
            
        Case "up_and_out_put":
            If S >= B:
                Return 0.0  Note: Already knocked out
            
            Note: Similar calculation for up-and-out put
            Return Options.calculate_up_and_out_put_analytical(params, B)
            
        Otherwise:
            Note: Use Monte Carlo for complex barriers
            Return Options.barrier_option_monte_carlo(params, B, barrier_type, 100000)
```

## Option Strategies

### Covered Call Strategy

```runa
Note: Covered call strategy analysis
Process called "covered_call_analysis" that takes stock_position as Float, call_option as OptionContract, current_price as Float returns Dictionary[String, Float]:
    Let strategy_analysis be Dictionary[String, Float].create()
    
    Note: Calculate breakeven point
    Let call_premium_received be call_option.premium
    Let breakeven be current_price - call_premium_received
    strategy_analysis["breakeven"] = breakeven
    
    Note: Maximum profit (if stock called away)
    Let max_profit be call_option.strike_price - current_price + call_premium_received
    strategy_analysis["max_profit"] = max_profit * stock_position
    
    Note: Maximum loss (stock goes to zero)
    let max_loss be current_price - call_premium_received
    strategy_analysis["max_loss"] = max_loss * stock_position
    
    Note: Profit/loss at different stock prices
    Let price_scenarios be [current_price * 0.8, current_price * 0.9, current_price, current_price * 1.1, current_price * 1.2]
    Let scenario_profits be List[Float].create()
    
    For scenario_price in price_scenarios:
        Let stock_pnl be (scenario_price - current_price) * stock_position
        Let call_pnl be 0.0
        
        If scenario_price > call_option.strike_price:
            Note: Call is exercised
            call_pnl = call_premium_received - (scenario_price - call_option.strike_price)
        Otherwise:
            call_pnl = call_premium_received
        
        Let total_pnl be stock_pnl + call_pnl
        scenario_profits.add(total_pnl)
    
    strategy_analysis["scenario_profits"] = Options.list_to_string(scenario_profits)
    
    Return strategy_analysis
```

### Straddle Strategy

```runa
Note: Long straddle strategy for volatility plays
Process called "long_straddle_analysis" that takes call_option as OptionContract, put_option as OptionContract returns Dictionary[String, Float]:
    Let straddle_analysis be Dictionary[String, Float].create()
    
    Let total_premium_paid be call_option.premium + put_option.premium
    straddle_analysis["total_cost"] = total_premium_paid
    
    Note: Breakeven points
    straddle_analysis["upper_breakeven"] = call_option.strike_price + total_premium_paid
    straddle_analysis["lower_breakeven"] = put_option.strike_price - total_premium_paid
    
    Note: Maximum loss (at strike price)
    straddle_analysis["max_loss"] = total_premium_paid
    
    Note: Theoretical unlimited profit
    straddle_analysis["max_profit"] = Float.positive_infinity()
    
    Note: Volatility requirement for profitability
    Let required_move_percent be total_premium_paid / call_option.strike_price * 100.0
    straddle_analysis["required_move_percentage"] = required_move_percent
    
    Return straddle_analysis
```

## Risk Management

### Position Greeks Aggregation

```runa
Note: Aggregate Greeks across multiple option positions
Process called "aggregate_portfolio_greeks" that takes positions as List[Dictionary[String, String]] returns Dictionary[String, Float]:
    Let portfolio_greeks be Dictionary[String, Float].create()
    
    Note: Initialize totals
    portfolio_greeks["total_delta"] = 0.0
    portfolio_greeks["total_gamma"] = 0.0
    portfolio_greeks["total_theta"] = 0.0
    portfolio_greeks["total_vega"] = 0.0
    portfolio_greeks["total_rho"] = 0.0
    
    For position in positions:
        Let quantity be Float.parse(position["quantity"])
        Let position_greeks be Options.parse_greeks(position["greeks"])
        
        Note: Weight Greeks by position size
        portfolio_greeks["total_delta"] = portfolio_greeks["total_delta"] + quantity * position_greeks["delta"]
        portfolio_greeks["total_gamma"] = portfolio_greeks["total_gamma"] + quantity * position_greeks["gamma"]
        portfolio_greeks["total_theta"] = portfolio_greeks["total_theta"] + quantity * position_greeks["theta"]
        portfolio_greeks["total_vega"] = portfolio_greeks["total_vega"] + quantity * position_greeks["vega"]
        portfolio_greeks["total_rho"] = portfolio_greeks["total_rho"] + quantity * position_greeks["rho"]
    
    Note: Calculate risk metrics
    portfolio_greeks["dollar_delta"] = portfolio_greeks["total_delta"] * 100.0  Note: Per $1 move
    portfolio_greeks["gamma_risk"] = portfolio_greeks["total_gamma"] * 100.0 * 100.0  Note: For $1 move
    portfolio_greeks["theta_decay_daily"] = portfolio_greeks["total_theta"] / 365.0  Note: Daily theta decay
    
    Return portfolio_greeks
```

## Error Handling and Validation

### Parameter Validation

```runa
Note: Validate Black-Scholes parameters
Process called "validate_bs_parameters" that takes params as BlackScholesParameters returns Boolean:
    If params.spot_price <= 0.0:
        Return false  Note: Stock price must be positive
    
    If params.strike_price <= 0.0:
        Return false  Note: Strike price must be positive
    
    If params.time_to_expiration <= 0.0:
        Return false  Note: Time to expiration must be positive
    
    If params.volatility <= 0.0:
        Return false  Note: Volatility must be positive
    
    If params.volatility > 5.0:
        Return false  Note: Volatility seems unreasonably high
    
    If params.risk_free_rate < -0.10 or params.risk_free_rate > 0.50:
        Return false  Note: Risk-free rate outside reasonable bounds
    
    If params.dividend_yield < 0.0 or params.dividend_yield > 0.20:
        Return false  Note: Dividend yield outside reasonable bounds
    
    If params.option_type != "call" and params.option_type != "put":
        Return false  Note: Invalid option type
    
    Return true
```

### Numerical Stability Checks

```runa
Note: Check for numerical stability issues in calculations
Process called "check_numerical_stability" that takes params as BlackScholesParameters returns Dictionary[String, Boolean]:
    Let stability_checks be Dictionary[String, Boolean].create()
    
    Note: Check for extreme values that could cause numerical issues
    Let T be params.time_to_expiration
    Let sigma be params.volatility
    
    Note: Very short time to expiration
    stability_checks["short_expiry_stable"] = T > 0.001  Note: More than ~8 hours
    
    Note: Very high volatility
    stability_checks["volatility_stable"] = sigma < 2.0  Note: Less than 200%
    
    Note: Deep in/out of the money
    Let moneyness be params.spot_price / params.strike_price
    stability_checks["moneyness_stable"] = moneyness > 0.1 and moneyness < 10.0
    
    Note: d1 and d2 not too extreme
    Let d1 be Options.calculate_d1(params)
    stability_checks["d1_stable"] = Options.abs(d1) < 10.0
    
    stability_checks["overall_stable"] = stability_checks["short_expiry_stable"] and 
                                        stability_checks["volatility_stable"] and 
                                        stability_checks["moneyness_stable"] and 
                                        stability_checks["d1_stable"]
    
    Return stability_checks
```

## Related Documentation

- **[Risk](risk.md)** - Risk management and Value at Risk calculations
- **[Portfolio](portfolio.md)** - Portfolio optimization and performance metrics
- **[Fixed Income](fixed_income.md)** - Bond pricing and yield calculations
- **[Derivatives](derivatives.md)** - Other derivative instruments pricing
- **[Time Series](time_series.md)** - Financial time series analysis and volatility modeling
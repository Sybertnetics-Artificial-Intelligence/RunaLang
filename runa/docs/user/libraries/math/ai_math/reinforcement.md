# Reinforcement Learning Mathematics

The Reinforcement Learning Mathematics module (`math/ai_math/reinforcement`) provides comprehensive mathematical foundations for reinforcement learning including value functions, policy gradients, Q-learning mathematics, temporal difference learning, actor-critic methods, exploration strategies, reward functions, and Bellman equations. This module covers both model-free and model-based RL algorithms.

## Overview

This module implements the core mathematical concepts underlying modern reinforcement learning:

- **Value Functions**: State values V(s) and action values Q(s,a)
- **Policy Methods**: Policy gradients, actor-critic algorithms
- **Temporal Difference Learning**: TD(0), TD(λ), SARSA
- **Q-Learning**: Deep Q-Networks (DQN), Double DQN, Dueling DQN
- **Exploration Strategies**: ε-greedy, Upper Confidence Bounds, Thompson Sampling
- **Model-Based RL**: Dynamics models, planning algorithms
- **Multi-Agent RL**: Nash equilibria, game theory

## Key Features

### Mathematical Foundations
- **Bellman Equations**: Optimal value function relationships
- **Policy Gradients**: Direct policy optimization
- **Temporal Difference**: Sample-based value updates
- **Function Approximation**: Neural network value functions

### Algorithm Support
- **Model-Free**: Q-learning, SARSA, policy gradient methods
- **Model-Based**: Dyna-Q, Monte Carlo Tree Search
- **Actor-Critic**: A3C, PPO, SAC, TD3
- **Multi-Agent**: Independent learning, centralized training

### Exploration Methods
- **Classical**: ε-greedy, softmax exploration
- **Advanced**: UCB, Thompson sampling, curiosity-driven
- **Noise-Based**: Parameter noise, action noise

## Core Types

### Environment Configuration
```runa
Type called "RLEnvironment":
    state_space as StateSpace
    action_space as ActionSpace
    reward_function as RewardFunction
    transition_function as TransitionFunction
    discount_factor as Float
    max_steps as Integer

Type called "StateSpace":
    space_type as String              Note: discrete, continuous, mixed
    dimensions as Integer             Note: State space dimensionality
    bounds as Optional[Tuple[Vector[Float], Vector[Float]]]  Note: Min/max bounds
    discrete_size as Optional[Integer]  Note: Size of discrete space
```

### Value Functions
```runa
Type called "ValueFunction":
    function_type as String           Note: tabular, linear, neural
    parameters as Matrix[Float]       Note: Function parameters/weights
    state_features as Optional[FeatureExtractor]
    approximation_error as Float

Type called "QFunction":
    function_type as String           Note: tabular, linear, dqn
    parameters as Matrix[Float]       Note: Q-function parameters
    target_parameters as Optional[Matrix[Float]]  Note: Target network parameters
    update_frequency as Integer       Note: Target network update frequency
```

## Bellman Equations and Value Functions

### State Value Function
```runa
Import "math/ai_math/reinforcement" as RL

Note: Bellman equation for state value function
Let environment be RLEnvironment with:
    state_space: discrete_state_space
    action_space: discrete_action_space
    discount_factor: 0.99
    max_steps: 100

Let value_config be ValueFunctionConfig with:
    function_type: "tabular"
    num_states: environment.state_space.discrete_size
    learning_rate: 0.1
    convergence_threshold: 1e-6

Let state_values be RL.initialize_state_value_function(value_config)

Note: Value iteration using Bellman equation
Let converged be false
Let iteration be 0
While not converged and iteration < 1000:
    Let updated_values be RL.bellman_value_update(
        state_values,
        environment,
        value_config
    )
    
    Let value_change be RL.compute_value_change(state_values, updated_values)
    Set converged to value_change < value_config.convergence_threshold
    Set state_values to updated_values
    Set iteration to iteration + 1

Display "Value iteration converged after " joined with String(iteration) joined with " iterations"
```

**Mathematical Formula**: V(s) = max_a Σ_{s'} P(s'|s,a)[R(s,a,s') + γV(s')]

**Properties**:
- Represents expected future reward from state s
- Satisfies Bellman optimality equation
- Unique solution for given MDP

### Action Value Function (Q-Function)
```runa
Note: Q-function representing state-action values
Let q_config be QFunctionConfig with:
    function_type: "tabular"
    num_states: environment.state_space.discrete_size
    num_actions: environment.action_space.discrete_size
    learning_rate: 0.1
    epsilon_greedy: 0.1

Let q_function be RL.initialize_q_function(q_config)

Note: Q-learning update rule
Process called "q_learning_update" that takes state as Integer, action as Integer, reward as Float, next_state as Integer, done as Boolean:
    Let current_q be RL.get_q_value(q_function, state, action)
    
    Let next_q_max as String
    If done:
        Set next_q_max to "0.0"
    Otherwise:
        Set next_q_max to RL.get_max_q_value(q_function, next_state)
    
    Note: Q-learning update: Q(s,a) ← Q(s,a) + α[r + γmax Q(s',a') - Q(s,a)]
    Let target_q be MathOps.add(reward.to_string(), 
        MathOps.multiply(environment.discount_factor.to_string(), next_q_max, 15).result_value, 15)
    
    Let td_error be MathOps.subtract(target_q.result_value, current_q, 15)
    Let learning_step be MathOps.multiply(q_config.learning_rate.to_string(), td_error.result_value, 15)
    Let new_q_value be MathOps.add(current_q, learning_step.result_value, 15)
    
    Call RL.update_q_value(q_function, state, action, new_q_value.result_value)
```

**Mathematical Formula**: Q(s,a) = Σ_{s'} P(s'|s,a)[R(s,a,s') + γ max_{a'} Q(s',a')]

## Deep Q-Learning (DQN)

### Deep Q-Network Implementation
```runa
Note: Neural network Q-function approximation
Let dqn_config be DQNConfig with:
    state_dimension: 84 * 84 * 4      Note: Atari-style state representation
    action_dimension: environment.action_space.discrete_size
    hidden_layers: [512, 512]         Note: Hidden layer sizes
    learning_rate: 2.5e-4            Note: Adam learning rate
    batch_size: 32                   Note: Minibatch size
    target_update_frequency: 1000    Note: Target network update frequency
    experience_replay_size: 100000   Note: Replay buffer size

Let main_network be RL.create_dqn_network(dqn_config)
Let target_network be RL.create_dqn_network(dqn_config)

Note: Initialize target network with main network weights
Call RL.copy_network_parameters(main_network, target_network)

Note: Experience replay buffer
Let replay_buffer be RL.create_experience_replay_buffer(dqn_config.experience_replay_size)
```

### DQN Training Step
```runa
Note: DQN training with experience replay
Process called "dqn_training_step" that takes experience as Experience:
    Note: Add experience to replay buffer
    Call RL.add_experience(replay_buffer, experience)
    
    If RL.buffer_size(replay_buffer) >= dqn_config.batch_size:
        Note: Sample minibatch from replay buffer
        Let minibatch be RL.sample_minibatch(replay_buffer, dqn_config.batch_size)
        
        Note: Compute Q-targets using target network
        Let q_targets be RL.compute_dqn_targets(
            minibatch,
            target_network,
            environment.discount_factor
        )
        
        Note: Compute Q-values using main network
        Let q_values be RL.compute_dqn_values(minibatch, main_network)
        
        Note: Compute loss and update main network
        Let loss be RL.compute_dqn_loss(q_values, q_targets)
        Let gradients be RL.compute_dqn_gradients(loss, main_network)
        Call RL.update_network_parameters(main_network, gradients, dqn_config.learning_rate)
        
        Note: Update target network periodically
        If training_step % dqn_config.target_update_frequency == 0:
            Call RL.copy_network_parameters(main_network, target_network)
```

### Double DQN Enhancement
```runa
Note: Double DQN to reduce overestimation bias
Process called "compute_double_dqn_targets" that takes minibatch as List[Experience], main_net as NeuralNetwork, target_net as NeuralNetwork, gamma as Float returns Vector[Float]:
    Let targets be List[String]()
    
    For Each experience in minibatch:
        If experience.done:
            Call targets.add(experience.reward.to_string())
        Otherwise:
            Note: Use main network to select action
            Let next_q_values be RL.forward_network(main_net, experience.next_state)
            Let best_action be RL.argmax_q_values(next_q_values)
            
            Note: Use target network to evaluate selected action
            Let target_q_values be RL.forward_network(target_net, experience.next_state)
            Let target_q_value be target_q_values.get(best_action)
            
            Let discounted_future be MathOps.multiply(gamma.to_string(), target_q_value, 15)
            Let target_value be MathOps.add(experience.reward.to_string(), discounted_future.result_value, 15)
            Call targets.add(target_value.result_value)
    
    Return Vector with components: targets
```

## Policy Gradient Methods

### Policy Representation
```runa
Note: Neural network policy representation
Let policy_config be PolicyConfig with:
    state_dimension: environment.state_space.dimensions
    action_dimension: environment.action_space.dimensions
    hidden_layers: [256, 256]
    activation: "tanh"
    output_activation: "softmax"    Note: For discrete actions
    learning_rate: 3e-4

Let policy_network be RL.create_policy_network(policy_config)
```

### REINFORCE Algorithm
```runa
Note: Monte Carlo policy gradient (REINFORCE)
Process called "reinforce_update" that takes episode_trajectory as List[Experience]:
    Let policy_gradients be RL.initialize_gradients(policy_network)
    Let baseline_value be RL.compute_episode_baseline(episode_trajectory)
    
    Note: Compute returns and advantages
    Let returns be RL.compute_discounted_returns(episode_trajectory, environment.discount_factor)
    
    Let step_idx be 0
    For Each experience in episode_trajectory:
        Let return_value be returns.get(step_idx)
        Let advantage be MathOps.subtract(return_value, baseline_value, 15)
        
        Note: Compute log probability of taken action
        Let action_probs be RL.forward_policy_network(policy_network, experience.state)
        Let log_prob be RL.compute_log_probability(action_probs, experience.action)
        
        Note: Policy gradient: ∇J(θ) = ∇log π(a|s,θ) * A(s,a)
        Let gradient_contribution be MathOps.multiply(log_prob, advantage.result_value, 15)
        Call RL.accumulate_gradients(policy_gradients, gradient_contribution.result_value)
        
        Set step_idx to step_idx + 1
    
    Note: Update policy parameters
    Call RL.update_policy_parameters(policy_network, policy_gradients, policy_config.learning_rate)

Display "REINFORCE policy update completed"
```

**Mathematical Formula**: ∇J(θ) = E[∇log π(a|s,θ) Q(s,a)]

### Actor-Critic Methods
```runa
Note: Actor-Critic combines policy gradient with value function
Let actor_critic_config be ActorCriticConfig with:
    actor_lr: 3e-4                   Note: Policy learning rate
    critic_lr: 1e-3                  Note: Value function learning rate
    gamma: 0.99                      Note: Discount factor
    lambda: 0.95                     Note: GAE lambda parameter

Let actor_network be RL.create_policy_network(policy_config)
Let critic_network be RL.create_value_network(value_config)

Process called "actor_critic_update" that takes experience as Experience:
    Note: Compute value estimates
    Let state_value be RL.forward_value_network(critic_network, experience.state)
    Let next_state_value be RL.forward_value_network(critic_network, experience.next_state)
    
    Note: Compute TD error for critic
    Let target_value as String
    If experience.done:
        Set target_value to experience.reward.to_string()
    Otherwise:
        Let discounted_next = MathOps.multiply(actor_critic_config.gamma.to_string(), next_state_value, 15)
        Set target_value to MathOps.add(experience.reward.to_string(), discounted_next.result_value, 15).result_value
    
    Let td_error be MathOps.subtract(target_value, state_value, 15)
    
    Note: Update critic (value function)
    Let critic_loss be MathOps.multiply(td_error.result_value, td_error.result_value, 15)  Note: Squared TD error
    Let critic_gradients be RL.compute_critic_gradients(critic_loss.result_value, critic_network)
    Call RL.update_network_parameters(critic_network, critic_gradients, actor_critic_config.critic_lr)
    
    Note: Update actor (policy) using TD error as advantage
    Let action_probs be RL.forward_policy_network(actor_network, experience.state)
    Let log_prob be RL.compute_log_probability(action_probs, experience.action)
    Let policy_loss be MathOps.multiply("-1.0", MathOps.multiply(log_prob, td_error.result_value, 15).result_value, 15)
    
    Let actor_gradients be RL.compute_actor_gradients(policy_loss.result_value, actor_network)
    Call RL.update_network_parameters(actor_network, actor_gradients, actor_critic_config.actor_lr)

Display "Actor-Critic update completed"
```

## Advanced RL Algorithms

### Proximal Policy Optimization (PPO)
```runa
Note: PPO with clipped surrogate objective
Let ppo_config be PPOConfig with:
    learning_rate: 3e-4
    clip_ratio: 0.2                  Note: Clipping parameter ε
    value_coef: 0.5                  Note: Value function coefficient
    entropy_coef: 0.01               Note: Entropy regularization
    max_grad_norm: 0.5               Note: Gradient clipping
    ppo_epochs: 4                    Note: PPO update epochs
    batch_size: 64

Process called "ppo_update" that takes trajectory_batch as List[Experience]:
    Note: Compute old action probabilities for importance sampling
    Let old_action_probs be RL.compute_trajectory_action_probs(actor_network, trajectory_batch)
    
    Let epoch be 0
    While epoch < ppo_config.ppo_epochs:
        Note: Compute current action probabilities
        Let current_action_probs be RL.compute_trajectory_action_probs(actor_network, trajectory_batch)
        
        Note: Compute importance sampling ratio
        Let prob_ratios be RL.compute_probability_ratios(current_action_probs, old_action_probs)
        
        Note: Compute advantages using GAE
        Let advantages be RL.compute_gae_advantages(trajectory_batch, critic_network, ppo_config)
        
        Note: PPO clipped surrogate objective
        Let clipped_ratios be RL.clip_probability_ratios(prob_ratios, ppo_config.clip_ratio)
        Let surrogate_1 be element_wise_multiply(prob_ratios, advantages)
        Let surrogate_2 be element_wise_multiply(clipped_ratios, advantages)
        Let policy_loss be MathOps.multiply("-1.0", element_wise_min(surrogate_1, surrogate_2), 15)
        
        Note: Value function loss
        Let value_predictions be RL.compute_trajectory_values(critic_network, trajectory_batch)
        Let value_targets be RL.compute_value_targets(trajectory_batch, ppo_config.gamma)
        Let value_loss be RL.mse_loss(value_predictions, value_targets)
        
        Note: Entropy bonus for exploration
        Let entropy_bonus = RL.compute_policy_entropy(current_action_probs)
        
        Note: Combined loss
        Let total_loss be MathOps.add(
            policy_loss.result_value,
            MathOps.multiply(ppo_config.value_coef.to_string(), value_loss, 15).result_value,
            15
        )
        Set total_loss to MathOps.subtract(
            total_loss.result_value,
            MathOps.multiply(ppo_config.entropy_coef.to_string(), entropy_bonus, 15).result_value,
            15
        )
        
        Note: Update networks
        Let gradients be RL.compute_combined_gradients(total_loss.result_value, actor_network, critic_network)
        Let clipped_gradients be RL.clip_gradients(gradients, ppo_config.max_grad_norm)
        Call RL.update_networks(actor_network, critic_network, clipped_gradients, ppo_config.learning_rate)
        
        Set epoch to epoch + 1

Display "PPO update completed with " joined with String(ppo_config.ppo_epochs) joined with " epochs"
```

### Soft Actor-Critic (SAC)
```runa
Note: SAC for continuous control with entropy regularization
Let sac_config be SACConfig with:
    actor_lr: 3e-4
    critic_lr: 3e-4
    alpha_lr: 3e-4                   Note: Temperature parameter learning rate
    gamma: 0.99
    tau: 0.005                       Note: Soft target update rate
    alpha: 0.2                       Note: Initial temperature
    automatic_entropy_tuning: true

Let sac_actor be RL.create_sac_actor_network(policy_config)
Let sac_critic_1 be RL.create_sac_critic_network(value_config)
Let sac_critic_2 be RL.create_sac_critic_network(value_config)
Let sac_target_critic_1 be RL.create_sac_critic_network(value_config)
Let sac_target_critic_2 be RL.create_sac_critic_network(value_config)

Process called "sac_update" that takes batch as List[Experience]:
    Note: Update critics using Bellman backup
    Let next_actions, next_log_probs be RL.sample_actions_with_log_probs(sac_actor, get_next_states(batch))
    
    Let target_q1 be RL.compute_critic_values(sac_target_critic_1, get_next_states(batch), next_actions)
    Let target_q2 be RL.compute_critic_values(sac_target_critic_2, get_next_states(batch), next_actions)
    Let target_q be element_wise_min(target_q1, target_q2)
    
    Note: SAC target: r + γ(Q_target - α*log_π)
    Let entropy_term be element_wise_multiply(sac_config.alpha.to_string(), next_log_probs)
    Let bellman_target be element_wise_subtract(target_q, entropy_term)
    Set bellman_target to element_wise_add(get_rewards(batch), 
        element_wise_multiply(sac_config.gamma.to_string(), bellman_target))
    
    Note: Critic loss
    Let q1_values be RL.compute_critic_values(sac_critic_1, get_states(batch), get_actions(batch))
    Let q2_values be RL.compute_critic_values(sac_critic_2, get_states(batch), get_actions(batch))
    
    Let critic1_loss be RL.mse_loss(q1_values, bellman_target)
    Let critic2_loss be RL.mse_loss(q2_values, bellman_target)
    
    Call RL.update_critic_networks(sac_critic_1, sac_critic_2, critic1_loss, critic2_loss, sac_config.critic_lr)
    
    Note: Update actor
    Let current_actions, current_log_probs be RL.sample_actions_with_log_probs(sac_actor, get_states(batch))
    Let q1_new be RL.compute_critic_values(sac_critic_1, get_states(batch), current_actions)
    Let q2_new be RL.compute_critic_values(sac_critic_2, get_states(batch), current_actions)
    Let q_new be element_wise_min(q1_new, q2_new)
    
    Note: SAC actor loss: α*log_π - Q
    Let entropy_penalty be element_wise_multiply(sac_config.alpha.to_string(), current_log_probs)
    Let actor_loss be element_wise_subtract(entropy_penalty, q_new)
    
    Call RL.update_actor_network(sac_actor, actor_loss, sac_config.actor_lr)
    
    Note: Soft target update
    Call RL.soft_update_target_networks(
        sac_critic_1, sac_target_critic_1,
        sac_critic_2, sac_target_critic_2,
        sac_config.tau
    )

Display "SAC update completed"
```

## Exploration Strategies

### ε-Greedy Exploration
```runa
Note: ε-greedy action selection
Process called "epsilon_greedy_action" that takes q_values as Vector[Float], epsilon as Float, step as Integer returns Integer:
    Let decay_rate be 0.995
    Let current_epsilon be MathOps.multiply(
        epsilon.to_string(),
        MathOps.power(decay_rate.to_string(), step.to_string(), 15).result_value,
        15
    )
    
    Let random_val be SecureRandom.generate_uniform_float(random_generator, 0.0, 1.0)
    
    If random_val < Parse current_epsilon.result_value as Float:
        Note: Explore: choose random action
        Let num_actions be q_values.dimension
        Let random_action be SecureRandom.generate_uniform_integer(random_generator, 0, num_actions - 1)
        Return random_action
    Otherwise:
        Note: Exploit: choose greedy action
        Return RL.argmax_q_values(q_values)
```

### Upper Confidence Bound (UCB)
```runa
Note: UCB for multi-armed bandits and exploration
Process called "ucb_action_selection" that takes q_values as Vector[Float], action_counts as Vector[Integer], total_steps as Integer, c as Float returns Integer:
    Let ucb_values be List[String]()
    
    Let action_idx be 0
    While action_idx < q_values.dimension:
        Let q_value be q_values.components.get(action_idx)
        Let count be action_counts.components.get(action_idx)
        
        If Parse count as Integer == 0:
            Note: Unvisited actions get infinite confidence
            Call ucb_values.add("999999.0")
        Otherwise:
            Note: UCB: Q(a) + c*sqrt(ln(t)/N(a))
            Let confidence_term be MathOps.multiply(
                c.to_string(),
                MathOps.square_root(
                    MathOps.divide(
                        MathOps.natural_logarithm(total_steps.to_string(), 15).result_value,
                        count,
                        15
                    ).result_value,
                    15
                ).result_value,
                15
            )
            
            Let ucb_value be MathOps.add(q_value, confidence_term.result_value, 15)
            Call ucb_values.add(ucb_value.result_value)
        
        Set action_idx to action_idx + 1
    
    Return RL.argmax_values(Vector with components: ucb_values)
```

### Thompson Sampling
```runa
Note: Bayesian exploration via posterior sampling
Process called "thompson_sampling_action" that takes reward_means as Vector[Float], reward_variances as Vector[Float] returns Integer:
    Let sampled_values be List[String]()
    
    Let action_idx be 0
    While action_idx < reward_means.dimension:
        Let mean be reward_means.components.get(action_idx)
        Let variance be reward_variances.components.get(action_idx)
        
        Note: Sample from Gaussian posterior
        Let sampled_reward be Distributions.sample_normal(
            Parse mean as Float,
            MathOps.square_root(variance, 15).result_value
        )
        
        Call sampled_values.add(sampled_reward.to_string())
        Set action_idx to action_idx + 1
    
    Return RL.argmax_values(Vector with components: sampled_values)
```

## Model-Based Reinforcement Learning

### Dynamics Model Learning
```runa
Note: Learn environment dynamics from experience
Let dynamics_config be DynamicsModelConfig with:
    state_dim: environment.state_space.dimensions
    action_dim: environment.action_space.dimensions
    hidden_layers: [256, 256]
    ensemble_size: 5                 Note: Model ensemble for uncertainty
    learning_rate: 1e-3

Let dynamics_model be RL.create_dynamics_ensemble(dynamics_config)

Process called "train_dynamics_model" that takes experience_buffer as List[Experience]:
    Let training_data be RL.prepare_dynamics_training_data(experience_buffer)
    
    Let epoch be 0
    While epoch < dynamics_config.training_epochs:
        Let batch be RL.sample_dynamics_batch(training_data, dynamics_config.batch_size)
        
        Note: Predict next state and reward
        Let predictions be RL.forward_dynamics_ensemble(dynamics_model, batch)
        Let targets be RL.extract_dynamics_targets(batch)
        
        Note: Compute ensemble loss with uncertainty
        Let ensemble_loss be RL.compute_ensemble_loss(predictions, targets)
        
        Note: Update each model in ensemble
        Let model_idx be 0
        While model_idx < dynamics_config.ensemble_size:
            Let model_gradients be RL.compute_model_gradients(
                dynamics_model.models.get(model_idx),
                ensemble_loss.model_losses.get(model_idx)
            )
            Call RL.update_model_parameters(
                dynamics_model.models.get(model_idx),
                model_gradients,
                dynamics_config.learning_rate
            )
            Set model_idx to model_idx + 1
        
        Set epoch to epoch + 1

Display "Dynamics model training completed"
```

### Model Predictive Control (MPC)
```runa
Note: MPC using learned dynamics model
Let mpc_config be MPCConfig with:
    planning_horizon: 10             Note: Number of steps to plan ahead
    num_samples: 1000               Note: Number of action sequences to sample
    num_top_candidates: 100         Note: Top sequences to refine
    num_iterations: 5               Note: CEM iterations

Process called "mpc_planning" that takes current_state as Vector[Float] returns Integer:
    Note: Cross-Entropy Method for action sequence optimization
    Let action_dim be environment.action_space.dimensions
    Let sequence_length be mpc_config.planning_horizon
    
    Note: Initialize action sequence distribution
    Let mean_actions be RL.initialize_zero_actions(sequence_length, action_dim)
    Let action_covariance be RL.initialize_identity_covariance(sequence_length, action_dim)
    
    Let iteration be 0
    While iteration < mpc_config.num_iterations:
        Note: Sample action sequences
        Let action_sequences be RL.sample_action_sequences(
            mean_actions,
            action_covariance,
            mpc_config.num_samples
        )
        
        Note: Evaluate sequences using dynamics model
        Let sequence_rewards be List[Float]()
        For Each sequence in action_sequences:
            Let predicted_reward be RL.evaluate_action_sequence(
                current_state,
                sequence,
                dynamics_model,
                environment.reward_function,
                environment.discount_factor
            )
            Call sequence_rewards.add(predicted_reward)
        
        Note: Select top performing sequences
        Let top_sequences be RL.select_top_sequences(
            action_sequences,
            sequence_rewards,
            mpc_config.num_top_candidates
        )
        
        Note: Update distribution parameters
        Set mean_actions to RL.compute_sequence_mean(top_sequences)
        Set action_covariance to RL.compute_sequence_covariance(top_sequences, mean_actions)
        
        Set iteration to iteration + 1
    
    Note: Return first action of best sequence
    Return mean_actions.get(0)
```

## Multi-Agent Reinforcement Learning

### Independent Q-Learning
```runa
Note: Multiple agents learning independently
Let num_agents be 3
Let agent_configs be List[QFunctionConfig]()

Let agent_idx be 0
While agent_idx < num_agents:
    Let agent_config be QFunctionConfig with:
        function_type: "neural"
        state_dimension: environment.state_space.dimensions
        action_dimension: environment.action_space.discrete_size
        learning_rate: 1e-3
        epsilon_greedy: 0.1
    Call agent_configs.add(agent_config)
    Set agent_idx to agent_idx + 1

Let agent_q_functions be RL.create_agent_q_functions(agent_configs)

Process called "multi_agent_update" that takes joint_experience as MultiAgentExperience:
    Let agent_idx be 0
    While agent_idx < num_agents:
        Let agent_experience be joint_experience.agent_experiences.get(agent_idx)
        Let agent_q_function be agent_q_functions.get(agent_idx)
        
        Note: Independent Q-learning update
        Call RL.q_learning_update(
            agent_q_function,
            agent_experience,
            agent_configs.get(agent_idx)
        )
        
        Set agent_idx to agent_idx + 1

Display "Multi-agent independent learning update completed"
```

### Centralized Training Decentralized Execution (CTDE)
```runa
Note: MADDPG-style centralized critic
Let maddpg_config be MADDPGConfig with:
    num_agents: 3
    actor_lr: 1e-3
    critic_lr: 1e-3
    gamma: 0.95
    tau: 0.01

Let actors be RL.create_multi_agent_actors(maddpg_config)
Let centralized_critic be RL.create_centralized_critic(maddpg_config)

Process called "maddpg_update" that takes joint_batch as List[MultiAgentExperience]:
    Note: Compute centralized Q-values using global state and all actions
    Let global_states be RL.extract_global_states(joint_batch)
    Let joint_actions be RL.extract_joint_actions(joint_batch)
    Let centralized_q_values be RL.forward_centralized_critic(
        centralized_critic,
        global_states,
        joint_actions
    )
    
    Note: Compute centralized targets
    Let next_actions be RL.compute_next_joint_actions(actors, joint_batch)
    Let target_q_values be RL.compute_centralized_targets(
        centralized_critic,
        joint_batch,
        next_actions,
        maddpg_config.gamma
    )
    
    Note: Update centralized critic
    Let critic_loss be RL.mse_loss(centralized_q_values, target_q_values)
    Call RL.update_centralized_critic(centralized_critic, critic_loss, maddpg_config.critic_lr)
    
    Note: Update each agent's actor using centralized critic gradients
    Let agent_idx be 0
    While agent_idx < maddpg_config.num_agents:
        Let actor_gradients be RL.compute_actor_gradients_with_centralized_critic(
            actors.get(agent_idx),
            centralized_critic,
            joint_batch,
            agent_idx
        )
        Call RL.update_actor(actors.get(agent_idx), actor_gradients, maddpg_config.actor_lr)
        Set agent_idx to agent_idx + 1

Display "MADDPG centralized training update completed"
```

## Evaluation and Analysis

### Performance Metrics
```runa
Note: Comprehensive RL evaluation metrics
Process called "evaluate_rl_agent" that takes agent as RLAgent, eval_episodes as Integer returns RLEvaluationReport:
    Let episode_returns be List[Float]()
    Let episode_lengths be List[Integer]()
    Let success_rate be 0
    
    Let episode be 0
    While episode < eval_episodes:
        Let state be environment.reset()
        Let episode_return be 0.0
        Let episode_length be 0
        Let done be false
        
        While not done and episode_length < environment.max_steps:
            Let action be RL.select_action(agent, state, evaluation_mode: true)
            Let step_result be environment.step(action)
            
            Set state to step_result.next_state
            Set episode_return to episode_return + step_result.reward
            Set episode_length to episode_length + 1
            Set done to step_result.done
        
        Call episode_returns.add(episode_return)
        Call episode_lengths.add(episode_length)
        
        If RL.is_successful_episode(step_result):
            Set success_rate to success_rate + 1
        
        Set episode to episode + 1
    
    Let mean_return be compute_mean(episode_returns)
    Let std_return be compute_std(episode_returns)
    Let mean_length be compute_mean(episode_lengths)
    Set success_rate to success_rate / eval_episodes
    
    Return RLEvaluationReport with:
        mean_return: mean_return
        std_return: std_return
        mean_episode_length: mean_length
        success_rate: success_rate
        episode_returns: episode_returns
```

### Learning Curve Analysis
```runa
Note: Analyze learning progress and convergence
Process called "analyze_learning_curve" that takes training_history as List[Float] returns LearningAnalysis:
    Let smoothed_returns be RL.smooth_learning_curve(training_history, window_size: 100)
    Let convergence_point be RL.detect_convergence(smoothed_returns, patience: 200)
    Let sample_efficiency be RL.compute_sample_efficiency(training_history)
    Let final_performance be compute_mean(training_history.slice(-100))
    
    Return LearningAnalysis with:
        convergence_episode: convergence_point
        sample_efficiency: sample_efficiency
        final_performance: final_performance
        improvement_rate: RL.compute_improvement_rate(smoothed_returns)
```

## Testing and Validation

### Algorithm Correctness Tests
```runa
Note: Test Q-learning convergence on simple MDP
Process called "test_q_learning_convergence":
    Let test_env be RL.create_gridworld_environment(5, 5)  Note: 5x5 gridworld
    Let test_config be QFunctionConfig with:
        function_type: "tabular"
        learning_rate: 0.1
        epsilon_greedy: 0.1
    
    Let q_function be RL.initialize_q_function(test_config)
    
    Note: Train for sufficient episodes
    Let episode be 0
    While episode < 10000:
        Let trajectory be RL.run_episode(test_env, q_function, test_config)
        For Each experience in trajectory:
            Call q_learning_update(
                experience.state,
                experience.action,
                experience.reward,
                experience.next_state,
                experience.done
            )
        Set episode to episode + 1
    
    Note: Test that learned policy reaches goal
    Let optimal_actions be RL.extract_greedy_policy(q_function)
    Let success_rate be RL.test_policy_performance(test_env, optimal_actions, 100)
    
    Assert success_rate > 0.9
    Display "Q-learning convergence test passed"
```

### Exploration Strategy Tests
```runa
Note: Test exploration strategy effectiveness
Process called "test_exploration_strategies":
    Let bandit_env be RL.create_multi_armed_bandit([0.1, 0.3, 0.7, 0.5])  Note: Reward probabilities
    
    Note: Test ε-greedy
    Let epsilon_rewards be RL.test_bandit_strategy(bandit_env, "epsilon_greedy", 1000)
    
    Note: Test UCB
    Let ucb_rewards be RL.test_bandit_strategy(bandit_env, "ucb", 1000)
    
    Note: Test Thompson Sampling
    Let thompson_rewards be RL.test_bandit_strategy(bandit_env, "thompson_sampling", 1000)
    
    Note: Compare cumulative regret
    Let epsilon_regret be RL.compute_cumulative_regret(epsilon_rewards, optimal_reward: 0.7)
    Let ucb_regret be RL.compute_cumulative_regret(ucb_rewards, optimal_reward: 0.7)
    Let thompson_regret be RL.compute_cumulative_regret(thompson_rewards, optimal_reward: 0.7)
    
    Display "Exploration strategy comparison:"
    Display "ε-greedy final regret: " joined with String(epsilon_regret.last())
    Display "UCB final regret: " joined with String(ucb_regret.last())
    Display "Thompson final regret: " joined with String(thompson_regret.last())
```

## Related Documentation

- **[AI Math Neural Ops](neural_ops.md)**: Neural network operations for function approximation
- **[AI Math Optimization](optimization.md)**: Optimization algorithms for policy updates
- **[AI Math Loss Functions](loss_functions.md)**: Loss functions for RL training
- **[Math Probability](../probability/README.md)**: Probability distributions and sampling
- **[Math Statistics](../statistics/README.md)**: Statistical methods for evaluation

The Reinforcement Learning Mathematics module provides the mathematical foundations for implementing state-of-the-art reinforcement learning algorithms, from classical dynamic programming to modern deep RL methods.
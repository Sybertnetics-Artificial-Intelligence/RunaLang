# Intelligent Routing Module

## Overview

The Intelligent Routing module (`routing.runa`) provides advanced message routing capabilities with dynamic path discovery, load balancing, and quality-aware routing for AI agent networks. This module implements sophisticated routing algorithms, topology learning, and adaptive routing strategies to ensure optimal message delivery across complex network topologies.

## Key Features

- **Dynamic Route Discovery**: Automatic topology learning and route optimization
- **Multi-Path Routing**: Intelligent load balancing across multiple network paths
- **Quality-Aware Routing**: Path selection based on latency, bandwidth, and reliability
- **Message Fragmentation**: Large message handling with reassembly capabilities
- **Dead Letter Queue Management**: Failed message handling and recovery
- **Adaptive Routing**: Real-time route adjustment based on network conditions

## Core Types

### Routing Table

```runa
Type called "RoutingTable":
    table_id as String
    creation_time as Float
    last_update_time as Float
    max_entries as Integer
    current_entries as Integer
    refresh_interval_seconds as Float
    route_entries as List[RouteEntry]
    topology_version as Integer
    statistics as RoutingStatistics
    metadata as Dictionary[String, Any]
```

### Route Entry

```runa
Type called "RouteEntry":
    destination as String
    next_hop as String
    cost as Integer
    latency_ms as Float
    bandwidth_mbps as Float
    reliability_score as Float
    hop_count as Integer
    last_updated as Float
    route_status as RouteStatus
    quality_metrics as QualityMetrics
    usage_statistics as RouteUsageStats
```

### Routing Algorithms

```runa
Type RoutingAlgorithm is:
    | ShortestPath       # Dijkstra-based shortest path
    | LoadBalanced       # Distribute traffic across paths
    | QualityAware       # Route based on quality metrics
    | AdaptiveRouting    # Dynamic algorithm selection
    | MultiPath          # Use multiple paths simultaneously
```

## Usage Examples

### Creating and Managing Routing Tables

```runa
Import "ai/comms/routing" as Routing

Process called "setup_agent_routing" that takes agent_id as String returns RoutingSetupResult:
    Print "Setting up intelligent routing for agent: " + agent_id
    
    Note: Create routing table
    Let routing_table = Routing.create_routing_table with
        table_id as agent_id + "_routing_table" and
        max_entries as 1000 and
        refresh_interval_seconds as 60
    
    If routing_table["current_entries"] is equal to 0:
        Print "✅ Routing table created"
        Print "  Table ID: " + routing_table["table_id"]
        Print "  Max entries: " + routing_table["max_entries"]
        Print "  Refresh interval: " + routing_table["refresh_interval_seconds"] + " seconds"
        
        Note: Configure routing algorithms
        Let algorithm_config = Routing.configure_routing_algorithms with
            table as routing_table and
            primary_algorithm as "quality_aware" and
            fallback_algorithm as "shortest_path" and
            load_balancing_enabled as true
        
        If algorithm_config["success"]:
            Print "✅ Routing algorithms configured"
            Print "  Primary: Quality-aware routing"
            Print "  Fallback: Shortest path"
            Print "  Load balancing: Enabled"
        
        Note: Initialize network topology discovery
        Let topology_discovery = Routing.initialize_topology_discovery with
            routing_table as routing_table and
            discovery_method as "proactive_and_reactive" and
            discovery_interval_seconds as 30
        
        If topology_discovery["success"]:
            Print "✅ Network topology discovery initialized"
            
            Return RoutingSetupResult with:
                success as true
                routing_table as routing_table
                algorithms_configured as true
                topology_discovery_active as true
        Else:
            Print "❌ Topology discovery initialization failed: " + topology_discovery["error"]
            Return RoutingSetupResult with success as false and error as topology_discovery["error"]
    Else:
        Print "❌ Routing table creation failed"
        Return RoutingSetupResult with success as false and error as "table_creation_failed"
```

### Dynamic Route Discovery

```runa
Process called "discover_network_routes" that takes routing_table as RoutingTable returns RouteDiscoveryResult:
    Print "Discovering network routes and topology..."
    
    Let discovery_results = list containing
    
    Note: Perform network topology scan
    Let topology_scan = Routing.perform_topology_scan with
        routing_table as routing_table and
        scan_depth as 5 and
        scan_timeout_seconds as 30
    
    If topology_scan["success"]:
        Print "✅ Network topology scan completed"
        Print "  Nodes discovered: " + topology_scan["nodes_discovered"]
        Print "  Links discovered: " + topology_scan["links_discovered"]
        Print "  Network diameter: " + topology_scan["network_diameter"]
        
        Note: Analyze discovered paths
        Let discovered_nodes = topology_scan["discovered_nodes"]
        
        For each node in discovered_nodes:
            Let path_analysis = Routing.analyze_paths_to_node with
                routing_table as routing_table and
                target_node as node and
                max_paths as 3
            
            If path_analysis["success"]:
                Print "Routes to " + node["node_id"] + ": " + path_analysis["path_count"] + " paths"
                
                For each path in path_analysis["discovered_paths"]:
                    Let route_entry = Routing.create_route_entry with
                        destination as node["node_id"] and
                        path_info as path and
                        quality_metrics as path["quality_metrics"]
                    
                    Let route_addition = Routing.add_route_entry with
                        table as routing_table and
                        route_entry as route_entry
                    
                    If route_addition["success"]:
                        Add route_entry to discovery_results
                
                Print "  Best path: " + path_analysis["best_path"]["next_hop"] + 
                      " (latency: " + path_analysis["best_path"]["latency_ms"] + "ms, " +
                      "cost: " + path_analysis["best_path"]["cost"] + ")"
            Else:
                Print "⚠️ Path analysis failed for " + node["node_id"] + ": " + path_analysis["error"]
        
        Note: Optimize routing table
        Let table_optimization = Routing.optimize_routing_table with
            table as routing_table and
            optimization_strategy as "remove_redundant_and_stale"
        
        If table_optimization["success"]:
            Print "✅ Routing table optimized"
            Print "  Routes before optimization: " + table_optimization["routes_before"]
            Print "  Routes after optimization: " + table_optimization["routes_after"]
            Print "  Optimization ratio: " + (table_optimization["routes_after"] * 100.0 / table_optimization["routes_before"]) + "%"
        
        Return RouteDiscoveryResult with:
            success as true
            routes_discovered as length of discovery_results
            network_nodes as topology_scan["nodes_discovered"]
            network_links as topology_scan["links_discovered"]
            table_optimized as table_optimization["success"]
    Else:
        Print "❌ Network topology scan failed: " + topology_scan["error"]
        Return RouteDiscoveryResult with success as false and error as topology_scan["error"]
```

### Quality-Aware Routing

```runa
Process called "implement_quality_aware_routing" that takes routing_table as RoutingTable and message as Dictionary returns QualityRoutingResult:
    Print "Implementing quality-aware routing for message: " + message["message_id"]
    
    Let destination = message["receiver_id"]
    Print "  Destination: " + destination
    Print "  Message size: " + message["size_bytes"] + " bytes"
    Print "  Priority: " + message["priority"]
    
    Note: Analyze message requirements
    Let message_requirements = Routing.analyze_message_requirements with message as message
    
    Print "Message routing requirements:"
    Print "  Max latency tolerance: " + message_requirements["max_latency_ms"] + "ms"
    Print "  Min bandwidth required: " + message_requirements["min_bandwidth_mbps"] + " Mbps"
    Print "  Reliability level: " + message_requirements["reliability_level"]
    Print "  Delivery guarantee: " + message_requirements["delivery_guarantee"]
    
    Note: Get available routes to destination
    Let available_routes = Routing.get_routes_to_destination with
        table as routing_table and
        destination as destination
    
    If length of available_routes is equal to 0:
        Print "❌ No routes available to destination: " + destination
        Return QualityRoutingResult with:
            success as false
            error as "no_routes_available"
            destination as destination
    
    Print "Available routes: " + length of available_routes
    
    Note: Score routes based on quality metrics
    Let route_scoring_results = list containing
    
    For each route in available_routes:
        Let quality_score = Routing.calculate_route_quality_score with
            route as route and
            message_requirements as message_requirements and
            scoring_weights as Dictionary with:
                "latency_weight" as 0.4
                "bandwidth_weight" as 0.3
                "reliability_weight" as 0.2
                "cost_weight" as 0.1
        
        Let route_score = Dictionary with:
            "route" as route
            "quality_score" as quality_score["total_score"]
            "score_breakdown" as quality_score["score_breakdown"]
            "meets_requirements" as quality_score["meets_requirements"]
        
        Add route_score to route_scoring_results
        
        Print "Route via " + route["next_hop"] + ": " + quality_score["total_score"] + "/100"
        Print "  Latency score: " + quality_score["score_breakdown"]["latency_score"]
        Print "  Bandwidth score: " + quality_score["score_breakdown"]["bandwidth_score"]
        Print "  Reliability score: " + quality_score["score_breakdown"]["reliability_score"]
        Print "  Cost score: " + quality_score["score_breakdown"]["cost_score"]
    
    Note: Select best route
    Let best_route = Routing.select_best_route with
        scored_routes as route_scoring_results and
        selection_criteria as "highest_quality_score"
    
    If best_route["meets_requirements"]:
        Print "✅ Optimal route selected: " + best_route["route"]["next_hop"]
        Print "  Quality score: " + best_route["quality_score"] + "/100"
        Print "  Expected latency: " + best_route["route"]["latency_ms"] + "ms"
        Print "  Available bandwidth: " + best_route["route"]["bandwidth_mbps"] + " Mbps"
        Print "  Reliability: " + (best_route["route"]["reliability_score"] * 100.0) + "%"
        
        Note: Update route usage statistics
        Let usage_update = Routing.update_route_usage_statistics with
            table as routing_table and
            route as best_route["route"] and
            message_size as message["size_bytes"]
        
        Return QualityRoutingResult with:
            success as true
            selected_route as best_route["route"]
            quality_score as best_route["quality_score"]
            meets_requirements as true
            routing_decision_time_ms as calculate_routing_decision_time()
    Else:
        Print "⚠️ No route fully meets requirements - selecting best available"
        
        Let fallback_route = select_fallback_route with scored_routes as route_scoring_results
        
        Print "Fallback route selected: " + fallback_route["route"]["next_hop"]
        Print "  Quality score: " + fallback_route["quality_score"] + "/100"
        Print "  Requirements met: Partial"
        
        Return QualityRoutingResult with:
            success as true
            selected_route as fallback_route["route"]
            quality_score as fallback_route["quality_score"]
            meets_requirements as false
            fallback_used as true
```

## Load Balancing and Multi-Path Routing

### Intelligent Load Distribution

```runa
Process called "implement_load_balanced_routing" that takes routing_table as RoutingTable and message_batch as List[Dictionary] returns LoadBalancingResult:
    Print "Implementing load-balanced routing for message batch..."
    Print "  Batch size: " + length of message_batch
    
    Let load_balancing_results = list containing
    Let route_loads = Dictionary containing
    
    Note: Analyze available routes and their current loads
    Let route_analysis = Routing.analyze_route_loads with table as routing_table
    
    Print "Current route load analysis:"
    For each route_load in route_analysis["route_loads"]:
        Set route_loads[route_load["route_id"]] to route_load["current_load"]
        Print "  " + route_load["route_id"] + ": " + route_load["current_load"] + "% utilization"
    
    Note: Configure load balancing strategy
    Let load_balancing_config = Routing.configure_load_balancing with
        table as routing_table and
        strategy as "weighted_round_robin" and
        weight_factors as Dictionary with:
            "bandwidth_capacity" as 0.4
            "current_utilization" as 0.3
            "latency_performance" as 0.2
            "reliability_history" as 0.1 and
        rebalancing_threshold as 20.0  Note: Trigger rebalancing if load diff > 20%
    
    If load_balancing_config["success"]:
        Print "✅ Load balancing configured: Weighted round-robin"
        
        Note: Distribute messages across routes
        For each message in message_batch:
            Let destination = message["receiver_id"]
            
            Note: Get suitable routes for this destination
            Let suitable_routes = Routing.get_suitable_routes_for_load_balancing with
                table as routing_table and
                destination as destination and
                message_requirements as analyze_message_requirements(message)
            
            If length of suitable_routes > 0:
                Note: Select route based on load balancing algorithm
                Let selected_route = Routing.select_route_for_load_balancing with
                    suitable_routes as suitable_routes and
                    current_loads as route_loads and
                    message_size as message["size_bytes"]
                
                Note: Update route load tracking
                Set route_loads[selected_route["route_id"]] to route_loads[selected_route["route_id"]] + calculate_message_load(message)
                
                Let routing_result = Dictionary with:
                    "message_id" as message["message_id"]
                    "selected_route" as selected_route
                    "destination" as destination
                    "load_balance_score" as selected_route["load_balance_score"]
                
                Add routing_result to load_balancing_results
                
                Print "Message " + message["message_id"] + " -> Route " + selected_route["next_hop"]
            Else:
                Print "⚠️ No suitable routes for message " + message["message_id"] + " to " + destination
        
        Note: Analyze load distribution effectiveness
        Let distribution_analysis = Routing.analyze_load_distribution with
            routing_results as load_balancing_results and
            final_loads as route_loads
        
        Print "Load balancing results:"
        Print "  Messages distributed: " + length of load_balancing_results
        Print "  Routes utilized: " + distribution_analysis["routes_used"]
        Print "  Load variance: " + distribution_analysis["load_variance"]
        Print "  Distribution efficiency: " + distribution_analysis["efficiency_score"] + "%"
        
        Return LoadBalancingResult with:
            success as true
            messages_distributed as length of load_balancing_results
            routes_utilized as distribution_analysis["routes_used"]
            load_variance as distribution_analysis["load_variance"]
            efficiency_score as distribution_analysis["efficiency_score"]
            routing_results as load_balancing_results
    Else:
        Print "❌ Load balancing configuration failed: " + load_balancing_config["error"]
        Return LoadBalancingResult with success as false and error as load_balancing_config["error"]
```

### Multi-Path Message Transmission

```runa
Process called "implement_multipath_transmission" that takes routing_table as RoutingTable and large_message as Dictionary returns MultipathResult:
    Print "Implementing multi-path transmission for large message..."
    Print "  Message ID: " + large_message["message_id"]
    Print "  Message size: " + large_message["size_bytes"] + " bytes"
    Print "  Destination: " + large_message["receiver_id"]
    
    Let destination = large_message["receiver_id"]
    
    Note: Get multiple paths to destination
    Let available_paths = Routing.get_multiple_paths_to_destination with
        table as routing_table and
        destination as destination and
        max_paths as 4 and
        path_diversity_threshold as 0.7
    
    If length of available_paths < 2:
        Print "❌ Insufficient paths for multi-path transmission (need at least 2)"
        Return MultipathResult with:
            success as false
            error as "insufficient_paths"
            paths_available as length of available_paths
    
    Print "Available paths for multi-path transmission: " + length of available_paths
    
    For each path in available_paths:
        Print "  Path " + path["path_id"] + " via " + path["next_hop"] + 
              " (bandwidth: " + path["bandwidth_mbps"] + " Mbps, " +
              "latency: " + path["latency_ms"] + "ms)"
    
    Note: Calculate optimal message fragmentation
    Let fragmentation_strategy = Routing.calculate_multipath_fragmentation with
        message as large_message and
        available_paths as available_paths and
        fragmentation_algorithm as "bandwidth_proportional"
    
    If fragmentation_strategy["success"]:
        Print "✅ Fragmentation strategy calculated"
        Print "  Total fragments: " + fragmentation_strategy["fragment_count"]
        Print "  Fragment size range: " + fragmentation_strategy["min_fragment_size"] + 
              " - " + fragmentation_strategy["max_fragment_size"] + " bytes"
        
        Note: Fragment the message
        Let message_fragments = Routing.fragment_message_for_multipath with
            message as large_message and
            fragmentation_strategy as fragmentation_strategy
        
        If length of message_fragments is equal to fragmentation_strategy["fragment_count"]:
            Print "✅ Message fragmented successfully"
            
            Let transmission_results = list containing
            
            Note: Transmit fragments across different paths
            For i from 0 to (length of message_fragments minus 1):
                Let fragment = message_fragments[i]
                Let path_index = i modulo length of available_paths
                Let selected_path = available_paths[path_index]
                
                Let fragment_transmission = Routing.transmit_fragment_via_path with
                    fragment as fragment and
                    path as selected_path and
                    transmission_priority as "high"
                
                If fragment_transmission["success"]:
                    Print "✅ Fragment " + fragment["fragment_id"] + 
                          " transmitted via " + selected_path["next_hop"]
                    
                    Add fragment_transmission to transmission_results
                Else:
                    Print "❌ Fragment " + fragment["fragment_id"] + 
                          " transmission failed: " + fragment_transmission["error"]
            
            Note: Monitor fragment delivery and reassembly
            Let reassembly_monitoring = Routing.monitor_fragment_reassembly with
                message_id as large_message["message_id"] and
                expected_fragments as length of message_fragments and
                reassembly_timeout_seconds as 60
            
            If reassembly_monitoring["success"]:
                Print "✅ Multi-path transmission completed successfully"
                Print "  Fragments transmitted: " + length of transmission_results
                Print "  Transmission time: " + reassembly_monitoring["total_transmission_time_ms"] + "ms"
                Print "  Reassembly time: " + reassembly_monitoring["reassembly_time_ms"] + "ms"
                Print "  Effective throughput: " + calculate_effective_throughput(large_message, reassembly_monitoring) + " Mbps"
                
                Return MultipathResult with:
                    success as true
                    paths_used as length of available_paths
                    fragments_transmitted as length of transmission_results
                    transmission_time_ms as reassembly_monitoring["total_transmission_time_ms"]
                    reassembly_time_ms as reassembly_monitoring["reassembly_time_ms"]
                    effective_throughput_mbps as calculate_effective_throughput(large_message, reassembly_monitoring)
            Else:
                Print "❌ Fragment reassembly failed: " + reassembly_monitoring["error"]
                Return MultipathResult with success as false and error as reassembly_monitoring["error"]
        Else:
            Print "❌ Message fragmentation failed"
            Return MultipathResult with success as false and error as "fragmentation_failed"
    Else:
        Print "❌ Fragmentation strategy calculation failed: " + fragmentation_strategy["error"]
        Return MultipathResult with success as false and error as fragmentation_strategy["error"]
```

## Adaptive Routing and Network Optimization

### Real-Time Route Adaptation

```runa
Process called "implement_adaptive_routing" that takes routing_table as RoutingTable returns AdaptiveRoutingResult:
    Print "Implementing adaptive routing system..."
    
    Note: Set up network condition monitoring
    Let network_monitoring = Routing.setup_network_condition_monitoring with
        table as routing_table and
        monitoring_interval_seconds as 10 and
        metrics_to_monitor as list containing "latency" and "bandwidth" and "packet_loss" and "jitter"
    
    If network_monitoring["success"]:
        Print "✅ Network condition monitoring active"
        
        Note: Configure adaptive routing parameters
        Let adaptive_config = Routing.configure_adaptive_routing with
            table as routing_table and
            adaptation_sensitivity as "medium" and
            adaptation_triggers as Dictionary with:
                "latency_increase_threshold_percent" as 50.0
                "bandwidth_decrease_threshold_percent" as 30.0
                "packet_loss_threshold_percent" as 5.0
                "route_failure_threshold" as 3 and
            adaptation_strategies as list containing "route_switching" and "load_redistribution" and "path_discovery"
        
        If adaptive_config["success"]:
            Print "✅ Adaptive routing configured"
            Print "  Sensitivity: Medium"
            Print "  Adaptation triggers: 4 metrics"
            Print "  Adaptation strategies: 3 strategies"
            
            Note: Start adaptive routing engine
            Let adaptive_engine = Routing.start_adaptive_routing_engine with
                table as routing_table and
                monitoring_system as network_monitoring["monitoring_system"] and
                adaptation_config as adaptive_config
            
            If adaptive_engine["success"]:
                Print "✅ Adaptive routing engine started"
                
                Note: Simulate network condition changes and adaptation
                Let adaptation_simulation = simulate_network_adaptation with
                    routing_table as routing_table and
                    adaptive_engine as adaptive_engine["engine"]
                
                Print "Adaptive routing simulation results:"
                Print "  Network events simulated: " + adaptation_simulation["events_simulated"]
                Print "  Adaptations triggered: " + adaptation_simulation["adaptations_triggered"]
                Print "  Average adaptation time: " + adaptation_simulation["average_adaptation_time_ms"] + "ms"
                Print "  Performance improvement: " + adaptation_simulation["performance_improvement_percent"] + "%"
                
                Return AdaptiveRoutingResult with:
                    success as true
                    monitoring_active as true
                    adaptive_engine_running as true
                    adaptations_triggered as adaptation_simulation["adaptations_triggered"]
                    performance_improvement_percent as adaptation_simulation["performance_improvement_percent"]
            Else:
                Print "❌ Adaptive routing engine failed to start: " + adaptive_engine["error"]
                Return AdaptiveRoutingResult with success as false and error as adaptive_engine["error"]
        Else:
            Print "❌ Adaptive routing configuration failed: " + adaptive_config["error"]
            Return AdaptiveRoutingResult with success as false and error as adaptive_config["error"]
    Else:
        Print "❌ Network monitoring setup failed: " + network_monitoring["error"]
        Return AdaptiveRoutingResult with success as false and error as network_monitoring["error"]
```

### Predictive Route Optimization

```runa
Process called "implement_predictive_routing" that takes routing_table as RoutingTable returns PredictiveRoutingResult:
    Print "Implementing predictive route optimization..."
    
    Note: Collect historical routing data
    Let historical_data = Routing.collect_historical_routing_data with
        table as routing_table and
        data_period_hours as 168 and  Note: One week
        metrics_to_collect as list containing "route_usage" and "performance_metrics" and "failure_patterns"
    
    If historical_data["success"]:
        Print "✅ Historical routing data collected"
        Print "  Data points: " + historical_data["data_point_count"]
        Print "  Time period: " + historical_data["data_period_hours"] + " hours"
        Print "  Routes analyzed: " + historical_data["routes_analyzed"]
        
        Note: Build predictive models
        Let predictive_models = Routing.build_predictive_routing_models with
            historical_data as historical_data["routing_data"] and
            model_types as list containing "performance_prediction" and "failure_prediction" and "congestion_prediction"
        
        If predictive_models["success"]:
            Print "✅ Predictive models built successfully"
            Print "  Performance prediction model accuracy: " + predictive_models["performance_model_accuracy"] + "%"
            Print "  Failure prediction model accuracy: " + predictive_models["failure_model_accuracy"] + "%"
            Print "  Congestion prediction model accuracy: " + predictive_models["congestion_model_accuracy"] + "%"
            
            Note: Generate route optimization recommendations
            Let optimization_recommendations = Routing.generate_route_optimizations with
                table as routing_table and
                predictive_models as predictive_models["models"] and
                prediction_horizon_hours as 24
            
            Print "Route optimization recommendations:"
            For each recommendation in optimization_recommendations["recommendations"]:
                Print "  " + recommendation["type"] + ": " + recommendation["description"]
                Print "    Expected benefit: " + recommendation["expected_benefit"]
                Print "    Implementation priority: " + recommendation["priority"]
                Print "    Confidence level: " + recommendation["confidence_percent"] + "%"
            
            Note: Apply high-priority optimizations
            Let applied_optimizations = list containing
            
            For each recommendation in optimization_recommendations["recommendations"]:
                If recommendation["priority"] is equal to "high" and recommendation["confidence_percent"] >= 80.0:
                    Let optimization_application = Routing.apply_route_optimization with
                        table as routing_table and
                        optimization as recommendation
                    
                    If optimization_application["success"]:
                        Add recommendation["type"] to applied_optimizations
                        Print "✅ Applied optimization: " + recommendation["type"]
                    Else:
                        Print "❌ Failed to apply optimization: " + recommendation["type"]
            
            Print "Predictive routing optimization completed:"
            Print "  Recommendations generated: " + length of optimization_recommendations["recommendations"]
            Print "  Optimizations applied: " + length of applied_optimizations
            
            Return PredictiveRoutingResult with:
                success as true
                models_built as true
                recommendations_count as length of optimization_recommendations["recommendations"]
                optimizations_applied as length of applied_optimizations
                prediction_accuracy as calculate_average_accuracy(predictive_models)
        Else:
            Print "❌ Predictive model building failed: " + predictive_models["error"]
            Return PredictiveRoutingResult with success as false and error as predictive_models["error"]
    Else:
        Print "❌ Historical data collection failed: " + historical_data["error"]
        Return PredictiveRoutingResult with success as false and error as historical_data["error"]
```

## Dead Letter Queue and Error Handling

### Failed Message Management

```runa
Process called "manage_failed_message_routing" that takes routing_table as RoutingTable and failed_message as Dictionary returns FailedMessageResult:
    Print "Managing failed message routing..."
    Print "  Message ID: " + failed_message["message_id"]
    Print "  Original destination: " + failed_message["original_destination"]
    Print "  Failure reason: " + failed_message["failure_reason"]
    Print "  Retry count: " + failed_message["retry_count"]
    
    Note: Analyze failure reason
    Let failure_analysis = Routing.analyze_routing_failure with
        message as failed_message and
        routing_table as routing_table and
        failure_context as failed_message["failure_context"]
    
    Print "Failure analysis:"
    Print "  Failure category: " + failure_analysis["failure_category"]
    Print "  Recoverable: " + (If failure_analysis["recoverable"] then "Yes" else "No")
    Print "  Recommended action: " + failure_analysis["recommended_action"]
    
    Match failure_analysis["recommended_action"]:
        When "retry_with_different_route":
            Note: Find alternative routes
            Let alternative_routes = Routing.find_alternative_routes with
                table as routing_table and
                destination as failed_message["original_destination"] and
                exclude_failed_routes as failed_message["previously_tried_routes"]
            
            If length of alternative_routes > 0:
                Print "✅ Alternative routes found: " + length of alternative_routes
                
                Let best_alternative = select_best_alternative_route with routes as alternative_routes
                
                Let retry_result = Routing.retry_message_routing with
                    message as failed_message and
                    alternative_route as best_alternative and
                    retry_strategy as "immediate"
                
                If retry_result["success"]:
                    Print "✅ Message successfully routed via alternative path"
                    Return FailedMessageResult with:
                        success as true
                        action_taken as "retried_alternative_route"
                        alternative_route as best_alternative
                        delivery_successful as true
                Else:
                    Print "❌ Alternative route retry failed: " + retry_result["error"]
                    Note: Send to dead letter queue
                    Let dlq_result = send_to_dead_letter_queue with
                        message as failed_message and
                        failure_reason as "alternative_route_failed"
                    
                    Return FailedMessageResult with:
                        success as false
                        action_taken as "sent_to_dlq"
                        dlq_result as dlq_result
            Else:
                Print "❌ No alternative routes available"
                Let dlq_result = send_to_dead_letter_queue with
                    message as failed_message and
                    failure_reason as "no_alternative_routes"
                
                Return FailedMessageResult with:
                    success as false
                    action_taken as "sent_to_dlq"
                    dlq_result as dlq_result
        
        When "schedule_delayed_retry":
            Let delay_seconds = calculate_retry_delay with retry_count as failed_message["retry_count"]
            
            Let delayed_retry = Routing.schedule_delayed_message_retry with
                message as failed_message and
                delay_seconds as delay_seconds and
                max_retries as 5
            
            If delayed_retry["success"]:
                Print "✅ Message scheduled for delayed retry in " + delay_seconds + " seconds"
                Return FailedMessageResult with:
                    success as true
                    action_taken as "scheduled_delayed_retry"
                    retry_delay_seconds as delay_seconds
            Else:
                Print "❌ Delayed retry scheduling failed: " + delayed_retry["error"]
                Return FailedMessageResult with success as false and error as delayed_retry["error"]
        
        When "send_to_dead_letter_queue":
            Let dlq_result = send_to_dead_letter_queue with
                message as failed_message and
                failure_reason as failure_analysis["failure_category"]
            
            Print "Message sent to dead letter queue"
            Return FailedMessageResult with:
                success as false
                action_taken as "sent_to_dlq"
                dlq_result as dlq_result
        
        Otherwise:
            Print "Unknown failure handling action: " + failure_analysis["recommended_action"]
            Return FailedMessageResult with:
                success as false
                error as "unknown_failure_action"
```

## Configuration Integration

### Routing Configuration

```runa
Process called "configure_routing_from_config" returns RoutingConfiguration:
    Import "ai/comms/config" as CommsConfig
    
    Let config = CommsConfig.get_comms_config()
    Let routing_config = config["routing"]
    
    Let routing_settings = Dictionary with:
        "max_route_entries" as routing_config["max_route_entries"]
        "route_refresh_interval_seconds" as routing_config["route_refresh_interval_seconds"]
        "default_routing_algorithm" as routing_config["algorithms"]["default_algorithm"]
        "load_balancing_enabled" as routing_config["load_balancing"]["enabled"]
        "multipath_routing_enabled" as routing_config["multipath"]["enabled"]
        "max_paths_per_destination" as routing_config["multipath"]["max_paths_per_destination"]
        "adaptive_routing_enabled" as routing_config["adaptive"]["enabled"]
        "topology_discovery_interval" as routing_config["discovery"]["topology_discovery_interval_seconds"]
        "route_quality_monitoring" as routing_config["monitoring"]["quality_monitoring_enabled"]
        "predictive_optimization" as routing_config["optimization"]["predictive_optimization_enabled"]
        "dead_letter_queue_enabled" as routing_config["error_handling"]["dead_letter_queue_enabled"]
        "max_retry_attempts" as routing_config["error_handling"]["max_retry_attempts"]
    
    Print "Routing system configured:"
    Print "  Max route entries: " + routing_settings["max_route_entries"]
    Print "  Refresh interval: " + routing_settings["route_refresh_interval_seconds"] + " seconds"
    Print "  Default algorithm: " + routing_settings["default_routing_algorithm"]
    Print "  Load balancing: " + (If routing_settings["load_balancing_enabled"] then "Enabled" else "Disabled")
    Print "  Multi-path routing: " + (If routing_settings["multipath_routing_enabled"] then "Enabled" else "Disabled")
    Print "  Adaptive routing: " + (If routing_settings["adaptive_routing_enabled"] then "Enabled" else "Disabled")
    Print "  Quality monitoring: " + (If routing_settings["route_quality_monitoring"] then "Enabled" else "Disabled")
    Print "  Predictive optimization: " + (If routing_settings["predictive_optimization"] then "Enabled" else "Disabled")
    
    Return routing_settings
```

## Best Practices

### 1. **Route Management**
- Regularly refresh routing tables to maintain current topology
- Use appropriate routing algorithms based on network characteristics
- Implement proper route metrics collection and analysis

### 2. **Quality Optimization**
- Monitor route quality metrics continuously
- Use quality-aware routing for critical communications
- Implement adaptive routing for dynamic network conditions

### 3. **Load Balancing**
- Distribute traffic based on route capacity and current load
- Use multi-path routing for large message transmission
- Monitor load distribution effectiveness regularly

### 4. **Error Handling**
- Implement comprehensive retry strategies with exponential backoff
- Use dead letter queues for messages that cannot be delivered
- Monitor and analyze routing failure patterns

### 5. **Performance**
- Use predictive modeling for proactive route optimization
- Implement caching for frequently accessed routing decisions
- Optimize routing table size based on network scale

The Intelligent Routing module provides sophisticated routing capabilities that enable AI agents to communicate efficiently across complex, dynamic network topologies with optimal performance, reliability, and adaptability.
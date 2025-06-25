"""
Runa Performance Monitor - Production-Ready Framework

Comprehensive performance monitoring for Runa language:
- Compilation time tracking (<100ms target)
- Memory usage monitoring (<500MB target)
- Performance regression detection
- Real-time metrics collection
- Performance optimization recommendations
"""

import time
import psutil
import threading
import json
import os
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, asdict
from enum import Enum
from contextlib import contextmanager
import statistics
from collections import defaultdict, deque


class MetricType(Enum):
    """Performance metric types."""
    COMPILATION_TIME = "compilation_time"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    TOKENIZATION_TIME = "tokenization_time"
    PARSING_TIME = "parsing_time"
    SEMANTIC_ANALYSIS_TIME = "semantic_analysis_time"
    BYTECODE_GENERATION_TIME = "bytecode_generation_time"
    ERROR_COUNT = "error_count"
    WARNING_COUNT = "warning_count"


class PerformanceLevel(Enum):
    """Performance level classifications."""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    POOR = "poor"
    CRITICAL = "critical"


@dataclass
class PerformanceMetric:
    """Individual performance metric with metadata."""
    metric_type: MetricType
    value: float
    unit: str
    timestamp: float
    context: Dict[str, Any]
    performance_level: PerformanceLevel
    target_value: Optional[float] = None
    threshold_warning: Optional[float] = None
    threshold_critical: Optional[float] = None


@dataclass
class PerformanceReport:
    """Complete performance report with analysis."""
    report_id: str
    timestamp: float
    duration: float
    metrics: List[PerformanceMetric]
    summary: Dict[str, Any]
    recommendations: List[str]
    alerts: List[str]


class PerformanceTargets:
    """Performance targets for Runa language."""
    
    # Compilation targets
    COMPILATION_TIME_100_LINES = 50.0  # ms
    COMPILATION_TIME_1000_LINES = 100.0  # ms
    COMPILATION_TIME_10000_LINES = 500.0  # ms
    
    # Memory targets
    MEMORY_USAGE_BASELINE = 50.0  # MB
    MEMORY_USAGE_LARGE_PROGRAM = 500.0  # MB
    MEMORY_USAGE_COMPLEX_OPERATION = 1000.0  # MB
    
    # Component targets
    TOKENIZATION_TIME_PER_LINE = 0.1  # ms
    PARSING_TIME_PER_LINE = 0.2  # ms
    SEMANTIC_ANALYSIS_TIME_PER_LINE = 0.3  # ms
    BYTECODE_GENERATION_TIME_PER_LINE = 0.2  # ms
    
    # Error targets
    MAX_ERRORS_PER_COMPILATION = 10
    MAX_WARNINGS_PER_COMPILATION = 50


class PerformanceMonitor:
    """
    Production-ready performance monitor for Runa language.
    
    Features:
    - Real-time performance tracking
    - Automatic threshold detection
    - Performance regression alerts
    - Optimization recommendations
    - Historical trend analysis
    """
    
    def __init__(self, output_dir: str = "performance_logs"):
        self.output_dir = output_dir
        self.metrics_history = defaultdict(lambda: deque(maxlen=1000))
        self.active_monitors = {}
        self.performance_targets = PerformanceTargets()
        self.alert_callbacks = []
        self.report_callbacks = []
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "reports"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "alerts"), exist_ok=True)
        
        # Initialize baseline metrics
        self.baseline_metrics = self._initialize_baseline_metrics()
        
        # Start background monitoring
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._background_monitoring, daemon=True)
        self.monitor_thread.start()
    
    def _initialize_baseline_metrics(self) -> Dict[str, float]:
        """Initialize baseline performance metrics."""
        return {
            MetricType.COMPILATION_TIME.value: 0.0,
            MetricType.MEMORY_USAGE.value: psutil.Process().memory_info().rss / 1024 / 1024,  # MB
            MetricType.CPU_USAGE.value: 0.0,
            MetricType.TOKENIZATION_TIME.value: 0.0,
            MetricType.PARSING_TIME.value: 0.0,
            MetricType.SEMANTIC_ANALYSIS_TIME.value: 0.0,
            MetricType.BYTECODE_GENERATION_TIME.value: 0.0,
            MetricType.ERROR_COUNT.value: 0.0,
            MetricType.WARNING_COUNT.value: 0.0
        }
    
    @contextmanager
    def monitor_compilation(self, source_lines: int = 0, source_file: str = None):
        """Context manager for monitoring compilation performance."""
        monitor_id = f"compilation_{int(time.time() * 1000)}"
        
        # Start monitoring
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024
        start_cpu = psutil.cpu_percent()
        
        self.active_monitors[monitor_id] = {
            'type': 'compilation',
            'start_time': start_time,
            'start_memory': start_memory,
            'start_cpu': start_cpu,
            'source_lines': source_lines,
            'source_file': source_file,
            'metrics': {}
        }
        
        try:
            yield monitor_id
        finally:
            # End monitoring
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024
            end_cpu = psutil.cpu_percent()
            
            compilation_time = (end_time - start_time) * 1000  # Convert to ms
            memory_usage = end_memory - start_memory
            cpu_usage = (end_cpu + start_cpu) / 2
            
            # Record metrics
            self._record_metric(MetricType.COMPILATION_TIME, compilation_time, "ms", {
                'monitor_id': monitor_id,
                'source_lines': source_lines,
                'source_file': source_file
            })
            
            self._record_metric(MetricType.MEMORY_USAGE, memory_usage, "MB", {
                'monitor_id': monitor_id,
                'source_lines': source_lines,
                'source_file': source_file
            })
            
            self._record_metric(MetricType.CPU_USAGE, cpu_usage, "%", {
                'monitor_id': monitor_id,
                'source_lines': source_lines,
                'source_file': source_file
            })
            
            # Check performance targets
            self._check_compilation_targets(compilation_time, source_lines, monitor_id)
            
            # Clean up
            del self.active_monitors[monitor_id]
    
    @contextmanager
    def monitor_component(self, component: MetricType, context: Dict[str, Any] = None):
        """Context manager for monitoring specific component performance."""
        monitor_id = f"{component.value}_{int(time.time() * 1000)}"
        
        # Start monitoring
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss / 1024 / 1024
        
        self.active_monitors[monitor_id] = {
            'type': component.value,
            'start_time': start_time,
            'start_memory': start_memory,
            'context': context or {}
        }
        
        try:
            yield monitor_id
        finally:
            # End monitoring
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            component_time = (end_time - start_time) * 1000  # Convert to ms
            memory_usage = end_memory - start_memory
            
            # Record metrics
            self._record_metric(component, component_time, "ms", {
                'monitor_id': monitor_id,
                'context': context or {}
            })
            
            self._record_metric(MetricType.MEMORY_USAGE, memory_usage, "MB", {
                'monitor_id': monitor_id,
                'component': component.value,
                'context': context or {}
            })
            
            # Clean up
            del self.active_monitors[monitor_id]
    
    def _record_metric(self, metric_type: MetricType, value: float, unit: str, context: Dict[str, Any]):
        """Record a performance metric."""
        timestamp = time.time()
        performance_level = self._classify_performance(metric_type, value)
        target_value, warning_threshold, critical_threshold = self._get_thresholds(metric_type)
        
        metric = PerformanceMetric(
            metric_type=metric_type,
            value=value,
            unit=unit,
            timestamp=timestamp,
            context=context,
            performance_level=performance_level,
            target_value=target_value,
            threshold_warning=warning_threshold,
            threshold_critical=critical_threshold
        )
        
        # Store in history
        self.metrics_history[metric_type.value].append(metric)
        
        # Check for alerts
        if performance_level in [PerformanceLevel.POOR, PerformanceLevel.CRITICAL]:
            self._trigger_alert(metric)
        
        # Update baseline if performance is good
        if performance_level in [PerformanceLevel.EXCELLENT, PerformanceLevel.GOOD]:
            self._update_baseline(metric_type, value)
    
    def _classify_performance(self, metric_type: MetricType, value: float) -> PerformanceLevel:
        """Classify performance level based on metric value."""
        target_value, warning_threshold, critical_threshold = self._get_thresholds(metric_type)
        
        if target_value is None:
            return PerformanceLevel.ACCEPTABLE
        
        if value <= target_value:
            return PerformanceLevel.EXCELLENT
        elif value <= warning_threshold:
            return PerformanceLevel.GOOD
        elif value <= critical_threshold:
            return PerformanceLevel.POOR
        else:
            return PerformanceLevel.CRITICAL
    
    def _get_thresholds(self, metric_type: MetricType) -> tuple[Optional[float], Optional[float], Optional[float]]:
        """Get performance thresholds for a metric type."""
        if metric_type == MetricType.COMPILATION_TIME:
            return (
                self.performance_targets.COMPILATION_TIME_1000_LINES,  # Target
                self.performance_targets.COMPILATION_TIME_1000_LINES * 1.5,  # Warning
                self.performance_targets.COMPILATION_TIME_1000_LINES * 3.0   # Critical
            )
        elif metric_type == MetricType.MEMORY_USAGE:
            return (
                self.performance_targets.MEMORY_USAGE_BASELINE,  # Target
                self.performance_targets.MEMORY_USAGE_LARGE_PROGRAM,  # Warning
                self.performance_targets.MEMORY_USAGE_COMPLEX_OPERATION  # Critical
            )
        elif metric_type == MetricType.TOKENIZATION_TIME:
            return (
                self.performance_targets.TOKENIZATION_TIME_PER_LINE,  # Target
                self.performance_targets.TOKENIZATION_TIME_PER_LINE * 2,  # Warning
                self.performance_targets.TOKENIZATION_TIME_PER_LINE * 5   # Critical
            )
        elif metric_type == MetricType.PARSING_TIME:
            return (
                self.performance_targets.PARSING_TIME_PER_LINE,  # Target
                self.performance_targets.PARSING_TIME_PER_LINE * 2,  # Warning
                self.performance_targets.PARSING_TIME_PER_LINE * 5   # Critical
            )
        elif metric_type == MetricType.SEMANTIC_ANALYSIS_TIME:
            return (
                self.performance_targets.SEMANTIC_ANALYSIS_TIME_PER_LINE,  # Target
                self.performance_targets.SEMANTIC_ANALYSIS_TIME_PER_LINE * 2,  # Warning
                self.performance_targets.SEMANTIC_ANALYSIS_TIME_PER_LINE * 5   # Critical
            )
        elif metric_type == MetricType.BYTECODE_GENERATION_TIME:
            return (
                self.performance_targets.BYTECODE_GENERATION_TIME_PER_LINE,  # Target
                self.performance_targets.BYTECODE_GENERATION_TIME_PER_LINE * 2,  # Warning
                self.performance_targets.BYTECODE_GENERATION_TIME_PER_LINE * 5   # Critical
            )
        else:
            return None, None, None
    
    def _check_compilation_targets(self, compilation_time: float, source_lines: int, monitor_id: str):
        """Check if compilation meets performance targets."""
        if source_lines <= 100 and compilation_time > self.performance_targets.COMPILATION_TIME_100_LINES:
            self._trigger_alert_with_message(
                f"Compilation time {compilation_time:.2f}ms exceeds target for {source_lines} lines",
                "performance_target_exceeded",
                monitor_id
            )
        elif source_lines <= 1000 and compilation_time > self.performance_targets.COMPILATION_TIME_1000_LINES:
            self._trigger_alert_with_message(
                f"Compilation time {compilation_time:.2f}ms exceeds target for {source_lines} lines",
                "performance_target_exceeded",
                monitor_id
            )
        elif source_lines <= 10000 and compilation_time > self.performance_targets.COMPILATION_TIME_10000_LINES:
            self._trigger_alert_with_message(
                f"Compilation time {compilation_time:.2f}ms exceeds target for {source_lines} lines",
                "performance_target_exceeded",
                monitor_id
            )
    
    def _trigger_alert(self, metric: PerformanceMetric):
        """Trigger a performance alert."""
        alert_data = {
            'timestamp': metric.timestamp,
            'metric_type': metric.metric_type.value,
            'value': metric.value,
            'unit': metric.unit,
            'performance_level': metric.performance_level.value,
            'context': metric.context,
            'target_value': metric.target_value,
            'threshold_warning': metric.threshold_warning,
            'threshold_critical': metric.threshold_critical
        }
        
        # Save alert to file
        alert_file = os.path.join(self.output_dir, "alerts", f"alert_{int(metric.timestamp * 1000)}.json")
        with open(alert_file, 'w') as f:
            json.dump(alert_data, f, indent=2)
        
        # Call alert callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert_data)
            except Exception as e:
                print(f"Alert callback failed: {e}")
    
    def _trigger_alert_with_message(self, message: str, alert_type: str, context_id: str):
        """Trigger a performance alert with a custom message."""
        alert_data = {
            'timestamp': time.time(),
            'alert_type': alert_type,
            'message': message,
            'context_id': context_id
        }
        
        # Save alert to file
        alert_file = os.path.join(self.output_dir, "alerts", f"alert_{int(alert_data['timestamp'] * 1000)}.json")
        with open(alert_file, 'w') as f:
            json.dump(alert_data, f, indent=2)
        
        # Call alert callbacks
        for callback in self.alert_callbacks:
            try:
                callback(alert_data)
            except Exception as e:
                print(f"Alert callback failed: {e}")
    
    def _update_baseline(self, metric_type: MetricType, value: float):
        """Update baseline metrics with good performance values."""
        self.baseline_metrics[metric_type.value] = value
    
    def _background_monitoring(self):
        """Background monitoring thread."""
        while self.monitoring_active:
            try:
                # Monitor system resources
                current_memory = psutil.Process().memory_info().rss / 1024 / 1024
                current_cpu = psutil.cpu_percent()
                
                # Record system metrics
                self._record_metric(MetricType.MEMORY_USAGE, current_memory, "MB", {
                    'monitor_type': 'background',
                    'timestamp': time.time()
                })
                
                self._record_metric(MetricType.CPU_USAGE, current_cpu, "%", {
                    'monitor_type': 'background',
                    'timestamp': time.time()
                })
                
                # Sleep for monitoring interval
                time.sleep(5)  # Monitor every 5 seconds
                
            except Exception as e:
                print(f"Background monitoring error: {e}")
                time.sleep(10)  # Wait longer on error
    
    def get_performance_summary(self, duration_hours: float = 1.0) -> Dict[str, Any]:
        """Get performance summary for the last specified duration."""
        end_time = time.time()
        start_time = end_time - (duration_hours * 3600)
        
        summary = {
            'duration_hours': duration_hours,
            'start_time': start_time,
            'end_time': end_time,
            'metrics': {},
            'alerts': [],
            'recommendations': []
        }
        
        # Aggregate metrics by type
        for metric_type, history in self.metrics_history.items():
            recent_metrics = [m for m in history if start_time <= m.timestamp <= end_time]
            if recent_metrics:
                values = [m.value for m in recent_metrics]
                summary['metrics'][metric_type] = {
                    'count': len(values),
                    'min': min(values),
                    'max': max(values),
                    'mean': statistics.mean(values),
                    'median': statistics.median(values),
                    'std_dev': statistics.stdev(values) if len(values) > 1 else 0.0,
                    'excellent_count': sum(1 for m in recent_metrics if m.performance_level == PerformanceLevel.EXCELLENT),
                    'good_count': sum(1 for m in recent_metrics if m.performance_level == PerformanceLevel.GOOD),
                    'acceptable_count': sum(1 for m in recent_metrics if m.performance_level == PerformanceLevel.ACCEPTABLE),
                    'poor_count': sum(1 for m in recent_metrics if m.performance_level == PerformanceLevel.POOR),
                    'critical_count': sum(1 for m in recent_metrics if m.performance_level == PerformanceLevel.CRITICAL)
                }
        
        return summary
    
    def generate_performance_report(self, duration_hours: float = 1.0) -> PerformanceReport:
        """Generate a comprehensive performance report."""
        summary = self.get_performance_summary(duration_hours)
        
        # Collect all metrics in the time range
        end_time = time.time()
        start_time = end_time - (duration_hours * 3600)
        
        all_metrics = []
        for history in self.metrics_history.values():
            recent_metrics = [m for m in history if start_time <= m.timestamp <= end_time]
            all_metrics.extend(recent_metrics)
        
        # Sort by timestamp
        all_metrics.sort(key=lambda m: m.timestamp)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(summary)
        
        # Generate alerts
        alerts = self._generate_alerts(summary)
        
        report = PerformanceReport(
            report_id=f"report_{int(time.time() * 1000)}",
            timestamp=time.time(),
            duration=duration_hours * 3600,
            metrics=all_metrics,
            summary=summary,
            recommendations=recommendations,
            alerts=alerts
        )
        
        # Save report to file
        report_file = os.path.join(self.output_dir, "reports", f"{report.report_id}.json")
        with open(report_file, 'w') as f:
            json.dump(asdict(report), f, indent=2, default=str)
        
        # Call report callbacks
        for callback in self.report_callbacks:
            try:
                callback(report)
            except Exception as e:
                print(f"Report callback failed: {e}")
        
        return report
    
    def _generate_recommendations(self, summary: Dict[str, Any]) -> List[str]:
        """Generate performance optimization recommendations."""
        recommendations = []
        
        # Check compilation time
        if 'compilation_time' in summary['metrics']:
            comp_time = summary['metrics']['compilation_time']
            if comp_time['mean'] > self.performance_targets.COMPILATION_TIME_1000_LINES:
                recommendations.append(
                    f"Compilation time is {comp_time['mean']:.2f}ms on average, "
                    f"exceeding target of {self.performance_targets.COMPILATION_TIME_1000_LINES}ms. "
                    "Consider optimizing parser or semantic analyzer."
                )
        
        # Check memory usage
        if 'memory_usage' in summary['metrics']:
            memory = summary['metrics']['memory_usage']
            if memory['mean'] > self.performance_targets.MEMORY_USAGE_LARGE_PROGRAM:
                recommendations.append(
                    f"Memory usage is {memory['mean']:.2f}MB on average, "
                    f"exceeding target of {self.performance_targets.MEMORY_USAGE_LARGE_PROGRAM}MB. "
                    "Consider implementing memory optimization strategies."
                )
        
        # Check component performance
        for component in ['tokenization_time', 'parsing_time', 'semantic_analysis_time', 'bytecode_generation_time']:
            if component in summary['metrics']:
                comp_metrics = summary['metrics'][component]
                if comp_metrics['mean'] > self.performance_targets.TOKENIZATION_TIME_PER_LINE * 10:
                    recommendations.append(
                        f"{component.replace('_', ' ').title()} is taking "
                        f"{comp_metrics['mean']:.2f}ms on average. "
                        "Consider optimizing this component."
                    )
        
        return recommendations
    
    def _generate_alerts(self, summary: Dict[str, Any]) -> List[str]:
        """Generate alerts based on performance summary."""
        alerts = []
        
        # Check for critical performance issues
        for metric_type, metrics in summary['metrics'].items():
            if metrics['mean'] > metrics.get('threshold_critical', float('inf')):
                alerts.append(
                    f"Critical performance issue: {metric_type} average "
                    f"{metrics['mean']:.2f} exceeds critical threshold"
                )
        
        return alerts
    
    def add_alert_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Add a callback function for performance alerts."""
        self.alert_callbacks.append(callback)
    
    def add_report_callback(self, callback: Callable[[PerformanceReport], None]):
        """Add a callback function for performance reports."""
        self.report_callbacks.append(callback)
    
    def stop_monitoring(self):
        """Stop background monitoring."""
        self.monitoring_active = False
        if self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5)
    
    def get_current_metrics(self) -> Dict[str, float]:
        """Get current performance metrics."""
        return {
            MetricType.COMPILATION_TIME.value: self._get_latest_metric(MetricType.COMPILATION_TIME),
            MetricType.MEMORY_USAGE.value: psutil.Process().memory_info().rss / 1024 / 1024,
            MetricType.CPU_USAGE.value: psutil.cpu_percent(),
            MetricType.TOKENIZATION_TIME.value: self._get_latest_metric(MetricType.TOKENIZATION_TIME),
            MetricType.PARSING_TIME.value: self._get_latest_metric(MetricType.PARSING_TIME),
            MetricType.SEMANTIC_ANALYSIS_TIME.value: self._get_latest_metric(MetricType.SEMANTIC_ANALYSIS_TIME),
            MetricType.BYTECODE_GENERATION_TIME.value: self._get_latest_metric(MetricType.BYTECODE_GENERATION_TIME),
            MetricType.ERROR_COUNT.value: self._get_latest_metric(MetricType.ERROR_COUNT),
            MetricType.WARNING_COUNT.value: self._get_latest_metric(MetricType.WARNING_COUNT)
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get performance statistics (alias for get_current_metrics for backward compatibility)."""
        return self.get_current_metrics()
    
    def _get_latest_metric(self, metric_type: MetricType) -> float:
        """Get the latest value for a specific metric type."""
        if metric_type.value in self.metrics_history and self.metrics_history[metric_type.value]:
            return self.metrics_history[metric_type.value][-1].value
        return 0.0
    
    def record_operation(self, operation_name: str, duration: float, context: Dict[str, Any] = None):
        """Record a custom operation performance."""
        self._record_metric(
            MetricType.COMPILATION_TIME,
            duration * 1000,  # Convert to ms
            "ms",
            {
                'operation': operation_name,
                'context': context or {}
            }
        )
    
    def record_error(self, error_message: str):
        """Record an error occurrence."""
        self._record_metric(
            MetricType.ERROR_COUNT,
            1.0,
            "count",
            {'error_message': error_message}
        )


# Global performance monitor instance
_performance_monitor = None


def get_performance_monitor() -> PerformanceMonitor:
    """Get the global performance monitor instance."""
    global _performance_monitor
    if _performance_monitor is None:
        _performance_monitor = PerformanceMonitor()
    return _performance_monitor


@contextmanager
def monitor_compilation(source_lines: int = 0, source_file: str = None):
    """Global compilation monitoring context manager."""
    monitor = get_performance_monitor()
    with monitor.monitor_compilation(source_lines, source_file) as monitor_id:
        yield monitor_id


@contextmanager
def monitor_component(component: MetricType, context: Dict[str, Any] = None):
    """Global component monitoring context manager."""
    monitor = get_performance_monitor()
    with monitor.monitor_component(component, context) as monitor_id:
        yield monitor_id


def record_metric(metric_type: MetricType, value: float, unit: str, context: Dict[str, Any] = None):
    """Record a performance metric globally."""
    monitor = get_performance_monitor()
    monitor._record_metric(metric_type, value, unit, context or {})


def main():
    """Test the performance monitor."""
    monitor = PerformanceMonitor()
    
    # Test compilation monitoring
    with monitor.monitor_compilation(100, "test.runa"):
        time.sleep(0.1)  # Simulate compilation
    
    # Test component monitoring
    with monitor.monitor_component(MetricType.TOKENIZATION_TIME, {"lines": 50}):
        time.sleep(0.05)  # Simulate tokenization
    
    # Generate report
    report = monitor.generate_performance_report(0.1)  # Last 6 minutes
    print(f"Generated performance report: {report.report_id}")
    print(f"Recommendations: {len(report.recommendations)}")
    print(f"Alerts: {len(report.alerts)}")
    
    monitor.stop_monitoring()


if __name__ == "__main__":
    main() 
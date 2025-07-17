#!/usr/bin/env python3
"""
Performance Benchmark Tests for MCP Windows Security Tools
"""

import pytest
import asyncio
import time
import psutil
import threading
import concurrent.futures
import statistics
from unittest.mock import patch, MagicMock
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Import the functions we need to test
from unified_server import (
    set_user_preference,
    get_user_preference,
    list_user_preferences,
    get_system_info,
    list_processes,
    get_window_list,
    take_screenshot,
    get_mouse_position,
    move_mouse,
    click_at_coordinates,
    send_keyboard_shortcut,
    type_text,
    run_command,
    monitor_system_activity,
    get_installed_programs,
    get_startup_programs
)

class PerformanceMetrics:
    """Helper class to collect performance metrics"""
    
    def __init__(self):
        self.response_times = []
        self.memory_usage = []
        self.cpu_usage = []
        self.start_time = None
        self.end_time = None
    
    def start_measurement(self):
        """Start performance measurement"""
        self.start_time = time.time()
        self.memory_usage.append(psutil.virtual_memory().percent)
        self.cpu_usage.append(psutil.cpu_percent(interval=None))
    
    def end_measurement(self):
        """End performance measurement"""
        self.end_time = time.time()
        response_time = (self.end_time - self.start_time) * 1000  # Convert to ms
        self.response_times.append(response_time)
        self.memory_usage.append(psutil.virtual_memory().percent)
        self.cpu_usage.append(psutil.cpu_percent(interval=None))
        return response_time
    
    def get_stats(self):
        """Get performance statistics"""
        return {
            'avg_response_time': statistics.mean(self.response_times),
            'max_response_time': max(self.response_times),
            'min_response_time': min(self.response_times),
            'avg_memory_usage': statistics.mean(self.memory_usage),
            'max_memory_usage': max(self.memory_usage),
            'avg_cpu_usage': statistics.mean(self.cpu_usage),
            'max_cpu_usage': max(self.cpu_usage)
        }

class TestPerformance:
    """Performance benchmark tests"""
    
    def setup_method(self):
        """Setup test environment"""
        self.metrics = PerformanceMetrics()
        self.test_iterations = 100
        self.concurrent_users = 10
        
    def teardown_method(self):
        """Cleanup after test"""
        pass
    
    @pytest.mark.asyncio
    async def test_response_time_benchmarks(self):
        """Test response time benchmarks for all major functions"""
        
        # Test user preference operations
        for i in range(self.test_iterations):
            self.metrics.start_measurement()
            await set_user_preference("test", f"key_{i}", f"value_{i}")
            response_time = self.metrics.end_measurement()
            assert response_time < 100, f"set_user_preference took {response_time}ms (> 100ms)"
        
        # Test system info queries
        for i in range(self.test_iterations):
            self.metrics.start_measurement()
            await get_system_info()
            response_time = self.metrics.end_measurement()
            assert response_time < 500, f"get_system_info took {response_time}ms (> 500ms)"
        
        # Test process listing
        for i in range(10):  # Fewer iterations for heavier operations
            self.metrics.start_measurement()
            await list_processes()
            response_time = self.metrics.end_measurement()
            assert response_time < 1000, f"list_processes took {response_time}ms (> 1000ms)"
        
        stats = self.metrics.get_stats()
        print(f"Performance Stats: {stats}")
        
        # Verify performance targets
        assert stats['avg_response_time'] < 200, f"Average response time {stats['avg_response_time']}ms exceeds target"
        assert stats['max_response_time'] < 2000, f"Max response time {stats['max_response_time']}ms exceeds target"
    
    @pytest.mark.asyncio
    async def test_memory_usage_monitoring(self):
        """Test memory usage under various loads"""
        
        # Baseline memory usage
        baseline_memory = psutil.virtual_memory().percent
        
        # Test memory usage under normal operations
        tasks = []
        for i in range(50):
            tasks.append(set_user_preference("memory_test", f"key_{i}", f"value_{i}"))
        
        await asyncio.gather(*tasks)
        
        # Check memory usage
        current_memory = psutil.virtual_memory().percent
        memory_increase = current_memory - baseline_memory
        
        assert memory_increase < 10, f"Memory usage increased by {memory_increase}% (> 10%)"
        
        # Test memory cleanup
        await asyncio.sleep(1)  # Allow cleanup
        cleanup_memory = psutil.virtual_memory().percent
        
        # Memory should not continuously grow
        assert cleanup_memory <= current_memory + 2, "Memory not properly cleaned up"
    
    @pytest.mark.asyncio
    async def test_cpu_utilization_tracking(self):
        """Test CPU utilization under load"""
        
        # Baseline CPU usage
        baseline_cpu = psutil.cpu_percent(interval=1)
        
        # Create CPU-intensive workload
        start_time = time.time()
        tasks = []
        
        for i in range(20):
            tasks.append(get_system_info())
            tasks.append(list_processes())
        
        await asyncio.gather(*tasks)
        
        # Check CPU usage during load
        load_cpu = psutil.cpu_percent(interval=1)
        
        # CPU should not spike excessively
        assert load_cpu < 80, f"CPU usage during load: {load_cpu}% (> 80%)"
        
        # Test CPU recovery
        await asyncio.sleep(2)
        recovery_cpu = psutil.cpu_percent(interval=1)
        
        # CPU should return to reasonable levels
        assert recovery_cpu < baseline_cpu + 20, f"CPU not recovered: {recovery_cpu}%"
    
    @pytest.mark.asyncio
    async def test_concurrent_request_handling(self):
        """Test handling of concurrent requests"""
        
        async def worker_task(worker_id):
            """Worker task for concurrent testing"""
            results = []
            for i in range(10):
                start_time = time.time()
                await set_user_preference(f"worker_{worker_id}", f"key_{i}", f"value_{i}")
                end_time = time.time()
                results.append((end_time - start_time) * 1000)
            return results
        
        # Create concurrent workers
        workers = []
        for i in range(self.concurrent_users):
            workers.append(worker_task(i))
        
        # Execute all workers concurrently
        start_time = time.time()
        results = await asyncio.gather(*workers)
        end_time = time.time()
        
        # Analyze results
        all_response_times = [rt for worker_results in results for rt in worker_results]
        avg_response_time = statistics.mean(all_response_times)
        max_response_time = max(all_response_times)
        
        total_time = end_time - start_time
        throughput = (len(all_response_times) / total_time)
        
        # Performance assertions
        assert avg_response_time < 200, f"Average concurrent response time: {avg_response_time}ms"
        assert max_response_time < 1000, f"Max concurrent response time: {max_response_time}ms"
        assert throughput > 10, f"Throughput too low: {throughput} requests/second"
    
    @pytest.mark.asyncio
    async def test_database_query_performance(self):
        """Test performance of database-like operations"""
        
        # Set up test data
        test_data = []
        for i in range(1000):
            test_data.append(("category", f"key_{i}", f"value_{i}"))
        
        # Test bulk insert performance
        start_time = time.time()
        for category, key, value in test_data:
            await set_user_preference(category, key, value)
        insert_time = time.time() - start_time
        
        insert_rate = len(test_data) / insert_time
        assert insert_rate > 100, f"Insert rate too low: {insert_rate} ops/second"
        
        # Test bulk query performance
        start_time = time.time()
        for category, key, value in test_data[:100]:  # Sample queries
            await get_user_preference(category, key)
        query_time = time.time() - start_time
        
        query_rate = 100 / query_time
        assert query_rate > 200, f"Query rate too low: {query_rate} ops/second"
    
    @pytest.mark.asyncio
    async def test_large_data_processing(self):
        """Test performance with large data sets"""
        
        # Test with large preference data
        large_value = "x" * 10000  # 10KB value
        
        start_time = time.time()
        await set_user_preference("large_data", "big_key", large_value)
        set_time = time.time() - start_time
        
        assert set_time < 1.0, f"Large data set took too long: {set_time}s"
        
        # Test retrieval of large data
        start_time = time.time()
        result = await get_user_preference("large_data", "big_key")
        get_time = time.time() - start_time
        
        assert get_time < 0.5, f"Large data retrieval took too long: {get_time}s"
        assert large_value in result, "Large data not properly retrieved"
    
    @pytest.mark.asyncio
    async def test_system_resource_cleanup(self):
        """Test proper cleanup of system resources"""
        
        # Monitor resource usage before operations
        initial_memory = psutil.virtual_memory().percent
        initial_handles = len(psutil.Process().open_files())
        
        # Perform operations that might leak resources
        for i in range(100):
            await get_system_info()
            await list_processes()
            await get_window_list()
        
        # Force garbage collection
        import gc
        gc.collect()
        
        # Check resource usage after operations
        final_memory = psutil.virtual_memory().percent
        final_handles = len(psutil.Process().open_files())
        
        memory_increase = final_memory - initial_memory
        handle_increase = final_handles - initial_handles
        
        # Resources should be properly cleaned up
        assert memory_increase < 5, f"Memory leak detected: {memory_increase}% increase"
        assert handle_increase < 10, f"Handle leak detected: {handle_increase} handles"
    
    @pytest.mark.asyncio
    async def test_ui_automation_performance(self):
        """Test performance of UI automation operations"""
        
        # Test mouse operations
        mouse_times = []
        for i in range(50):
            start_time = time.time()
            await get_mouse_position()
            end_time = time.time()
            mouse_times.append((end_time - start_time) * 1000)
        
        avg_mouse_time = statistics.mean(mouse_times)
        assert avg_mouse_time < 50, f"Mouse operations too slow: {avg_mouse_time}ms"
        
        # Test keyboard operations
        keyboard_times = []
        for i in range(20):
            start_time = time.time()
            await type_text("test")
            end_time = time.time()
            keyboard_times.append((end_time - start_time) * 1000)
        
        avg_keyboard_time = statistics.mean(keyboard_times)
        assert avg_keyboard_time < 100, f"Keyboard operations too slow: {avg_keyboard_time}ms"
    
    @pytest.mark.asyncio
    async def test_system_monitoring_performance(self):
        """Test performance of system monitoring operations"""
        
        # Test continuous monitoring performance
        monitoring_times = []
        
        for i in range(10):
            start_time = time.time()
            await monitor_system_activity(duration=1)
            end_time = time.time()
            monitoring_times.append(end_time - start_time)
        
        avg_monitoring_time = statistics.mean(monitoring_times)
        
        # Monitoring should be efficient
        assert avg_monitoring_time < 2.0, f"System monitoring too slow: {avg_monitoring_time}s"
        
        # Test program enumeration performance
        start_time = time.time()
        await get_installed_programs()
        installed_time = time.time() - start_time
        
        assert installed_time < 5.0, f"Program enumeration too slow: {installed_time}s"
        
        start_time = time.time()
        await get_startup_programs()
        startup_time = time.time() - start_time
        
        assert startup_time < 3.0, f"Startup program enumeration too slow: {startup_time}s"
    
    @pytest.mark.asyncio
    async def test_command_execution_performance(self):
        """Test performance of command execution"""
        
        # Test simple command execution
        simple_commands = [
            "echo hello",
            "dir",
            "time /t",
            "whoami"
        ]
        
        for cmd in simple_commands:
            start_time = time.time()
            await run_command(cmd)
            end_time = time.time()
            
            execution_time = end_time - start_time
            assert execution_time < 2.0, f"Command '{cmd}' too slow: {execution_time}s"
    
    @pytest.mark.asyncio
    async def test_stress_testing(self):
        """Stress test the system with high load"""
        
        # Create high-load scenario
        stress_tasks = []
        
        # Add various types of operations
        for i in range(200):
            stress_tasks.append(set_user_preference(f"stress_{i}", "key", "value"))
        
        for i in range(50):
            stress_tasks.append(get_system_info())
        
        for i in range(20):
            stress_tasks.append(list_processes())
        
        # Execute all tasks concurrently
        start_time = time.time()
        results = await asyncio.gather(*stress_tasks, return_exceptions=True)
        end_time = time.time()
        
        # Analyze stress test results
        total_time = end_time - start_time
        success_count = sum(1 for r in results if not isinstance(r, Exception))
        error_count = len(results) - success_count
        
        # System should handle stress gracefully
        assert total_time < 30.0, f"Stress test took too long: {total_time}s"
        assert error_count < len(results) * 0.1, f"Too many errors under stress: {error_count}"
        
        # System should still be responsive after stress
        post_stress_start = time.time()
        await get_system_info()
        post_stress_time = time.time() - post_stress_start
        
        assert post_stress_time < 2.0, f"System not responsive after stress: {post_stress_time}s"
    
    def test_memory_leak_detection(self):
        """Test for memory leaks in synchronous operations"""
        
        import gc
        
        # Baseline memory
        gc.collect()
        baseline_memory = psutil.virtual_memory().percent
        
        # Perform operations that might cause memory leaks
        for i in range(1000):
            # Simulate operations that create and destroy objects
            data = {"key": f"value_{i}" for i in range(100)}
            del data
        
        # Force garbage collection
        gc.collect()
        
        # Check memory usage
        final_memory = psutil.virtual_memory().percent
        memory_increase = final_memory - baseline_memory
        
        assert memory_increase < 2, f"Memory leak detected: {memory_increase}% increase"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

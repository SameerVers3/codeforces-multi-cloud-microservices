import docker
import tempfile
import os
import subprocess
import time
from typing import Dict, List, Optional
from app.config import settings

class CppExecutor:
    def __init__(self):
        try:
            # Try to connect to Docker socket
            self.client = docker.from_env()
            # Test connection
            self.client.ping()
        except Exception as e:
            print(f"Warning: Could not connect to Docker: {e}")
            self.client = None
    
    def execute(self, code: str, test_cases: List[Dict], time_limit_seconds: int = 2, memory_limit_mb: int = 256) -> Dict:
        """Execute C++ code against test cases"""
        if not self.client:
            return {
                "status": "error",
                "error_message": "Docker not available",
                "test_cases_passed": 0,
                "total_test_cases": len(test_cases),
                "results": []
            }
        
        results = []
        total_passed = 0
        
        # Create temporary directory for code
        with tempfile.TemporaryDirectory() as temp_dir:
            code_file = os.path.join(temp_dir, "main.cpp")
            with open(code_file, "w") as f:
                f.write(code)
            
            # Compile code
            compile_result = self._compile_code(temp_dir)
            if not compile_result["success"]:
                return {
                    "status": "compilation_error",
                    "error_message": compile_result["error"],
                    "test_cases_passed": 0,
                    "total_test_cases": len(test_cases),
                    "results": []
                }
            
            # Execute against each test case
            for test_case in test_cases:
                result = self._run_test_case(
                    temp_dir,
                    test_case["input_data"],
                    test_case["expected_output"],
                    time_limit_seconds,
                    memory_limit_mb
                )
                results.append(result)
                if result["status"] == "passed":
                    total_passed += 1
            
            # Determine overall status
            if total_passed == len(test_cases):
                overall_status = "accepted"
            elif any(r["status"] == "timeout" for r in results):
                overall_status = "time_limit_exceeded"
            elif any(r["status"] == "error" for r in results):
                overall_status = "runtime_error"
            else:
                overall_status = "wrong_answer"
            
            # Calculate average execution time
            execution_times = [r["execution_time_ms"] for r in results if r.get("execution_time_ms")]
            avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
            
            # Calculate max memory used
            memory_used = max([r.get("memory_used_mb", 0) for r in results], default=0)
            
            return {
                "status": overall_status,
                "test_cases_passed": total_passed,
                "total_test_cases": len(test_cases),
                "execution_time_ms": int(avg_execution_time),
                "memory_used_mb": memory_used,
                "results": results
            }
    
    def _compile_code(self, code_dir: str) -> Dict:
        """Compile C++ code"""
        try:
            result = self.client.containers.run(
                image="gcc:latest",
                command=["g++", "-o", "/tmp/main", "/code/main.cpp", "-std=c++17", "-O2"],
                volumes={code_dir: {"bind": "/code", "mode": "ro"}},
                remove=True,
                mem_limit=f"{settings.MAX_MEMORY_MB}m",
                network_disabled=True,
                timeout=30
            )
            return {"success": True}
        except docker.errors.ContainerError as e:
            return {"success": False, "error": e.stderr.decode() if e.stderr else str(e)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _run_test_case(self, code_dir: str, input_data: str, expected_output: str, time_limit: int, memory_limit: int) -> Dict:
        """Run code against a single test case"""
        start_time = time.time()
        
        try:
            # Create input file
            input_file = os.path.join(code_dir, "input.txt")
            with open(input_file, "w") as f:
                f.write(input_data)
            
            # Run executable
            container = self.client.containers.run(
                image="gcc:latest",
                command=["sh", "-c", "/tmp/main < /code/input.txt"],
                volumes={code_dir: {"bind": "/code", "mode": "ro"}},
                mem_limit=f"{memory_limit}m",
                network_disabled=True,
                detach=True,
                remove=True
            )
            
            # Wait for completion with timeout
            try:
                container.wait(timeout=time_limit)
                execution_time = (time.time() - start_time) * 1000  # Convert to ms
                
                # Get output
                logs = container.logs().decode("utf-8")
                
                # Check if output matches expected
                actual_output = logs.strip()
                expected_output_stripped = expected_output.strip()
                
                if actual_output == expected_output_stripped:
                    status = "passed"
                else:
                    status = "failed"
                
                # Get memory stats
                stats = container.stats(stream=False)
                memory_used = stats.get("memory_stats", {}).get("usage", 0) / (1024 * 1024)  # Convert to MB
                
                return {
                    "status": status,
                    "execution_time_ms": int(execution_time),
                    "memory_used_mb": round(memory_used, 2),
                    "actual_output": actual_output[:1000],  # Limit output size
                    "expected_output": expected_output_stripped[:1000]
                }
            except docker.errors.ContainerError as e:
                return {
                    "status": "error",
                    "execution_time_ms": int((time.time() - start_time) * 1000),
                    "error_message": e.stderr.decode() if e.stderr else str(e)
                }
            except Exception as e:
                if "timeout" in str(e).lower():
                    return {
                        "status": "timeout",
                        "execution_time_ms": time_limit * 1000,
                        "error_message": "Execution timeout"
                    }
                return {
                    "status": "error",
                    "execution_time_ms": int((time.time() - start_time) * 1000),
                    "error_message": str(e)
                }
        except Exception as e:
            return {
                "status": "error",
                "execution_time_ms": 0,
                "error_message": str(e)
            }


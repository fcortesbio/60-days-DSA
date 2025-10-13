# 60-days DSA Utilities Package

A comprehensive utilities package for the 60-days Data Structures and Algorithms learning journey. This package provides reusable components for testing, benchmarking, and analyzing algorithm implementations across all days.

## Package Structure

```
utils/
├── __init__.py          # Main package with convenient imports
├── config.py            # Configuration constants and settings
├── models.py            # Data structures and type definitions
├── benchmark.py         # Performance benchmarking utilities  
├── testing.py           # Algorithm validation and testing
└── README.md           # This documentation
```

## Quick Start

### Basic Import

```python
# Import everything you need
from utils import (
    TestCase, BenchmarkResult, 
    STANDARD_ARRAY_SIZE, LARGE_ARRAY_SIZE,
    benchmark_functions, analyze_performance, run_validation_tests
)
```

### Creating Test Cases

```python
# Manual test cases
test_cases = [
    TestCase(array=[1, 2, 3], expected=20, name="Basic test"),
    TestCase(array=[2, 1, 3], expected=19, name="Reordered test"),
]

# Or use standard test cases
from utils.testing import create_standard_test_cases
test_cases = create_standard_test_cases("subarray_sum")
```

### Running Validations

```python
# Validate algorithm correctness
functions = [my_algorithm1, my_algorithm2, my_algorithm3]
validation_results = run_validation_tests(functions, test_cases)

# Check if all tests passed
all_passed = all(result.passed for result in validation_results)
```

### Benchmarking Performance

```python
# Benchmark algorithm performance
test_array = list(range(STANDARD_ARRAY_SIZE))
benchmark_results = benchmark_functions(functions, test_array, STANDARD_REPLICAS)

# Analyze and display results
analyze_performance(benchmark_results, len(test_array))
```

## Data Structures

### TestCase
```python
@dataclass
class TestCase:
    array: list[int]              # Input array
    expected: Union[int, float, list, Any]  # Expected result
    name: str                     # Test case name
    description: Optional[str] = None  # Optional description
```

### BenchmarkResult
```python
@dataclass
class BenchmarkResult:
    function: Callable            # The benchmarked function
    time: float                  # Total execution time
    memory_usage: Optional[float] = None
    iterations: Optional[int] = None
```

### ValidationResult
```python
@dataclass
class ValidationResult:
    function_name: str           # Name of tested function
    test_case: TestCase          # The test case used
    actual_result: Any           # Actual function output
    passed: bool                 # Whether test passed
    error_message: Optional[str] = None
    execution_time: Optional[float] = None
```

## Configuration Constants

### Array Sizes
```python
STANDARD_ARRAY_SIZE = 100      # Standard test size
LARGE_ARRAY_SIZE = 1500        # Large-scale testing  
EXTRA_LARGE_ARRAY_SIZE = 30000 # Extra large testing
```

### Benchmarking Parameters
```python
STANDARD_REPLICAS = 1000       # Standard benchmark iterations
LARGE_REPLICAS = 100           # Large-scale benchmark iterations
EXTRA_LARGE_REPLICAS = 10      # Extra large benchmark iterations
```

### Display Formatting
```python
SECTION_WIDTH = 70             # Width for section headers
FUNCTION_NAME_WIDTH = 30       # Width for function names
RANKING_MEDALS = ["🥇", "🥈", "🥉"]  # Medal emojis
```

## Usage Examples

### Complete Algorithm Testing Workflow

```python
#!/usr/bin/env python3
from utils import *

def my_algorithm(arr: list[int]) -> int:
    """Your algorithm implementation"""
    return sum(arr)  # Example

def main():
    # Define algorithms to test
    functions = [my_algorithm]
    
    # Create test cases
    test_cases = [
        TestCase(array=[1, 2, 3], expected=6, name="Simple sum"),
    ]
    
    # Validate correctness
    validation_results = run_validation_tests(functions, test_cases)
    
    # Benchmark performance
    test_array = list(range(STANDARD_ARRAY_SIZE))
    benchmark_results = benchmark_functions(functions, test_array, STANDARD_REPLICAS)
    
    # Analyze results
    analyze_performance(benchmark_results, len(test_array))

if __name__ == "__main__":
    main()
```

### Advanced Benchmarking

```python
from utils.benchmark import compare_scale_performance

# Test at different scales
small_results = benchmark_functions(functions, small_array, STANDARD_REPLICAS)
large_results = benchmark_functions(functions, large_array, LARGE_REPLICAS)

# Compare scaling behavior
compare_scale_performance(small_results, large_results, len(small_array), len(large_array))
```

### Custom Test Case Validation

```python
from utils.testing import validate_test_cases

# Validate test case integrity
is_valid = validate_test_cases(test_cases)
if not is_valid:
    print("❌ Some test cases are invalid")
```

## Adding to New Day Implementations

1. **Add import path** (if not in root):
```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

2. **Import utilities**:
```python
from utils import TestCase, benchmark_functions, run_validation_tests
```

3. **Use in main function**:
```python
def main():
    functions = [your_algorithms]
    test_cases = [TestCase(...)]
    
    run_validation_tests(functions, test_cases)
    results = benchmark_functions(functions, test_array, STANDARD_REPLICAS)
    analyze_performance(results, len(test_array))
```

## Benefits

### ✅ **Consistency**
- Standardized testing and benchmarking across all days
- Consistent output formatting and analysis
- Unified configuration management

### ✅ **Reusability** 
- Write test utilities once, use everywhere
- Extensible data structures for new use cases
- Modular design allows selective imports

### ✅ **Maintainability**
- Centralized utility functions
- Easy to update and improve across all implementations
- Clear separation of concerns

### ✅ **Professional Quality**
- Comprehensive error handling
- Type safety with dataclasses
- Detailed performance analysis

## Extension Points

### Adding New Problem Types

```python
# In utils/testing.py
def create_standard_test_cases(problem_type: str):
    if problem_type == "your_new_type":
        return [
            TestCase(array=..., expected=..., name="..."),
            # Add more test cases
        ]
```

### Custom Performance Metrics

```python
# Extend BenchmarkResult for new metrics
@dataclass 
class ExtendedBenchmarkResult(BenchmarkResult):
    memory_peak: Optional[float] = None
    cpu_usage: Optional[float] = None
```

This utilities package transforms your DSA learning journey from ad-hoc testing to professional-grade algorithm analysis! 🚀
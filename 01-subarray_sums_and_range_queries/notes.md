# Day 1: Subarray Sums & Range Queries

> **Learning Objectives:** Master prefix sum technique, understand contribution method, and solve range query problems efficiently.

---

## 📚 Concept 1: Sum of All Subarray Sums

### Problem Statement
Given an integer array $A$ of length $N$, find the sum of all subarray sums.

**Definition:** A subarray is a contiguous part of an array obtained by deleting zero or more elements from either end. A subarray sum is the sum of all elements in that subarray.

### 📊 Examples

| Input | Array | Output | 
|-------|-------|--------|
| 1 | `[1, 2, 3]` | `20` |
| 2 | `[2, 1, 3]` | `19` |

### 🔍 Detailed Explanation

**Example 1: `[1, 2, 3]`**

Subarrays:
- `[1]` → sum = 1
- `[2]` → sum = 2  
- `[3]` → sum = 3
- `[1, 2]` → sum = 3
- `[2, 3]` → sum = 5
- `[1, 2, 3]` → sum = 6

**Total:** 1 + 2 + 3 + 3 + 5 + 6 = **20**

**Example 2: `[2, 1, 3]`**

Subarrays:
- `[2]` → sum = 2
- `[1]` → sum = 1
- `[3]` → sum = 3  
- `[2, 1]` → sum = 3
- `[1, 3]` → sum = 4
- `[2, 1, 3]` → sum = 6

**Total:** 2 + 1 + 3 + 3 + 4 + 6 = **19**

### 💻 Solutions

#### 🐌 Approach 1: Naive Brute Force
**Strategy**: Generate all possible subarrays and calculate their sums.

**Algorithm:**
* Use three nested loops
* Outer two loops generate subarray boundaries
* Inner loop calculates sum of current subarray

**Pseudocode**:
```pseudocode
FUNCTION naive_brute_force(array):
    n = length(array)
    total_sum = 0
    
    FOR i FROM 0 TO n - 1:

        FOR j FROM i TO n - 1:
            subarray_sum = 0

            FOR k FROM i TO j:
                subarray_sum += array[k]

            total_sum += subarray_sum
    
    RETURN total_sum
```

**Complexity:**
- 🕰️ Time: `O(n³)`

### Approach 2: Optimized Brute Force
**Strategy**: Execute running sum while new subarray is generated.

**Algorithm**:
* Use two nested loops instead of three
* the outer loop picks the starting index $i$ of every subarray
* the inner loop extends the subarray to each possible index $j$ (from $i$ to $n-1$)
* A variable accumulates the running sum for the subarray `[i, ..., j]` — this avoids the need for a third loop that explicitly sums each array from scratch

**Pseudocode**:
```pseudocode
FUNCTION optimized_brute_force(array):
    n = length(array)
    total_sum = 0
    
    FOR i FROM 0 TO n - 1:
        current_subarray_sum = 0

        FOR j FROM i TO n - 1:
            current_subarray_sum += array[j]
            total_sum += current_subarray_sum
    
    RETURN total_sum
```

**Complexity:**
- 🕰️ Time: `O(n²)`

#### ✨ Approach 3: Contribution Technique
Instead of generating subarrays, we realize we can count how many times each element contributes to the final sum.

**Key Insight:** Element at index `i` appears in `(i + 1) × (n - i)` subarrays

**Example with `[1, 2, 3]`:**
- Element `1` (index 0): appears in `(0+1) × (3-0) = 3` subarrays
- Element `2` (index 1): appears in `(1+1) × (3-1) = 4` subarrays  
- Element `3` (index 2): appears in `(2+1) × (3-2) = 3` subarrays

**Contribution calculation:**
- `1 × 3 = 3`
- `2 × 4 = 8`
- `3 × 3 = 9`
- **Total:** `3 + 8 + 9 = 20`

**Mathematical Derivation**

Consider an array: `arr = [a₀, a₁, a₂, ..., aₙ₋₁]`

**Question:** How many subarrays contain element `arr[k]` at position `k`?

**Analysis:**
For element `arr[k]` to be included in a subarray `[i, j]`, we need:
- Starting index: `i ≤ k` 
- Ending index: `j ≥ k`

**Counting Possibilities:**
- **Left choices:** Starting index `i` can be `{0, 1, 2, ..., k}` → **(k + 1)** options
- **Right choices:** Ending index `j` can be `{k, k+1, ..., n-1}` → **(n - k)** options
- **Total subarrays:** Each left choice can pair with each right choice

**Formula:** Number of subarrays containing `arr[k]` = **(k + 1) × (n - k)**

**Contribution Calculation:**
Since `arr[k]` appears exactly once in each of these subarrays:
- **Element contribution:** `arr[k] × (k + 1) × (n - k)`

**Final Sum:**
Sum all individual contributions:
$$\text{Total Sum} = \sum_{k=0}^{n-1} arr[k] \times (k + 1) \times (n - k)$$

**Complexity:** O(n) time - single pass through the array


**Pseudocode**:
```pseudocode
FUNCTION contribution_technique(array):
    n = length(array)
    total_sum = 0
    
    FOR k FROM 0 TO n - 1:
        left_choices = k + 1        // positions where subarray can start
        right_choices = n - k       // positions where subarray can end  
        contribution = array[k] * left_choices * right_choices
        total_sum = total_sum + contribution
    
    RETURN total_sum
```

**Complexity:**
- 🕰️ Time: `O(n)` - single pass through array
- 💾 Space: `O(1)` - only using constant extra space

---

#### ✨ Approach 4: Vectorized Contribution (Space-Time Trade-off)

**Strategy**: 
Express the subarray sum as the dot product between the original array and a precomputed contributions array.

**Key Insight:**
Since the contribution formula $c_k = (k + 1) × (n - k)$ creates a **symmetric pattern**, we can optimize memory usage by computing only half the contributions array.

**Pattern Analysis:**
For arrays of different lengths, the contributions form symmetric patterns:

```
n = 1: [1]              # single element
n = 2: [2, 2]           # symmetric pair  
n = 3: [3, 4, 3]        # symmetric with center peak
n = 4: [4, 6, 6, 4]     # symmetric pair peaks
n = 5: [5, 8, 9, 8, 5]  # symmetric with center peak
n = 6: [6, 10, 12, 12, 10, 6] # symmetric pair peaks
```

**Mathematical Properties:**
- The contribution formula $c_k = (k + 1) × (n - k)$ is a quadratic function in $k$
- Expanding: $c_k = -k^2 + (n-1)k + n$ (downward-opening parabola)
- **Symmetry property:** $c_k = c_{n-k-1}$ for all valid $k$

**Optimization Strategy:**
Since the contributions array is symmetric, we can:
1. Compute only the first half of the contributions
2. Mirror this half to create the complete array
3. Calculate the final sum as a dot product

**Algorithm Steps:**
1. Calculate midpoint: `m = ⌈n/2⌉` (includes center for odd lengths)
2. Compute contributions for indices `0` to `m-1` 
3. Mirror the array appropriately:
   - **Even length:** Mirror the entire first half
   - **Odd length:** Mirror all except the last element (center is unique)
4. Calculate dot product with original array

**Example with n=5:**
- First half: `[5, 8, 9]` (indices 0, 1, 2)
- Mirror (excluding center): `[8, 5]` (reverse of indices 0, 1)
- Complete contributions: `[5, 8, 9, 8, 5]`

**Pseudocode**:
```pseudocode
FUNCTION vectorized_contribution(array):
    n = length(array)
    m = (n + 1) // 2  # ceiling division for midpoint
    
    // Compute first half of contributions
    first_half = new Array
    FOR k FROM 0 to m-1:
        APPEND (k + 1) * (n - k) TO first_half
    
    // Create mirror based on array length parity
    IF n % 2 == 0:
        // Even: mirror entire first half
        mirror = REVERSE(first_half)
    ELSE: 
        // Odd: mirror all except center element
        mirror = REVERSE(first_half[0:m-2])
    
    contributions = CONCAT(first_half, mirror)
    
    // Calculate dot product
    total_sum = 0
    FOR i FROM 0 TO n - 1:
        total_sum += array[i] * contributions[i]
    
    RETURN total_sum
```

**Complexity:**
- 🕰️ Time: `O(n)` - single pass through array
- 💾 Space: `O(n)` for the contributions array

**Trade-off Analysis:**
- **Pro:** Can precompute contributions once and reuse for multiple arrays of same length
- **Con:** Uses additional O(n) space compared to direct contribution method
- **Use case:** Beneficial when processing multiple arrays of the same length


## 📚 Concept 2: Range Sum Query

### Problem Statement
Given an integer array `A` of length `N` and a 2D array `B` with `M` queries, where each query is `[L, R]`. For each query, find the sum of elements from index `L` to `R` (inclusive, 0-indexed).

**Formula:** `A[L] + A[L+1] + A[L+2] + ... + A[R]`

### 📊 Examples

| Test | Array | Queries | Output |
|------|-------|---------|--------|
| 1 | `[1, 2, 3, 4, 5]` | `[[0, 3], [1, 2]]` | `[10, 5]` |
| 2 | `[2, 2, 2]` | `[[0, 0], [1, 2]]` | `[2, 4]` |

### 🔍 Detailed Explanation

**Example 1:** `A = [1, 2, 3, 4, 5]`
- Query `[0, 3]`: Sum of `A[0]` to `A[3]` = `1 + 2 + 3 + 4 = 10`
- Query `[1, 2]`: Sum of `A[1]` to `A[2]` = `2 + 3 = 5`
- **Result:** `[10, 5]`

**Example 2:** `A = [2, 2, 2]`
- Query `[0, 0]`: Sum of `A[0]` to `A[0]` = `2`
- Query `[1, 2]`: Sum of `A[1]` to `A[2]` = `2 + 2 = 4`
- **Result:** `[2, 4]`

### 💻 Solutions

#### 🐌 Approach 1: Brute Force
For each query, iterate through the range and calculate sum.

**Algorithm:**
1. For each query `[L, R]`
2. Initialize `sum = 0`
3. Loop from `L` to `R` and add `A[i]` to sum
4. Return sum for current query

**Complexity:**
- 🕰️ Time: `O(N × Q)` where N = array length, Q = number of queries
- 💾 Space: `O(1)`

#### ✨ Approach 2: Prefix Sum (Optimized)
Preprocess the array to build prefix sums, then answer queries in O(1).

**Key Insight:** `sum[L:R] = prefix[R+1] - prefix[L]`

**Algorithm:**
1. **Preprocessing:** Build prefix sum array where `prefix[i] = sum of first i elements`
2. **Query:** For range `[L, R]`, return `prefix[R+1] - prefix[L]`

**Example:** `A = [1, 2, 3, 4, 5]`
- Prefix array: `[0, 1, 3, 6, 10, 15]`
- Query `[1, 3]`: `prefix[4] - prefix[1] = 10 - 1 = 9` → `2 + 3 + 4 = 9` ✓

**Complexity:**
- 🕰️ Time: `O(N + Q)` (N for preprocessing + Q for queries)
- 💾 Space: `O(N)` for prefix array

---

## 🧠 Quick Challenge

**Given:** `A = [2, 2, 2]` and queries `[[0, 0], [1, 2]]`

**Question:** What's the output using prefix sum approach?

<details>
<summary>👁️ Click to reveal answer</summary>

**Answer:** `[2, 4]`

**Explanation:**
- Prefix array: `[0, 2, 4, 6]`
- Query `[0, 0]`: `prefix[1] - prefix[0] = 2 - 0 = 2`
- Query `[1, 2]`: `prefix[3] - prefix[1] = 6 - 2 = 4`

</details>

---

## 🔑 Key Takeaways

### 🎯 Core Concepts Learned
1. **Contribution Technique** → Count element participation instead of generating subarrays
2. **Prefix Sum** → Preprocess once, answer queries in O(1)
3. **Trade-off Pattern** → Space for time complexity optimization

### 🔗 Building Blocks For
- Sliding Window problems
- Segment Trees and Fenwick Trees  
- 2D Range Sum queries
- Difference Arrays
- Dynamic Programming on arrays

### 📝 Pattern Recognition
- **When you see "sum of subarrays"** → Think contribution technique
- **When you see "range queries"** → Think prefix sum or segment trees
- **When you see "multiple queries"** → Preprocessing is usually beneficial

---

## 🧪 Performance Analysis Insights

### ⚡ Empirical Discoveries
Comprehensive benchmarking across 7 algorithm implementations revealed surprising insights about modern Python performance:

### 📊 Small Arrays (n=99):
- 🥇 **Pure Python contribution technique** (4.0 μs) - Simple loops + JIT compilation
- 🥈 **Python with half-optimization** (4.2 μs) - Minimal memory savings benefit  
- 🥉 **NumPy vectorized** (5.0 μs) - Function call overhead dominates

### 📊 Large Arrays (n=1,000):
- 🥇 **NumPy vectorized** (27.8 μs) - C-level optimization takes over
- 🥈 **NumPy half-optimization** (28.0 μs) - Vectorization benefits dominate
- 🥉 **Python techniques** (51.9 μs) - Loop overhead becomes significant

### 🔍 Key Performance Insights:

#### **Modern Python JIT Optimization**
- Python 3.13+ JIT compilation **heavily optimizes simple arithmetic loops**
- Pure Python beats NumPy for **small problem sizes** (n < 1,000)
- **Constant factors and overhead** matter more than algorithmic complexity for small data

#### **NumPy Crossover Point**
- **Crossover occurs around n ≈ 1,000 elements**
- NumPy has **better scaling characteristics** (5.6x vs 13.2x growth)
- **Memory allocation overhead** dominates computational savings for small arrays

#### **Optimization Strategy Effectiveness**
- **Half-array + mirror optimization** saves only 2-5% computation time
- **Memory operations cost** often exceeds computational benefits
- **Simple, direct implementations** often outperform "clever" optimizations

### 💡 Practical Lessons:
- **Profile before optimizing** - assumptions about performance can be wrong
- **Problem size matters** for choosing optimization strategies  
- **Modern Python is fast** for simple numeric operations
- **Library overhead** may not be worth it for small datasets
- **Algorithmic complexity** isn't everything - measure real performance!

**Next:** Ready for Day 2 🚀

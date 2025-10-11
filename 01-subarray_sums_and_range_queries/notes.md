# Day 1: Subarray Sums & Range Queries

> **Learning Objectives:** Master prefix sum technique, understand contribution method, and solve range query problems efficiently.

---

## 📚 Concept 1: Sum of All Subarray Sums

### Problem Statement
Given an integer array `A` of length `N`, find the sum of all subarray sums.

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

#### 🐌 Approach 1: Brute Force
Generate all possible subarrays and calculate their sums.

**Algorithm:**
1. Use three nested loops
2. Outer two loops generate subarray boundaries
3. Inner loop calculates sum of current subarray

**Complexity:**
- 🕰️ Time: `O(n³)`
- 💾 Space: `O(1)`

#### ✨ Approach 2: Contribution Technique (Optimized)
Instead of generating subarrays, count how many times each element contributes to the final sum.

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

**Complexity:**
- 🕰️ Time: `O(n)`
- 💾 Space: `O(1)`

---

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

**Next:** Ready for Day 2 🚀

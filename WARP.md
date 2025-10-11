# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository Overview

This is a 60-day Data Structures and Algorithms learning repository following Neha Gupta's roadmap. Each day focuses on one concept with implementations in Python, JavaScript, and Java.

## Architecture & Structure

```
60-days-DSA/
├── README.md                    # Project overview and progress tracker
├── XX-topic_name/              # Daily learning directories (01-60)
│   ├── notes.md                # Concept explanation and theory
│   ├── solution.py             # Python implementation  
│   ├── solution.js             # JavaScript/Node.js implementation
│   └── Solution.java           # Java implementation
└── WARP.md                     # This file
```

### Daily Directory Pattern
- **Naming Convention:** `XX-topic_name` (e.g., `01-subarray_sums_and_range_queries`)
- **Notes Structure:** Problem statement → Examples → Solutions (brute force + optimized)
- **Implementation Files:** All three languages implement the same algorithms with comprehensive test cases

## Development Commands

### Running Solutions

**Python:**
```bash
cd XX-topic_name/
python solution.py
```

**JavaScript/Node.js:**
```bash
cd XX-topic_name/
node solution.js
```

**Java:**
```bash
cd XX-topic_name/
javac Solution.java
java Solution
```

### Testing Multiple Languages
```bash
# Quick test all implementations for a specific day
cd XX-topic_name/
python solution.py && echo "---" && node solution.js && echo "---" && javac Solution.java && java Solution
```

## Version Control Setup

This repository uses **both Git and Jujutsu (jj)** version control:

- **Primary VCS:** Jujutsu (`jj`) for advanced workflow features
- **Secondary:** Git for compatibility and remote hosting

### Common jj Commands
```bash
jj status                    # Check working copy status
jj log                       # View commit history  
jj new                       # Create new change
jj describe -m "message"     # Set commit message
jj git push                  # Push to remote
```

### Commit Pattern
Follow conventional commits for this learning journey:
- `feat: add day XX - topic_name` - New daily implementation
- `docs: improve day XX notes` - Documentation updates
- `fix: correct algorithm in day XX` - Bug fixes
- `refactor: optimize day XX solutions` - Code improvements

## Code Standards

### Implementation Requirements
1. **All three languages** must implement the same algorithms
2. **Comprehensive documentation** with time/space complexity
3. **Test cases** included in each implementation file
4. **Both brute force and optimized** solutions when applicable

### File Templates
- Each implementation should include author, date, and problem description
- Functions/methods should be well-documented with parameters and return values
- Include test cases that validate correctness

### Notes.md Structure
```markdown
# Day X: Topic Name

> Learning Objectives: Brief summary

## 📚 Concept 1: Problem Name
### Problem Statement
### 📊 Examples  
### 🔍 Detailed Explanation
### 💻 Solutions
#### 🐌 Approach 1: Brute Force
#### ✨ Approach 2: Optimized

## 🔑 Key Takeaways
```

## Learning Patterns

### Problem Recognition
- **Subarray problems** → Contribution technique or sliding window
- **Range queries** → Prefix sums or segment trees
- **Multiple queries** → Preprocessing usually beneficial

### Complexity Analysis
Always include both time and space complexity for each approach, explaining the trade-offs.

### Implementation Strategy
1. **Understand** the problem thoroughly
2. **Start with brute force** - get a working solution first
3. **Optimize** using appropriate data structures/algorithms
4. **Test** with provided examples and edge cases
5. **Document** learnings and patterns

## Progress Tracking

Update the README.md progress table after completing each day:
- Mark implementation files as ✅ when completed
- Update the status column (⏳ Pending → 🔄 In Progress → ✅ Completed)

## External Resources

- **Primary Guide:** [Neha Gupta's Medium](https://medium.com/@nehaguptacareercoach)
- **Practice Platform:** LeetCode for additional problems
- **Reference:** GeeksforGeeks for concept clarification

## Tips for Future Days

1. **Consistency is key** - Complete one concept daily
2. **Focus on patterns** - Look for recurring themes across problems  
3. **Language comparison** - Notice syntax differences but algorithmic similarities
4. **Build upon previous days** - Each concept builds on earlier learnings
5. **Document insights** - Update key takeaways as patterns emerge

This structured approach ensures comprehensive understanding while building a valuable reference for interview preparation.
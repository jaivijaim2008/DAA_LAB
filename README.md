# DAA Lab - Design and Analysis of Algorithms

This repository contains lab assignments for the **Design and Analysis of Algorithms (DAA)** course.

## Lab 1: Interpolation Search

### Problem
Implement and analyze the Interpolation Search algorithm for searching elements in a sorted array.

### Description
Interpolation Search is an improved variant of Binary Search for instances where the values in a sorted array are **uniformly distributed**. Instead of always going to the middle element, it estimates the position of the target element based on the value being searched.

### Algorithm
- Calculates the probable position using the formula:
  ```
  pos = low + ((target - arr[low]) * (high - low)) / (arr[high] - arr[low])
  ```
- Adjusts the search range based on comparison results

### Complexity
| Case         | Time Complexity |
|--------------|-----------------|
| Best Case    | O(1)            |
| Average Case | O(log log n)    |
| Worst Case   | O(n)            |
| Space        | O(1)            |

### Features
- Interactive input for custom array and target
- Performance analysis comparing Interpolation Search vs Binary Search
- Comparison count tracking for both algorithms

---

## Lab 2: String Matching Algorithms

### Problem
Implement and compare different string matching algorithms: Naive, KMP, and Rabin-Karp.

### Description
String matching is the problem of finding all occurrences of a pattern string within a text string. This lab implements three fundamental approaches and compares their performance.

### Algorithms Implemented

#### 1. Naive String Matching
- Brute-force approach that checks every possible position
- **Time Complexity:** O((n-m+1) × m) average, O(n × m) worst case

#### 2. KMP (Knuth-Morris-Pratt) Algorithm
- Uses preprocessing to avoid redundant comparisons
- Builds a Longest Proper Prefix Suffix (LPS) array
- **Time Complexity:** O(n + m)

#### 3. Rabin-Karp Algorithm
- Uses rolling hash technique for efficient matching
- Compares hash values before character-by-character verification
- **Time Complexity:** O((n-m+1) × m) average, O(n + m) best case

### Features
- Demonstrates all three algorithms on sample text
- Performance comparison with varying pattern lengths
- Tracks comparison counts for each algorithm

---

## How to Run

### Prerequisites
- Python 3.x

### Running Lab 1
```bash
python lab1.py
```
Follow the prompts to enter a sorted array and target value.

### Running Lab 2
```bash
python lab2.py
```
The program runs automatically with sample data and generates performance comparison.

---

## Author
- **Name:** Jai Vijai M
- **Course:** Design and Analysis of Algorithms (DAA)

---

## License
This project is for educational purposes as part of DAA course lab assignments.

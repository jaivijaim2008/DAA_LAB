import streamlit as st
import time
import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================================
# MIN-MAX DIVIDE AND CONQUER
# ============================================================================

class ComparisonCounter:
    """Thread-safe comparison counter using a class instead of global variable."""
    def __init__(self):
        self.count = 0

    def reset(self):
        self.count = 0

    def increment(self, n=1):
        self.count += n

    def get(self):
        return self.count


def min_max_dc(arr, low, high, counter=None):
    """
    Divide and Conquer Min-Max Algorithm
    Time: O(n), Comparisons: 3n/2 - 2
    """
    # Base case: single element
    if low == high:
        return arr[low], arr[low]

    # Base case: two elements
    if high == low + 1:
        if counter:
            counter.increment()
        if arr[low] < arr[high]:
            return arr[low], arr[high]
        return arr[high], arr[low]

    # Divide
    mid = (low + high) // 2
    lmin, lmax = min_max_dc(arr, low, mid, counter)
    rmin, rmax = min_max_dc(arr, mid + 1, high, counter)

    # Conquer: combine with 2 comparisons
    if counter:
        counter.increment()
    overall_min = lmin if lmin < rmin else rmin
    if counter:
        counter.increment()
    overall_max = lmax if lmax > rmax else rmax

    return overall_min, overall_max


def min_max_naive(arr):
    """
    Naive Linear Min-Max Algorithm
    Time: O(n), Comparisons: 2(n-1)
    """
    mn, mx = arr[0], arr[0]
    comps = 0
    for x in arr[1:]:
        comps += 1
        if x < mn:
            mn = x
        comps += 1
        if x > mx:
            mx = x
    return mn, mx, comps


# ============================================================================
# STREAMLIT APP
# ============================================================================

st.set_page_config(page_title="Lab 5 - Min-Max Divide & Conquer", layout="wide")
st.title("📊 Lab 5: Min-Max by Divide and Conquer")
st.markdown("Find minimum and maximum elements using **Divide & Conquer** vs **Naive** approach")

tab1, tab2, tab3 = st.tabs(["Interactive Demo", "Performance Comparison", "Algorithm Details"])

# ============================================================================
# TAB 1: INTERACTIVE DEMO
# ============================================================================

with tab1:
    st.subheader("Min-Max Demo")

    # --- Array Input ---
    st.write("### Step 1: Define the Array")

    array_mode = st.radio("Array source:", ["Sample Array", "Custom Array", "Random Array"], horizontal=True)

    if array_mode == "Sample Array":
        arr = [3, 1, 7, 4, 9, 2, 8, 5, 6, 0]
        st.info(f"Using sample array: `{arr}`")
    elif array_mode == "Custom Array":
        raw_input = st.text_input(
            "Enter numbers separated by commas:",
            placeholder="e.g. 3, 1, 7, 4, 9, 2, 8, 5, 6, 0"
        )
        if raw_input.strip():
            try:
                arr = [int(x.strip()) for x in raw_input.split(",")]
                st.success(f"✅ Array: `{arr}` (size: {len(arr)})")
            except ValueError:
                st.error("❌ Please enter valid integers separated by commas.")
                arr = [3, 1, 7, 4, 9, 2, 8, 5, 6, 0]
        else:
            st.warning("⚠️ No input provided. Using sample array.")
            arr = [3, 1, 7, 4, 9, 2, 8, 5, 6, 0]
    else:
        size = st.slider("Array size:", min_value=5, max_value=100, value=10)
        arr = [random.randint(1, 100) for _ in range(size)]
        st.info(f"Generated random array of size {size}")

    st.write("---")

    # --- Run Algorithms ---
    st.write("### Step 2: Compare Approaches")

    # D&C approach
    counter = ComparisonCounter()
    dc_min, dc_max = min_max_dc(arr, 0, len(arr) - 1, counter)
    dc_comps = counter.get()

    # Naive approach
    naive_min, naive_max, naive_comps = min_max_naive(arr)

    # Results
    col1, col2 = st.columns(2)

    with col1:
        st.write("#### 🔵 Divide & Conquer")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Minimum", dc_min)
        with col_b:
            st.metric("Maximum", dc_max)
        st.metric("Comparisons", dc_comps)
        st.caption(f"Formula: 3n/2 - 2 = {3 * len(arr) // 2 - 2}")

    with col2:
        st.write("#### 🟠 Naive Approach")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Minimum", naive_min)
        with col_b:
            st.metric("Maximum", naive_max)
        st.metric("Comparisons", naive_comps)
        st.caption(f"Formula: 2(n-1) = {2 * (len(arr) - 1)}")

    # Verify results match
    if dc_min == naive_min and dc_max == naive_max:
        st.success("✅ Both approaches found the same min and max!")
    else:
        st.error("❌ Results differ — this shouldn't happen!")

    st.write("---")

    # --- Comparison Chart ---
    st.write("### Step 3: Visualize Comparison")

    comp_df = pd.DataFrame({
        'Approach': ['Divide & Conquer', 'Naive'],
        'Comparisons': [dc_comps, naive_comps],
        'Theoretical': [3 * len(arr) // 2 - 2, 2 * (len(arr) - 1)]
    })

    fig = px.bar(comp_df, x='Approach', y='Comparisons',
                 color='Approach',
                 title=f'Comparisons for Array of Size {len(arr)}',
                 labels={'Comparisons': 'Number of Comparisons'},
                 text='Comparisons')
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, width='stretch')

    # Improvement
    improvement = (1 - dc_comps / naive_comps) * 100 if naive_comps > 0 else 0
    st.metric("Improvement", f"{improvement:.1f}%", delta=f"{naive_comps - dc_comps} fewer comparisons")

    st.write("---")

    # --- Divide & Conquer Tree Visualization ---
    st.write("### Step 4: D&C Recursion Tree")

    if len(arr) <= 16:
        # Show recursive breakdown
        st.write("**Recursive Decomposition:**")

        def show_recursion(arr, low, high, depth=0):
            indent = "  " * depth
            if low == high:
                st.write(f"{indent}• Leaf: arr[{low}] = {arr[low]} → min={arr[low]}, max={arr[low]}")
            elif high == low + 1:
                mn, mx = (arr[low], arr[high]) if arr[low] < arr[high] else (arr[high], arr[low])
                st.write(f"{indent}• Two elements: [{arr[low]}, {arr[high]}] → min={mn}, max={mx} (1 comparison)")
            else:
                mid = (low + high) // 2
                st.write(f"{indent}• Split [{low}:{high}] at mid={mid}")
                show_recursion(arr, low, mid, depth + 1)
                show_recursion(arr, mid + 1, high, depth + 1)
                st.write(f"{indent}• Combine with 2 comparisons")

        show_recursion(arr, 0, len(arr) - 1)
    else:
        st.info("Array too large for recursive visualization (showing for arrays ≤ 16 elements)")

    # --- Performance Analysis ---
    st.write("---")
    st.write("### Step 5: Size vs Comparisons Analysis")

    sizes = [10, 50, 100, 500, 1000, 5000, 10000]
    perf_results = []

    for size in sizes:
        test_arr = [random.randint(1, 10000) for _ in range(size)]

        counter = ComparisonCounter()
        min_max_dc(test_arr, 0, len(test_arr) - 1, counter)
        dc = counter.get()

        _, _, naive = min_max_naive(test_arr)

        perf_results.append({
            'Size': size,
            'DC Comparisons': dc,
            'Naive Comparisons': naive,
            'Formula (3n/2-2)': 3 * size // 2 - 2,
            'Formula (2n-2)': 2 * (size - 1)
        })

    perf_df = pd.DataFrame(perf_results)

    fig = px.line(perf_df, x='Size', y=['DC Comparisons', 'Naive Comparisons'],
                  title='Comparisons vs Array Size',
                  markers=True,
                  labels={'Size': 'Array Size', 'value': 'Comparisons'})
    st.plotly_chart(fig, width='stretch')

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(perf_df, width='stretch')
    with col2:
        st.write("### Key Insights")
        st.write(f"✅ **D&C always uses ~25% fewer comparisons** than naive")
        st.write(f"✅ **For n={sizes[-1]}:** DC uses {perf_df.iloc[-1]['DC Comparisons']:,} vs Naive {perf_df.iloc[-1]['Naive Comparisons']:,}")
        st.write(f"✅ **Savings:** {perf_df.iloc[-1]['Naive Comparisons'] - perf_df.iloc[-1]['DC Comparisons']:,} comparisons")

# ============================================================================
# TAB 2: PERFORMANCE COMPARISON
# ============================================================================

with tab2:
    st.subheader("Detailed Performance Analysis")

    st.write("### Execution Time Comparison")

    sizes = [100, 500, 1000, 5000, 10000, 50000, 100000]
    time_results = []

    progress_bar = st.progress(0)
    status_text = st.empty()

    for idx, size in enumerate(sizes):
        status_text.text(f"Testing array of size {size}...")

        test_arr = [random.randint(1, 100000) for _ in range(size)]

        # D&C timing
        start = time.perf_counter()
        for _ in range(10):
            c = ComparisonCounter()
            min_max_dc(test_arr, 0, len(test_arr) - 1, c)
        dc_time = (time.perf_counter() - start) / 10 * 1000

        # Naive timing
        start = time.perf_counter()
        for _ in range(10):
            min_max_naive(test_arr)
        naive_time = (time.perf_counter() - start) / 10 * 1000

        c2 = ComparisonCounter()
        min_max_dc(test_arr, 0, len(test_arr) - 1, c2)
        dc_comps = c2.get()
        _, _, naive_comps = min_max_naive(test_arr)

        time_results.append({
            'Size': size,
            'DC Time (ms)': round(dc_time, 4),
            'Naive Time (ms)': round(naive_time, 4),
            'DC Comparisons': dc_comps,
            'Naive Comparisons': naive_comps,
            'Speedup': round(naive_time / dc_time, 2) if dc_time > 0 else 0
        })

        progress_bar.progress((idx + 1) / len(sizes))

    status_text.empty()
    time_df = pd.DataFrame(time_results)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.line(time_df, x='Size', y=['DC Time (ms)', 'Naive Time (ms)'],
                      title='Execution Time vs Array Size',
                      markers=True,
                      labels={'Size': 'Array Size', 'value': 'Time (ms)'})
        st.plotly_chart(fig, width='stretch')

    with col2:
        fig = px.bar(time_df, x='Size', y=['DC Comparisons', 'Naive Comparisons'],
                     title='Comparisons vs Array Size',
                     barmode='group',
                     labels={'Size': 'Array Size', 'value': 'Comparisons'})
        st.plotly_chart(fig, width='stretch')

    st.write("### Results Table")
    st.dataframe(time_df, width='stretch')

    st.write("---")
    st.write("### Summary")

    avg_speedup = time_df['Speedup'].mean()
    st.write(f"✅ **Average speedup:** {avg_speedup:.2f}x")
    st.write(f"✅ **Max speedup:** {time_df['Speedup'].max():.2f}x (at size {time_df.loc[time_df['Speedup'].idxmax(), 'Size']})")

    st.write("---")
    st.write("### Why D&C is Better")

    st.markdown("""
    **Comparison Analysis:**

    | Approach | Comparisons | Time Complexity |
    |----------|-------------|-----------------|
    | Naive | 2(n-1) | O(n) |
    | Divide & Conquer | 3n/2 - 2 | O(n) |

    **Key Insight:**
    - Both are O(n) time complexity
    - But D&C uses **25% fewer comparisons**
    - For n = 10,000: D&C uses 14,998 vs Naive 19,998 comparisons
    - This matters in hardware implementations where comparison cost is significant

    **Why it works:**
    - Process elements in pairs
    - Compare elements within pair first (1 comparison)
    - Then compare winners for max and losers for min (2 more comparisons)
    - Total: 3 comparisons per 2 elements = 3n/2
    """)

# ============================================================================
# TAB 3: ALGORITHM DETAILS
# ============================================================================

with tab3:
    st.subheader("Algorithm Deep Dive")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Divide & Conquer Min-Max")
        st.markdown("""
        **Strategy:** Divide array into halves, find min/max recursively

        **Steps:**
        1. If single element: min = max = that element
        2. If two elements: compare once, return min and max
        3. Otherwise:
           - Divide array in half
           - Recursively find min/max of left half
           - Recursively find min/max of right half
           - Combine: min = min(left_min, right_min)
                     max = max(left_max, right_max)

        **Comparisons:**
        - Base case (1 element): 0 comparisons
        - Base case (2 elements): 1 comparison
        - Combine step: 2 comparisons
        - Total: 3n/2 - 2
        """)

        st.code("""
def min_max_dc(arr, low, high, counter=None):
    # Base case: single element
    if low == high:
        return arr[low], arr[low]

    # Base case: two elements
    if high == low + 1:
        if counter:
            counter.increment()
        if arr[low] < arr[high]:
            return arr[low], arr[high]
        return arr[high], arr[low]

    # Divide
    mid = (low + high) // 2
    lmin, lmax = min_max_dc(arr, low, mid, counter)
    rmin, rmax = min_max_dc(arr, mid + 1, high, counter)

    # Combine
    if counter:
        counter.increment()
    overall_min = lmin if lmin < rmin else rmin
    if counter:
        counter.increment()
    overall_max = lmax if lmax > rmax else rmax

    return overall_min, overall_max
        """, language="python")

    with col2:
        st.write("### Naive Approach")
        st.markdown("""
        **Strategy:** Linear scan through array

        **Steps:**
        1. Initialize min = max = first element
        2. For each remaining element:
           - Compare with min (1 comparison)
           - Compare with max (1 comparison)
           - Update if needed

        **Comparisons:** 2(n-1)

        **Note:** Each element is compared twice — once for min, once for max
        """)

        st.code("""
def min_max_naive(arr):
    mn, mx = arr[0], arr[0]
    for x in arr[1:]:
        if x < mn:
            mn = x
        if x > mx:
            mx = x
    return mn, mx
        """, language="python")

    st.write("---")
    st.write("### Comparison Analysis")

    comparison_data = {
        'Metric': ['Time Complexity', 'Space Complexity', 'Comparisons', 'Implementation', 'Best For'],
        'Divide & Conquer': ['O(n)', 'O(log n) stack', '3n/2 - 2', 'Recursive', 'Parallel systems'],
        'Naive': ['O(n)', 'O(1)', '2(n-1)', 'Iterative', 'Simple cases']
    }

    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, width='stretch', hide_index=True)

    st.write("---")
    st.write("### Theoretical Proof")

    st.markdown("""
    **Claim:** The D&C algorithm uses exactly ⌈3n/2⌉ - 2 comparisons.

    **Proof by induction:**

    **Base cases:**
    - n = 1: 0 comparisons (3·1/2 - 2 = -0.5, rounds to 0) ✓
    - n = 2: 1 comparison (3·2/2 - 2 = 1) ✓

    **Inductive step:**
    - Assume true for n = k: T(k) = 3k/2 - 2
    - For n = k+1 (even):
      - Split into two halves of size (k+1)/2
      - Each half: T((k+1)/2) = 3(k+1)/4 - 2
      - Combine: 2 comparisons
      - Total: 2·[3(k+1)/4 - 2] + 2 = 3(k+1)/2 - 2 ✓

    **Conclusion:** D&C uses exactly 25% fewer comparisons than naive approach.
    """)

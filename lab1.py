import streamlit as st
import time
import random
import pandas as pd
import plotly.express as px

# ============================================================================
# INTERPOLATION SEARCH SECTION
# ============================================================================

def interpolation_search(arr, target):
    """Interpolation Search Algorithm"""
    low, high = 0, len(arr) - 1
    comparisons = 0
    
    while low <= high and arr[low] <= target <= arr[high]:
        comparisons += 1
        if low == high:
            if arr[low] == target:
                return low, comparisons
            return -1, comparisons
        
        pos = low + int(((target - arr[low]) * (high - low)) / (arr[high] - arr[low]))
        
        if arr[pos] == target:
            return pos, comparisons
        elif arr[pos] < target:
            low = pos + 1
        else:
            high = pos - 1
    
    return -1, comparisons

def binary_search(arr, target):
    """Binary Search for comparison"""
    low, high = 0, len(arr) - 1
    comparisons = 0
    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, comparisons

# ============================================================================
# STREAMLIT APP
# ============================================================================

st.set_page_config(page_title="Lab 1 - Interpolation Search", layout="wide")
st.title("🔍 Lab 1: Interpolation Search Analysis")
st.markdown("Compare **Interpolation Search** vs **Binary Search** performance")

tab1, tab2 = st.tabs(["Single Search", "Performance Comparison"])

with tab1:
    st.subheader("Search Demo")
    col1, col2 = st.columns(2)
    
    with col1:
        demo_mode = st.radio("Choose mode:", ["Sample Array", "Random Array"])
        
        if demo_mode == "Sample Array":
            arr = [2, 5, 10, 15, 23, 35, 48, 60, 75, 90, 105, 120]
            target = st.number_input("Target value:", value=35, min_value=min(arr), max_value=max(arr))
        else:
            size = st.slider("Array size:", 50, 500, 100)
            arr = sorted(random.sample(range(size * 10), size))
            target = st.number_input("Target value:", value=arr[len(arr)//2], min_value=min(arr), max_value=max(arr))
    
    with col2:
        st.write(f"**Array:** {arr[:10]}{'...' if len(arr) > 10 else ''}")
        st.write(f"**Array size:** {len(arr)}")
        st.write(f"**Searching for:** {target}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Interpolation Search")
        idx_is, comp_is = interpolation_search(arr, target)
        st.metric("Found at index", idx_is if idx_is != -1 else "Not found")
        st.metric("Comparisons", comp_is)
    
    with col2:
        st.write("### Binary Search")
        idx_bs, comp_bs = binary_search(arr, target)
        st.metric("Found at index", idx_bs if idx_bs != -1 else "Not found")
        st.metric("Comparisons", comp_bs)

with tab2:
    st.subheader("Performance Analysis")
    
    sizes = [1000, 5000, 10000, 50000, 100000]
    results = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, size in enumerate(sizes):
        status_text.text(f"Testing size {size}...")
        arr = sorted(random.sample(range(size * 10), size))
        target = arr[random.randint(0, size - 1)]
        
        # Interpolation Search timing
        start = time.perf_counter()
        for _ in range(100):
            interpolation_search(arr, target)
        is_time = (time.perf_counter() - start) / 100 * 1000
        
        # Binary Search timing
        start = time.perf_counter()
        for _ in range(100):
            binary_search(arr, target)
        bs_time = (time.perf_counter() - start) / 100 * 1000
        
        results.append({
            'Size': size,
            'Interpolation Search (ms)': is_time,
            'Binary Search (ms)': bs_time
        })
        
        progress_bar.progress((idx + 1) / len(sizes))
    
    status_text.empty()
    df = pd.DataFrame(results)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(df, x='Size', y=['Interpolation Search (ms)', 'Binary Search (ms)'],
                     title='Search Time Comparison',
                     markers=True,
                     labels={'Size': 'Array Size', 'value': 'Time (ms)'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("### Results Table")
        st.dataframe(df, use_container_width=True)
        
        st.write("---")
        st.write("### Algorithm Details")
        st.markdown("""
        - **Interpolation Search:** O(log log n) average, O(n) worst case
        - **Binary Search:** O(log n) — consistent performance
        
        **When IS is better:** Uniformly distributed data
        """)

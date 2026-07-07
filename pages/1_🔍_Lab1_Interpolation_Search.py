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
# PAGE
# ============================================================================

st.title("🔍 Lab 1: Interpolation Search Analysis")
st.markdown("Compare **Interpolation Search** vs **Binary Search** performance")

tab1, tab2 = st.tabs(["Single Search", "Performance Comparison"])

with tab1:
    st.subheader("Search Demo")

    st.write("### Step 1: Enter Your Array")
    array_mode = st.radio("Array source:", ["Sample Array", "Custom Array"], horizontal=True)

    default_arr = [2, 5, 10, 15, 23, 35, 48, 60, 75, 90, 105, 120]

    if array_mode == "Sample Array":
        arr = default_arr
        st.info(f"Using sample array: `{arr}`")
    else:
        raw_input = st.text_input(
            "Enter numbers separated by commas:",
            placeholder="e.g. 3, 7, 12, 19, 25, 40, 55"
        )
        if raw_input.strip():
            try:
                arr = sorted([int(x.strip()) for x in raw_input.split(",")])
                st.success(f"✅ Sorted array: `{arr}`")
            except ValueError:
                st.error("❌ Please enter valid integers separated by commas.")
                arr = default_arr
        else:
            st.warning("⚠️ No input provided. Using sample array.")
            arr = default_arr

    st.write("---")

    st.write("### Step 2: Enter Search Target")

    col1, col2 = st.columns(2)

    with col1:
        target_mode = st.radio("Target source:", ["Pick from array", "Enter manually"], horizontal=True)

        if target_mode == "Pick from array":
            target = st.selectbox("Select a value to search:", sorted(set(arr)))
        else:
            target = st.number_input("Enter target value:", value=int(arr[len(arr)//2]))

    with col2:
        st.write("**Array info:**")
        st.write(f"- Size: `{len(arr)}`")
        st.write(f"- Min: `{min(arr)}`")
        st.write(f"- Max: `{max(arr)}`")
        st.write(f"- Values: `{arr}`")

    st.write("---")

    st.write("### Step 3: Results")

    col1, col2 = st.columns(2)

    with col1:
        st.write("#### 🔵 Interpolation Search")
        idx_is, comp_is = interpolation_search(arr, int(target))
        if idx_is != -1:
            st.success(f"✅ Found `{target}` at index `{idx_is}`")
        else:
            st.error(f"❌ `{target}` not found in array")
        st.metric("Comparisons", comp_is)

    with col2:
        st.write("#### 🟠 Binary Search")
        idx_bs, comp_bs = binary_search(arr, int(target))
        if idx_bs != -1:
            st.success(f"✅ Found `{target}` at index `{idx_bs}`")
        else:
            st.error(f"❌ `{target}` not found in array")
        st.metric("Comparisons", comp_bs)

    st.write("---")
    st.write("### Comparison Chart")
    comp_df = pd.DataFrame({
        'Algorithm': ['Interpolation Search', 'Binary Search'],
        'Comparisons': [comp_is, comp_bs]
    })
    fig = px.bar(comp_df, x='Algorithm', y='Comparisons',
                 color='Algorithm',
                 title=f'Comparisons to find target `{target}`',
                 labels={'Comparisons': 'Number of Comparisons'})
    st.plotly_chart(fig, width='stretch')

with tab2:
    st.subheader("Performance Analysis")

    sizes = [1000, 5000, 10000, 50000, 100000]
    results = []

    progress_bar = st.progress(0)
    status_text = st.empty()

    for idx, size in enumerate(sizes):
        status_text.text(f"Testing size {size}...")
        arr_perf = sorted(random.sample(range(size * 10), size))
        target_perf = arr_perf[random.randint(0, size - 1)]

        start = time.perf_counter()
        for _ in range(100):
            interpolation_search(arr_perf, target_perf)
        is_time = (time.perf_counter() - start) / 100 * 1000

        start = time.perf_counter()
        for _ in range(100):
            binary_search(arr_perf, target_perf)
        bs_time = (time.perf_counter() - start) / 100 * 1000

        results.append({
            'Size': size,
            'Interpolation Search (ms)': round(is_time, 6),
            'Binary Search (ms)': round(bs_time, 6)
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
        st.plotly_chart(fig, width='stretch')

    with col2:
        st.write("### Results Table")
        st.dataframe(df, width='stretch')

        st.write("---")
        st.write("### Summary")
        avg_is = df['Interpolation Search (ms)'].mean()
        avg_bs = df['Binary Search (ms)'].mean()
        faster = "Interpolation Search" if avg_is < avg_bs else "Binary Search"
        st.write(f"✅ **Faster on average:** **{faster}**")

        st.write("---")
        st.write("### Algorithm Details")
        st.markdown("""
        - **Interpolation Search:** O(log log n) average, O(n) worst case
        - **Binary Search:** O(log n) — consistent performance

        **When IS is better:** Uniformly distributed data
        """)

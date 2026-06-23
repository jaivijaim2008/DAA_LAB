import streamlit as st
import pandas as pd
import random
import time

st.set_page_config(page_title="Interpolation Search Explorer", page_icon="🔍", layout="wide")


def interpolation_search(arr, target):
    """Interpolation search that also records a step-by-step trace."""
    low, high = 0, len(arr) - 1
    comparisons = 0
    steps = []
    while low <= high and arr[low] <= target <= arr[high]:
        comparisons += 1
        if low == high:
            result = "found" if arr[low] == target else "not found"
            steps.append({"low": low, "high": high, "pos": low, "value": arr[low], "result": result})
            return (low if result == "found" else -1), comparisons, steps

        pos = low + int(((target - arr[low]) * (high - low)) / (arr[high] - arr[low]))
        pos = max(low, min(pos, high))  # safety clamp

        if arr[pos] == target:
            steps.append({"low": low, "high": high, "pos": pos, "value": arr[pos], "result": "found"})
            return pos, comparisons, steps
        elif arr[pos] < target:
            steps.append({"low": low, "high": high, "pos": pos, "value": arr[pos], "result": "go right"})
            low = pos + 1
        else:
            steps.append({"low": low, "high": high, "pos": pos, "value": arr[pos], "result": "go left"})
            high = pos - 1

    steps.append({"low": low, "high": high, "pos": None, "value": None, "result": "not found"})
    return -1, comparisons, steps


def binary_search(arr, target):
    """Binary search that also records a step-by-step trace."""
    low, high = 0, len(arr) - 1
    comparisons = 0
    steps = []
    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        if arr[mid] == target:
            steps.append({"low": low, "high": high, "pos": mid, "value": arr[mid], "result": "found"})
            return mid, comparisons, steps
        elif arr[mid] < target:
            steps.append({"low": low, "high": high, "pos": mid, "value": arr[mid], "result": "go right"})
            low = mid + 1
        else:
            steps.append({"low": low, "high": high, "pos": mid, "value": arr[mid], "result": "go left"})
            high = mid - 1
    steps.append({"low": low, "high": high, "pos": None, "value": None, "result": "not found"})
    return -1, comparisons, steps


st.title("🔍 Interpolation Search vs Binary Search")
st.caption("CS5303 – DAA Lab · Chennai Institute of Technology")

tab1, tab2 = st.tabs(["🎯 Single Search Demo", "📊 Performance Analysis"])

# ---------------------------------------------------------------- TAB 1
with tab1:
    st.subheader("Try a search")
    col1, col2 = st.columns(2)

    with col1:
        mode = st.radio("Array source", ["Generate random sorted array", "Enter custom array"])
        if mode == "Generate random sorted array":
            size = st.slider("Array size", 5, 50, 12)
            max_val = st.slider("Max value", size * 2, size * 20, size * 10)
            if st.button("🎲 Generate new array") or "arr" not in st.session_state:
                st.session_state.arr = sorted(random.sample(range(max_val), size))
            arr = st.session_state.arr
        else:
            raw = st.text_input("Comma-separated sorted numbers", "2,5,10,15,23,35,48,60,75,90,105,120")
            try:
                arr = sorted(int(x.strip()) for x in raw.split(",") if x.strip() != "")
            except ValueError:
                st.error("Please enter valid integers separated by commas.")
                arr = []

    with col2:
        st.write("**Array:**")
        st.code(str(arr))
        target = st.number_input("Target value", value=arr[len(arr) // 2] if arr else 0, step=1)

    if arr and st.button("🔍 Run search", type="primary"):
        idx_is, comp_is, steps_is = interpolation_search(arr, target)
        idx_bs, comp_bs, steps_bs = binary_search(arr, target)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### Interpolation Search")
            st.metric("Result", f"Index {idx_is}" if idx_is != -1 else "Not found")
            st.metric("Comparisons", comp_is)
            st.dataframe(pd.DataFrame(steps_is), use_container_width=True)
        with c2:
            st.markdown("### Binary Search")
            st.metric("Result", f"Index {idx_bs}" if idx_bs != -1 else "Not found")
            st.metric("Comparisons", comp_bs)
            st.dataframe(pd.DataFrame(steps_bs), use_container_width=True)

# ---------------------------------------------------------------- TAB 2
with tab2:
    st.subheader("Compare performance across array sizes")
    sizes = st.multiselect(
        "Array sizes to test",
        [1000, 5000, 10000, 50000, 100000, 500000],
        default=[1000, 5000, 10000, 50000, 100000],
    )
    runs = st.slider("Timing runs per size (higher = more accurate, slower)", 10, 200, 50)

    if st.button("▶️ Run performance analysis", type="primary"):
        results = []
        progress = st.progress(0.0)
        for i, size in enumerate(sizes):
            big_arr = sorted(random.sample(range(size * 10), size))
            target = big_arr[random.randint(0, size - 1)]

            start = time.perf_counter()
            for _ in range(runs):
                idx_is, comp_is, _ = interpolation_search(big_arr, target)
            is_time = (time.perf_counter() - start) / runs * 1000

            start = time.perf_counter()
            for _ in range(runs):
                idx_bs, comp_bs, _ = binary_search(big_arr, target)
            bs_time = (time.perf_counter() - start) / runs * 1000

            results.append({
                "Size": size,
                "IS Time (ms)": is_time,
                "BS Time (ms)": bs_time,
                "IS Comparisons": comp_is,
                "BS Comparisons": comp_bs,
            })
            progress.progress((i + 1) / max(len(sizes), 1))

        df = pd.DataFrame(results)
        st.dataframe(df, use_container_width=True)

        st.markdown("**Time (ms) by array size**")
        st.line_chart(df.set_index("Size")[["IS Time (ms)", "BS Time (ms)"]])

        st.markdown("**Comparisons by array size**")
        st.bar_chart(df.set_index("Size")[["IS Comparisons", "BS Comparisons"]])

st.divider()
st.caption("Interpolation Search: O(log log n) average / O(n) worst case · Binary Search: O(log n)")

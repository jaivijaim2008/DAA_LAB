import streamlit as st

st.set_page_config(
    page_title="DAA Lab - Algorithm Visualizer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
<style>
    .main .block-container { padding-top: 2rem; }
    .stAppHeader { display: none; }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .hero-subtitle {
        font-size: 1.15rem;
        color: #666;
        text-align: center;
        margin-bottom: 2.5rem;
    }
    .lab-card {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
    }
    .lab-card:hover {
        border-color: #667eea;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.15);
        transform: translateY(-2px);
    }
    .lab-icon { font-size: 3rem; margin-bottom: 0.8rem; }
    .lab-title { font-size: 1.3rem; font-weight: 700; color: #1a1a2e; margin-bottom: 0.5rem; }
    .lab-desc { font-size: 0.9rem; color: #555; line-height: 1.6; margin-bottom: 1rem; }
    .lab-tag {
        display: inline-block;
        background: #f0f0ff;
        color: #667eea;
        padding: 0.25rem 0.7rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 0.15rem;
    }
    .footer-text { text-align: center; color: #999; font-size: 0.8rem; margin-top: 3rem; }
</style>
""", unsafe_allow_html=True)

# --- Hero ---
st.markdown('<div class="hero-title">DAA Lab — Algorithm Visualizer</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Interactive visualizations for Design & Analysis of Algorithms labs<br>'
    'Chennai Institute of Technology &middot; Dept. of CSE</div>',
    unsafe_allow_html=True
)

# --- Lab Cards ---
st.write("")

col1, col2, col3 = st.columns(3)
col4, col5 = st.columns(2)

with col1:
    st.markdown("""
    <div class="lab-card">
        <div class="lab-icon">🔍</div>
        <div class="lab-title">Lab 1 — Interpolation Search</div>
        <div class="lab-desc">
            Compare <b>Interpolation Search</b> vs <b>Binary Search</b> on sorted arrays.
            Visualize comparisons, step-by-step execution, and benchmark performance across array sizes.
        </div>
        <span class="lab-tag">Searching</span>
        <span class="lab-tag">O(log log n)</span>
        <span class="lab-tag">Comparison</span>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("▶  Open Lab 1", key="lab1", use_container_width=True):
        st.switch_page("pages/1_🔍_Lab1_Interpolation_Search.py")

with col2:
    st.markdown("""
    <div class="lab-card">
        <div class="lab-icon">🔤</div>
        <div class="lab-title">Lab 2 — String Matching</div>
        <div class="lab-desc">
            Compare <b>Naive</b>, <b>KMP</b>, and <b>Rabin-Karp</b> string matching algorithms.
            Analyze character comparisons and find all occurrences of a pattern in text.
        </div>
        <span class="lab-tag">String Matching</span>
        <span class="lab-tag">KMP</span>
        <span class="lab-tag">Rolling Hash</span>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("▶  Open Lab 2", key="lab2", use_container_width=True):
        st.switch_page("pages/2_🔤_Lab2_String_Matching.py")

with col3:
    st.markdown("""
    <div class="lab-card">
        <div class="lab-icon">🌳</div>
        <div class="lab-title">Lab 3 — Minimum Spanning Tree</div>
        <div class="lab-desc">
            Compare <b>Kruskal's</b> and <b>Prim's</b> algorithms for MST.
            Visualize graph structures, edge selections, and total MST cost with interactive graphs.
        </div>
        <span class="lab-tag">Graph Theory</span>
        <span class="lab-tag">Greedy</span>
        <span class="lab-tag">Union-Find</span>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("▶  Open Lab 3", key="lab3", use_container_width=True):
        st.switch_page("pages/3_🌳_Lab3_MST_Algorithms.py")

with col4:
    st.markdown("""
    <div class="lab-card">
        <div class="lab-icon">📐</div>
        <div class="lab-title">Lab 4 — Dijkstra's Shortest Path</div>
        <div class="lab-desc">
            Implement <b>Dijkstra's Algorithm</b> to find shortest paths from a single source.
            Visualize graph relaxations, path reconstruction, and compare performance.
        </div>
        <span class="lab-tag">Graph Theory</span>
        <span class="lab-tag">Greedy</span>
        <span class="lab-tag">O((V+E) log V)</span>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("▶  Open Lab 4", key="lab4", use_container_width=True):
        st.switch_page("pages/4_📐_Lab4_Dijkstra_Shortest_Path.py")

with col5:
    st.markdown("""
    <div class="lab-card">
        <div class="lab-icon">📊</div>
        <div class="lab-title">Lab 5 — Min-Max Divide & Conquer</div>
        <div class="lab-desc">
            Find <b>min and max</b> simultaneously using Divide & Conquer.
            Compare 3n/2 - 2 comparisons vs 2(n-1) naive approach with analysis.
        </div>
        <span class="lab-tag">Divide & Conquer</span>
        <span class="lab-tag">O(n)</span>
        <span class="lab-tag">Optimal</span>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("▶  Open Lab 5", key="lab5", use_container_width=True):
        st.switch_page("pages/5_📊_Lab5_Min_Max_Divide_Conquer.py")

# --- Lab 6 Row ---
st.write("")
col6, col7, col8 = st.columns(3)

with col6:
    st.markdown("""
    <div class="lab-card">
        <div class="lab-icon">🔗</div>
        <div class="lab-title">Lab 6 — Matrix Chain Multiplication</div>
        <div class="lab-desc">
            Find the <b>optimal parenthesization</b> to minimize scalar multiplications.
            Compare <b>DP</b> O(n³) vs <b>Naive</b> O(2ⁿ) with interactive DP table visualization.
        </div>
        <span class="lab-tag">Dynamic Programming</span>
        <span class="lab-tag">O(n³)</span>
        <span class="lab-tag">Optimization</span>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("▶  Open Lab 6", key="lab6", use_container_width=True):
        st.switch_page("pages/6_🔗_Lab6_Matrix_Chain_Multiplication.py")

# --- Footer ---
st.markdown("---")
st.markdown(
    '<p class="footer-text">CS5303 — Design & Analysis of Algorithms Lab &middot; '
    'Chennai Institute of Technology &middot; Dept. of CSE</p>',
    unsafe_allow_html=True
)

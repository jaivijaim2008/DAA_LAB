import streamlit as st
import time
import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================================
# MATRIX CHAIN MULTIPLICATION
# ============================================================================

def matrix_chain_order(dims):
    """
    Matrix Chain Multiplication using DP
    dims: list of dimensions, matrix i has dims[i-1] x dims[i]
    Returns m (cost table) and s (split table)
    Time: O(n^3), Space: O(n^2)
    """
    n = len(dims) - 1
    m = [[0] * (n + 1) for _ in range(n + 1)]
    s = [[0] * (n + 1) for _ in range(n + 1)]
    
    for l in range(2, n + 1):
        for i in range(1, n - l + 2):
            j = i + l - 1
            m[i][j] = float('inf')
            for k in range(i, j):
                cost = m[i][k] + m[k + 1][j] + dims[i - 1] * dims[k] * dims[j]
                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k
    return m, s


def print_optimal_parens(s, i, j):
    """Recursively print optimal parenthesization"""
    if i == j:
        return f'A{i}'
    k = s[i][j]
    left = print_optimal_parens(s, i, k)
    right = print_optimal_parens(s, k + 1, j)
    return f'({left} x {right})'


def get_parenthesization_steps(s, i, j, depth=0):
    """Get step-by-step parenthesization breakdown"""
    steps = []
    if i == j:
        return [{'matrix': f'A{i}', 'range': (i, i), 'depth': depth, 'result': f'A{i}'}]
    
    k = s[i][j]
    left_steps = get_parenthesization_steps(s, i, k, depth + 1)
    right_steps = get_parenthesization_steps(s, k + 1, j, depth + 1)
    
    steps.extend(left_steps)
    steps.extend(right_steps)
    steps.append({
        'operation': f'Multiply A{i}..A{k} with A{k+1}..A{j}',
        'range': (i, j),
        'depth': depth,
        'result': f'({print_optimal_parens(s, i, k)} x {print_optimal_parens(s, k+1, j)})'
    })
    return steps


def matrix_chain_naive(dims):
    """Naive recursive approach for small n"""
    n = len(dims) - 1
    
    def helper(i, j):
        if i == j:
            return 0
        min_cost = float('inf')
        for k in range(i, j):
            cost = helper(i, k) + helper(k + 1, j) + dims[i - 1] * dims[k] * dims[j]
            min_cost = min(min_cost, cost)
        return min_cost
    
    return helper(1, n)


def visualize_dp_table(m, s, n):
    """Create an interactive heatmap of the DP table"""
    z = []
    text = []
    for i in range(1, n + 1):
        row = []
        text_row = []
        for j in range(1, n + 1):
            if j < i:
                row.append(None)
                text_row.append('')
            else:
                val = m[i][j]
                row.append(val if val != float('inf') else None)
                text_row.append(f'{val:,}' if val != float('inf') else '∞')
        z.append(row)
        text.append(text_row)
    
    fig = go.Figure(data=go.Heatmap(
        z=z,
        text=text,
        texttemplate='%{text}',
        textfont={"size": 14},
        x=[f'A{j}' for j in range(1, n + 1)],
        y=[f'A{i}' for i in range(1, n + 1)],
        colorscale='Viridis',
        colorbar=dict(title='Scalar Multiplications'),
        hoverongaps=False,
        hovertemplate='m[%{y}][%{x}] = %{text}<extra></extra>'
    ))
    
    fig.update_layout(
        title='DP Cost Table m[i][j]',
        xaxis_title='j (End Matrix)',
        yaxis_title='i (Start Matrix)',
        height=500,
        width=600
    )
    
    return fig


def visualize_chain(dims):
    """Visualize the matrix chain as connected rectangles"""
    n = len(dims) - 1
    fig = go.Figure()
    
    x_pos = 0
    colors = px.colors.qualitative.Set2
    
    for i in range(n):
        width = dims[i + 1] / 10
        height = dims[i] / 10
        
        fig.add_shape(
            type="rect",
            x0=x_pos, y0=0, x1=x_pos + width, y1=height,
            fillcolor=colors[i % len(colors)],
            line=dict(color='black', width=2),
            opacity=0.8
        )
        
        fig.add_annotation(
            x=x_pos + width/2, y=height/2,
            text=f"A{i+1}<br>{dims[i]}×{dims[i+1]}",
            showarrow=False,
            font=dict(size=12, color='white')
        )
        
        x_pos += width + 0.2
    
    fig.update_layout(
        title='Matrix Chain Visualization',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=250,
        plot_bgcolor='white'
    )
    
    return fig


# ============================================================================
# PAGE
# ============================================================================

st.title("🔗 Lab 6: Matrix Chain Multiplication")
st.markdown("Find the **optimal parenthesization** to minimize scalar multiplications using **Dynamic Programming**")

tab1, tab2, tab3, tab4 = st.tabs(["Interactive Demo", "DP Table Visualization", "Performance Comparison", "Algorithm Details"])

# ============================================================================
# TAB 1: INTERACTIVE DEMO
# ============================================================================

with tab1:
    st.subheader("Matrix Chain Multiplication Demo")

    st.write("### Step 1: Define Matrix Dimensions")

    dims_mode = st.radio("Input method:", ["Sample Chain", "Custom Chain", "Random Chain"], horizontal=True)

    if dims_mode == "Sample Chain":
        dims = [10, 30, 5, 60, 10]
        n = len(dims) - 1
        st.info(f"Using sample chain: {n} matrices")
        for i in range(n):
            st.write(f"  **A{i+1}**: {dims[i]} × {dims[i+1]}")
    elif dims_mode == "Custom Chain":
        st.write("Enter dimensions as comma-separated values (n+1 values for n matrices):")
        col1, col2 = st.columns([2, 1])
        with col1:
            dims_input = st.text_input(
                "Dimensions:",
                value="10, 30, 5, 60, 10",
                placeholder="e.g. 10, 30, 5, 60, 10"
            )
        with col2:
            st.write("**Format:** dims[0]×dims[1], dims[1]×dims[2], ...")
            st.write("**Example:** `10, 30, 5, 60, 10`")
            st.write("→ A1: 10×30, A2: 30×5, A3: 5×60, A4: 60×10")
        
        try:
            dims = [int(x.strip()) for x in dims_input.split(",")]
            if len(dims) < 3:
                st.error("❌ Need at least 3 dimensions (2 matrices)")
                dims = [10, 30, 5, 60, 10]
            n = len(dims) - 1
            st.success(f"✅ Chain: {n} matrices defined")
            for i in range(n):
                st.write(f"  **A{i+1}**: {dims[i]} × {dims[i+1]}")
        except ValueError:
            st.error("❌ Please enter valid integers separated by commas.")
            dims = [10, 30, 5, 60, 10]
            n = len(dims) - 1
    else:
        n_matrices = st.slider("Number of matrices:", min_value=2, max_value=10, value=4)
        min_dim = st.number_input("Min dimension:", value=1, min_value=1, max_value=100)
        max_dim = st.number_input("Max dimension:", value=100, min_value=1, max_value=1000)
        dims = [random.randint(min_dim, max_dim) for _ in range(n_matrices + 1)]
        n = len(dims) - 1
        st.info(f"Generated random chain: {n} matrices")
        for i in range(n):
            st.write(f"  **A{i+1}**: {dims[i]} × {dims[i+1]}")

    st.write("### Matrix Chain Visualization")
    st.plotly_chart(visualize_chain(dims), width='stretch')

    st.write("---")

    st.write("### Step 2: Find Optimal Solution")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("#### 📊 DP Approach")
        start_time = time.perf_counter()
        m, s = matrix_chain_order(dims)
        dp_time = (time.perf_counter() - start_time) * 1000
        optimal_cost = m[1][n]
        optimal_parens = print_optimal_parens(s, 1, n)
        st.metric("Minimum Multiplications", f"{optimal_cost:,}")
        st.metric("Time", f"{dp_time:.4f} ms")
    
    with col2:
        st.write("#### 🔢 Naive Approach (n ≤ 10)")
        if n <= 10:
            start_time = time.perf_counter()
            naive_cost = matrix_chain_naive(dims)
            naive_time = (time.perf_counter() - start_time) * 1000
            st.metric("Minimum Multiplications", f"{naive_cost:,}")
            st.metric("Time", f"{naive_time:.4f} ms")
            speedup = naive_time / dp_time if dp_time > 0 else 0
            st.metric("Speedup", f"{speedup:.0f}x")
        else:
            st.warning("Too many matrices for naive approach (n ≤ 10)")
            naive_cost = None
    
    with col3:
        st.write("#### 📈 Complexity")
        st.metric("Matrices", n)
        st.metric("DP Table Size", f"{n}×{n}")
        st.metric("Operations", f"{n**3:,}")

    st.write("---")

    st.write("### Step 3: Optimal Parenthesization")

    st.success(f"**Optimal Order:** `{optimal_parens}`")
    st.info(f"**Minimum Scalar Multiplications:** {optimal_cost:,}")

    if n <= 8:
        st.write("#### Step-by-Step Breakdown")
        steps = get_parenthesization_steps(s, 1, n)
        
        step_data = []
        for idx, step in enumerate(steps):
            if 'operation' in step:
                step_data.append({
                    'Step': idx + 1,
                    'Operation': step['operation'],
                    'Result': step['result'],
                    'Depth': step['depth']
                })
        
        if step_data:
            steps_df = pd.DataFrame(step_data)
            st.dataframe(steps_df, width='stretch', hide_index=True)

    st.write("---")

    st.write("### Step 4: DP Cost Table")

    st.write("**Cost Table m[i][j]** - Minimum multiplications to multiply matrices i through j:")
    
    table_data = []
    for i in range(1, n + 1):
        row = {'Matrix': f'A{i}'}
        for j in range(1, n + 1):
            if j < i:
                row[f'A{j}'] = '—'
            else:
                row[f'A{j}'] = f"{m[i][j]:,}" if m[i][j] != float('inf') else '∞'
        table_data.append(row)
    
    table_df = pd.DataFrame(table_data)
    st.dataframe(table_df, width='stretch', hide_index=True)

    st.write("**Split Table s[i][j]** - Optimal split point:")
    
    split_data = []
    for i in range(1, n + 1):
        row = {'Matrix': f'A{i}'}
        for j in range(1, n + 1):
            if j <= i:
                row[f'A{j}'] = '—'
            else:
                row[f'A{j}'] = f"k={s[i][j]}" if s[i][j] > 0 else '—'
        split_data.append(row)
    
    split_df = pd.DataFrame(split_data)
    st.dataframe(split_df, width='stretch', hide_index=True)

# ============================================================================
# TAB 2: DP TABLE VISUALIZATION
# ============================================================================

with tab2:
    st.subheader("DP Table Interactive Visualization")
    
    fig = visualize_dp_table(m, s, n)
    st.plotly_chart(fig, width='stretch')
    
    st.write("### How to Read the Table")
    st.markdown("""
    - **Rows (i):** Starting matrix index
    - **Columns (j):** Ending matrix index
    - **Cell m[i][j]:** Minimum scalar multiplications to compute A_i × A_i+1 × ... × A_j
    - **—:** Invalid (i > j)
    
    **Example:** m[1][4] = minimum cost to multiply A1 through A4
    """)
    
    st.write("### 3D Cost Surface")
    
    x_data = []
    y_data = []
    z_data = []
    text_data = []
    
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if j >= i:
                x_data.append(j)
                y_data.append(i)
                z_data.append(m[i][j])
                text_data.append(f"A{i}..A{j}: {m[i][j]:,}")
    
    fig_3d = go.Figure(data=[go.Scatter3d(
        x=x_data, y=y_data, z=z_data,
        mode='markers+text',
        text=[f'{z:,}' for z in z_data],
        textposition='top center',
        marker=dict(
            size=8,
            color=z_data,
            colorscale='Viridis',
            opacity=0.8
        ),
        hovertext=text_data,
        hoverinfo='text'
    )])
    
    fig_3d.update_layout(
        title='3D Cost Surface',
        scene=dict(
            xaxis_title='j (End)',
            yaxis_title='i (Start)',
            zaxis_title='Cost'
        ),
        height=500
    )
    
    st.plotly_chart(fig_3d, width='stretch')

# ============================================================================
# TAB 3: PERFORMANCE COMPARISON
# ============================================================================

with tab3:
    st.subheader("Performance Analysis")
    
    st.write("### Execution Time vs Number of Matrices")
    
    results = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    matrix_counts = list(range(2, 16))
    
    for idx, count in enumerate(matrix_counts):
        status_text.text(f"Testing chain of {count} matrices...")
        
        test_dims = [random.randint(5, 100) for _ in range(count + 1)]
        
        start = time.perf_counter()
        for _ in range(10):
            matrix_chain_order(test_dims)
        dp_time = (time.perf_counter() - start) / 10 * 1000
        
        naive_time = None
        if count <= 12:
            start = time.perf_counter()
            for _ in range(max(1, 10 - count)):
                matrix_chain_naive(test_dims)
            naive_time = (time.perf_counter() - start) / max(1, 10 - count) * 1000
        
        m_test, _ = matrix_chain_order(test_dims)
        optimal_cost = m_test[1][count]
        
        results.append({
            'Matrices': count,
            'DP Time (ms)': round(dp_time, 4),
            'Naive Time (ms)': round(naive_time, 4) if naive_time else None,
            'Optimal Cost': optimal_cost,
            'Table Size': f'{count}×{count}',
            'Operations': count ** 3
        })
        
        progress_bar.progress((idx + 1) / len(matrix_counts))
    
    status_text.empty()
    perf_df = pd.DataFrame(results)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.line(perf_df, x='Matrices', y=['DP Time (ms)'],
                      title='DP Algorithm Execution Time',
                      markers=True,
                      labels={'Matrices': 'Number of Matrices', 'value': 'Time (ms)'})
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        if 'Naive Time (ms)' in perf_df.columns and perf_df['Naive Time (ms)'].notna().any():
            fig = px.line(perf_df.dropna(subset=['Naive Time (ms)']), 
                          x='Matrices', y=['DP Time (ms)', 'Naive Time (ms)'],
                          title='DP vs Naive Execution Time',
                          markers=True,
                          labels={'Matrices': 'Number of Matrices', 'value': 'Time (ms)'})
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("Naive comparison available for n ≤ 12")
    
    st.write("### Detailed Results")
    st.dataframe(perf_df, width='stretch', hide_index=True)
    
    st.write("---")
    st.write("### Complexity Analysis")
    
    complexity_data = {
        'Metric': ['Time Complexity', 'Space Complexity', 'Subproblems', 'Time per Subproblem', 'Total Operations'],
        'DP Approach': ['O(n³)', 'O(n²)', 'O(n²)', 'O(n)', 'O(n³)'],
        'Naive Approach': ['O(2ⁿ)', 'O(n)', 'Exponential', 'O(1)', 'O(2ⁿ)']
    }
    
    complexity_df = pd.DataFrame(complexity_data)
    st.dataframe(complexity_df, width='stretch', hide_index=True)

# ============================================================================
# TAB 4: ALGORITHM DETAILS
# ============================================================================

with tab4:
    st.subheader("Algorithm Deep Dive")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Dynamic Programming Approach")
        st.markdown("""
        **Key Insight:** Matrix chain multiplication has **optimal substructure** — the optimal solution contains optimal solutions to subproblems.
        
        **Recurrence:**
        - Base case: m[i][i] = 0 (single matrix, no multiplication)
        - Recursive case: m[i][j] = min over k of:
          m[i][k] + m[k+1][j] + dims[i-1] × dims[k] × dims[j]
        
        **Steps:**
        1. Fill diagonal (single matrices): cost = 0
        2. Fill diagonals for chains of length 2, 3, ..., n
        3. For each chain length, try all possible split points
        4. Record minimum cost and split point
        
        **Time:** O(n³) — three nested loops
        **Space:** O(n²) — for cost and split tables
        """)
        
        st.code("""
def matrix_chain_order(dims):
    n = len(dims) - 1
    m = [[0] * (n + 1) for _ in range(n + 1)]
    s = [[0] * (n + 1) for _ in range(n + 1)]
    
    # l = chain length
    for l in range(2, n + 1):
        for i in range(1, n - l + 2):
            j = i + l - 1
            m[i][j] = float('inf')
            for k in range(i, j):
                cost = m[i][k] + m[k+1][j] + \\
                       dims[i-1] * dims[k] * dims[j]
                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k
    return m, s
        """, language="python")
    
    with col2:
        st.write("### Naive Recursive Approach")
        st.markdown("""
        **Strategy:** Try all possible parenthesizations recursively
        
        **Recurrence:**
        - If i == j: cost = 0 (single matrix)
        - Otherwise: try all split points k
        
        **Time:** O(2ⁿ) — exponential
        **Space:** O(n) — recursion stack
        
        **Why it's slow:**
        - Same subproblems solved repeatedly
        - No memoization
        - For n matrices, there are Catalan(n) possible parenthesizations
        """)
        
        st.code("""
def matrix_chain_naive(dims):
    def helper(i, j):
        if i == j:
            return 0
        min_cost = float('inf')
        for k in range(i, j):
            cost = helper(i, k) + \\
                   helper(k + 1, j) + \\
                   dims[i-1] * dims[k] * dims[j]
            min_cost = min(min_cost, cost)
        return min_cost
    
    return helper(1, n)
        """, language="python")
    
    st.write("---")
    st.write("### Why DP Works")
    
    st.markdown("""
    **Optimal Substructure:**
    - The optimal parenthesization of A₁...Aₙ must split at some point k
    - The left part A₁...Aₖ must be optimally parenthesized
    - The right part Aₖ₊₁...Aₙ must be optimally parenthesized
    
    **Overlapping Subproblems:**
    - The same subchain appears multiple times in recursive calls
    - DP stores results to avoid recomputation
    
    **Example:**
    For matrices A₁(10×30), A₂(30×5), A₃(5×60), A₄(60×10):
    
    Possible parenthesizations:
    1. ((A₁ × A₂) × A₃) × A₄ = 10×30×5 + 10×5×60 + 10×60×10 = 10,500
    2. (A₁ × (A₂ × A₃)) × A₄ = 30×5×60 + 10×30×60 + 10×60×10 = 33,000
    3. (A₁ × A₂) × (A₃ × A₄) = 10×30×5 + 5×60×10 + 10×5×10 = 5,000
    4. A₁ × ((A₂ × A₃) × A₄) = 30×5×60 + 30×60×10 + 10×30×10 = 30,000
    5. A₁ × (A₂ × (A₃ × A₄)) = 5×60×10 + 30×5×10 + 10×30×10 = 7,500
    
    **Optimal:** (A₁ × A₂) × (A₃ × A₄) with cost 5,000
    """)
    
    st.write("---")
    st.write("### Comparison Summary")
    
    summary_data = {
        'Aspect': ['Time Complexity', 'Space Complexity', 'Implementation', 'Best For'],
        'DP': ['O(n³)', 'O(n²)', 'Iterative', 'Large chains'],
        'Naive': ['O(2ⁿ)', 'O(n)', 'Recursive', 'Small chains']
    }
    
    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, width='stretch', hide_index=True)
    
    st.write("---")
    st.write("### Real-World Applications")
    
    st.markdown("""
    **1. Database Query Optimization**
    - Joining multiple tables: (A ⋈ B) ⋈ C vs A ⋈ (B ⋈ C)
    - Different join orders have vastly different costs
    
    **2. Matrix Computation**
    - Computer graphics transformations
    - Neural network layer computations
    - Scientific computing
    
    **3. Compiler Optimization**
    - Expression evaluation order
    - Function composition
    """)

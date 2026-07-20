import streamlit as st
import time
import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ============================================================================
# N-QUEENS BACKTRACKING ALGORITHM
# ============================================================================

def is_safe(board, row, col):
    """Check if it's safe to place a queen at board[row] = col"""
    for prev_row in range(row):
        placed = board[prev_row]
        if placed == col:  # Same column
            return False
        if abs(prev_row - row) == abs(placed - col):  # Diagonal
            return False
    return True


def solve_n_queens(n, record_steps=False):
    """
    Solve N-Queens using backtracking
    Returns list of solutions and backtrack count
    """
    board = [-1] * n
    solutions = []
    backtrack_count = [0]
    steps = [] if record_steps else None

    def backtrack(row):
        if row == n:
            solutions.append(board[:])
            if record_steps:
                steps.append({
                    'type': 'solution',
                    'board': board[:],
                    'row': row,
                    'message': f'Found solution! Queens placed at columns {board[:]}'
                })
            return
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                if record_steps:
                    steps.append({
                        'type': 'place',
                        'row': row,
                        'col': col,
                        'board': board[:],
                        'message': f'Place queen at row {row}, col {col}'
                    })
                backtrack(row + 1)
                board[row] = -1
                if record_steps:
                    steps.append({
                        'type': 'undo',
                        'row': row,
                        'col': col,
                        'board': board[:],
                        'message': f'Undo queen at row {row}, col {col}'
                    })
            backtrack_count[0] += 1

    backtrack(0)
    return solutions, backtrack_count[0], steps


def find_first_solution(n):
    """Find just the first solution (faster for large N)"""
    board = [-1] * n

    def backtrack(row):
        if row == n:
            return True
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                if backtrack(row + 1):
                    return True
                board[row] = -1
        return False

    if backtrack(0):
        return board
    return None


def create_chessboard_fig(solution, n, title="N-Queens Solution", highlight_attacks=False):
    """Create an interactive chessboard visualization with Plotly"""
    # Create checkerboard pattern
    z = []
    text = []
    
    for row in range(n):
        z_row = []
        text_row = []
        for col in range(n):
            # Checkerboard pattern
            is_light = (row + col) % 2 == 0
            z_row.append(0 if is_light else 1)
            
            # Mark queen position
            if solution and solution[row] == col:
                text_row.append('♛')
            else:
                text_row.append('')
        z.append(z_row)
        text.append(text_row)
    
    fig = go.Figure(data=go.Heatmap(
        z=z,
        text=text,
        texttemplate='%{text}',
        textfont={"size": 24 if n <= 10 else 16},
        colorscale=[[0, '#F0D9B5'], [1, '#B58863']],
        showscale=False,
        hoverongaps=False,
        hovertemplate='Row %{y}, Col %{x}<extra></extra>'
    ))
    
    # Add attack lines if requested
    if highlight_attacks and solution:
        for row1 in range(n):
            for row2 in range(row1 + 1, n):
                col1, col2 = solution[row1], solution[row2]
                if abs(row1 - row2) == abs(col1 - col2):  # Diagonal attack
                    fig.add_shape(
                        type="line",
                        x0=col1, y0=row1, x1=col2, y1=row2,
                        line=dict(color="red", width=2, dash="dash"),
                        opacity=0.7
                    )
    
    fig.update_layout(
        title=title,
        xaxis=dict(
            tickvals=list(range(n)),
            ticktext=[f'C{i}' for i in range(n)],
            side='top'
        ),
        yaxis=dict(
            tickvals=list(range(n)),
            ticktext=[f'R{i}' for i in range(n)],
            autorange='reversed'
        ),
        height=400 if n <= 10 else 300,
        width=400 if n <= 10 else 300,
        plot_bgcolor='white'
    )
    
    return fig


# ============================================================================
# KNOWN SOLUTION COUNTS
# ============================================================================

KNOWN_SOLUTIONS = {
    1: 1, 2: 0, 3: 0, 4: 2, 5: 10, 6: 4, 7: 40, 8: 92,
    9: 352, 10: 724, 11: 2680, 12: 14200
}


# ============================================================================
# PAGE
# ============================================================================

st.title("♛ Lab 7: N-Queens Problem")
st.markdown("Solve the N-Queens problem using **Backtracking** — place N queens on an N×N chessboard so no two queens attack each other")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Interactive Demo", 
    "Visualize Solutions", 
    "Backtracking Animation",
    "Performance Analysis",
    "Algorithm Details"
])

# ============================================================================
# TAB 1: INTERACTIVE DEMO
# ============================================================================

with tab1:
    st.subheader("N-Queens Interactive Demo")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("### Configuration")
        
        demo_mode = st.radio("Demo Mode:", ["Sample N Values", "Custom N"], horizontal=True)
        
        if demo_mode == "Sample N Values":
            selected_n = st.selectbox("Select board size:", [4, 5, 6, 7, 8])
        else:
            selected_n = st.slider("Board size (N):", min_value=1, max_value=12, value=8)
            if selected_n > 10:
                st.warning("⚠️ Large N may take time. Using first solution only for N > 10.")
        
        show_all = st.checkbox("Show all solutions", value=(selected_n <= 8))
        
        st.write("---")
        st.write("### Quick Stats")
        
        start_time = time.perf_counter()
        if show_all or selected_n <= 10:
            solutions, backtracks, _ = solve_n_queens(selected_n, record_steps=False)
        else:
            solutions = [find_first_solution(selected_n)] if find_first_solution(selected_n) else []
            backtracks = 0
        solve_time = (time.perf_counter() - start_time) * 1000
        
        st.metric("Solutions Found", len(solutions))
        st.metric("Backtracks", f"{backtracks:,}")
        st.metric("Time", f"{solve_time:.2f} ms")
        
        if selected_n in KNOWN_SOLUTIONS:
            expected = KNOWN_SOLUTIONS[selected_n]
            match = "✓" if len(solutions) == expected else "✗"
            st.metric("Expected Solutions", f"{expected} {match}")
    
    with col2:
        st.write("### Chessboard Visualization")
        
        if solutions:
            # Solution selector
            if len(solutions) > 1:
                sol_idx = st.selectbox(
                    f"Select solution (1-{len(solutions)}):", 
                    range(1, min(len(solutions), 100) + 1),
                    format_func=lambda x: f"Solution {x}"
                ) - 1
            else:
                sol_idx = 0
            
            selected_solution = solutions[sol_idx]
            
            # Create and display chessboard
            fig = create_chessboard_fig(
                selected_solution, 
                selected_n,
                title=f"N={selected_n} Solution #{sol_idx + 1}"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Show queen positions
            st.write("**Queen Positions:**")
            pos_df = pd.DataFrame({
                'Row': list(range(selected_n)),
                'Column': selected_solution,
                'Position': [f"({i}, {selected_solution[i]})" for i in range(selected_n)]
            })
            st.dataframe(pos_df, hide_index=True, use_container_width=True)
        else:
            st.warning(f"No solutions exist for N={selected_n}")
    
    # Solution table for small N
    if selected_n <= 8 and len(solutions) > 1:
        st.write("---")
        st.write("### All Solutions")
        
        sol_data = []
        for i, sol in enumerate(solutions, 1):
            sol_data.append({
                'Solution #': i,
                'Queen Positions': str(sol),
                'Columns': ', '.join([str(c) for c in sol])
            })
        
        sol_df = pd.DataFrame(sol_data)
        st.dataframe(sol_df, hide_index=True, use_container_width=True)

# ============================================================================
# TAB 2: VISUALIZE SOLUTIONS
# ============================================================================

with tab2:
    st.subheader("Solutions Gallery")
    
    gallery_n = st.slider("Board size for gallery:", min_value=4, max_value=10, value=6, key="gallery_n")
    
    with st.spinner(f"Finding all solutions for N={gallery_n}..."):
        solutions, _, _ = solve_n_queens(gallery_n, record_steps=False)
    
    if solutions:
        st.success(f"Found {len(solutions)} solutions for N={gallery_n}")
        
        # Display solutions in grid
        cols_per_row = 3
        for i in range(0, min(len(solutions), 12), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                sol_idx = i + j
                if sol_idx < len(solutions):
                    with col:
                        fig = create_chessboard_fig(
                            solutions[sol_idx], 
                            gallery_n,
                            title=f"Solution #{sol_idx + 1}"
                        )
                        st.plotly_chart(fig, use_container_width=True)
        
        if len(solutions) > 12:
            st.info(f"Showing first 12 of {len(solutions)} solutions")
    else:
        st.warning(f"No solutions exist for N={gallery_n}")

# ============================================================================
# TAB 3: BACKTRACKING ANIMATION
# ============================================================================

with tab3:
    st.subheader("Backtracking Visualization")
    
    anim_n = st.slider("Board size:", min_value=4, max_value=10, value=6, key="anim_n")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.write("### Backtracking Progress")
        
        if st.button("▶️ Run Backtracking", key="run_backtrack"):
            with st.spinner("Running backtracking algorithm..."):
                solutions, backtracks, steps = solve_n_queens(anim_n, record_steps=True)
            
            st.session_state['anim_steps'] = steps
            st.session_state['anim_solutions'] = solutions
            st.session_state['anim_backtracks'] = backtracks
            
            st.success(f"Complete! Found {len(solutions)} solutions")
        
        if 'anim_steps' in st.session_state:
            steps = st.session_state['anim_steps']
            solutions = st.session_state['anim_solutions']
            
            # Step counter
            total_steps = len(steps)
            step_idx = st.slider(
                "Step:", 
                min_value=0, 
                max_value=total_steps - 1, 
                value=0,
                key="step_slider"
            )
            
            # Step type statistics
            place_count = sum(1 for s in steps if s['type'] == 'place')
            undo_count = sum(1 for s in steps if s['type'] == 'undo')
            solution_count = sum(1 for s in steps if s['type'] == 'solution')
            
            st.metric("Placements", place_count)
            st.metric("Undos (Backtracks)", undo_count)
            st.metric("Solutions Found", solution_count)
            
            # Current step info
            if step_idx < total_steps:
                current_step = steps[step_idx]
                st.write(f"**Step {step_idx + 1}:** {current_step['message']}")
    
    with col2:
        st.write("### Board State")
        
        if 'anim_steps' in st.session_state and 'step_slider' in st.session_state:
            steps = st.session_state['anim_steps']
            step_idx = st.session_state.get('step_slider', 0)
            
            if step_idx < len(steps):
                current_board = steps[step_idx]['board']
                
                # Create board visualization
                fig = create_chessboard_fig(
                    current_board, 
                    anim_n,
                    title=f"Step {step_idx + 1} of {len(steps)}"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Show step history
                st.write("**Recent Steps:**")
                recent_steps = steps[max(0, step_idx-4):step_idx+1]
                for i, s in enumerate(recent_steps):
                    icon = "🟢" if s['type'] == 'place' else "🔴" if s['type'] == 'undo' else "🔵"
                    st.write(f"{icon} {s['message']}")
            else:
                st.info("Click 'Run Backtracking' to start visualization")
        else:
            st.info("Click 'Run Backtracking' to start visualization")
    
    # Backtracking tree visualization
    if 'anim_steps' in st.session_state:
        st.write("---")
        st.write("### Backtracking Step Distribution")
        
        steps = st.session_state['anim_steps']
        
        # Count step types
        type_counts = {}
        for s in steps:
            t = s['type']
            type_counts[t] = type_counts.get(t, 0) + 1
        
        fig = go.Figure(data=[go.Pie(
            labels=['Place Queen', 'Undo (Backtrack)', 'Solution Found'],
            values=[type_counts.get('place', 0), type_counts.get('undo', 0), type_counts.get('solution', 0)],
            marker=dict(colors=['#4CAF50', '#FF5722', '#2196F3']),
            hole=0.3
        )])
        
        fig.update_layout(
            title='Step Type Distribution',
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 4: PERFORMANCE ANALYSIS
# ============================================================================

with tab4:
    st.subheader("Performance Analysis")
    
    st.write("### Execution Time vs Board Size")
    
    max_n = st.slider("Maximum N to test:", min_value=4, max_value=14, value=10)
    
    if st.button("Run Benchmark"):
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for n in range(1, max_n + 1):
            status_text.text(f"Testing N={n}...")
            
            start = time.perf_counter()
            if n <= 12:
                solutions, backtracks, _ = solve_n_queens(n, record_steps=False)
            else:
                sol = find_first_solution(n)
                solutions = [sol] if sol else []
                backtracks = 0
            elapsed = (time.perf_counter() - start) * 1000
            
            results.append({
                'N': n,
                'Solutions': len(solutions),
                'Backtracks': backtracks,
                'Time (ms)': round(elapsed, 2),
                'Time (s)': round(elapsed / 1000, 4)
            })
            
            progress_bar.progress(n / max_n)
        
        status_text.empty()
        perf_df = pd.DataFrame(results)
        
        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(perf_df, x='N', y='Time (ms)', 
                         title='Execution Time vs Board Size',
                         markers=True)
            fig.update_layout(xaxis_title='N (Board Size)', yaxis_title='Time (ms)')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(perf_df, x='N', y='Backtracks',
                         title='Backtracks vs Board Size',
                         markers=True,
                         log_y=True)
            fig.update_layout(xaxis_title='N (Board Size)', yaxis_title='Backtracks (log scale)')
            st.plotly_chart(fig, use_container_width=True)
        
        # Results table
        st.write("### Detailed Results")
        st.dataframe(perf_df, hide_index=True, use_container_width=True)
        
        # Solution counts
        st.write("### Solution Counts")
        
        sol_data = []
        for row in results:
            n = row['N']
            expected = KNOWN_SOLUTIONS.get(n, 'Unknown')
            match = "✓" if row['Solutions'] == expected else ("N/A" if n > 12 else "✗")
            sol_data.append({
                'N': n,
                'Solutions': row['Solutions'],
                'Expected': expected if isinstance(expected, int) else 'N/A',
                'Match': match
            })
        
        sol_df = pd.DataFrame(sol_data)
        st.dataframe(sol_df, hide_index=True, use_container_width=True)

# ============================================================================
# TAB 5: ALGORITHM DETAILS
# ============================================================================

with tab5:
    st.subheader("Algorithm Deep Dive")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Backtracking Approach")
        st.markdown("""
        **Key Insight:** Place queens row by row, and whenever a conflict is found, backtrack to the previous row and try the next column.
        
        **Algorithm:**
        1. Start with an empty board
        2. Try placing a queen in each column of the current row
        3. Check if the position is safe (no conflicts with previously placed queens)
        4. If safe, place the queen and move to the next row
        5. If no safe position exists, backtrack to the previous row
        6. If all queens are placed, record the solution
        
        **Safety Check:**
        - No two queens in the same column
        - No two queens on the same diagonal
        - (Row conflict impossible since we place one queen per row)
        
        **Time Complexity:** O(N!) - In the worst case, we try all permutations
        **Space Complexity:** O(N) - For the board array and recursion stack
        """)
        
        st.code("""
def is_safe(board, row, col):
    for prev_row in range(row):
        placed = board[prev_row]
        # Same column
        if placed == col:
            return False
        # Diagonal
        if abs(prev_row - row) == abs(placed - col):
            return False
    return True

def solve_n_queens(n):
    board = [-1] * n
    solutions = []
    
    def backtrack(row):
        if row == n:
            solutions.append(board[:])
            return
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(row + 1)
                board[row] = -1  # Undo
    
    backtrack(0)
    return solutions
        """, language="python")
    
    with col2:
        st.write("### Why Backtracking Works")
        st.markdown("""
        **Principle:** 
        - Explore all possibilities systematically
        - Prune branches that cannot lead to valid solutions early
        
        **Optimization:**
        - We only check against queens in previous rows (since we haven't placed queens in future rows)
        - Each row has exactly one queen (reduces search space)
        
        **Complexity Analysis:**
        - For N=8: 92 solutions out of 4^8 ≈ 65,536 possible placements
        - Backtracking significantly reduces the search space
        
        **Comparison with Brute Force:**
        | Approach | Time | Space |
        |----------|------|-------|
        | Brute Force | O(N^(N²)) | O(N²) |
        | Backtracking | O(N!) | O(N) |
        | DP (bitmask) | O(N × 2^N) | O(2^N) |
        """)
        
        st.write("### Solution Counts (OEIS A000170)")
        
        sol_table = pd.DataFrame({
            'N': list(KNOWN_SOLUTIONS.keys()),
            'Solutions': list(KNOWN_SOLUTIONS.values())
        })
        st.dataframe(sol_table, hide_index=True, use_container_width=True)
    
    st.write("---")
    st.write("### Real-World Applications")
    
    st.markdown("""
    **1. Constraint Satisfaction Problems (CSP)**
    - Scheduling problems
    - Resource allocation
    - Puzzle solving
    
    **2. Circuit Design**
    - Placing components to avoid conflicts
    - VLSI design
    
    **3. Game Playing**
    - Chess puzzle solving
    - AI game engines
    
    **4. Optimization Problems**
    - When you need to find all valid configurations
    - Testing and verification
    """)
    
    st.write("---")
    st.write("### Comparison with Other Approaches")
    
    comparison_data = {
        'Approach': ['Backtracking', 'Bitmask DP', 'Warnsdorff\'s Rule', 'Genetic Algorithm'],
        'Time': ['O(N!)', 'O(N × 2^N)', 'O(N²)', 'Varies'],
        'Space': ['O(N)', 'O(2^N)', 'O(N²)', 'O(P × N)'],
        'Optimal': ['Yes', 'Yes', 'No', 'Heuristic'],
        'All Solutions': ['Yes', 'Yes', 'No', 'No']
    }
    
    comp_df = pd.DataFrame(comparison_data)
    st.dataframe(comp_df, hide_index=True, use_container_width=True)

import streamlit as st
import time
import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import heapq
import math

# ============================================================================
# UNION-FIND DATA STRUCTURE
# ============================================================================

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


# ============================================================================
# KRUSKAL'S ALGORITHM
# ============================================================================

def kruskal(n, edges):
    """Kruskal's MST Algorithm - O(E log E)"""
    edges_sorted = sorted(edges, key=lambda e: e[0])
    uf = UnionFind(n)
    mst = []
    cost = 0
    steps = []

    for w, u, v in edges_sorted:
        if uf.union(u, v):
            mst.append((u, v, w))
            cost += w
            steps.append((u, v, w, cost, True))
        else:
            steps.append((u, v, w, cost, False))
        if len(mst) == n - 1:
            break

    return mst, cost, steps


# ============================================================================
# PRIM'S ALGORITHM
# ============================================================================

def prim(n, adj, start=0):
    """Prim's MST Algorithm - O(E log V)"""
    INF = float('inf')
    key = [INF] * n
    parent = [-1] * n
    inMST = [False] * n
    key[start] = 0
    pq = [(0, start)]
    mst = []
    cost = 0
    steps = []

    while pq:
        w, u = heapq.heappop(pq)
        if inMST[u]:
            continue
        inMST[u] = True
        if parent[u] != -1:
            mst.append((parent[u], u, w))
            cost += w
            steps.append((parent[u], u, w, cost, True))

        for v, wt in adj.get(u, []):
            if not inMST[v] and wt < key[v]:
                key[v] = wt
                parent[v] = u
                heapq.heappush(pq, (wt, v))

    return mst, cost, steps


# ============================================================================
# GRAPH UTILITIES
# ============================================================================

def build_adjacency_list(n, edges):
    """Build adjacency list from edge list"""
    adj = {}
    for w, u, v in edges:
        adj.setdefault(u, []).append((v, w))
        adj.setdefault(v, []).append((u, w))
    return adj


def create_graph_fig(n, edges, mst_edges=None, title="Graph"):
    """Create a visual representation of the graph using Plotly"""
    pos = {}
    for i in range(n):
        angle = 2 * math.pi * i / n
        pos[i] = (math.cos(angle), math.sin(angle))

    edge_x, edge_y = [], []
    for w, u, v in edges:
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    mst_edge_x, mst_edge_y = [], []
    if mst_edges:
        for u, v, w in mst_edges:
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            mst_edge_x.extend([x0, x1, None])
            mst_edge_y.extend([y0, y1, None])

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        showlegend=False
    ))

    if mst_edge_x:
        fig.add_trace(go.Scatter(
            x=mst_edge_x, y=mst_edge_y,
            mode='lines',
            line=dict(width=3, color='#00CC96'),
            hoverinfo='none',
            name='MST Edges'
        ))

    edge_label_x, edge_label_y, edge_label_text = [], [], []
    for w, u, v in edges:
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        dx, dy = y1 - y0, -(x1 - x0)
        length = math.sqrt(dx * dx + dy * dy) or 1
        mx += dx / length * 0.1
        my += dy / length * 0.1
        edge_label_x.append(mx)
        edge_label_y.append(my)
        edge_label_text.append(str(w))

    fig.add_trace(go.Scatter(
        x=edge_label_x, y=edge_label_y,
        mode='text',
        text=edge_label_text,
        textfont=dict(size=10, color='#555'),
        hoverinfo='none',
        showlegend=False
    ))

    node_x = [pos[i][0] for i in range(n)]
    node_y = [pos[i][1] for i in range(n)]

    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        marker=dict(size=30, color='#636EFA', line=dict(width=2, color='white')),
        text=[str(i) for i in range(n)],
        textposition='middle center',
        textfont=dict(size=14, color='white', family='Arial Black'),
        hoverinfo='text',
        name='Nodes'
    ))

    fig.update_layout(
        title=title,
        showlegend=True,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='white',
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig


def create_step_graph_fig(n, edges, steps, current_step, title="Step-by-Step"):
    """Create a graph visualization showing the state at a specific algorithm step.

    Edge states:
    - pending (not yet considered): light gray, thin
    - considering (current step): orange/yellow, thick, dashed
    - accepted (in MST so far): green, thick
    - rejected (considered but not added): red, dashed
    """
    pos = {}
    for i in range(n):
        angle = 2 * math.pi * i / n
        pos[i] = (math.cos(angle), math.sin(angle))

    # Categorize edges by state at current_step
    accepted_edges = set()   # (min(u,v), max(u,v)) -> True
    rejected_edges = set()   # (min(u,v), max(u,v)) -> True
    current_edge = None      # (u, v, w)

    for i in range(min(current_step + 1, len(steps))):
        u, v, w, cost, accepted = steps[i]
        edge_key = (min(u, v), max(u, v))
        if i == current_step:
            current_edge = (u, v, w, accepted)
        elif accepted:
            accepted_edges.add(edge_key)
        else:
            rejected_edges.add(edge_key)

    fig = go.Figure()

    # --- Draw pending edges (not yet processed) ---
    pending_x, pending_y = [], []
    for w, u, v in edges:
        ek = (min(u, v), max(u, v))
        if ek not in accepted_edges and ek not in rejected_edges:
            if current_edge and (min(current_edge[0], current_edge[1]), max(current_edge[0], current_edge[1])) == ek:
                continue  # will draw as current
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            pending_x.extend([x0, x1, None])
            pending_y.extend([y0, y1, None])

    if pending_x:
        fig.add_trace(go.Scatter(
            x=pending_x, y=pending_y,
            mode='lines',
            line=dict(width=1, color='#d0d0d0'),
            hoverinfo='none',
            showlegend=False,
            name='Pending'
        ))

    # --- Draw rejected edges ---
    rej_x, rej_y = [], []
    for w, u, v in edges:
        ek = (min(u, v), max(u, v))
        if ek in rejected_edges:
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            rej_x.extend([x0, x1, None])
            rej_y.extend([y0, y1, None])

    if rej_x:
        fig.add_trace(go.Scatter(
            x=rej_x, y=rej_y,
            mode='lines',
            line=dict(width=2, color='#EF553B', dash='dash'),
            hoverinfo='none',
            showlegend=False,
            name='Rejected (cycle)'
        ))

    # --- Draw accepted edges ---
    acc_x, acc_y = [], []
    for w, u, v in edges:
        ek = (min(u, v), max(u, v))
        if ek in accepted_edges:
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            acc_x.extend([x0, x1, None])
            acc_y.extend([y0, y1, None])

    if acc_x:
        fig.add_trace(go.Scatter(
            x=acc_x, y=acc_y,
            mode='lines',
            line=dict(width=3, color='#00CC96'),
            hoverinfo='none',
            showlegend=False,
            name='In MST'
        ))

    # --- Draw current edge (being considered) ---
    if current_edge:
        cu, cv, cw, c_accepted = current_edge
        cx0, cy0 = pos[cu]
        cx1, cy1 = pos[cv]
        cur_color = '#00CC96' if c_accepted else '#EF553B'
        fig.add_trace(go.Scatter(
            x=[cx0, cx1, None], y=[cy0, cy1, None],
            mode='lines',
            line=dict(width=4, color=cur_color, dash='dot'),
            hoverinfo='none',
            showlegend=False,
            name='Considering'
        ))

    # --- Edge weight labels ---
    label_x, label_y, label_text, label_colors = [], [], [], []
    for w, u, v in edges:
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        dx, dy = y1 - y0, -(x1 - x0)
        length = math.sqrt(dx * dx + dy * dy) or 1
        mx += dx / length * 0.12
        my += dy / length * 0.12
        label_x.append(mx)
        label_y.append(my)
        label_text.append(str(w))
        ek = (min(u, v), max(u, v))
        if current_edge and (min(current_edge[0], current_edge[1]), max(current_edge[0], current_edge[1])) == ek:
            label_colors.append('#000')
        elif ek in accepted_edges:
            label_colors.append('#00CC96')
        elif ek in rejected_edges:
            label_colors.append('#EF553B')
        else:
            label_colors.append('#999')

    fig.add_trace(go.Scatter(
        x=label_x, y=label_y,
        mode='text',
        text=label_text,
        textfont=dict(size=11, color=label_colors, family='Arial Black'),
        hoverinfo='none',
        showlegend=False
    ))

    # --- Nodes ---
    node_x = [pos[i][0] for i in range(n)]
    node_y = [pos[i][1] for i in range(n)]
    node_colors = ['#636EFA'] * n
    if current_edge:
        cu, cv = current_edge[0], current_edge[1]
        node_colors[cu] = '#FFA15A'
        node_colors[cv] = '#FFA15A'

    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        marker=dict(size=32, color=node_colors, line=dict(width=2, color='white')),
        text=[str(i) for i in range(n)],
        textposition='middle center',
        textfont=dict(size=14, color='white', family='Arial Black'),
        hoverinfo='text',
        name='Nodes'
    ))

    # --- Legend annotations ---
    legend_items = [
        ('Pending', '#d0d0d0', 'solid'),
        ('In MST', '#00CC96', 'solid'),
        ('Rejected', '#EF553B', 'dash'),
        ('Considering', '#FFA15A', 'dot'),
    ]
    annotations = []
    for i, (label, color, dash) in enumerate(legend_items):
        annotations.append(dict(
            x=0.0, y=1.02 - i * 0.06,
            xref='paper', yref='paper',
            xanchor='left', yanchor='bottom',
            text=f'<b style="color:{color}">━━</b> {label}',
            showarrow=False,
            font=dict(size=11)
        ))

    fig.update_layout(
        title=title,
        showlegend=True,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='white',
        height=450,
        margin=dict(l=20, r=20, t=50, b=20),
        annotations=annotations
    )

    return fig


# ============================================================================
# DEFAULT GRAPH
# ============================================================================

DEFAULT_N = 7
DEFAULT_EDGES = [
    (7, 0, 1), (5, 0, 3), (8, 1, 2), (9, 1, 3),
    (7, 1, 4), (5, 2, 4), (15, 3, 4), (6, 3, 5),
    (8, 4, 5), (9, 4, 6), (11, 5, 6)
]


# ============================================================================
# PAGE
# ============================================================================

st.title("🌳 Lab 3: Minimum Spanning Tree Analysis")
st.markdown("Compare **Kruskal's** and **Prim's** algorithms for finding Minimum Spanning Trees")

tab1, tab2, tab3 = st.tabs(["Interactive Demo", "Performance Comparison", "Algorithm Details"])

# ============================================================================
# TAB 1: INTERACTIVE DEMO
# ============================================================================

with tab1:
    st.subheader("MST Demo")

    st.write("### Step 1: Define the Graph")

    graph_mode = st.radio("Graph source:", ["Sample Graph (7 nodes)", "Custom Graph"], horizontal=True)

    if graph_mode == "Sample Graph (7 nodes)":
        n = DEFAULT_N
        edges = DEFAULT_EDGES
        st.info(f"Using sample graph with **{n} nodes** and **{len(edges)} edges**")
    else:
        col_a, col_b = st.columns(2)
        with col_a:
            n = st.number_input("Number of nodes:", min_value=2, max_value=20, value=5)
        with col_b:
            raw_edges = st.text_area(
                "Enter edges (one per line, format: weight,u,v):",
                value="4,0,1\n8,0,2\n6,1,2\n5,1,3\n3,2,3\n9,2,4\n7,3,4",
                height=150
            )

        edges = []
        try:
            for line in raw_edges.strip().split("\n"):
                line = line.strip()
                if line:
                    parts = line.split(",")
                    w, u, v = int(parts[0]), int(parts[1]), int(parts[2])
                    edges.append((w, u, v))
            st.success(f"✅ Loaded **{len(edges)}** edges")
        except Exception as e:
            st.error(f"❌ Error parsing edges: {e}")
            edges = DEFAULT_EDGES
            n = DEFAULT_N

    st.write("---")

    st.write("### Step 2: Run MST Algorithms")

    adj = build_adjacency_list(n, edges)

    col1, col2 = st.columns(2)

    with col1:
        st.write("#### 🔵 Kruskal's Algorithm")
        k_mst, k_cost, k_steps = kruskal(n, edges[:])

        if len(k_mst) == n - 1:
            st.success(f"✅ MST found! **Total Cost: {k_cost}**")
        elif len(k_mst) > 0:
            st.warning(f"⚠️ Partial MST ({len(k_mst)} edges). Graph may be disconnected.")
        else:
            st.error("❌ No MST found")

        for u, v, w in k_mst:
            st.write(f"  Edge ({u} — {v}) Weight: **{w}**")

        st.metric("Total MST Cost", k_cost)

    with col2:
        st.write("#### 🟠 Prim's Algorithm")
        p_mst, p_cost, p_steps = prim(n, adj)

        if len(p_mst) == n - 1:
            st.success(f"✅ MST found! **Total Cost: {p_cost}**")
        elif len(p_mst) > 0:
            st.warning(f"⚠️ Partial MST ({len(p_mst)} edges). Graph may be disconnected.")
        else:
            st.error("❌ No MST found")

        for u, v, w in p_mst:
            st.write(f"  Edge ({u} — {v}) Weight: **{w}**")

        st.metric("Total MST Cost", p_cost)

    st.write("---")

    st.write("### Step 3: Visualize")

    viz_col1, viz_col2 = st.columns(2)

    with viz_col1:
        fig_k = create_graph_fig(n, edges, k_mst, title="Kruskal's MST")
        st.plotly_chart(fig_k, width='stretch')

    with viz_col2:
        fig_p = create_graph_fig(n, edges, p_mst, title="Prim's MST")
        st.plotly_chart(fig_p, width='stretch')

    # ========================================================================
    # STEP-BY-STEP ANIMATION
    # ========================================================================
    st.write("---")
    st.write("### Step-by-Step Animation")
    st.markdown("Drag the slider to walk through each step of the algorithm. **Green** = accepted into MST, **Red** = rejected (creates cycle), **Orange** = currently being considered.")

    algo_choice = st.radio(
        "Choose algorithm:",
        ["Kruskal's", "Prim's"],
        horizontal=True,
        key="step_algo"
    )

    if algo_choice == "Kruskal's":
        chosen_steps = k_steps
        chosen_mst = k_mst
    else:
        chosen_steps = p_steps
        chosen_mst = p_mst

    total_steps = len(chosen_steps)

    if total_steps > 0:
        step = st.slider(
            "Current step",
            min_value=0,
            max_value=total_steps - 1,
            value=0,
            format="Step %d / " + str(total_steps - 1),
            key="step_slider"
        )

        # Auto-play controls
        play_col1, play_col2, play_col3 = st.columns([1, 1, 4])
        with play_col1:
            if st.button("⏮ First", key="btn_first"):
                st.session_state.step_slider = 0
                st.rerun()
        with play_col2:
            if st.button("⏭ Last", key="btn_last"):
                st.session_state.step_slider = total_steps - 1
                st.rerun()

        # Step info
        u, v, w, cost_so_far, accepted = chosen_steps[step]

        info_col1, info_col2 = st.columns([2, 1])

        with info_col1:
            step_fig = create_step_graph_fig(n, edges, chosen_steps, step, title=f"{algo_choice} — Step {step + 1} of {total_steps}")
            st.plotly_chart(step_fig, width='stretch')

        with info_col2:
            st.write("#### Step Details")
            if accepted:
                st.success(f"✅ **Accepted** edge ({u} — {v}) with weight **{w}**")
                st.write(f"This edge connects two different components — no cycle created.")
            else:
                st.error(f"❌ **Rejected** edge ({u} — {v}) with weight **{w}**")
                st.write(f"Both endpoints are already in the same component — adding it would create a cycle.")

            st.metric("Running MST Cost", cost_so_far)
            edges_in_mst = sum(1 for s in chosen_steps[:step + 1] if s[4])
            st.metric("Edges in MST", f"{edges_in_mst} / {n - 1}")
            edges_rejected = (step + 1) - edges_in_mst
            st.metric("Edges Rejected", edges_rejected)

            st.write("---")
            st.write("#### Legend")
            st.markdown(
                '<span style="color:#d0d0d0">━━</span> Pending (not yet considered)<br>'
                '<span style="color:#00CC96">━━</span> <b>In MST</b> (accepted)<br>'
                '<span style="color:#EF553B">╌╌</span> Rejected (cycle)<br>'
                '<span style="color:#FFA15A">┈┈</span> Currently considering',
                unsafe_allow_html=True
            )
    else:
        st.info("No steps to animate.")

    st.write("---")
    st.write("### Cost Comparison")

    comp_df = pd.DataFrame({
        'Algorithm': ['Kruskal\'s', 'Prim\'s'],
        'MST Cost': [k_cost, p_cost],
        'Edges Selected': [len(k_mst), len(p_mst)],
        'Edges Considered': [len(k_steps), len(p_steps)]
    })

    fig = px.bar(comp_df, x='Algorithm', y='MST Cost',
                 color='Algorithm',
                 title='Total MST Cost Comparison',
                 labels={'MST Cost': 'Total Weight'},
                 text='MST Cost')
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, width='stretch')

    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(comp_df, width='stretch', hide_index=True)

    with col2:
        if k_cost == p_cost:
            st.success(f"✅ Both algorithms produce the same MST cost: **{k_cost}**")
        else:
            st.warning(f"⚠️ Different costs! Kruskal: {k_cost}, Prim: {p_cost}")

# ============================================================================
# TAB 2: PERFORMANCE COMPARISON
# ============================================================================

with tab2:
    st.subheader("Performance Analysis (varying graph sizes)")

    sizes = [10, 50, 100, 500, 1000]
    results = []

    progress_bar = st.progress(0)
    status_text = st.empty()

    for idx, size in enumerate(sizes):
        status_text.text(f"Testing graph with {size} nodes...")

        test_edges = []
        nodes = list(range(size))
        random.shuffle(nodes)
        for i in range(size - 1):
            w = random.randint(1, 100)
            test_edges.append((w, nodes[i], nodes[i + 1]))
        extra = size * 2
        for _ in range(extra):
            u, v = random.sample(range(size), 2)
            w = random.randint(1, 100)
            test_edges.append((w, u, v))

        test_adj = build_adjacency_list(size, test_edges)

        start = time.perf_counter()
        for _ in range(10):
            kruskal(size, test_edges[:])
        k_time = (time.perf_counter() - start) / 10 * 1000

        start = time.perf_counter()
        for _ in range(10):
            prim(size, test_adj)
        p_time = (time.perf_counter() - start) / 10 * 1000

        results.append({
            'Nodes': size,
            'Edges': len(test_edges),
            'Kruskal (ms)': round(k_time, 4),
            'Prim (ms)': round(p_time, 4)
        })

        progress_bar.progress((idx + 1) / len(sizes))

    status_text.empty()
    df = pd.DataFrame(results)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.line(df, x='Nodes', y=['Kruskal (ms)', 'Prim (ms)'],
                      title='Execution Time vs Graph Size',
                      markers=True,
                      labels={'Nodes': 'Number of Nodes', 'value': 'Time (ms)'})
        st.plotly_chart(fig, width='stretch')

    with col2:
        st.write("### Results Table")
        st.dataframe(df, width='stretch')

        st.write("---")
        st.write("### Summary")
        avg_k = df['Kruskal (ms)'].mean()
        avg_p = df['Prim (ms)'].mean()
        faster = "Kruskal's" if avg_k < avg_p else "Prim's"
        st.write(f"✅ **Faster on average:** **{faster}**")

        st.write("---")
        st.write("### Algorithm Complexity")
        st.markdown("""
        - **Kruskal's:** O(E log E) — sorts all edges, uses Union-Find
        - **Prim's:** O(E log V) — priority queue with decrease-key

        **When Kruskal's is better:** Sparse graphs, edge-list representation
        **When Prim's is better:** Dense graphs, adjacency matrix representation
        """)

# ============================================================================
# TAB 3: ALGORITHM DETAILS
# ============================================================================

with tab3:
    st.subheader("Algorithm Deep Dive")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Kruskal's Algorithm")
        st.markdown("""
        **Strategy:** Greedy — process edges in increasing weight order

        **Steps:**
        1. Sort all edges by weight
        2. For each edge (u, v):
           - If u and v are in different components → add to MST
           - Otherwise → skip (would create cycle)
        3. Stop when MST has (V-1) edges

        **Data Structure:** Union-Find (Disjoint Set Union)
        - `find(x)`: Find root of x (with path compression)
        - `union(x, y)`: Merge sets containing x and y (by rank)

        **Time Complexity:** O(E log E) ≈ O(E log V)
        - Dominated by sorting step
        - Union-Find operations are nearly O(1) amortized
        """)

        st.code("""
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry: return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True
        """, language="python")

    with col2:
        st.write("### Prim's Algorithm")
        st.markdown("""
        **Strategy:** Greedy — grow MST from a starting vertex

        **Steps:**
        1. Start with any vertex (key = 0, others = ∞)
        2. Extract minimum key vertex u from priority queue
        3. For each neighbor v of u:
           - If v not in MST and weight(u,v) < key[v]:
             - Update key[v] = weight(u,v)
             - Set parent[v] = u
        4. Repeat until all vertices are in MST

        **Data Structure:** Min-Heap (Priority Queue)
        - Extract min: O(log V)
        - Decrease key: O(log V)

        **Time Complexity:** O(E log V)
        - Each edge extracted at most once
        - Each vertex added to heap at most once
        """)

        st.code("""
def prim(n, adj, start=0):
    INF = float('inf')
    key = [INF] * n
    parent = [-1] * n
    inMST = [False] * n
    key[start] = 0
    pq = [(0, start)]
    mst, cost = [], 0

    while pq:
        w, u = heapq.heappop(pq)
        if inMST[u]: continue
        inMST[u] = True
        if parent[u] != -1:
            mst.append((parent[u], u, w))
            cost += w
        for v, wt in adj.get(u, []):
            if not inMST[v] and wt < key[v]:
                key[v] = wt
                parent[v] = u
                heapq.heappush(pq, (wt, v))
    return mst, cost
        """, language="python")

    st.write("---")
    st.write("### When to Use Which?")

    comparison_data = {
        'Criterion': ['Sparse graphs', 'Dense graphs', 'Edge list input', 'Adjacency list input',
                      'Implementation simplicity', 'Online edges', 'Time Complexity'],
        'Kruskal\'s': ['✅ Excellent', '⚠️ Okay', '✅ Excellent', '⚠️ Okay', '✅ Simple', '❌ No', 'O(E log E)'],
        'Prim\'s': ['⚠️ Okay', '✅ Excellent', '⚠️ Okay', '✅ Excellent', '⚠️ Moderate', '✅ Yes', 'O(E log V)']
    }

    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, width='stretch', hide_index=True)

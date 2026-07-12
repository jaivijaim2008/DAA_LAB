import streamlit as st
import time
import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import heapq
import math

# ============================================================================
# DIJKSTRA'S ALGORITHM
# ============================================================================

def dijkstra(graph, source):
    """
    Dijkstra's Algorithm using Min-Heap
    Time: O((V + E) log V), Space: O(V)
    graph: dict {u: [(v, weight), ...]}, 0-indexed
    """
    n = len(graph)
    dist = [float('inf')] * n
    prev = [None] * n
    dist[source] = 0
    pq = [(0, source)]
    visited = set()
    steps = []

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        steps.append({
            'vertex': u,
            'distance': d,
            'relaxed': []
        })

        for v, w in graph.get(u, []):
            if dist[u] + w < dist[v]:
                old_dist = dist[v]
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))
                steps[-1]['relaxed'].append({
                    'neighbor': v,
                    'weight': w,
                    'new_dist': dist[v],
                    'old_dist': old_dist
                })

    return dist, prev, steps


def reconstruct_path(prev, source, target):
    """Reconstruct the shortest path from source to target"""
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()
    if path[0] == source:
        return path
    return []


def build_directed_graph(n, edges):
    """Build adjacency list from edge list for directed graph"""
    graph = {i: [] for i in range(n)}
    for u, v, w in edges:
        graph[u].append((v, w))
    return graph


def create_graph_fig(n, edges, shortest_paths=None, distances=None, title="Graph"):
    """Create a visual representation of the graph using Plotly"""
    pos = {}
    for i in range(n):
        angle = 2 * math.pi * i / n - math.pi / 2
        pos[i] = (math.cos(angle), math.sin(angle))

    fig = go.Figure()

    # Draw all edges
    edge_x, edge_y = [], []
    for u, v, w in edges:
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        mode='lines',
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        showlegend=False,
        name='All Edges'
    ))

    # Highlight shortest path edges
    if shortest_paths:
        path_edge_x, path_edge_y = [], []
        for path in shortest_paths:
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                x0, y0 = pos[u]
                x1, y1 = pos[v]
                path_edge_x.extend([x0, x1, None])
                path_edge_y.extend([y0, y1, None])

        if path_edge_x:
            fig.add_trace(go.Scatter(
                x=path_edge_x, y=path_edge_y,
                mode='lines',
                line=dict(width=4, color='#00CC96'),
                hoverinfo='none',
                name='Shortest Paths'
            ))

    # Edge weight labels
    edge_label_x, edge_label_y, edge_label_text = [], [], []
    for u, v, w in edges:
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        dx, dy = y1 - y0, -(x1 - x0)
        length = math.sqrt(dx * dx + dy * dy) or 1
        mx += dx / length * 0.12
        my += dy / length * 0.12
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

    # Nodes
    node_x = [pos[i][0] for i in range(n)]
    node_y = [pos[i][1] for i in range(n)]
    node_text = [str(i) for i in range(n)]
    node_hover = []
    for i in range(n):
        d = distances[i] if distances and distances[i] != float('inf') else 'INF'
        node_hover.append(f"Vertex {i}<br>Distance: {d}")

    node_colors = ['#636EFA'] * n
    if distances:
        for i in range(n):
            if distances[i] == 0:
                node_colors[i] = '#00CC96'
            elif distances[i] != float('inf'):
                node_colors[i] = '#FFA15A'

    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        marker=dict(size=40, color=node_colors, line=dict(width=2, color='white')),
        text=node_text,
        textposition='middle center',
        textfont=dict(size=14, color='white', family='Arial Black'),
        hovertext=node_hover,
        hoverinfo='text',
        name='Vertices'
    ))

    # Distance labels below nodes
    if distances:
        dist_x, dist_y, dist_text = [], [], []
        for i in range(n):
            d = distances[i] if distances[i] != float('inf') else '∞'
            dist_x.append(pos[i][0])
            dist_y.append(pos[i][1] - 0.18)
            dist_text.append(f"d={d}")

        fig.add_trace(go.Scatter(
            x=dist_x, y=dist_y,
            mode='text',
            text=dist_text,
            textfont=dict(size=9, color='#333'),
            hoverinfo='none',
            showlegend=False
        ))

    fig.update_layout(
        title=title,
        showlegend=True,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='white',
        height=450,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    return fig


# ============================================================================
# DEFAULT GRAPH (from lab manual)
# ============================================================================

DEFAULT_N = 6
DEFAULT_EDGES = [
    (0, 1, 4), (0, 2, 1),
    (1, 3, 1),
    (2, 1, 2), (2, 3, 5),
    (3, 4, 3),
    (4, 5, 2)
]


# ============================================================================
# PAGE
# ============================================================================

st.title("📐 Lab 4: Single Source Shortest Path (Dijkstra's)")
st.markdown("Find shortest paths from a source vertex to all other vertices in a **weighted directed graph**")

tab1, tab2, tab3 = st.tabs(["Interactive Demo", "Performance Comparison", "Algorithm Details"])

# ============================================================================
# TAB 1: INTERACTIVE DEMO
# ============================================================================

with tab1:
    st.subheader("Dijkstra's Algorithm Demo")

    # --- Graph Input ---
    st.write("### Step 1: Define the Graph")

    graph_mode = st.radio("Graph source:", ["Sample Graph (6 nodes)", "Custom Graph"], horizontal=True)

    if graph_mode == "Sample Graph (6 nodes)":
        n = DEFAULT_N
        edges = DEFAULT_EDGES
        st.info(f"Using sample directed graph with **{n} nodes** and **{len(edges)} edges** (from lab manual)")
    else:
        col_a, col_b = st.columns(2)
        with col_a:
            n = st.number_input("Number of nodes:", min_value=2, max_value=20, value=6)
        with col_b:
            source = st.number_input("Source vertex:", min_value=0, max_value=n - 1, value=0)

        raw_edges = st.text_area(
            "Enter directed edges (one per line, format: u,v,weight):",
            value="0,1,4\n0,2,1\n1,3,1\n2,1,2\n2,3,5\n3,4,3\n4,5,2",
            height=150
        )

        edges = []
        try:
            for line in raw_edges.strip().split("\n"):
                line = line.strip()
                if line:
                    parts = line.split(",")
                    u, v, w = int(parts[0]), int(parts[1]), int(parts[2])
                    edges.append((u, v, w))
            st.success(f"✅ Loaded **{len(edges)}** directed edges")
        except Exception as e:
            st.error(f"❌ Error parsing edges: {e}")
            edges = DEFAULT_EDGES
            n = DEFAULT_N

    # Source vertex input (always shown after graph setup)
    source = st.number_input("Source vertex:", min_value=0, max_value=n - 1, value=0)

    st.write("---")

    # --- Run Algorithm ---
    st.write("### Step 2: Run Dijkstra's Algorithm")

    graph = build_directed_graph(n, edges)
    dist, prev, steps = dijkstra(graph, source)

    # Build all shortest paths
    all_paths = []
    for v in range(n):
        path = reconstruct_path(prev, source, v)
        if path:
            all_paths.append(path)

    # --- Results Table ---
    st.write("### Shortest Paths Results")

    results_data = []
    for v in range(n):
        path = reconstruct_path(prev, source, v)
        path_str = ' → '.join(map(str, path)) if path else 'No path'
        d = dist[v] if dist[v] != float('inf') else '∞'
        results_data.append({
            'Vertex': v,
            'Distance': d,
            'Path': path_str,
            'Hops': len(path) - 1 if path else '-'
        })

    results_df = pd.DataFrame(results_data)
    st.dataframe(results_df, width='stretch', hide_index=True)

    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        reachable = sum(1 for d in dist if d != float('inf'))
        st.metric("Reachable Vertices", f"{reachable} / {n}")
    with col2:
        total_dist = sum(d for d in dist if d != float('inf'))
        st.metric("Total Distance (all)", total_dist)
    with col3:
        st.metric("Algorithm Steps", len(steps))

    st.write("---")

    # --- Visualization ---
    st.write("### Step 3: Visualize")

    fig = create_graph_fig(n, edges, shortest_paths=all_paths, distances=dist,
                          title=f"Dijkstra's Shortest Paths from Vertex {source}")
    st.plotly_chart(fig, width='stretch')

    # --- Path Selection ---
    st.write("---")
    st.write("### Step 4: Explore Individual Paths")

    target_vertex = st.selectbox("Select destination vertex:", range(n), index=n - 1)

    path = reconstruct_path(prev, source, target_vertex)
    if path:
        path_str = ' → '.join(map(str, path))
        st.success(f"**Shortest path from {source} to {target_vertex}:** `{path_str}`")
        st.metric("Path Distance", dist[target_vertex])
        st.metric("Number of Hops", len(path) - 1)

        # Show edge breakdown
        st.write("**Edge breakdown:**")
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            for neighbor, weight in graph[u]:
                if neighbor == v:
                    st.write(f"  - Edge ({u} → {v}): weight = **{weight}**")
                    break
    else:
        st.error(f"❌ No path from {source} to {target_vertex}")

    # --- Step-by-Step Animation ---
    st.write("---")
    st.write("### Step-by-Step Execution")
    st.markdown("Walk through each step of Dijkstra's algorithm. **Green** = source, **Orange** = visited, **Blue** = unvisited.")

    total_steps = len(steps)

    if total_steps > 0:
        step = st.slider(
            "Current step",
            min_value=0,
            max_value=total_steps - 1,
            value=0,
            format="Step %d / " + str(total_steps - 1),
            key="dijkstra_step"
        )

        # Step info
        current = steps[step]
        visited_vertices = [s['vertex'] for s in steps[:step + 1]]
        visited_set = set(visited_vertices)

        info_col1, info_col2 = st.columns([2, 1])

        with info_col1:
            # Create visualization for this step
            step_fig = go.Figure()
            pos = {}
            for i in range(n):
                angle = 2 * math.pi * i / n - math.pi / 2
                pos[i] = (math.cos(angle), math.sin(angle))

            # Draw edges
            edge_x, edge_y = [], []
            for u, v, w in edges:
                x0, y0 = pos[u]
                x1, y1 = pos[v]
                edge_x.extend([x0, x1, None])
                edge_y.extend([y0, y1, None])

            step_fig.add_trace(go.Scatter(
                x=edge_x, y=edge_y,
                mode='lines',
                line=dict(width=1, color='#888'),
                hoverinfo='none',
                showlegend=False
            ))

            # Edge labels
            edge_label_x, edge_label_y, edge_label_text = [], [], []
            for u, v, w in edges:
                x0, y0 = pos[u]
                x1, y1 = pos[v]
                mx, my = (x0 + x1) / 2, (y0 + y1) / 2
                dx, dy = y1 - y0, -(x1 - x0)
                length = math.sqrt(dx * dx + dy * dy) or 1
                mx += dx / length * 0.12
                my += dy / length * 0.12
                edge_label_x.append(mx)
                edge_label_y.append(my)
                edge_label_text.append(str(w))

            step_fig.add_trace(go.Scatter(
                x=edge_label_x, y=edge_label_y,
                mode='text',
                text=edge_label_text,
                textfont=dict(size=10, color='#555'),
                hoverinfo='none',
                showlegend=False
            ))

            # Nodes
            node_x = [pos[i][0] for i in range(n)]
            node_y = [pos[i][1] for i in range(n)]
            node_colors = []
            for i in range(n):
                if i == source:
                    node_colors.append('#00CC96')
                elif i in visited_set:
                    node_colors.append('#FFA15A')
                else:
                    node_colors.append('#636EFA')

            step_fig.add_trace(go.Scatter(
                x=node_x, y=node_y,
                mode='markers+text',
                marker=dict(size=40, color=node_colors, line=dict(width=2, color='white')),
                text=[str(i) for i in range(n)],
                textposition='middle center',
                textfont=dict(size=14, color='white', family='Arial Black'),
                hoverinfo='text',
                name='Vertices'
            ))

            step_fig.update_layout(
                title=f"Dijkstra's — Step {step + 1} of {total_steps}",
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor='white',
                height=400,
                margin=dict(l=20, r=20, t=50, b=20)
            )

            st.plotly_chart(step_fig, width='stretch')

        with info_col2:
            st.write("#### Step Details")
            st.write(f"**Processing vertex:** {current['vertex']}")
            st.write(f"**Current distance:** {current['distance']}")

            if current['relaxed']:
                st.write("**Relaxed edges:**")
                for r in current['relaxed']:
                    st.write(f"  - → {r['neighbor']}: {r['old_dist']} → **{r['new_dist']}** (via weight {r['weight']})")
            else:
                st.info("No edges relaxed")

            st.write("---")
            st.write("#### Progress")
            st.metric("Vertices Visited", f"{len(visited_set)} / {n}")
            st.metric("Current Vertex", current['vertex'])

            st.write("---")
            st.write("#### Legend")
            st.markdown(
                '<span style="color:#00CC96">●</span> Source<br>'
                '<span style="color:#FFA15A">●</span> Visited<br>'
                '<span style="color:#636EFA">●</span> Unvisited',
                unsafe_allow_html=True
            )
    else:
        st.info("No steps to animate.")

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

        # Generate random directed graph
        test_edges = []
        for _ in range(size * 3):  # ~3 edges per node
            u = random.randint(0, size - 1)
            v = random.randint(0, size - 1)
            if u != v:
                w = random.randint(1, 100)
                test_edges.append((u, v, w))

        test_graph = build_directed_graph(size, test_edges)

        # Dijkstra's timing
        start = time.perf_counter()
        for _ in range(10):
            dijkstra(test_graph, 0)
        d_time = (time.perf_counter() - start) / 10 * 1000

        # Run once to get stats
        dist, prev, steps = dijkstra(test_graph, 0)
        reachable = sum(1 for d in dist if d != float('inf'))

        results.append({
            'Nodes': size,
            'Edges': len(test_edges),
            'Reachable': reachable,
            'Time (ms)': round(d_time, 4),
            'Steps': len(steps)
        })

        progress_bar.progress((idx + 1) / len(sizes))

    status_text.empty()
    df = pd.DataFrame(results)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.line(df, x='Nodes', y='Time (ms)',
                      title='Dijkstra\'s Execution Time vs Graph Size',
                      markers=True,
                      labels={'Nodes': 'Number of Vertices', 'Time (ms)': 'Time (ms)'})
        st.plotly_chart(fig, width='stretch')

    with col2:
        st.write("### Results Table")
        st.dataframe(df, width='stretch')

        st.write("---")
        st.write("### Summary")
        st.write(f"✅ **Average time per node:** {df['Time (ms)'].mean() / df['Nodes'].mean() * 1000:.4f} μs")
        st.write(f"✅ **Total edges processed:** {df['Edges'].sum()}")

        st.write("---")
        st.write("### Algorithm Complexity")
        st.markdown("""
        - **Dijkstra's:** O((V + E) log V) with min-heap
        - **Space:** O(V) for distance array and priority queue

        **Key Properties:**
        - Greedy algorithm — always processes closest unvisited vertex
        - Cannot handle negative edge weights
        - Guarantees optimal shortest paths for non-negative weights

        **Applications:**
        - GPS navigation systems
        - Network routing protocols (OSPF)
        - Game pathfinding
        """)

# ============================================================================
# TAB 3: ALGORITHM DETAILS
# ============================================================================

with tab3:
    st.subheader("Algorithm Deep Dive")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Dijkstra's Algorithm")
        st.markdown("""
        **Strategy:** Greedy — always process the closest unvisited vertex

        **Steps:**
        1. Initialize distances: source = 0, all others = ∞
        2. Add source to priority queue (min-heap)
        3. While queue is not empty:
           - Extract vertex u with minimum distance
           - For each neighbor v of u:
             - If dist[u] + weight(u,v) < dist[v]:
               - Update dist[v] = dist[u] + weight(u,v)
               - Set prev[v] = u
               - Add v to queue
        4. Return distances and predecessor array

        **Data Structure:** Min-Heap (Priority Queue)
        - Extract min: O(log V)
        - Insert/Update: O(log V)

        **Time Complexity:** O((V + E) log V)
        - Each vertex extracted at most once
        - Each edge relaxed at most once
        """)

        st.code("""
def dijkstra(graph, source):
    n = len(graph)
    dist = [float('inf')] * n
    prev = [None] * n
    dist[source] = 0
    pq = [(0, source)]
    visited = set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)

        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))

    return dist, prev
        """, language="python")

    with col2:
        st.write("### Path Reconstruction")
        st.markdown("""
        **Purpose:** Reconstruct the actual shortest path from source to any destination

        **Steps:**
        1. Start at target vertex
        2. Follow predecessor pointers back to source
        3. Reverse the path

        **Time Complexity:** O(V) worst case (path length)
        """)

        st.code("""
def reconstruct_path(prev, source, target):
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()

    if path[0] == source:
        return path
    return []  # No path exists
        """, language="python")

        st.write("---")
        st.write("### Why Dijkstra's Works")

        st.markdown("""
        **Greedy Choice Property:**
        - At each step, we select the vertex with minimum distance
        - This vertex's distance is guaranteed to be final

        **Optimal Substructure:**
        - Shortest path to any vertex v goes through other shortest paths
        - If we have shortest path to u, and edge (u,v), then shortest to v = dist[u] + w(u,v)

        **Limitations:**
        - ❌ Cannot handle negative edge weights
        - ❌ Cannot detect negative cycles
        - For negative weights, use Bellman-Ford algorithm
        """)

    st.write("---")
    st.write("### Comparison with Other Algorithms")

    comparison_data = {
        'Algorithm': ["Dijkstra's", "Bellman-Ford", "Floyd-Warshall", "A*"],
        'Time Complexity': ["O((V+E) log V)", "O(V × E)", "O(V³)", "O((V+E) log V)"],
        'Negative Weights': ["❌ No", "✅ Yes", "✅ Yes", "❌ No"],
        'Single Source': ["✅ Yes", "✅ Yes", "❌ No (all-pairs)", "✅ Yes"],
        'Best For': ["Non-negative graphs", "Negative weights", "All-pairs shortest", "Heuristic search"]
    }

    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, width='stretch', hide_index=True)

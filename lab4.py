import heapq
import math
import plotly.graph_objects as go
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
    pq = [(0, source)]  # (distance, vertex)
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

    # Node positions (circular layout)
    pos = {}
    for i in range(n):
        angle = 2 * math.pi * i / n - math.pi / 2  # Start from top
        pos[i] = (math.cos(angle), math.sin(angle))

    # Create figure
    fig = go.Figure()

    # Draw all edges (gray)
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

    # Highlight shortest path edges (if provided)
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
        # Offset label perpendicular to edge
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

    # Nodes with distance labels
    node_x = [pos[i][0] for i in range(n)]
    node_y = [pos[i][1] for i in range(n)]
    node_text = [str(i) for i in range(n)]
    node_hover = []
    for i in range(n):
        d = distances[i] if distances and distances[i] != float('inf') else 'INF'
        node_hover.append(f"Vertex {i}<br>Distance: {d}")

    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        marker=dict(
            size=40,
            color='#636EFA' if not distances else ['#00CC96' if distances and d == 0 else '#FFA15A' if distances and d != float('inf') else '#636EFA' for d in distances],
            line=dict(width=2, color='white')
        ),
        text=node_text,
        textposition='middle center',
        textfont=dict(size=14, color='white', family='Arial Black'),
        hovertext=node_hover,
        hoverinfo='text',
        name='Vertices'
    ))

    # Add distance labels below nodes
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

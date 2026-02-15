
import plotly.graph_objects as go
import json

def generate_3d_graph():
    with open('data/knowledge_graph.json', 'r') as f:
        data = json.load(f)

    # Simulação de coordenadas 3D para os nós
    nodes = data.get('nodes', [])
    x, y, z = [], [], []
    labels = []

    for i, node in enumerate(nodes):
        x.append(i * 0.5)
        y.append((i % 3) * 0.5)
        z.append((i % 2) * 0.5)
        labels.append(node.get('id', 'Unknown'))

    fig = go.Figure(data=[go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers+text',
        marker=dict(size=10, color=z, colorscale='Viridis'),
        text=labels
    )])

    fig.update_layout(title="WiseClaw Neural Graph 3D", template="plotly_dark")
    return fig

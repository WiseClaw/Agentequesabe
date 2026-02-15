import plotly.graph_objects as go
import json
import networkx as nx

def render_knowledge_graph():
    with open('data/knowledge_graph.json', 'r') as f:
        data = json.load(f)

    G = nx.DiGraph()
    for node in data['nodes']:
        G.add_node(node['id'], label=node['label'])
    for edge in data['edges']:
        G.add_edge(edge['from'], edge['to'], label=edge['label'])

    pos = nx.spring_layout(G)
    
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1, color='#888'), hoverinfo='none', mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode='markers+text',
        text=[G.nodes[n]['label'] for n in G.nodes()],
        textposition="top center",
        marker=dict(showscale=False, color='#00ffcc', size=20, line_width=2)
    )

    fig = go.Figure(data=[edge_trace, node_trace], layout=go.Layout(
        showlegend=False, hovermode='closest', margin=dict(b=0,l=0,r=0,t=0),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='white')
    ))
    return fig

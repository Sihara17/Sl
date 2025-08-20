import re
import plotly.graph_objects as go

def parse_dat_file(file_path):
    nodes = {}
    elements = {}
    with open(file_path, 'r') as f:
        lines = f.readlines()

    parsing_nodes = False
    for line in lines:
        line = line.strip()
        if not line or line.startswith('!'):
            continue

        if line.lower().startswith('nblock') or line.lower().startswith('n,') or line.lower().startswith('node,'):
            parsing_nodes = True
            continue

        if parsing_nodes:
            parts = re.split(r'\s+|,', line)
            if len(parts) >= 4:
                try:
                    node_id = int(parts[0])
                    x, y, z = map(float, parts[1:4])
                    nodes[node_id] = (x, y, z)
                except:
                    parsing_nodes = False
            else:
                parsing_nodes = False

        if line.upper().startswith('E,') or line.upper().startswith('ELEMENT,'):
            parts = re.split(r',\s*', line)
            try:
                elem_id = int(parts[1])
                connectivity = list(map(int, parts[2:]))
                elements[elem_id] = connectivity
            except:
                continue

    return nodes, elements

def detect_spring_nodes(nodes, jumlah_pegas=8):
    sorted_nodes = sorted(nodes.items(), key=lambda kv: kv[1][2])
    node_pegas = [nid for nid, _ in sorted_nodes[:jumlah_pegas]]
    return node_pegas

def plot_mesh_to_png(nodes, elements, node_pegas, beban_per_node, output_file="mesh_spring.png"):
    fig = go.Figure()

    # plot edges
    for conn in elements.values():
        xs, ys, zs = [], [], []
        for node_id in conn:
            if node_id in nodes:
                x, y, z = nodes[node_id]
                xs.append(x)
                ys.append(y)
                zs.append(z)
        xs.append(xs[0])
        ys.append(ys[0])
        zs.append(zs[0])
        fig.add_trace(go.Scatter3d(
            x=xs, y=ys, z=zs,
            mode='lines',
            line=dict(color='blue', width=2),
            name='Element'
        ))

    # plot semua nodes
    x_nodes = [c[0] for c in nodes.values()]
    y_nodes = [c[1] for c in nodes.values()]
    z_nodes = [c[2] for c in nodes.values()]
    fig.add_trace(go.Scatter3d(
        x=x_nodes, y=y_nodes, z=z_nodes,
        mode='markers',
        marker=dict(color='grey', size=4),
        name='Nodes'
    ))

    # highlight node pegas
    x_spring = [nodes[nid][0] for nid in node_pegas]
    y_spring = [nodes[nid][1] for nid in node_pegas]
    z_spring = [nodes[nid][2] for nid in node_pegas]
    fig.add_trace(go.Scatter3d(
        x=x_spring, y=y_spring, z=z_spring,
        mode='markers',
        marker=dict(color='red', size=6),
        name='Pegas'
    ))

    fig.update_layout(
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='data'
        ),
        title="Mesh dengan Node Pegas"
    )

    # simpan sebagai PNG
    fig.write_image(output_file)
    print(f"Mesh statis disimpan di {output_file}")

if __name__ == "__main__":
    file_path = "ds.dat"  # ganti ds.dat jika perlu
    nodes, elements = parse_dat_file(file_path)
    print(f"Total Nodes: {len(nodes)}, Total Elements: {len(elements)}")

    node_pegas = detect_spring_nodes(nodes, jumlah_pegas=8)
    print("Node pegas terdeteksi:", node_pegas)

    beban_per_node = 108045

    plot_mesh_to_png(nodes, elements, node_pegas, beban_per_node)

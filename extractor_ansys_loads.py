import re
import csv

# ----------- Konfigurasi ----------------
file_path = "ds.dat"       # file .dat yang bisa dibaca
jumlah_pegas = 8           # jumlah pegas di lokomotif
total_lokomotif_ton = 88.2 # total berat lokomotif
g = 9.81                   # percepatan gravitasi m/s^2
output_file = "spring_loads.csv"
# --------------------------------------

# Hitung beban rata-rata per pegas dalam Newton
beban_per_pegas = (total_lokomotif_ton / jumlah_pegas) * 1000 * g
print(f"Beban rata-rata per pegas: {beban_per_pegas:.0f} N\n")

# ----------- Parsing file .dat untuk semua node -----------
def parse_dat_file(file_path):
    nodes = {}
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('!'):
                continue
            # Jika baris dimulai dengan angka, anggap itu node
            if re.match(r'^\d+', line):
                parts = re.split(r'\s+', line)
                if len(parts) >= 4:
                    try:
                        node_id = int(parts[0])
                        x, y, z = map(float, parts[1:4])
                        nodes[node_id] = (x, y, z)
                    except:
                        continue
    return nodes

# ----------- Deteksi node pegas (terendah di sumbu Z) -----------
def detect_spring_nodes(nodes, jumlah_pegas):
    sorted_nodes = sorted(nodes.items(), key=lambda kv: kv[1][2])  # sort berdasarkan Z
    node_pegas = [nid for nid, _ in sorted_nodes[:jumlah_pegas]]
    return node_pegas

# ----------- Simpan hasil ke CSV -----------
def save_spring_loads_csv(node_pegas, beban_per_node, output_file):
    with open(output_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["NodeID", "Beban_N"])
        for nid in node_pegas:
            writer.writerow([nid, int(beban_per_node)])
    print(f"CSV berhasil dibuat: {output_file}")

# ----------- Main ---------------------------
nodes = parse_dat_file(file_path)
print(f"Total node terbaca: {len(nodes)}")

if len(nodes) == 0:
    print("Error: tidak ada node terbaca dari ds.dat. Pastikan file benar dan bisa dibaca.")
else:
    node_pegas = detect_spring_nodes(nodes, jumlah_pegas)
    print(f"Node pegas terdeteksi (8 node terendah Z): {node_pegas}\n")
    save_spring_loads_csv(node_pegas, beban_per_pegas, output_file)

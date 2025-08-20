from ansys.mapdl.core import launch_mapdl

# Jalankan MAPDL dari PyAnsys
mapdl = launch_mapdl()

# Baca input file dari ds.dat (atau act.dat jika ada script command)
mapdl.clear()
mapdl.input("ds.dat")   # <-- pastikan file ds.dat ada di folder project

# Cek summary
print("Title:", mapdl.title)
print("Number of nodes:", mapdl.get("NODE", 0))
print("Number of elements:", mapdl.get("ELEM", 0))

# Simpan database MAPDL
mapdl.save("model.db")

# Jalankan analisis (jika sudah ada beban dan solve di dat file)
mapdl.run("/SOLU")
mapdl.solve()

# Ambil hasil
mapdl.post1()
mapdl.set(1)
u = mapdl.get("U", "NODE", 1, "U", "X")
print("Displacement Node 1 (UX):", u)

mapdl.exit()

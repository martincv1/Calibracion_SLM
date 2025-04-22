from harvesters.core import Harvester

h = Harvester()

h.add_file('C:/Program Files/JAI/SDK/bin/JaiGevTL.cti')
h.update()

if h.device_info_list:
    print("Cámaras encontradas")
    for i, device in enumerate(h.device_info_list):
        print(f"[{i}] {device}")

else:
    print("No se detectaron cámaras.")

h.reset()
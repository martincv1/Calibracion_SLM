from harvesters.core import Harvester
import time

h = Harvester()
h.add_cti_file(r'C:\Program Files\JAI\SDK\bin\win64_x64\JaiGevTL.cti')
h.update()

ia = h.create_image_acquirer(0)
ia.num_buffers = 1

# Intentar setear Mono8
try:
    ia.device.node_map.PixelFormat.value = 'Mono8'
except Exception as e:
    print(f"No se pudo setear Mono8: {e}")

ia.start()
print("Adquisición iniciada")
time.sleep(1)

with ia.fetch_buffer() as buffer:
    component = buffer.payload.components[0]
    image = component.data
    print(f"Imagen recibida. Dimensiones: {image.shape}")

ia.stop()
ia.destroy()
h.reset()

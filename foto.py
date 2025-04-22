import numpy as np
import eBUS as eb
import lib.PvSampleUtils as psu
import cv2

BUFFER_COUNT = 16

kb = psu.PvKb()

opencv_is_available = True
try:
    # Detect if OpenCV is available
    import cv2
    opencv_version = cv2.__version__
except:
    opencv_is_available = False
    print("Warning: This sample requires python3-opencv to display a window")

def connect_to_device(connection_ID):
    # Connect to the GigE Vision or USB3 Vision device
    print("Connecting to device.")
    result, device = eb.PvDevice.CreateAndConnect(connection_ID)
    if device == None:
        print(f"Unable to connect to device: {result.GetCodeString()} ({result.GetDescription()})")
    return device

def open_stream(connection_ID):
    # Open stream to the GigE Vision or USB3 Vision device
    print("Opening stream from device.")
    result, stream = eb.PvStream.CreateAndOpen(connection_ID)
    if stream == None:
        print(f"Unable to stream from device. {result.GetCodeString()} ({result.GetDescription()})")
    return stream

def configure_stream(device, stream):
    # If this is a GigE Vision device, configure GigE Vision specific streaming parameters
    if isinstance(device, eb.PvDeviceGEV):
        # Negotiate packet size
        device.NegotiatePacketSize()
        # Configure device streaming destination
        device.SetStreamDestination(stream.GetLocalIPAddress(), stream.GetLocalPort())

def configure_stream_buffers(device, stream):
    buffer_list = []
    # Reading payload size from device
    size = device.GetPayloadSize()

    # Use BUFFER_COUNT or the maximum number of buffers, whichever is smaller
    buffer_count = stream.GetQueuedBufferMaximum()
    if buffer_count > BUFFER_COUNT:
        buffer_count = BUFFER_COUNT

    # Allocate buffers
    for i in range(buffer_count):
        # Create new pvbuffer object
        pvbuffer = eb.PvBuffer()
        # Have the new pvbuffer object allocate payload memory
        pvbuffer.Alloc(size)
        # Add to external list - used to eventually release the buffers
        buffer_list.append(pvbuffer)
    
    # Queue all buffers in the stream
    for pvbuffer in buffer_list:
        stream.QueueBuffer(pvbuffer)
    print(f"Created {buffer_count} buffers")
    return buffer_list

def get_frame(device, stream):
    # Ejecutar comandos necesarios para iniciar la adquisición
    device_params = device.GetParameters()
    start = device_params.Get("AcquisitionStart")
    stop = device_params.Get("AcquisitionStop")

    device.StreamEnable()
    start.Execute()

    # Recuperar un solo buffer
    result, pvbuffer, operational_result = stream.RetrieveBuffer(1000)

    image_data = None

    if result.IsOK() and operational_result.IsOK():
        payload_type = pvbuffer.GetPayloadType()
        if payload_type == eb.PvPayloadTypeImage:
            image = pvbuffer.GetImage()
            if image:
                width = image.GetWidth()
                height = image.GetHeight()
                pixel_type = image.GetPixelType()

                if pixel_type == eb.PvPixelMono8:
                    # Convertir a arreglo NumPy (grayscale)
                    image_data = np.ndarray((height, width), dtype=np.uint8, buffer=image.GetDataPointer())
                elif pixel_type == eb.PvPixelRGB8:
                    # Convertir a arreglo NumPy (RGB)
                    image_data = np.ndarray((height, width, 3), dtype=np.uint8, buffer=image.GetDataPointer())
                    image_data = cv2.cvtColor(image_data, cv2.COLOR_RGB2BGR)

        stream.QueueBuffer(pvbuffer)

    # Detener la adquisición y el streaming
    stop.Execute()
    device.StreamDisable()

    return image_data

# Main Program

print("PvStreamSample:")

connection_ID = psu.PvSelectDevice()
if connection_ID:
    device = connect_to_device(connection_ID)
    if device:
        stream = open_stream(connection_ID)
        if stream:
            configure_stream(device, stream)
            buffer_list = configure_stream_buffers(device, stream)

            # Captura una sola imagen
            frame = get_frame(device, stream)
            if frame is not None:
                cv2.imshow("Captured Frame", frame)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                print("No frame was captured.")

            # Clean up and close the stream
            buffer_list.clear()
            print("Closing stream")
            stream.Close()
            eb.PvStream.Free(stream)

        # Disconnect the device
        print("Disconnecting device")
        device.Disconnect()
        eb.PvDevice.Free(device)

print("<press a key to exit>")
kb.start()
kb.getch()
kb.stop()

#Importo librerias
import numpy as np
import eBUS as eb
import lib.PvSampleUtils as psu
import time

########################################## Defino funciones de configuración
BUFFER_COUNT = 16

kb = psu.PvKb()

opencv_is_available=True
try:
    # Detect if OpenCV is available
    import cv2
    opencv_version=cv2.__version__
except:
    opencv_is_available=False
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
########################################## 
# Defino función de adquisición de imagen
def tomar_foto(device, stream):
    #Inicializo sin_foto
    sin_foto = True
    # Get device parameters need to control streaming
    device_params = device.GetParameters()

    # Map the GenICam AcquisitionStart and AcquisitionStop commands
    start = device_params.Get("AcquisitionStart")
    stop = device_params.Get("AcquisitionStop")

    # Get stream parameters
    stream_params = stream.GetParameters()

    # Map a few GenICam stream stats counters
    frame_rate = stream_params.Get("AcquisitionRate")
    bandwidth = stream_params[ "Bandwidth" ]

    # Enable streaming and send the AcquisitionStart command
    print("Enabling streaming and sending AcquisitionStart command.")
    device.StreamEnable()
    start.Execute()

    doodle = "|\\-|-/"
    doodle_index = 0
    display_image = False
    warning_issued = False
    errors = 0
    decompression_filter = eb.PvDecompressionFilter()

    # Acquire images until the user instructs us to stop.
    print("\n<press a key to stop streaming>")
    kb.start()
    # Pongo un sleep por las dudas
    time.sleep(2)
    while not kb.is_stopping():
        # Retrieve next pvbuffer
        result, pvbuffer, operational_result = stream.RetrieveBuffer(1000)
        if result.IsOK():
            if operational_result.IsOK():
                #
                # We now have a valid pvbuffer. This is where you would typically process the pvbuffer.
                # -----------------------------------------------------------------------------------------
                # ...

                result, frame_rate_val = frame_rate.GetValue()
                result, bandwidth_val = bandwidth.GetValue()

                print(f"{doodle[doodle_index]} BlockID: {pvbuffer.GetBlockID():016d}", end='')

                image = None
                

                payload_type = pvbuffer.GetPayloadType()
                if payload_type == eb.PvPayloadTypeImage:
                    image = pvbuffer.GetImage()

                elif payload_type == eb.PvPayloadTypeChunkData:
                    print(f" Chunk Data payload type with {pvbuffer.GetChunkCount()} chunks", end='')

                elif payload_type == eb.PvPayloadTypeRawData:
                    print(f" Raw Data with {pvbuffer.GetRawData().GetPayloadLength()} bytes", end='')

                elif payload_type == eb.PvPayloadTypeMultiPart:
                    print(f" Multi Part with {pvbuffer.GetMultiPartContainer().GetPartCount()} parts", end='')

                elif payload_type == eb.PvPayloadTypePleoraCompressed:
                    if eb.PvDecompressionFilter.IsCompressed(pvbuffer):
                        result, pixel_type, width, height = eb.PvDecompressionFilter.GetOutputFormatFor(pvbuffer)
                        if result.IsOK():
                            calculated_size = eb.PvImage.GetPixelSize(pixel_type) * width * height / 8;
                            out_buffer = eb.PvBuffer()
                            result, decompressed_buffer = decompression_filter.Execute(pvbuffer, out_buffer)
                            image = decompressed_buffer.GetImage()
                            if result.IsOK():
                                decompressed_size = decompressed_buffer.GetSize()
                                compression_ratio = decompressed_size / pvbuffer.GetAcquiredSize()
                                if calculated_size != decompressed_size:
                                    errors = errors + 1
                                print(f" Pleora compressed type.   Compression ratio: {'{0:.2f}'.format(compression_ratio)} Errors: {errors}", end='')
                            else:
                                print(f" Could not decompress (Pleora compressed)", end='')
                                errors = errors + 1
                        else:
                            print(f" Could not read header (Pleora compressed)", end='')
                            errors = errors + 1
                    else:
                        print(f" Contents do not match payload type (Pleora compressed)", end='')
                        errors = errors + 1

                else:
                    print(" Payload type not supported by this sample", end='')
                while sin_foto:
                    if image:
                        print(f"  W: {image.GetWidth()} H: {image.GetHeight()} ", end='')
                        image_data = image.GetDataPointer()
                        if image.GetPixelType() == eb.PvPixelMono8:
                            foto_tipo = 'MONO8'
                        if image.GetPixelType() == eb.PvPixelRGB8:
                            foto_tipo = 'RGB8'
                        sin_foto = False


                print(f" {frame_rate_val:.1f} FPS  {bandwidth_val / 1000000.0:.1f} Mb/s     ", end='\r')
            else:
                # Non OK operational result
                print(f"{doodle[ doodle_index ]} {operational_result.GetCodeString()}       ", end='\r')
            # Re-queue the pvbuffer in the stream object
            stream.QueueBuffer(pvbuffer)

        else:
            # Retrieve pvbuffer failure
            print(f"{doodle[ doodle_index ]} {result.GetCodeString()}      ", end='\r')

        doodle_index = (doodle_index + 1) % 6
        if kb.kbhit():
            kb.getch()
            break;

    kb.stop()
    if opencv_is_available:
        cv2.destroyAllWindows()

    # Tell the device to stop sending images.
    print("\nSending AcquisitionStop command to the device")
    stop.Execute()

    # Disable streaming on the device
    print("Disable streaming on the controller.")
    device.StreamDisable()

    # Abort all buffers from the stream and dequeue
    print("Aborting buffers still in stream")
    stream.AbortQueuedBuffers()
    while stream.GetQueuedBufferCount() > 0:
        result, pvbuffer, lOperationalResult = stream.RetrieveBuffer()
    return image_data, foto_tipo

########################################## Corro el código para sacar una foto

connection_ID = psu.PvSelectDevice()
if connection_ID:
    device = connect_to_device(connection_ID)
    if device:
        stream = open_stream(connection_ID)
        if stream:
            configure_stream(device, stream)
            buffer_list = configure_stream_buffers(device, stream)
            foto, tipo = tomar_foto(device, stream)
            cv2.imwrite('fotin.jpg', foto)
            buffer_list.clear()
            
            # Close the stream
            print("Closing stream")
            stream.Close()
            eb.PvStream.Free(stream);    

        # Disconnect the device
        print("Disconnecting device")
        device.Disconnect()
        eb.PvDevice.Free(device)

print("<press a key to exit>")
kb.start()
kb.getch()
kb.stop()

#if tipo == 'MONO8':
#    cv2.imshow("foto",foto)
#if tipo == 'RGB8':
#    foto = cv2.cvtColor(foto, cv2.COLOR_RGB2BGR)
#    cv2.imshow("foto",foto)
height, width = foto.shape

print(f"Width: {width}, Height: {height}")
if foto is not None and isinstance(foto, np.ndarray):
    cv2.imshow("foto", foto)
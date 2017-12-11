import socket
import pickle
import struct

class QRSocketC():
    """sends images to the socket server of the class QRSocketS

    """
    clientsocket = None
    HOST = '192.168.0.5'

    def __init__(self):
        """connects to the socket server of the class QRSocketS

        """
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect((self.HOST, 8089))

    def send_image(self, frame):
        """sends a single image to the socket server

        :param frame: image
        :type frame: numpy.ndarray
        """
        try:
            data = pickle.dumps(frame)
            tmp = struct.pack("l", len(data)) + data
            self.clientsocket.sendall(tmp)
            print('sent')
        except socket.error:
            print('pipe broken')

    def closeSocket(self):
        self.clientsocket.close()

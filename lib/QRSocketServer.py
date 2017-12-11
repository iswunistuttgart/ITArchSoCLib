import socket
import struct
import pickle


class QRSocketS():
    """This class is used to create a socket server, that receives numpy array images from a socket client.
    """

    HOST = ''
    PORT = 8089
    conn = None
    data = ""
    addr = None
    payload_size = None
    s = None
    def __init__(self):
        """creates and binds a socket, that connects to the next requesting client
        """

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')
        self.s.bind((self.HOST, self.PORT))
        print('Socket bind complete')
        self.s.listen(10)
        print('Socket now listening')
        self.conn, self.addr = self.s.accept()
        self.payload_size = struct.calcsize("L")

    def receive_image(self):
        """waits until an image is received, then returns the image
        :rtype: numpy.ndarray
        :return: received frame
        """
        while len(self.data) < self.payload_size:
            tmp = self.conn.recv(4096)
            if not tmp:
                self.conn, self.addr = self.s.accept()
                self.data = ""
                pass
            self.data += tmp
        packed_msg_size = self.data[:self.payload_size]
        self.data = self.data[self.payload_size:]
        msg_size = struct.unpack("l", packed_msg_size)[0]
        while len(self.data) < msg_size:
            tmp = self.conn.recv(4096)
            if not tmp:
                self.conn, self.addr = self.s.accept()
                self.data = ""
                pass
            self.data += tmp
        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]
        frame = pickle.loads(frame_data)
        return frame

    #def chechConnection(self):



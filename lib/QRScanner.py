""" provides functions to extract, read, and compare qr codes
"""



import numpy as np
import np_opencv_module
import cv2
import zbar
from PIL import Image


def crop_qr_code(frame):
    """crops a qr code from an image and returns it binarized

    :param frame: the image
    :type frame: numpy.ndarray
    :return: cropped and binarized qr code
    :rtype: numpy.ndarray
    """

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Uses PIL to convert the grayscale image into a ndary array that ZBar can understand.
    image = Image.fromarray(gray)
    width, height = image.size
    zbar_image = zbar.Image(width, height, 'Y800', image.tostring())
    # Scans the zbar image.
    scanner = zbar.ImageScanner()
    scanner.scan(zbar_image)

    for decoded in zbar_image:
        qpoints = np.asarray(decoded.location)
        pts1 = np.float32([qpoints[0], qpoints[3], qpoints[1], qpoints[2]])
        pts2 = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        dst = cv2.warpPerspective(gray, M, (300, 300))
        ret3, th = cv2.threshold(dst, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return th


def read_qr_code(qrcode_frame):
    """reads a qr code image and returns its decoded information

    :param qrcode_frame: image of a qr code
    :return: decoded string
    :type: qrcode_frame: numpy.ndarray
    :rtype: String
    """

    image = Image.fromarray(qrcode_frame)
    width, height = image.size
    zbar_image = zbar.Image(width, height, 'Y800', image.tostring())
    scanner = zbar.ImageScanner()
    scanner.scan(zbar_image)

    for decoded in zbar_image:
        return decoded.data


def qr_codes_equal(qr1, qr2):
    """checks if two qr codes are equal

    :param qr1: image of first qr code
    :param qr2: image of second qr code
    :return: True if equal, False if not
    :rtype: bool
    """

    if qr2 is None:
        return False
    else:
        image = Image.fromarray(qr1)
        width, height = image.size
        zbar_image = zbar.Image(width, height, 'Y800', image.tostring())

        # Scans the zbar image.
        scanner = zbar.ImageScanner()
        scanner.scan(zbar_image)

        string1 = 'a'
        for decoded in zbar_image:
            string1 = decoded.data

        image = Image.fromarray(qr2)
        width, height = image.size
        zbar_image = zbar.Image(width, height, 'Y800', image.tostring())

        # Scans the zbar image.
        scanner = zbar.ImageScanner()
        scanner.scan(zbar_image)

        string2 = 'b'
        for decoded in zbar_image:
            string2 = decoded.data

        if string1.strip() == string2.strip():
            return True
        else:
            return False

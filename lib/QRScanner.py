""" provides functions to extract, read, and compare qr codes
"""

import numpy as np
import cv2
import pyzbar.pyzbar as pyzbar


def crop_qr_code(frame):
    """crops a qr code from an image and returns it binarized

    :param frame: the image
    :type frame: numpy.ndarray
    :return: cropped and binarized qr code
    :rtype: numpy.ndarray
    """
    barcode = pyzbar.decode(frame, symbols=[pyzbar.ZBarSymbol.QRCODE])
    retval = None
    if barcode:
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = frame[:, :, 0]

        # Only check first recognized barcode
        qpoints = np.asarray(decode_results[0].polygon)
        pts1 = np.float32([qpoints[0], qpoints[3], qpoints[1], qpoints[2]])
        pts2 = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]])
        M = cv2.getPerspectiveTransform(pts1, pts2)
        dst = cv2.warpPerspective(gray, M, (300, 300))
        ret3, th = cv2.threshold(dst, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        retval = th

    return retval


def read_qr_code(qrcode_frame):
    """reads a qr code image and returns its decoded information

    :param qrcode_frame: image of a qr code
    :return: decoded string
    :type: qrcode_frame: numpy.ndarray
    :rtype: String
    """

    barcode = pyzbar.decode(qrcode_frame)
    retval = None

    if barcode:
        # Handle encoding errors: https://sourceforge.net/p/zbar/discussion/664596/thread/ed7aca9d/#e9bf
        try:
            retval = barcode[0].data.decode("ascii")
        except UnicodeDecodeError:
            retval = barcode[0].data.decode("utf-8").encode("sjis").decode('utf-8')

    return retval


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
        string1 = read_qr_code(qr1)
        string2 = read_qr_code(qr2)

        if string1 and string2 and string1.strip() == string2.strip():
            return True
        else:
            return False

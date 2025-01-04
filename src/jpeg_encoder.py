import cv2
import numpy as np

class SimpleJpegEncoder:
    def __init__(self, width, height, fps=30):
        self.width = width
        self.height = height
        self.fps = fps

    def encode(self, frame, quality=75):
        """
        Encodes a BGR8 frame into JPEG format.
        
        Parameters:
            frame (np.ndarray): Input image in BGR format.
            quality (int): Quality of the JPEG encoding (0-100, higher is better).

        Returns:
            bytes: Encoded JPEG image.
        """
        # Resize the frame to the target width and height
        resized_frame = cv2.resize(frame, (self.width, self.height))

        # Encode as JPEG
        encode_params = [cv2.IMWRITE_JPEG_QUALITY, quality]
        success, encoded_image = cv2.imencode('.jpg', resized_frame, encode_params)

        if not success:
            raise ValueError("Failed to encode frame as JPEG")

        return encoded_image.tobytes()


# Instantiate the encoder
_ENCODER = SimpleJpegEncoder(width=224, height=224, fps=21)

def bgr8_to_jpeg_gst(value):
    """Encodes a BGR8 image using SimpleJpegEncoder."""
    return _ENCODER.encode(value)

def bgr8_to_jpeg(value, quality=75):
    """Encodes a BGR8 image directly using OpenCV."""
    encode_params = [cv2.IMWRITE_JPEG_QUALITY, quality]
    success, encoded_image = cv2.imencode('.jpg', value, encode_params)

    if not success:
        raise ValueError("Failed to encode frame as JPEG")

    return encoded_image.tobytes()

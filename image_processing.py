import easyocr
import numpy as np
from PIL import Image
from streamlit.runtime.uploaded_file_manager import UploadedFile


def read_image(image_file: UploadedFile) -> str:
    reader = easyocr.Reader(
        ["ch_sim", "en"]
    )  # this needs to run only once to load the model into memory
    img = Image.open(image_file)
    img_array = np.array(img)
    result = reader.readtext(img_array)
    raw_text = "\n".join([text[1] for text in result])
    return raw_text

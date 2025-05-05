import os

import tempfile
import unicodedata
from io import BytesIO
from importlib.resources import Package
from pylatex import Document, Package, NoEscape, Command
from pdf2image import convert_from_bytes

from .text_to_text import markdown_to_latex
from utils.image_utils.processing import crop_white_borders_with_padding


def latex_to_image_bytes(latex_text: str) -> list[bytes]:
    latex_text = markdown_to_latex(latex_text)
    latex_text = unicodedata.normalize('NFKC', latex_text)
    with tempfile.TemporaryDirectory() as tempdir:
        doc = Document()
        doc.packages.append(Package('inputenc', options=['utf8']))
        doc.packages.append(Package('fontenc', options=['T2A']))
        doc.packages.append(Package('babel', options=['russian', 'english']))
        doc.packages.append(Package('amsmath'))
        doc.preamble.append(Command('pagestyle', 'empty'))
        doc.append(NoEscape(latex_text))
        temp_path = os.path.join(tempdir, 'output')
        doc.generate_pdf(
            temp_path,
            clean=True,
            clean_tex=True,
            compiler='pdflatex',
            compiler_args=['-interaction=nonstopmode']
        )
        with open(f"{temp_path}.pdf", 'rb') as f:
            pdf_bytes = f.read()
        images = convert_from_bytes(pdf_bytes)
        if not images:
            raise ValueError("Не удалось сконвертировать PDF в изображения")
        png_bytes_list = []
        for image in images:
            cropped_image = crop_white_borders_with_padding(image)
            img_byte_arr = BytesIO()
            cropped_image.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            png_bytes_list.append(img_byte_arr.getvalue())
        return png_bytes_list
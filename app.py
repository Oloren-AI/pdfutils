import oloren as olo
import sys
import io
import os

import pypdfium2 as pdfium

@olo.register()
def pdfimageiter(file = olo.File(), func = olo.Func()):
    # from pdf2image import convert_from_path
    # images = convert_from_path(file)
    # page_outputs = []
    # for i, image in enumerate(images):
    #     print(f"Processing page {i} ", image)
    #     with open("page.jpg", "wb") as f:
    #         image.save(f, "JPEG")
    #         
    #         file_json = olo.upload_file("page.jpg")
    #         page_output = func(file_json[0])
    #         page_outputs.append(page_output)
    # return page_outputs
    
    # use pdfium
    pdf = pdfium.PdfDocument(file)
    page_outputs = []
    for i in range(len(pdf)):
        page = pdf[i]

        bitmap = page.render(
            scale=1,
        )
        pil_image = bitmap.to_pil()
        pil_image.save(f"page{i}.jpg", "JPEG")
        
        file_json = olo.upload_file(f"page{i}.jpg")
        print("Inputs ", i)
        print(file_json[0])
        
        page_output = func(file_json[0])
        page_outputs.append(page_output)
    return page_outputs

@olo.register(description="Extracts text from PDF")
def pdf2txt(file = olo.File()):
    with open(file, "rb") as file:
        from PyPDF2 import PdfReader
        reader = PdfReader(file)
        return "\n".join([page.extract_text() for i, page in enumerate(reader.pages)])

@olo.register(description="Extracts text from PDF, paginated")
def pdf2txt_paginated(file = olo.File()):
    with open(file, "rb") as file:
        from PyPDF2 import PdfReader
        reader = PdfReader(file)
        return [page.extract_text() for i, page in enumerate(reader.pages)]

@olo.register()
def pdf_first_text(file = olo.File()):
    with open(file, "rb") as file:
        from PyPDF2 import PdfReader
        reader = PdfReader(file)
        first_page = reader.pages[0]
        return first_page.extract_text()
    
if __name__ == "__main__":
    olo.run("pdfutils", port=80)
import oloren as olo
import sys
import io
import os

import pypdfium2 as pdfium

@olo.register()
def get_num_pages(file = olo.File()):
    pdf = pdfium.PdfDocument(file)
    print("PDF", len(pdf))
    return len(pdf)

@olo.register()
def pdfpage2image(file = olo.File(), num = olo.Num()):
    pdf = pdfium.PdfDocument(file)
    page = pdf[num]
    bitmap = page.render(
        scale=1,
    )
    pil_image = bitmap.to_pil()
    pil_image.save("page.jpg", "JPEG")
    return olo.OutputFile("page.jpg")

@olo.register()
def pdfpageannotation2image(file = olo.File(), num = olo.Num(), annotation = olo.Json()):
    # {"x1":64,"x2":308,"y1":615,"y2":728,"label":"0","confidence":0.9146367907524109}
    pdf = pdfium.PdfDocument(file)
    page = pdf[num]
    bitmap = page.render(
        scale=1,
    )
    pil_image = bitmap.to_pil()
    
    # crop
    x1 = annotation["x1"]
    x2 = annotation["x2"]
    y1 = annotation["y1"]
    y2 = annotation["y2"]
    pil_image = pil_image.crop((x1, y1, x2, y2))
    
    pil_image.save("page.jpg", "JPEG")
    
    return olo.OutputFile("page.jpg")

@olo.register()
def pdfimageiter(file = olo.File(), func = olo.Func()):
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
    
@olo.register()
def pdfpage2txt(file = olo.File(), num = olo.Num()):
    with open(file, "rb") as file:
        from PyPDF2 import PdfReader
        reader = PdfReader(file)
        return reader.pages[num].extract_text()

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
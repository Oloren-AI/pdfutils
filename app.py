import oloren as olo
import sys
import io
import os

import PIL
import pypdfium2 as pdfium

@olo.register()
def download_pdf(url = olo.String()):
    import requests
    r = requests.get(url)
    with open("file.pdf", "wb") as file:
        file.write(r.content)
    return olo.OutputFile("file.pdf")

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
def pdf2imagelist(file = olo.File()):
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

        page_outputs.append(file_json[0])
    return page_outputs

@olo.register()
def imageannotation2image(file = olo.File(), annotation = olo.Json()):
    image = PIL.Image.open(file)

    # crop
    x1 = annotation["x1"]
    x2 = annotation["x2"]
    y1 = annotation["y1"]
    y2 = annotation["y2"]
    image = image.crop((x1, y1, x2, y2))

    image.save("page.jpg", "JPEG")

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

import json
from pypdf import PdfReader
import random

@olo.register()
def parse_pdf(file = olo.File(), log_message=print):
    def img2file(img):
        file_name = f"{img.name}_{random.randint(0, 1000000)}.jpg"

        with open(file_name, "wb") as file:
            file.write(img.data)

        fileinfo = olo.upload_file(file_name, dispatcher_url=log_message.dispatcher_url)

        fileinfo["name"] = img.name

        return fileinfo



    with open(file, "rb") as file:
        reader = PdfReader(file)

        # page in pdf
        pdf_dict = []
        for i, page in enumerate(reader.pages):
            log_message(f"Parsing page {i}")
            pdf_dict.append({
                "page": i,
                "text": page.extract_text(),
                "images": [img2file(img) for img in page.images]
            })

    return pdf_dict

@olo.register()
def keep_pages(file = olo.File() , pages = olo.Json()):
    from PyPDF2 import PdfWriter, PdfReader
    output = PdfWriter()
    input_pdf = PdfReader(file)

    for page_number in pages:
        output.add_page(input_pdf.pages[page_number])

    new_pdf_file = "new_pdf_file.pdf"
    with open(new_pdf_file, "wb") as outputStream:
        output.write(outputStream)

    return olo.OutputFile(new_pdf_file)

if __name__ == "__main__":
    olo.run("pdfutils", port=80)
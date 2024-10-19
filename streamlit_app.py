import streamlit as st
import fitz  # PyMuPDF
import tempfile
import os
from PIL import Image
import io
import pytesseract
from pdf2image import convert_from_path

def extract_images_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            images.append(image)
    return images

def perform_ocr(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""
    for i, image in enumerate(images):
        text += f"\n\n--- Page {i+1} ---\n\n"
        text += pytesseract.image_to_string(image)
    return text

st.title("PDF Image Extractor with OCR")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_input:
        temp_input.write(uploaded_file.read())
        temp_input_path = temp_input.name

    st.write("Extracting images...")
    images = extract_images_from_pdf(temp_input_path)

    st.write(f"Extracted {len(images)} images")

    for i, img in enumerate(images):
        st.image(img, caption=f"Image {i+1}", use_column_width=True)

    st.write("Performing OCR...")
    ocr_text = perform_ocr(temp_input_path)

    st.write("OCR Result:")
    st.text_area("Extracted Text", ocr_text, height=300)

    # Clean up temporary file
    os.unlink(temp_input_path)

st.write("Upload a PDF to extract images and perform OCR.")

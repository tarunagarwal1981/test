import streamlit as st
import ocrmypdf
import fitz  # PyMuPDF
import tempfile
import os
from PIL import Image
import io

def process_pdf_with_ocr(input_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_output:
        ocrmypdf.ocr(input_file, temp_output.name, deskew=True, optimize=3, skip_text=True)
        return temp_output.name

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

st.title("PDF Image Extractor with OCR")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.write("Processing PDF with OCR...")
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_input:
        temp_input.write(uploaded_file.read())
        temp_input_path = temp_input.name

    # Process with OCR
    ocr_output_path = process_pdf_with_ocr(temp_input_path)

    st.write("Extracting images...")
    images = extract_images_from_pdf(ocr_output_path)

    st.write(f"Extracted {len(images)} images")

    for i, img in enumerate(images):
        st.image(img, caption=f"Image {i+1}", use_column_width=True)

    # Clean up temporary files
    os.unlink(temp_input_path)
    os.unlink(ocr_output_path)

st.write("Upload a PDF to extract images.")

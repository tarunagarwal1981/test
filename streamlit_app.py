import streamlit as st
import fitz  # PyMuPDF
import tempfile
import os
from PIL import Image
import io
import pytesseract
from pdf2image import convert_from_bytes

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
            if image.width > 50 and image.height > 50:
                images.append(image)
    doc.close()
    return images

def perform_ocr(pdf_bytes):
    images = convert_from_bytes(pdf_bytes)
    text = ""
    for i, image in enumerate(images):
        text += f"\n\n--- Page {i+1} ---\n\n"
        text += pytesseract.image_to_string(image)
    return text

st.title("PDF Image Extractor with OCR")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    pdf_bytes = uploaded_file.read()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(pdf_bytes)
        temp_pdf_path = temp_pdf.name

    st.write("Extracting images...")
    images = extract_images_from_pdf(temp_pdf_path)

    st.write(f"Extracted {len(images)} images")
    for i, img in enumerate(images):
        st.image(img, caption=f"Image {i+1}", use_column_width=True)

    st.write("Performing OCR...")
    try:
        ocr_text = perform_ocr(pdf_bytes)
        st.success("OCR processing completed successfully.")
        st.write("Extracted Text:")
        st.text_area("Text Content", ocr_text, height=300)
    except Exception as e:
        st.error(f"An error occurred during OCR processing: {str(e)}")

    # Clean up temporary file
    os.unlink(temp_pdf_path)

st.write("Upload a PDF to extract images and perform OCR.")

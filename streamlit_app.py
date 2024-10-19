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

def extract_images_and_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    images = []
    text = ""
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # Extract images
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            if image.width > 50 and image.height > 50:
                images.append(image)
        
        # Extract text
        text += f"\n\n--- Page {page_num + 1} ---\n\n"
        text += page.get_text()
    
    doc.close()
    return images, text

st.title("PDF Image Extractor with OCR")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.write("Processing PDF with OCR...")
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_input:
        temp_input.write(uploaded_file.read())
        temp_input_path = temp_input.name

    # Process with OCR
    try:
        ocr_output_path = process_pdf_with_ocr(temp_input_path)
        st.success("OCR processing completed successfully.")
    except Exception as e:
        st.error(f"An error occurred during OCR processing: {str(e)}")
        st.stop()

    st.write("Extracting images and text...")
    images, extracted_text = extract_images_and_text_from_pdf(ocr_output_path)

    st.write(f"Extracted {len(images)} images")

    for i, img in enumerate(images):
        st.image(img, caption=f"Image {i+1}", use_column_width=True)

    st.write("Extracted Text:")
    st.text_area("Text Content", extracted_text, height=300)

    # Clean up temporary files
    os.unlink(temp_input_path)
    os.unlink(ocr_output_path)

st.write("Upload a PDF to process with OCR and extract images and text.")

import streamlit as st
import fitz  # PyMuPDF
import tempfile
import os
from PIL import Image
import io

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
            images.append(image)
        
        # Extract text
        text += f"\n\n--- Page {page_num + 1} ---\n\n"
        text += page.get_text()
    
    doc.close()
    return images, text

st.title("PDF Image and Text Extractor")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_input:
        temp_input.write(uploaded_file.read())
        temp_input_path = temp_input.name

    st.write("Extracting images and text...")
    images, extracted_text = extract_images_and_text_from_pdf(temp_input_path)

    st.write(f"Extracted {len(images)} images")

    for i, img in enumerate(images):
        st.image(img, caption=f"Image {i+1}", use_column_width=True)

    st.write("Extracted Text:")
    st.text_area("Text Content", extracted_text, height=300)

    # Clean up temporary file
    os.unlink(temp_input_path)

st.write("Upload a PDF to extract images and text.")

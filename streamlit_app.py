import streamlit as st
import fitz  # PyMuPDF
import io
from PIL import Image
import numpy as np

def extract_images_from_pdf(doc):
    images = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # Method 1: Extract images using get_images()
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            images.append((f"Page {page_num + 1}, Image {img_index + 1} (Method 1)", image))
        
        # Method 2: Render page and extract as image
        pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))  # 300 DPI
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append((f"Page {page_num + 1}, Full Page (Method 2)", img))
    
    return images

st.title("Improved PDF Image Extractor for Technical Diagrams")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    with st.spinner("Extracting images..."):
        pdf_bytes = uploaded_file.read()
        
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            images = extract_images_from_pdf(doc)
        
        st.success(f"Extracted {len(images)} images")
        
        for img_name, img in images:
            st.subheader(img_name)
            st.image(img, use_column_width=True)
            
            # Add a download button for each image
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            st.download_button(
                label="Download this image",
                data=img_byte_arr,
                file_name=f"{img_name.replace(' ', '_').replace(',', '')}.png",
                mime="image/png"
            )

st.write("Upload a PDF to extract images, including technical diagrams and illustrations.")

import streamlit as st
import fitz  # PyMuPDF
import io
from PIL import Image
import numpy as np

def extract_images_from_page(page, page_num):
    images = []
    try:
        # Method 1: Extract images using get_images()
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            try:
                xref = img[0]
                base_image = page.parent.extract_image(xref)
                image_bytes = base_image["image"]
                image = Image.open(io.BytesIO(image_bytes))
                images.append((f"Page {page_num + 1}, Image {img_index + 1} (Method 1)", image))
            except Exception as e:
                st.warning(f"Could not extract image {img_index + 1} from page {page_num + 1}: {str(e)}")
        
        # Method 2: Render page and extract as image
        pix = page.get_pixmap(matrix=fitz.Matrix(150/72, 150/72))  # Reduced to 150 DPI
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append((f"Page {page_num + 1}, Full Page (Method 2)", img))
    except Exception as e:
        st.error(f"Error processing page {page_num + 1}: {str(e)}")
    
    return images

def process_pdf(doc):
    for page_num in range(len(doc)):
        st.write(f"Processing page {page_num + 1}...")
        page = doc[page_num]
        images = extract_images_from_page(page, page_num)
        
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

st.title("Robust PDF Image Extractor for Technical Diagrams")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            st.write(f"Processing PDF with {len(doc)} pages...")
            process_pdf(doc)
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")

st.write("Upload a PDF to extract images, including technical diagrams and illustrations.")

import streamlit as st
import fitz  # PyMuPDF
import io
from PIL import Image
import numpy as np
import cv2

def extract_images_from_page(page, page_num):
    # Render the page at a higher resolution
    zoom = 2  # Increase this for higher resolution
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    # Convert to numpy array and process
    img_np = np.array(img)
    gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
    
    # Threshold to separate text from graphics
    _, binary = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    
    # Find contours
    contours, _ = cv2.findContours(255 - binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    images = []
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        if w > 100 and h > 100:  # Filter out small contours
            roi = img_np[y:y+h, x:x+w]
            pil_img = Image.fromarray(roi)
            images.append((f"Page {page_num + 1}, Image {i + 1}", pil_img))
    
    return images

def process_pdf(doc):
    all_images = []
    for page_num in range(len(doc)):
        st.write(f"Processing page {page_num + 1}...")
        page = doc[page_num]
        images = extract_images_from_page(page, page_num)
        all_images.extend(images)
    return all_images

st.title("Advanced PDF Image Extractor")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            st.write(f"Processing PDF with {len(doc)} pages...")
            extracted_images = process_pdf(doc)
            
            st.success(f"Extracted {len(extracted_images)} images")
            
            for img_name, img in extracted_images:
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
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")

st.write("Upload a PDF to extract images, including complex diagrams and illustrations.")

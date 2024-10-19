import streamlit as st
import fitz  # PyMuPDF
import tempfile
import os
from PIL import Image
import io

def extract_text_and_images(pdf_path):
    doc = fitz.open(pdf_path)
    images = []
    full_text = ""
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # Extract text from the page
        page_text = page.get_text()
        full_text += f"\n\n--- Page {page_num + 1} ---\n\n{page_text}"
        
        # Extract images from the page
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            
            if image.width > 50 and image.height > 50:
                images.append((f"Page {page_num + 1}, Image {img_index + 1}", image))
    
    doc.close()
    return full_text, images

st.title("PDF Text and Image Extractor")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(uploaded_file.getvalue())
        temp_pdf_path = temp_pdf.name

    st.write("Extracting text and images...")
    try:
        extracted_text, extracted_images = extract_text_and_images(temp_pdf_path)
        st.success("Extraction completed successfully.")
        
        st.write("Extracted Text:")
        st.text_area("Text Content", extracted_text, height=300)

        st.write(f"Extracted {len(extracted_images)} images")
        for img_name, img in extracted_images:
            st.image(img, caption=img_name, use_column_width=True)

    except Exception as e:
        st.error(f"An error occurred during extraction: {str(e)}")

    # Clean up temporary file
    os.unlink(temp_pdf_path)

st.write("Upload a PDF to extract text and images separately.")

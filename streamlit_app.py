import streamlit as st
import fitz  # PyMuPDF
import io
from PIL import Image

def extract_images_from_page(page, page_num):
    images = []
    image_list = page.get_images(full=True)
    for img_index, img in enumerate(image_list):
        try:
            xref = img[0]
            base_image = page.parent.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            
            # Filter out very small images (likely to be icons or artifacts)
            if image.width > 100 and image.height > 100:
                images.append((f"Page {page_num + 1}, Image {img_index + 1}", image))
        except Exception as e:
            st.warning(f"Could not extract image {img_index + 1} from page {page_num + 1}: {str(e)}")
    return images

def process_pdf(doc):
    all_images = []
    for page_num in range(len(doc)):
        st.write(f"Processing page {page_num + 1}...")
        page = doc[page_num]
        images = extract_images_from_page(page, page_num)
        all_images.extend(images)
    
    return all_images

st.title("PDF Image Extractor for Embedded Images")

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

st.write("Upload a PDF to extract embedded images only.")

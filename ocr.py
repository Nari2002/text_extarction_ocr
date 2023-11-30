
import streamlit as st
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import tempfile
import os
import re

# OCR setup
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 

def perform_ocr(img_path):
    text = pytesseract.image_to_string(img_path)
    return text

def check_document_validity(text):
    # Example: Check if the document contains specific keywords or patterns
    keywords = ['confidential', 'do not duplicate', 'top secret']
    for keyword in keywords:
        if re.search(keyword, text, re.IGNORECASE):
            return False
    return True

def main():
    st.title("Document Verification App")
    st.write("Upload a document, and we'll perform checks to identify whether it's fraudulent or genuine.")

    # Upload document through Streamlit
    uploaded_file = st.file_uploader("Choose a document...", type=["jpg", "jpeg", "png", "pdf"])

    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
         
            images = convert_from_path(uploaded_file, 500)
            for i, img in enumerate(images):
               
                img_path = os.path.join(tempfile.gettempdir(), f"temp_page_{i + 1}.png")
                img.save(img_path)
                st.image(img, caption=f"Page {i + 1}", use_column_width=True)
                text = perform_ocr(img_path)
                st.write(f"OCR Result (Page {i + 1}): {text}")
                is_valid = check_document_validity(text)
                st.write(f"Document Validity (Page {i + 1}): {'Genuine' if is_valid else 'Fraudulent'}")
                os.remove(img_path)
        else:
           
            img = Image.open(uploaded_file)
            img_path = os.path.join(tempfile.gettempdir(), "temp_image.png")
            img.save(img_path)
            st.image(img, caption="Uploaded Document", use_column_width=True)
            text = perform_ocr(img_path)
            st.write(f"OCR Result: {text}")
            is_valid = check_document_validity(text)
            st.write(f"Document Validity: {'Genuine' if is_valid else 'Fraudulent'}")
           
            os.remove(img_path)

if __name__ == "__main__":
    main()

from app.ai import classify_image
import streamlit as st
from PIL import Image

st.title("Nutrition Facts Extractor")
st.markdown(
    """
Upload an image containing nutrition facts, and the system will extract and display the information in a structured format.
"""
)

uploaded_file = st.file_uploader("Upload an image file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    st.write("Extracting nutrition facts...")
    try:
        result = classify_image(image)
        st.write("### Extracted Nutrition Facts:")
        if isinstance(result, dict) and result:
            st.json(result)
        else:
            st.warning("No nutrition facts were detected in the image.")
    except Exception as e:
        st.error(f"An error occurred while processing the image: {e}")

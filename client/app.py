import streamlit as st

def run_client():
    st.title("PlantPal")
    st.write("Welcome to PlantPal! Upload an image of your plant to identify it and check for diseases.")

    # Image upload option
    uploaded_file = st.file_upload("Choose a plant image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption='Uploaded Plant Image', use_column_width=True)
        st.write("Analyzing...")
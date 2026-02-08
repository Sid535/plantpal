import streamlit as st
from server.analyzer import analyze_plant_image

def run_client():
    st.title("PlantPal")
    st.write("Welcome to PlantPal! Upload an image of your plant to identify it and check for diseases.")

    uploaded_file = st.file_uploader("Choose a plant image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption='Uploaded Plant Image', use_container_width=True)
        
        # Trigger the analysis
        if st.button("Analyze Plant"):
            with st.spinner('Analyzing...'):
                results = analyze_plant_image(uploaded_file)
                
                st.success("Analysis Complete!")
                st.subheader(f"Plant: {results['plant_name']}")
                st.write(f"**Condition:** {results['condition']}")
                st.write(f"**Recommended Treatment:** {results['treatment']}")

if __name__ == "__main__":
    run_client()
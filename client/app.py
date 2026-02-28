import streamlit as st
from server.analyzer import analyze_plant_image

def run_client():
    # Set page configuration for a professional look
    st.set_page_config(
        page_title="PlantPal | Smart Health Assistant",
        page_icon="🌿",
        layout="centered"
    )

    # Custom CSS for styling
    st.markdown("""
        <style>
        .main {
            background-color: #f5f7f9;
        }
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
            background-color: #2e7d32;
            color: white;
        }
        .result-card {
            padding: 20px;
            border-radius: 10px;
            background-color: white;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    # Header section
    st.title("🌿 PlantPal")
    st.markdown("### AI-Powered Plant Disease Diagnostic Tool")
    st.write("Upload a photo of your plant's leaves to identify potential health issues and get treatment advice.")

    st.divider()

    # Layout: Sidebar for inputs to keep the main area clean
    with st.sidebar:
        st.header("Diagnosis Settings")
        plant_type = st.selectbox(
            "Target Plant Species", 
            ["Tomato", "Apple", "Corn"],
            help="Select the specific plant type to improve model accuracy."
        )
        st.info("Ensure the leaf is well-lit and centered in the frame for best results.")

    # Main area for file upload
    uploaded_file = st.file_uploader(
        "Drop your plant image here", 
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        # Create columns for image and results
        col1, col2 = st.columns([1, 1], gap="medium")

        with col1:
            st.image(
                uploaded_file, 
                caption='Uploaded Leaf Sample', 
                use_container_width=True
            )
        
        with col2:
            if st.button("🔍 Run Analysis"):
                with st.spinner('Accessing Neural Network...'):
                    results = analyze_plant_image(uploaded_file, plant_type)
                
                if results:
                    st.success("Analysis Complete!")
                    
                    # Displaying results in an organized way
                    st.markdown("#### Diagnosis Results")
                    st.metric("Detected Plant", results['plant_name'])
                    
                    # Highlighting the condition
                    condition_color = "red" if "healthy" not in results['condition'].lower() else "green"
                    st.markdown(f"**Health Status:** :{condition_color}[{results['condition']}]")
                    
                    st.markdown("---")
                    st.markdown("** Recommended Treatment:**")
                    st.write(results['treatment'])
                else:
                    st.error("Model Error: Could not process the image.")

    # Footer
    # st.markdown("---")
    # st.caption("Disclaimer: PlantPal provides AI-generated insights. For commercial farming, consult an agronomist.")

if __name__ == "__main__":
    run_client()
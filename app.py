import streamlit as st
import face_recognition
import numpy as np
from PIL import Image
import requests
import os
from io import BytesIO
import glob

st.set_page_config(page_title="Face Recognition App", layout="wide")

st.title("🔍 Face Recognition App")
st.markdown("Compare faces to determine if two photos contain the same person")

# Tabs for different modes
tab1, tab2, tab3 = st.tabs(["Upload Photos", "Remote URLs", "Compare Folder"])

# ============= TAB 1: Upload Photos =============
with tab1:
    st.header("Upload Two Photos")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Photo 1")
        photo1 = st.file_uploader("Choose first photo", type=["jpg", "jpeg", "png"], key="photo1")
    
    with col2:
        st.subheader("Photo 2")
        photo2 = st.file_uploader("Choose second photo", type=["jpg", "jpeg", "png"], key="photo2")
    
    if st.button("Compare Photos", key="compare_upload"):
        if photo1 and photo2:
            try:
                # Load images
                image1 = face_recognition.load_image_file(photo1)
                image2 = face_recognition.load_image_file(photo2)
                
                # Get face encodings
                face_encodings1 = face_recognition.face_encodings(image1)
                face_encodings2 = face_recognition.face_encodings(image2)
                
                if len(face_encodings1) == 0 or len(face_encodings2) == 0:
                    st.error("❌ No face detected in one or both images. Please try different photos.")
                else:
                    # Compare faces
                    results = face_recognition.compare_faces([face_encodings1[0]], face_encodings2[0])
                    distance = face_recognition.face_distance([face_encodings1[0]], face_encodings2[0])[0]
                    
                    # Display results
                    col1_result, col2_result = st.columns(2)
                    with col1_result:
                        st.image(photo1, caption="Photo 1", use_column_width=True)
                    with col2_result:
                        st.image(photo2, caption="Photo 2", use_column_width=True)
                    
                    if results[0]:
                        st.success(f"✅ **SAME FACE DETECTED!** (Confidence: {(1-distance)*100:.2f}%)")
                    else:
                        st.warning(f"❌ **DIFFERENT FACES** (Similarity: {(1-distance)*100:.2f}%)")
                    
                    st.info(f"Face Distance Score: {distance:.4f} (Lower = More Similar)")
            
            except Exception as e:
                st.error(f"Error processing images: {str(e)}")
        else:
            st.warning("Please upload both photos")

# ============= TAB 2: Remote URLs =============
with tab2:
    st.header("Compare Photos from URLs")
    
    url1 = st.text_input("URL of Photo 1", placeholder="https://example.com/photo1.jpg")
    url2 = st.text_input("URL of Photo 2", placeholder="https://example.com/photo2.jpg")
    
    if st.button("Compare URLs", key="compare_urls"):
        if url1 and url2:
            try:
                with st.spinner("Downloading images..."):
                    # Download images from URLs
                    response1 = requests.get(url1, timeout=10)
                    response2 = requests.get(url2, timeout=10)
                    
                    image1_pil = Image.open(BytesIO(response1.content))
                    image2_pil = Image.open(BytesIO(response2.content))
                    
                    # Convert to numpy arrays for face_recognition
                    image1 = np.array(image1_pil)
                    image2 = np.array(image2_pil)
                    
                    # Get face encodings
                    face_encodings1 = face_recognition.face_encodings(image1)
                    face_encodings2 = face_recognition.face_encodings(image2)
                    
                    if len(face_encodings1) == 0 or len(face_encodings2) == 0:
                        st.error("❌ No face detected in one or both images.")
                    else:
                        # Compare faces
                        results = face_recognition.compare_faces([face_encodings1[0]], face_encodings2[0])
                        distance = face_recognition.face_distance([face_encodings1[0]], face_encodings2[0])[0]
                        
                        # Display results
                        col1_result, col2_result = st.columns(2)
                        with col1_result:
                            st.image(image1_pil, caption="Photo 1", use_column_width=True)
                        with col2_result:
                            st.image(image2_pil, caption="Photo 2", use_column_width=True)
                        
                        if results[0]:
                            st.success(f"✅ **SAME FACE DETECTED!** (Confidence: {(1-distance)*100:.2f}%)")
                        else:
                            st.warning(f"❌ **DIFFERENT FACES** (Similarity: {(1-distance)*100:.2f}%)")
                        
                        st.info(f"Face Distance Score: {distance:.4f} (Lower = More Similar)")
            
            except Exception as e:
                st.error(f"Error downloading/processing images: {str(e)}")
        else:
            st.warning("Please enter both URLs")

# ============= TAB 3: Compare Folder =============
with tab3:
    st.header("Compare All Photos in a Folder")
    
    # Create sample folder structure
    sample_folder = "sample_photos"
    if not os.path.exists(sample_folder):
        os.makedirs(sample_folder)
    
    st.info("📁 **Instructions:**")
    st.markdown("""
    1. Create a folder named `sample_photos` in the same directory as this app
    2. Place your photos (jpg, jpeg, png) in that folder
    3. This will automatically compare all photos and identify matching faces
    """)
    
    if st.button("Scan Folder for Matching Faces"):
        # Get all image files
        image_files = glob.glob(os.path.join(sample_folder, "*.jpg")) + \
                     glob.glob(os.path.join(sample_folder, "*.jpeg")) + \
                     glob.glob(os.path.join(sample_folder, "*.png"))
        
        if len(image_files) == 0:
            st.warning(f"❌ No images found in '{sample_folder}' folder")
        else:
            st.success(f"Found {len(image_files)} image(s)")
            
            try:
                with st.spinner("Processing images..."):
                    # Load all images and get encodings
                    face_data = {}
                    for img_path in image_files:
                        image = face_recognition.load_image_file(img_path)
                        encodings = face_recognition.face_encodings(image)
                        if len(encodings) > 0:
                            face_data[img_path] = encodings[0]
                    
                    if len(face_data) == 0:
                        st.error("❌ No faces detected in any images")
                    else:
                        st.success(f"✅ Detected faces in {len(face_data)} image(s)")
                        
                        # Compare all pairs
                        results_data = []
                        image_list = list(face_data.keys())
                        
                        for i in range(len(image_list)):
                            for j in range(i+1, len(image_list)):
                                img1_name = os.path.basename(image_list[i])
                                img2_name = os.path.basename(image_list[j])
                                
                                distance = face_recognition.face_distance(
                                    [face_data[image_list[i]]], 
                                    face_data[image_list[j]]
                                )[0]
                                
                                is_same = distance < 0.6  # Threshold
                                
                                results_data.append({
                                    "Photo 1": img1_name,
                                    "Photo 2": img2_name,
                                    "Same Face?": "✅ Yes" if is_same else "❌ No",
                                    "Distance": f"{distance:.4f}",
                                    "Confidence": f"{(1-distance)*100:.2f}%"
                                })
                        
                        # Display results in table
                        st.subheader("Comparison Results")
                        st.dataframe(results_data, use_container_width=True)
                        
                        # Summary
                        matching_pairs = sum(1 for r in results_data if "Yes" in r["Same Face?"])
                        st.success(f"Found {matching_pairs} matching face pair(s) out of {len(results_data)} comparisons")
            
            except Exception as e:
                st.error(f"Error processing folder: {str(e)}")

# ============= Footer =============
st.markdown("---")
st.markdown("""
**How it works:**
- Extracts unique facial features from each photo
- Compares the features using deep learning
- Distance score < 0.6 = Same face | Distance score ≥ 0.6 = Different faces
- Supports local uploads, remote URLs, and folder batch processing
""")

# Setup Guide - Face Recognition App

## Step-by-Step Installation

### Step 1: Install Python
- Download Python 3.8+ from [python.org](https://www.python.org/)
- Make sure to check "Add Python to PATH" during installation

### Step 2: Clone or Download the Repository
```bash
git clone https://github.com/pochanee/face-recognition-app.git
cd face-recognition-app
```

Or download as ZIP and extract it.

### Step 3: Create Virtual Environment (Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

⏳ This may take 5-10 minutes as it downloads the face recognition models.

### Step 5: Run the Application
```bash
streamlit run app.py
```

The web app should automatically open in your browser at `http://localhost:8501`

---

## Using Each Mode

### 📤 Mode 1: Upload Photos

1. Go to the **"Upload Photos"** tab
2. Click on "Choose first photo" and select an image file
3. Click on "Choose second photo" and select another image file
4. Click **"Compare Photos"** button
5. View the results:
   - ✅ **Same Face**: If confidence is high
   - ❌ **Different Faces**: If confidence is low
   - **Confidence %**: How sure the app is

**Tips:**
- Use clear, face-forward photos
- JPG/PNG formats work best
- 100x100 pixels minimum resolution

---

### 🔗 Mode 2: Remote URLs

1. Go to the **"Remote URLs"** tab
2. Paste the URL of the first photo in the first box
   - Example: `https://example.com/photo1.jpg`
3. Paste the URL of the second photo in the second box
4. Click **"Compare URLs"** button
5. Wait for download and processing
6. View results

**Tips:**
- URLs must be publicly accessible
- Direct image links work best (ends with .jpg/.png)
- No login/authentication required for the URLs

**Example URLs:**
- Direct GitHub raw images
- Public image hosting sites (Imgur, etc.)
- AWS S3 public images

---

### 📁 Mode 3: Batch Folder Comparison

1. **Create a folder named `sample_photos`** in the same directory as `app.py`
   ```
   face-recognition-app/
   ├── app.py
   ├── sample_photos/  ← Create this folder
   └── requirements.txt
   ```

2. **Add photos to the folder**
   - Copy 2+ photos (jpg, jpeg, png) into `sample_photos/`
   - Examples:
     ```
     sample_photos/
     ├── person1_photo1.jpg
     ├── person1_photo2.jpg
     ├── person2_photo1.jpg
     └── person2_photo2.jpg
     ```

3. Go to the **"Compare Folder"** tab

4. Click **"Scan Folder for Matching Faces"**

5. View the results table showing:
   - Photo 1 name
   - Photo 2 name
   - Whether they're the same face
   - Distance score (0-1)
   - Confidence percentage

**Tips:**
- The app compares every pair of photos
- 5 photos = 10 comparisons
- Keep folder under 100 images for faster processing
- Higher distance = more different faces

---

## Understanding Results

### Distance Score
- **0.0 - 0.3**: Very Similar (Same Person) ✅
- **0.3 - 0.6**: Similar (Likely Same Person) ✅
- **0.6 - 1.0**: Not Similar (Different Persons) ❌

### Confidence Score
- **70% - 100%**: Very Confident Same Face ✅
- **50% - 70%**: Somewhat Confident
- **0% - 50%**: Not the Same Face ❌

### Example Results
```
Photo 1: john_pic1.jpg
Photo 2: john_pic2.jpg
Result: ✅ SAME FACE DETECTED! (Confidence: 85%)
Distance: 0.28
```

---

## Troubleshooting

### Issue: "No module named 'face_recognition'"
**Solution:**
```bash
pip install --upgrade face-recognition
```

### Issue: "No face detected in image"
**Causes:**
- Photo is blurry
- Face is too small
- Face is angled away
- Image quality is poor

**Solutions:**
- Use clearer photos
- Ensure face is front-facing
- Use higher resolution images

### Issue: "SSL certificate error" when using URLs
**Solution:**
- Make sure URL is correct
- Try using `http://` instead of `https://`
- Download image and upload instead

### Issue: App is very slow
**Causes:**
- Too many images in folder
- Low RAM on computer
- Large image files

**Solutions:**
- Compare fewer photos at a time
- Use smaller resolution images
- Close other applications

### Issue: Python not found
**Solution:**
- Add Python to PATH or restart computer
- Use `python3` instead of `python` (macOS/Linux)

---

## Advanced Tips

### Batch Processing Large Folders
For 50+ photos, consider splitting into smaller batches:
```
sample_photos/
├── batch1/
│   ├── photo1.jpg
│   └── photo2.jpg
├── batch2/
│   ├── photo3.jpg
│   └── photo4.jpg
```

### Using Command-Line Arguments
```bash
streamlit run app.py --logger.level=debug  # Show debug info
streamlit run app.py --client.maxMessageSize=2000  # For large images
```

### Adjusting Sensitivity
The threshold (0.6) can be modified in `app.py`:
```python
is_same = distance < 0.5  # More strict (fewer matches)
is_same = distance < 0.7  # More lenient (more matches)
```

---

## Next Steps

1. ✅ Install and run the app
2. 🧪 Test with sample photos
3. 📖 Read the results carefully
4. 🔄 Experiment with different photo types
5. 🚀 Use it for your project!

---

## Need Help?

- Check the README.md file
- Review the code comments in app.py
- Check troubleshooting section above
- Create an issue on GitHub

Happy face comparing! 🎉

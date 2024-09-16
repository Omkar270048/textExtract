# text_extractor.py
import google.generativeai as genai
from config import GEMINI_API_KEY
from datetime import datetime

# Configure the API key for authentication
genai.configure(api_key=GEMINI_API_KEY)

def extract_text_from_image(image_path: str) -> str:
    """
    Extracts text from the given image using Google's generative AI model.

    :param image_path: Path to the image file.
    :return: Extracted text from the image.
    """
    start = datetime.now()
    
    try:
        # Upload the image file
        myfile = genai.upload_file(image_path)
        print(f"Uploaded file: {myfile}")
        
        # Initialize the model
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Generate content (text extraction from image)
        result = model.generate_content(
            [myfile, "\n\n", "extract text from image"]
        )
        
        # Get the extracted text
        extracted_text = result.text if result.text else "No text extracted."
        
    except Exception as e:
        extracted_text = f"Error during text extraction: {str(e)}"
    
    end = datetime.now()
    print("Time taken:", (end - start))
    
    return extracted_text

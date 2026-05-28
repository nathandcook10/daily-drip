import os
import requests
import shutil

try:
    from google import genai
    from google.genai import types
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

PIPELINE_DIR = "pipeline_staging"

def setup_directory():
    if not os.path.exists(PIPELINE_DIR):
        os.makedirs(PIPELINE_DIR)
        print(f"Created directory: {PIPELINE_DIR}/")

def generate_concepts(prompt):
    print(f"\n[API] Generating 3 concepts for: '{prompt}'...")
    concept_paths = []
    
    if HAS_GENAI and os.environ.get("GEMINI_API_KEY"):
        client = genai.Client()
        try:
            print("Generating images with Imagen 3...")
            response = client.models.generate_images(
                model="imagen-3.0-generate-002",
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=3,
                    aspect_ratio="1:1",
                    output_mime_type="image/png"
                )
            )
            for i, generated_image in enumerate(response.generated_images, start=1):
                filename = f"concept_{i}.png"
                filepath = os.path.join(PIPELINE_DIR, filename)
                
                # google-genai returns a PIL Image in the .image property
                generated_image.image.save(filepath)
                concept_paths.append(filepath)
                print(f"Concept {i} saved to: {filepath}")
                
            return concept_paths
        except Exception as e:
            print(f"Error during Gemini API generation: {e}")
            print("Falling back to placeholder images for demonstration.")
    else:
        print("Gemini API key or library not found. Using placeholder images.")
        print("To use real generation, ensure 'google-genai' and 'pillow' are installed (pip install google-genai pillow)")
        print("and set your environment variable: export GEMINI_API_KEY='your-key-here'")
        
    # Fallback / Mock behavior using placehold.co
    urls = [
        f"https://placehold.co/1024x1024.png?text=Concept+1",
        f"https://placehold.co/1024x1024.png?text=Concept+2",
        f"https://placehold.co/1024x1024.png?text=Concept+3"
    ]
    
    for i, url in enumerate(urls, start=1):
        filename = f"concept_{i}.png"
        filepath = os.path.join(PIPELINE_DIR, filename)
        try:
            r = requests.get(url, stream=True)
            r.raise_for_status()
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            concept_paths.append(filepath)
            print(f"Concept {i} saved to: {filepath}")
        except Exception as e:
            print(f"Failed to download image from {url}: {e}")
            
    return concept_paths

def main():
    setup_directory()
    print("=== Phase 1: T-Shirt Design Generator ===")
    brief = input("Enter your initial design brief: ")
    
    current_prompt = brief
    
    while True:
        concept_paths = generate_concepts(current_prompt)
        
        if not concept_paths:
            print("Failed to generate concepts. Exiting.")
            break
                
        print("\n" + "="*40)
        print("REVIEW REQUIRED")
        print(f"Please open the images in the {PIPELINE_DIR}/ folder to review.")
        print("Options:")
        print(" - Enter '1', '2', or '3' to approve a concept.")
        print(" - Enter any other text to provide feedback and regenerate.")
        print(" - Enter 'q' to quit.")
        
        user_input = input("\nYour choice or feedback: ").strip()
        
        if user_input.lower() == 'q':
            print("Exiting pipeline.")
            break
            
        if user_input in ['1', '2', '3']:
            chosen_index = int(user_input) - 1
            
            if chosen_index >= len(concept_paths):
                print("Invalid choice. Try again.")
                continue
                
            chosen_path = concept_paths[chosen_index]
            final_path = os.path.join(PIPELINE_DIR, "approved_design.png")
            
            # Copy the approved concept to approved_design.png
            shutil.copy2(chosen_path, final_path)
            
            print(f"\nSuccess! Concept {user_input} approved.")
            print(f"Final design saved to: {final_path}")
            
            # Clean up concept files
            for path in concept_paths:
                if os.path.exists(path):
                    os.remove(path)
            
            print("Phase 1 Complete.")
            break
        else:
            print("\nFeedback received. Refining prompt...")
            # Refine the prompt based on feedback
            current_prompt = f"Original brief: {brief}\nMake sure to incorporate this new feedback: {user_input}"

if __name__ == "__main__":
    main()

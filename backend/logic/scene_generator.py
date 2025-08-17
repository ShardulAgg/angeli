# 이미지 종류는 이것이것이것 중에서 사용할수 있다.

import os
import yaml
import base64
from typing import List, Dict, Any
from google import genai
from google.genai import types
import PIL.Image
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

abs_path = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(abs_path, "..", "assets")


def load_influencer_info(influencer_name: str) -> Dict[str, Any]:
    """Load influencer information from YAML file.
    
    Args:
        influencer_name: Name of the influencer
        
    Returns:
        Dictionary containing influencer information
        
    Raises:
        FileNotFoundError: If influencer info file doesn't exist
        ValueError: If influencer name is invalid
    """
    influencers_dir = os.path.join(ASSETS_DIR, "influencers")
    influencer_path = os.path.join(influencers_dir, influencer_name.lower(), "info.yaml")
    
    if not os.path.exists(influencer_path):
        raise FileNotFoundError(f"Influencer info not found at: {influencer_path}")
    
    with open(influencer_path, 'r', encoding='utf-8') as f:
        influencer_data = yaml.safe_load(f)
    
    return influencer_data


def get_influencer_image_path(influencer_name: str, image_type: str = "full_body") -> str:
    """Get the path to an influencer's image.
    
    Args:
        influencer_name: Name of the influencer
        image_type: Type of image (full_body, portrait, inside_bedroom)
        
    Returns:
        Path to the influencer image
    """
    influencers_dir = os.path.join(ASSETS_DIR, "influencers")
    image_path = os.path.join(influencers_dir, influencer_name.lower(), "images", f"{image_type}.png")
    
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Influencer image not found at: {image_path}")
    
    return image_path


def load_product_info(product_name: str) -> Dict[str, Any]:
    """Load product information from YAML file.
    
    Args:
        product_name: Name of the product (should match directory name)
        
    Returns:
        Dictionary containing product information
        
    Raises:
        FileNotFoundError: If product info file doesn't exist
    """
    products_dir = os.path.join(ASSETS_DIR, "products")
    product_path = os.path.join(products_dir, product_name.lower(), "info.yaml")
    
    if not os.path.exists(product_path):
        raise FileNotFoundError(f"Product info not found at: {product_path}")
    
    with open(product_path, 'r', encoding='utf-8') as f:
        product_data = yaml.safe_load(f)
    
    return product_data


def get_product_image_path(product_name: str, image_name: str = None) -> str:
    """Get the path to a product image.
    
    Args:
        product_name: Name of the product
        image_name: Specific image name (if None, looks for common names)
        
    Returns:
        Path to the product image
    """
    products_dir = os.path.join(ASSETS_DIR, "products")
    product_images_dir = os.path.join(products_dir, product_name.lower(), "images")
    
    if image_name:
        image_path = os.path.join(product_images_dir, image_name)
    else:
        # Try common image names
        common_names = [f"{product_name.lower()}.png", "main.png", "product.png"]
        for name in common_names:
            image_path = os.path.join(product_images_dir, name)
            if os.path.exists(image_path):
                break
        else:
            raise FileNotFoundError(f"No product image found in: {product_images_dir}")
    
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Product image not found at: {image_path}")
    
    return image_path


def create_product_data_from_form(product_name: str, brand_name: str, brand_personality: str, meme_type: str) -> Dict[str, Any]:
    """Create product data structure from form parameters.
    
    Args:
        product_name: Name of the product
        brand_name: Name of the brand
        brand_personality: Personality traits of the brand
        meme_type: Type of meme to generate
        
    Returns:
        Dictionary containing product information in expected format
    """
    return {
        'product': {
            'name': product_name,
            'brand': brand_name,
            'category': 'product'
        },
        'features': {
            'key_features': [f"High-quality {product_name}", "Trendy design", "Perfect for content creation"]
        },
        'marketing_angles': {
            'lifestyle': [f"Perfect for {meme_type} content", "Trendy and stylish", "Content creator approved"],
            'technical': ["Premium quality", "Durable design"],
            'emotional': ["Express yourself", "Feel confident", "Stand out"]
        },
        'content_themes': {
            'lifestyle': [f"{meme_type} content", "Daily routine", "Style showcase"],
            'entertainment': ["Fun moments", "Creative content", "Viral potential"]
        },
        'viral_potential': {
            'trends': [f"{meme_type} trend", "Product showcase", "Lifestyle content"],
            'challenges': [f"{brand_name} challenge", f"{product_name} styling", "Creative showcase"]
        },
        'brand_personality': brand_personality
    }


def create_personalized_storyboard_prompt(influencer_data: Dict[str, Any], product_data: Dict[str, Any]) -> str:
    """Create a personalized storyboard system prompt based on influencer and product data."""
    
    # Influencer info
    personality_traits = ", ".join(influencer_data.get('personality', {}).get('traits', []))
    content_focus = ", ".join(influencer_data.get('content_focus', []))
    brand_voice_tone = influencer_data.get('brand_voice', {}).get('tone', 'engaging')
    brand_voice_style = influencer_data.get('brand_voice', {}).get('style', 'casual')
    content_style = influencer_data.get('influencer', {}).get('content_style', 'lifestyle content')
    influencer_name = influencer_data.get('influencer', {}).get('name', 'the influencer')
    
    # Product info
    product_name = product_data.get('product', {}).get('name', 'the product')
    product_category = product_data.get('product', {}).get('category', '')
    key_features = ", ".join(product_data.get('features', {}).get('key_features', []))
    
    # Marketing angles that match influencer style
    lifestyle_angles = product_data.get('marketing_angles', {}).get('lifestyle', [])
    technical_angles = product_data.get('marketing_angles', {}).get('technical', [])
    emotional_angles = product_data.get('marketing_angles', {}).get('emotional', [])
    
    # Content themes that could work
    content_themes = []
    for theme_category in product_data.get('content_themes', {}).values():
        if isinstance(theme_category, list):
            content_themes.extend(theme_category)
    
    # Viral potential
    viral_trends = ", ".join(product_data.get('viral_potential', {}).get('trends', []))
    viral_challenges = ", ".join(product_data.get('viral_potential', {}).get('challenges', []))
    
    # Get brand personality from product data
    brand_personality_text = product_data.get('brand_personality', 'fun and engaging')
    
    return f"""
You are a viral meme storyboard expert creating {', '.join(content_themes[:2])} content for {influencer_name}.

Influencer Profile:
- Type: {influencer_data.get('influencer', {}).get('type', 'Influencer')}
- Content Style: {content_style}
- Personality Traits: {personality_traits}
- Content Focus: {content_focus}
- Brand Voice: {brand_voice_tone}, {brand_voice_style}
- Target Audience: {influencer_data.get('audience', {}).get('primary', 'general audience')}

Product & Brand Profile:
- Product: {product_name}
- Brand: {product_data.get('product', {}).get('brand', 'Brand')}
- Brand Personality: {brand_personality_text}
- Category: {product_category}
- Key Features: {key_features}
- Marketing Angles: {', '.join(lifestyle_angles[:3])}
- Viral Trends: {viral_trends}
- Content Themes: {', '.join(content_themes[:5])}

Create a storyboard for a {', '.join(content_themes[:1])} meme that:
1. Authentically showcases {product_name} from {product_data.get('product', {}).get('brand', 'the brand')} through {influencer_name}'s unique lens
2. Reflects the brand's {brand_personality_text} personality
3. Leverages {influencer_name}'s {content_style} expertise
4. Incorporates relevant product features naturally in a {', '.join(content_themes[:1])} format
5. Taps into current viral trends and challenges
6. Appeals to both {influencer_name}'s audience and the brand's target market
7. Creates an engaging 8-second video with exactly 3 scenes
8. Feels genuine to {influencer_name}'s established persona
9. Embodies the {brand_personality_text} brand personality throughout

Consider these viral opportunities: {viral_challenges}
Focus on these content angles: {', '.join(content_themes[:3])}
Meme Style: Emphasize {', '.join(content_themes[:1])} elements that showcase both the product and brand personality
"""

STORYBOARD_OUTPUT_INSTRUCTION = """
Output the storyboard in the following format:

Storyboard format:
1.	Scene description (background, character positions)
2.	Character expressions/poses
3.	Visual effects or points of emphasis

IMPORTANT:
1. DO NOT INCLUDE ANY TEXT(text overlay) IN THE STORYBOARD.
"""

IMAGE_GENERATION_PROMPT = """
Create a scene image with applying second image in first image given below information: 

{storyboard_item}

IMPORTANT:
1. NOT TO INCLUDE ANY TEXT IN IMAGE.


"""
# Get GENAI_API_KEY from environment variables
GENAI_API_KEY = os.getenv("GENAI_API_KEY")


def generate_storyboard_scenes_gemini(product_image,
                                      product_name: str,
                                      brand_name: str,
                                      brand_personality: str,
                                      influencer_name: str,
                                      meme_type: str):
    """Generate storyboard scenes and create images using Gemini.
    
    Args:
        product_image: Uploaded product image file
        product_name: Name of the product for the storyboard
        brand_name: Name of the brand
        brand_personality: Personality traits of the brand
        influencer_name: Name of the influencer
        meme_type: Type of meme to generate
    """
    
    # Load influencer information (still needed for image)
    try:
        influencer_data = load_influencer_info(influencer_name)
        influencer_image_path = get_influencer_image_path(influencer_name, "full_body")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error loading influencer data: {e}")
        return
    
    # Create product data from form parameters
    product_data = create_product_data_from_form(product_name, brand_name, brand_personality, meme_type)
    
    # Check if API key is available
    if not GENAI_API_KEY:
        raise ValueError("GENAI_API_KEY is not set in environment variables. Please check your .env file.")
    
    client = genai.Client(api_key=GENAI_API_KEY)

    # Create personalized storyboard prompt with product context
    personalized_system_prompt = create_personalized_storyboard_prompt(influencer_data, product_data)
    
    # Generate storyboard using Gemini text generation with full context
    context_prompt = f"""
Product: {product_data.get('product', {}).get('name', product_name)} ({product_data.get('product', {}).get('category', '')})
Influencer: {influencer_data.get('influencer', {}).get('name', influencer_name)}

Key Product Features to Highlight: {', '.join(product_data.get('features', {}).get('key_features', [])[:3])}
Suggested Content Angles: {', '.join(list(product_data.get('content_themes', {}).get('lifestyle', []))[:2])}
Viral Opportunity: {', '.join(product_data.get('viral_potential', {}).get('trends', [])[:2])}

Create a storyboard that:
- Showcases {product_name} authentically through {influencer_data.get('influencer', {}).get('name', influencer_name)}'s lens
- Incorporates their content expertise: {', '.join(influencer_data.get('content_focus', []))}
- Leverages current trends and viral potential
- Feels natural to their established style and audience
"""
    
    storyboard_prompt = f"""
    {personalized_system_prompt}
    
    {STORYBOARD_OUTPUT_INSTRUCTION}
    
    Please format each scene like this:
    SCENE 1:
    Description: [scene description that fits {influencer_data.get('influencer', {}).get('name', influencer_name)}'s style]
    Character Expression: [expression matching their personality]
    Visual Effects: [visual effects that align with their brand aesthetic]
    
    SCENE 2:
    Description: [scene description that fits {influencer_data.get('influencer', {}).get('name', influencer_name)}'s style]
    Character Expression: [expression matching their personality]
    Visual Effects: [visual effects that align with their brand aesthetic]
    """
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=storyboard_prompt
    )
    
    # Parse the plain text response
    storyboard_items = []
    scenes = response.text.split('SCENE ')[1:]  # Skip empty first element
    for scene in scenes:
        lines = scene.strip().replace("\n", "")
        storyboard_items.append(lines)

    # Load images for Gemini
    # Handle product image - can be a file path, None, or PIL Image
    if product_image:
        if isinstance(product_image, str):
            # It's a file path
            product_img = PIL.Image.open(product_image)
        elif isinstance(product_image, PIL.Image.Image):
            # It's already a PIL Image
            product_img = product_image
        else:
            # Try to open it as a file-like object
            product_img = PIL.Image.open(product_image)
    else:
        # No product image provided, create a placeholder or skip
        # For now, we'll create a simple placeholder image
        product_img = PIL.Image.new('RGB', (512, 512), color='white')
    
    influencer_img = PIL.Image.open(influencer_image_path)

    # Create output directory if it doesn't exist
    output_dir = os.path.join(ASSETS_DIR, "outputs", product_name, influencer_name)
    os.makedirs(output_dir, exist_ok=True)

    # save storyboard text into file
    with open(os.path.join(output_dir, "storyboard.txt"), "w") as f:
        f.write("\n".join(storyboard_items))

    for i, storyboard_item in enumerate(storyboard_items):
        print("Description: ", storyboard_item)

        # Generate scene image using Gemini with image generation capability
        image_prompt = IMAGE_GENERATION_PROMPT.format(
            storyboard_item=storyboard_item
        )
        try:
            # Use Gemini's multimodal generation with image output
            img_result = client.models.generate_content(
                model="gemini-2.0-flash-preview-image-generation",
                contents=[
                    image_prompt,
                    influencer_img,
                    product_img
                ],
                config=types.GenerateContentConfig(
                    response_modalities=['TEXT', 'IMAGE']
                )
            )
            
            # Process the generated images
            for j, part in enumerate(img_result.candidates[0].content.parts):
                if part.inline_data:
                    # Save the generated image
                    image_data = part.inline_data.data
                    with open(f"{output_dir}/storyboard.png", "wb") as f:
                        f.write(image_data)
                    print(f"Saved image: storyboard.png")
                    break
                    
        except Exception as e:
            print(f"Error generating image for scene {i+1}: {e}")
        break

    return storyboard_items, os.path.join(output_dir, "storyboard.png")


if __name__ == "__main__":
    # Example usage - replace with your actual values
    influencer_name = "angeli"  # or "agiverse"
    product_name = "dress"
    brand_name = "FashionBrand"
    brand_personality = "trendy, youthful, and confident"
    meme_type = "GRWM"  # Get Ready With Me
    
    # For testing, you would need to provide an actual image file
    product_image = open("../assets/products/dress/images/product.png", "rb")
    
    generate_storyboard_scenes_gemini(
        product_image=product_image,
        product_name=product_name,
        brand_name=brand_name,
        brand_personality=brand_personality,
        influencer_name=influencer_name,
        meme_type=meme_type
    )
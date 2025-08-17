# 이미지 종류는 이것이것이것 중에서 사용할수 있다.

import os
import yaml
import base64
from typing import List, Dict, Any
from google import genai
from google.genai import types
import PIL.Image

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
    
    return f"""
You are a viral meme storyboard expert creating content for {influencer_name}.

Influencer Profile:
- Type: {influencer_data.get('influencer', {}).get('type', 'Influencer')}
- Content Style: {content_style}
- Personality Traits: {personality_traits}
- Content Focus: {content_focus}
- Brand Voice: {brand_voice_tone}, {brand_voice_style}
- Target Audience: {influencer_data.get('audience', {}).get('primary', 'general audience')}

Product Profile:
- Name: {product_name}
- Category: {product_category}
- Key Features: {key_features}
- Marketing Angles: {', '.join(lifestyle_angles[:3])}
- Viral Trends: {viral_trends}
- Content Themes: {', '.join(content_themes[:5])}

Create a storyboard for a meme that:
1. Authentically showcases {product_name} through {influencer_name}'s unique lens
2. Leverages {influencer_name}'s {content_style} expertise
3. Incorporates relevant product features naturally
4. Taps into current viral trends and challenges
5. Appeals to both {influencer_name}'s audience and {product_name}'s target market
6. Creates an engaging 8-second video with exactly 3 scenes
7. Feels genuine to {influencer_name}'s established persona

Consider these viral opportunities: {viral_challenges}
Focus on these content angles: {', '.join(content_themes[:3])}
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
GENAI_API_KEY = os.getenv("GENAI_API_KEY", "")


def generate_storyboard_scenes_gemini(influencer_name: str,
                                      product_name: str):
    """Generate storyboard scenes and create images using Gemini.
    
    Args:
        influencer_name: Name of the influencer
        product_name: Name of the product for the storyboard
    """
    
    # Load influencer and product information
    try:
        influencer_data = load_influencer_info(influencer_name)
        influencer_image_path = get_influencer_image_path(influencer_name, "full_body")
        product_data = load_product_info(product_name)
        product_image_path = get_product_image_path(product_name)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error loading data: {e}")
        return
    
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
    product_img = PIL.Image.open(product_image_path)
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
                    with open(f"{output_dir}/storyboard_{i+1}.png", "wb") as f:
                        f.write(image_data)
                    print(f"Saved image: storyboard_{i+1}.png")
                    break
                    
        except Exception as e:
            print(f"Error generating image for scene {i+1}: {e}")
        break


if __name__ == "__main__":
    # Example usage - replace with your actual values
    influencer_name = "angeli"  # or "agiverse"
    product_name = "dress"  # matches directory name
    
    generate_storyboard_scenes_gemini(
        influencer_name=influencer_name,
        product_name=product_name
    )

# prompts = [
#     "**Description: Angeli is in her bedroom, makeup already partially done. She's wearing pajamas and messy hair. Her room has a generally clean, aesthetic vibe. A shelf in the background has some of her favorite things, like plants, books, and subtle One Piece figurines.Character Expression: Playful exasperation. She looks at the camera with a slight eye roll and a small, amused smile, like she's about to do something a little silly.Visual Effects: Text overlay: \"Me every morning:\" with a sparkly, handwritten-style font that's on brand for Angeli. A quick, gentle zoom in on her face.**",
#     "**Description: Quick montage. Angeli rapidly changes into a casual outfit featuring One Piece merchandise: A One Piece graphic tee (maybe Luffy or the Straw Hat Jolly Roger), comfy joggers, and sneakers. Each piece of clothing is shown briefly but clearly.Character Expression: Focused, slightly hurried but still enjoying the process. A confident smirk as she puts on the tee.Visual Effects: Fast-paced, energetic transitions between outfit pieces. Sound effect: quick whoosh noises. A highlight or subtle glow effect around the One Piece graphic on the t-shirt as she puts it on. Text overlay: \"deciding what to wear to finally find the One Piece\" (handwritten-style font again).**",
#     "**Description: Angeli strikes a confident pose in front of a mirror, now fully dressed in the One Piece tee, joggers, and sneakers. She's doing a quick \"check yourself out\" move.Character Expression: Big, confident smile. She winks at the camera. She grabs a straw hat off a hook by her mirror and places it on her head.Visual Effects: A shimmering filter briefly washes over the scene. Text overlay: \"Adventure awaits! \" and a link to the One Piece merch website (or a swipe up arrow). A cartoon treasure chest opens and shines briefly in the corner of the screen. Final shot lingers for a beat before the video ends.**Justification:***   **Authentically showcases One Piece Merchandise:** The whole video revolves around wearing One Piece apparel, highlighting the t-shirt as a key item. The subtle background figurines cater to collectors.*   **Leverages Angeli's GRWM Expertise:**",
# ]
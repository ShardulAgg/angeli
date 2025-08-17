# import os
# from tkinter import Image
# from openai import OpenAI
# import yaml
# from pydantic import BaseModel
# import base64
# from typing import List
# from google import genai
# from google.genai import types
# import json
# import PIL.Image
# from io import BytesIO

# class StoryboardItem(BaseModel):
#     description: str
#     character_expression: str
#     text_content: str
#     visual_effects: str

# class Storyboard(BaseModel):
#     items: List[StoryboardItem]

# def encode_image(image_path):
#     with open(image_path, "rb") as f:
#         return base64.b64encode(f.read()).decode("utf-8")


# STORYBOARD_SYSTEM_PROMPT = """
# You are a viral meme storyboard expert. Based on the topic or situation provided by the user, create a storyboard for a meme that can gain popularity on the internet for 8 seconds video.
# """

# STORYBOARD_OUTPUT_INSTRUCTION = """
# Output the storyboard in the following format:

# Storyboard format:
# 2.	Scene description (background, character positions)
# 3.	Character expressions/poses
# 4.	Text content (with placement)
# 5.	Visual effects or points of emphasis
# """

# IMAGE_GENERATION_PROMPT = """
# Create a scene image with applying second image in first image given below information: 

# Description: {description}
# Character Expression: {character_expression}
# Text Content: {text_content}
# Visual Effects: {visual_effects}

# """

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
# GENAI_API_KEY = os.getenv("GENAI_API_KEY", "")


# def generate_storyboard_scenes(product_name: str, product_image: str, influencer_image: str, output_dir: str = "assets/outputs/storyboard"):
#     """Generate storyboard scenes and create images using OpenAI.
    
#     Args:
#         product_name: Name of the product for the storyboard
#         product_image: Path to the product image
#         influencer_image: Path to the influencer image
#         output_dir: Directory to save generated storyboard images
#     """
    
#     client = OpenAI(api_key=OPENAI_API_KEY)

#     influencer_prompt = f"Create a storyboard for the product {product_name} with the meme"
#     response = client.chat.completions.parse(
#         model="gpt-4o",
#         messages=[
#             {"role": "system", "content": STORYBOARD_SYSTEM_PROMPT + STORYBOARD_OUTPUT_INSTRUCTION},
#             {"role": "user", "content": influencer_prompt}],
#         response_format=Storyboard
#     )
#     storyboard_result = response.choices[0].message.parsed

#     product_img_base64 = encode_image(product_image)
#     influencer_img_base64 = encode_image(influencer_image)

#     img1 = open(influencer_image, "rb")
#     img2 = open(product_image, "rb")

#     img1_base64 = base64.b64encode(img1.read()).decode("utf-8")
#     img2_base64 = base64.b64encode(img2.read()).decode("utf-8")

#     # Create output directory if it doesn't exist
#     os.makedirs(output_dir, exist_ok=True)

#     for i, item in enumerate(storyboard_result.items):
#         print(f"Item {i+1}:")
#         print("Description: ", item.description)

#         # Generate scene image for each
#         # FOR DEBUG: we need to use small size
#         # size = "1024x1024"
#         # quality = "low"
#         img_result = client.images.edit(
#             model="gpt-image-1",
#             image=[img1, img2],
#             prompt=IMAGE_GENERATION_PROMPT.format(
#                 description=item.description,
#                 character_expression=item.character_expression,
#                 text_content=item.text_content,
#                 visual_effects=item.visual_effects
#             ),
#             quality="auto",
#             output_compression=50,
#             output_format="jpeg",
#             size="1536x1024"
#         )

#         image_base64 = img_result.data[0].b64_json
#         image_bytes = base64.b64decode(image_base64)

#         with open(f"{output_dir}/storyboard_{i+1}.png", "wb") as f:
#             f.write(image_bytes)


# if __name__ == "__main__":
#     # Example usage - replace with your actual values
#     product_name = "Example Product"
#     product_image = "../assets/products/iphone.png"
#     influencer_image = "../assets/influencers/angeli/images/full_body.png"
#     output_dir = "../assets/outputs/storyboard"
    
#     generate_storyboard_scenes(
#         product_name=product_name,
#         product_image=product_image,
#         influencer_image=influencer_image,
#         output_dir=output_dir
#     )
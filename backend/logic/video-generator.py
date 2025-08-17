import time
from google.genai import types
from google import genai
from IPython.display import Video, HTML
from PIL import Image
import io
import imageio  # pip install imageio
import subprocess
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips



# Configuration
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "..", "assets")


GENAI_API_KEY = os.getenv("GENAI_API_KEY", "")
VEO_MODEL_ID = "veo-3.0-fast-generate-preview"
client = genai.Client(api_key=GENAI_API_KEY)

def generate_video(prompts: str, initial_image_path: str):
    output_folder = os.path.join(ASSETS_PATH, "outputs", "veo3")
    os.makedirs(output_folder, exist_ok=True)

    
    # Initial input image
    initial_image = initial_image_path
    negative_prompt = "ugly, low quality, low resolution, blurry, grainy, cartoon, watermark, compression artifacts, aliasing, unnatural proportions"
    negative_prompt = "low quality, low resolution, blurry, grainy, noise, jittery, shaky camera, black bars, letterbox, pillarbox, watermark, logo, timestamp, subtitles, compression artifacts, muted colors, vignette, chromatic aberration, over-saturated, film grain, ugly, cartoon, aliasing, unnatural proportions"
    aspect_ratio = "16:9"
    number_of_videos = 1
    video_paths = []
    image_path = initial_image
    for idx, prompt in enumerate(prompts):
        # print(idx)
        # print(image_path)
        # print(prompt)
        # Load current input image
        im = Image.open(image_path)
        image_bytes_io = io.BytesIO()
        im.save(image_bytes_io, format=im.format)
        image_bytes = image_bytes_io.getvalue()
        # Launch video generation
        operation = client.models.generate_videos(
            model=VEO_MODEL_ID,
            prompt=prompt,
            image=types.Image(image_bytes=image_bytes, mime_type=im.format),
            config=types.GenerateVideosConfig(
                aspect_ratio=aspect_ratio,
                number_of_videos=number_of_videos,
                negative_prompt=negative_prompt,
            ),
        )
        # Wait for completion
        while not operation.done:
            time.sleep(20)
            operation = client.operations.get(operation)
            print(operation)
        print(operation.result.generated_videos)
        generated_video = operation.result.generated_videos[0]
        out_path = os.path.join(output_folder, f"video_{idx}.mp4")
        client.files.download(file=generated_video.video)
        generated_video.video.save(out_path)
        video_paths.append(out_path)
        # Extract last frame to feed into next iteration
        reader = imageio.get_reader(out_path, format='mp4')
        last_frame = reader.get_data(reader.count_frames() - 1)
        next_im = Image.fromarray(last_frame)
        image_path = os.path.join(output_folder, f"frame_{idx}_last.png")
        next_im.save(image_path)
    print(image_path)
    print("All videos generated and looped.")

    # merge videos
    clips = [VideoFileClip(path) for path in video_paths]
    final_clip = concatenate_videoclips(clips, method="compose")
    combined_path = os.path.join(output_folder, "combined.mp4")
    final_clip.write_videofile(combined_path, codec="libx264", audio_codec="aac")

    return os.path.join(output_folder, "combined.mp4")


if __name__ == "__main__":
    prompts = [
        "Description: Angeli is in her bedroom, makeup already partially done. She's wearing pajamas and messy hair. Her room has a generally clean, aesthetic vibe. A shelf in the background has some of her favorite things, like plants, books, and subtle One Piece figurines. Character Expression: Playful exasperation. She looks at the camera with a slight eye roll and a small, amused smile, like she's about to do something a little silly. Visual Effects: Text overlay: 'Me every morning:' with a sparkly, handwritten-style font that's on brand for Angeli. A quick, gentle zoom in on her face.",
        "Description: Quick montage. Angeli rapidly changes into a casual outfit featuring One Piece merchandise: A One Piece graphic tee (maybe Luffy or the Straw Hat Jolly Roger), comfy joggers, and sneakers. Each piece of clothing is shown briefly but clearly. Character Expression: Focused, slightly hurried but still enjoying the process. A confident smirk as she puts on the tee. Visual Effects: Fast-paced, energetic transitions between outfit pieces. Sound effect: quick whoosh noises. A highlight or subtle glow effect around the One Piece graphic on the t-shirt as she puts it on. Text overlay: 'deciding what to wear to finally find the One Piece' (handwritten-style font again).",
        "Description: Angeli strikes a confident pose in front of a mirror, now fully dressed in the One Piece tee, joggers, and sneakers. She's doing a quick 'check yourself out' move. Character Expression: Big, confident smile. She winks at the camera. She grabs a straw hat off a hook by her mirror and places it on her head. Visual Effects: A shimmering filter briefly washes over the scene. Text overlay: 'Adventure awaits!' and a link to the One Piece merch website (or a swipe up arrow). A cartoon treasure chest opens and shines briefly in the corner of the screen. Final shot lingers for a beat before the video ends. Justification: Authentically showcases One Piece Merchandise: The whole video revolves around wearing One Piece apparel, highlighting the t-shirt as a key item. The subtle background figurines cater to collectors. Leverages Angeli's GRWM Expertise."
    ]
    initial_image_path = os.path.join(ASSETS_PATH, "outputs", "dress", "angeli", "storyboard.png")
    generate_video(prompts, initial_image_path)
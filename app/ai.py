import base64
import json
import re
import numpy as np
from app import config
import io
from PIL import Image
import cv2

from app.service import ClaudeService, OpenAIService


def encode_image(image, format):
    if image.mode == "RGBA":
        image = image.convert("RGB")
    buffered = io.BytesIO()
    image.save(buffered, format=format)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def check_type(data):
    if isinstance(data, str):
        try:
            json.loads(data)
            return "JSON string"
        except ValueError:
            return "Regular string"
    elif isinstance(data, dict):
        return "JSON object"
    else:
        return "Unknown data type."


def process_completion(completion_text):
    data_type = check_type(completion_text)

    try:
        if data_type == "JSON string":
            return json.loads(completion_text)

        elif data_type == "Regular string":
            pattern = r"```(?:\w*)\n(.*?)```"
            match = re.search(pattern, completion_text, re.DOTALL)
            if match:
                json_string = match.group(1).strip()
                try:
                    return json.loads(json_string)
                except json.JSONDecodeError:
                    return None
            else:
                return None

        elif data_type == "JSON object":
            return completion_text

        else:
            return None
    except Exception as e:
        return None


def resize_image(input_image):
    width, height = input_image.size
    resized_image = input_image.resize((width * 2, height * 2))
    return resized_image


def enhance_image(image):
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_img = clahe.apply(blur)
    enhanced_pil_image = Image.fromarray(enhanced_img)
    return enhanced_pil_image


def classify_image(file):
    resized_image = resize_image(file)
    enhanced_image = enhance_image(resized_image)
    image_format = enhanced_image.format or "JPEG"
    base64_image = encode_image(enhanced_image, image_format)
    image_media_type = f"image/{image_format.lower()}"
    print(image_media_type)
    # system_prompt = f"""
    #    You are a system designed to extract nutrition information from input data.
    #    Analyze the provided image and identify any nutrition facts present, including their corresponding values.
    #    Format the output as a JSON object where each key represents a nutrient and its value includes the quantity and unit (if specified).
    #    If the image does not contain any recognizable nutrition facts, return an empty JSON object.
    # """
    system_prompt = f"""
       Anda adalah sistem yang dirancang untuk mengekstrak informasi gizi dari data masukan. 
       Analisis gambar yang diberikan dan identifikasi fakta gizi yang ada, termasuk nilai-nilainya. 
       Formatkan keluaran sebagai objek JSON di mana setiap kunci mewakili nutrisi dan nilainya mencakup jumlah serta unitnya (jika ada). 
       Jika gambar tidak mengandung fakta gizi yang dapat dikenali, kembalikan objek JSON kosong.
    """
    # messages = [
    #     dict(
    #         {"role": "system", "content": system_prompt},
    #         content=[
    #             {
    #                 "type": "image",
    #                 "source": {
    #                     "type": "base64",
    #                     "media_type": image_media_type,
    #                     "data": base64_image,
    #                 },
    #             },
    #         ],
    #     ),
    # ]

    # chat_completion = (
    #     ClaudeService()
    #     .get_client()
    #     .messages.create(
    #         model=config.CLAUDE_MODEL_NAME,
    #         max_tokens=8192,
    #         temperature=0.8,
    #         system=system_prompt,
    #         messages=messages,
    #         extra_headers={"anthropic-beta": "max-tokens-3-5-sonnet-2024-07-15"},
    #     )
    # )

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": system_prompt,
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64, {base64_image}"},
                },
            ],
        }
    ]

    chat_completion = (
        OpenAIService()
        .get_client()
        .chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=8192,
            temperature=0.8,
        )
    )

    print(chat_completion)
    raw_content = chat_completion.choices[0].message.content
    parsed_content = process_completion(raw_content)
    return parsed_content if parsed_content else raw_content

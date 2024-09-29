import os
import json
from openai import OpenAI, OpenAIError

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def calculate_mode(numbers):
    return max(numbers, key=numbers.count) if len(
        set(numbers)) > 1 else numbers[0]


def analyze_diabetic_retinopathy(image: str) -> int | str:
    if not OPENAI_API_KEY:
        return "error: OpenAI API key is not set"

    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = '''
    Consider yourself to be a diagnostic bot. your job is to get retina scan images from the user and check it thoroughly. Come up with your analysis to detect diabetic retinopathy (DR). 
    Scale it based on 0 to 4. Respond ONLY with a numeric value. Examples - "1", "0".

    Definition:
    0 - No_DR
    1 - Mild
    2 - Moderate
    3 - Severe
    4 - Proliferate_DR
    '''
    data = []
    i = 0
    try:
        while len(data) < 3 or i < 6:
            i += 1
            response = client.chat.completions.create(
                model="gpt-4o-2024-05-13",
                messages=[{
                    "role": "system",
                    "content": prompt
                }, {
                    "role":
                    "user",
                    "content": [{
                        "type": "text",
                        "text": "This is the image"
                    }, {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image}",
                            "detail": "high"
                        }
                    }]
                }],
                max_tokens=500)

            content = response.choices[0].message.content
            if content and content.isdigit():
                data.append(content)
                if len(data) == 3:
                    return calculate_mode(data)
            else:
                return "error:Non-numeric response from OpenAI"
        return calculate_mode(data)
    except json.JSONDecodeError as e:
        return f"error: Invalid JSON response {str(e)}"
    except Exception as e:
        return f"error: Unexpected error - {str(e)}"


def fallback_diabetic_retinopathy_info() -> dict:
    """
    Provide a fallback response when the API call fails.
    """
    return {
        "dr_scale":
        "Unable to determine",
        "detailed_analysis":
        "An error occurred during the analysis. Please try again or consult with a healthcare professional for accurate information about Diabetic Retinopathy."
    }


def details(image: str, category: str):
    if not OPENAI_API_KEY:
        return {
            "error": "OpenAI API key is not set",
            "details": "Please set the OPENAI_API_KEY environment variable."
        }

    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = f'''
    Consider yourself to be a diagnostic bot. your job is to get retina scan images from the user and check it thoroughly. Come up with your analysis and recommendations. You will be given image of {category}. Don't mention the category to the user. Be professional and respond as if you are giving a report.
    Focus on the following features:
    1. Microaneurysms: small, round, dark red spots
    2. Hemorrhages: larger, irregularly shaped dark spots
    3. Hard exudates: small yellow-white deposits
    4. Soft exudates (cotton wool spots): fluffy white patches
    5. Neovascularization: abnormal growth of blood vessels
    6. Macular edema: swelling in the macula area

    Provide a brief assessment of these features if present, and their severity.
    '''
    response = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        messages=[{
            "role": "system",
            "content": prompt
        }, {
            "role":
            "user",
            "content": [{
                "type": "text",
                "text": "This is the image."
            }, {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image}",
                    "detail": "high"
                }
            }]
        }],
        max_tokens=500)

    content = response.choices[0].message.content
    if content:
        return content
    else:
        return {
            "error": "Non-numeric response from OpenAI",
            "details": "The API returned an non-numeric response."
        }

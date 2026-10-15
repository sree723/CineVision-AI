
import json
import logging
import os
import time

from django.shortcuts import render
from google import genai
from google.genai.errors import ServerError

logger = logging.getLogger(__name__)


STORYBOARD_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "analysis": {
            "type": "OBJECT",
            "properties": {
                "logline": {"type": "STRING"},
                "summary": {"type": "STRING"},
                "central_conflict": {"type": "STRING"},
                "themes": {
                    "type": "ARRAY",
                    "items": {"type": "STRING"},
                },
                "tone": {"type": "STRING"},
                "setting": {"type": "STRING"},
                "characters": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "name": {"type": "STRING"},
                            "role": {"type": "STRING"},
                            "description": {"type": "STRING"},
                            "visual_appearance": {"type": "STRING"},
                        },
                        "required": [
                            "name",
                            "role",
                            "description",
                            "visual_appearance",
                        ],
                    },
                },
            },
            "required": [
                "logline",
                "summary",
                "central_conflict",
                "themes",
                "tone",
                "setting",
                "characters",
            ],
        },
        "scenes": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "scene_number": {"type": "INTEGER"},
                    "title": {"type": "STRING"},
                    "purpose": {"type": "STRING"},
                    "location": {"type": "STRING"},
                    "time_of_day": {"type": "STRING"},
                    "action": {"type": "STRING"},
                    "dialogue": {"type": "STRING"},
                    "duration_seconds": {"type": "INTEGER"},
                    "camera_shot": {"type": "STRING"},
                    "camera_angle": {"type": "STRING"},
                    "camera_movement": {"type": "STRING"},
                    "lighting": {"type": "STRING"},
                    "color_palette": {"type": "STRING"},
                    "mood": {"type": "STRING"},
                    "sound_design": {"type": "STRING"},
                    "director_notes": {"type": "STRING"},
                    "image_prompt": {"type": "STRING"},
                },
                "required": [
                    "scene_number",
                    "title",
                    "purpose",
                    "location",
                    "time_of_day",
                    "action",
                    "dialogue",
                    "duration_seconds",
                    "camera_shot",
                    "camera_angle",
                    "camera_movement",
                    "lighting",
                    "color_palette",
                    "mood",
                    "sound_design",
                    "director_notes",
                    "image_prompt",
                ],
            },
        },
    },
    "required": ["analysis", "scenes"],
}


def home(request):
    return render(request, "storyboard/index.html")


def input_page(request):
    return render(request, "storyboard/input.html")


def generate(request):
    if request.method != "POST":
        return render(request, "storyboard/input.html")

    title = request.POST.get("title", "").strip()
    genre = request.POST.get("genre", "").strip()
    duration = request.POST.get("duration", "").strip()
    story = request.POST.get("story", "").strip()

    context = {
        "title": title,
        "genre": genre,
        "duration": duration,
        "story": story,
        "analysis": None,
        "scenes": [],
        "error": None,
    }

    if not title or not genre or not duration or not story:
        context["error"] = "Please complete all fields before generating."
        return render(request, "storyboard/input.html", context)

    if not os.getenv("GEMINI_API_KEY"):
        context["error"] = (
            "Gemini API key is missing. Configure GEMINI_API_KEY "
            "in your environment and restart the server."
        )
        return render(request, "storyboard/input.html", context)

    prompt = f"""
You are the story analyst and film director for CineVision AI.

Analyse the user's story and turn it into a practical cinematic storyboard.

PROJECT DETAILS
Title: {title}
Genre: {genre}
Target duration: {duration}

USER'S STORY
<story>
{story}
</story>

INSTRUCTIONS

1. Understand the story before dividing it into scenes.
2. Preserve the user's core plot, characters, and intended ending.
3. Analyse the logline, summary, central conflict, themes, tone,
   setting, and important characters.
4. Create approximately 4 to 10 logical scenes appropriate to the
   requested runtime.
5. Give each scene a clear purpose and visible actions.
6. Specify camera shot, angle, movement, lighting, colour palette,
   mood, and sound design for every scene.
7. Write practical director's notes for each scene.
8. Write a detailed image-generation prompt for each scene, maintaining
   character appearance and visual continuity.
9. Estimate realistic scene durations in seconds.
10. Make reasonable creative choices where details are unspecified.
11. Return the requested structured JSON data only.
"""

    try:
        client = genai.Client()

        response = None

        # Retry temporary Gemini 503 errors up to three attempts.
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=os.getenv(
                        "GEMINI_MODEL",
                        "gemini-3.8-flash",
                    ),
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_schema": STORYBOARD_SCHEMA,
                        "temperature": 0.7,
                    },
                )
                break

            except ServerError as exc:
                if exc.code != 503 or attempt == 2:
                    raise

                wait_seconds = 2 ** (attempt + 1)
                logger.warning(
                    "Gemini returned 503. Retrying in %s seconds "
                    "(attempt %s of 3).",
                    wait_seconds,
                    attempt + 1,
                )
                time.sleep(wait_seconds)

        if response is None or not response.text:
            raise ValueError("Gemini returned an empty response.")

        ai_result = json.loads(response.text)

        analysis = ai_result.get("analysis")
        scenes = ai_result.get("scenes")

        if not isinstance(analysis, dict):
            raise ValueError("Gemini returned invalid story analysis.")

        if not isinstance(scenes, list) or not scenes:
            raise ValueError("Gemini returned no storyboard scenes.")

        context["analysis"] = analysis
        context["scenes"] = scenes

    except Exception:
        logger.exception("CineVision AI storyboard generation failed.")
        context["error"] = (
            "We couldn't generate your storyboard right now. "
            "Your story is still available in the form. "
            "Please try again shortly."
        )
        return render(request, "storyboard/input.html", context)

    return render(request, "storyboard/result.html", context)

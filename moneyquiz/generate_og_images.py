#!/usr/bin/env python3
"""머니퀴즈 공유 카드 OG 이미지 5장 생성 — 귀여운 캐릭터 (가로형 최적화)"""
import os, io
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image

MODEL = "gemini-3.1-flash-image-preview"
api_key = os.environ.get("GEMINI_API_KEY", "REDACTED")
client = genai.Client(api_key=api_key)
out_dir = Path(__file__).parent
out_dir.mkdir(parents=True, exist_ok=True)

OG_W, OG_H = 1200, 630

def gen(prompt: str, filename: str) -> None:
    out = out_dir / filename
    print(f"  generating: {filename} ({OG_W}x{OG_H}) ...")
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )
        img_bytes = None
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                img_bytes = part.inline_data.data
                break
        if img_bytes is None:
            print(f"  FAIL no image: {filename}")
            return
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        iw, ih = img.size
        tr = OG_W / OG_H
        cr = iw / ih
        if cr > tr:
            nw = int(ih * tr); l = (iw - nw) // 2
            img = img.crop((l, 0, l + nw, ih))
        elif cr < tr:
            nh = int(iw / tr); t = (ih - nh) // 2
            img = img.crop((0, t, iw, t + nh))
        img = img.resize((OG_W, OG_H), Image.LANCZOS)
        img.save(out, "PNG", optimize=True)
        print(f"  OK: {out}")
    except Exception as e:
        print(f"  FAIL: {e}")

# 가로형 배너에 맞춘 캐릭터 일러스트 베이스
base = (
    "cute kawaii illustration, chibi character, big sparkly eyes, "
    "WIDE LANDSCAPE BANNER composition, 2:1 aspect ratio layout, "
    "small full-body character centered in the middle, "
    "lots of empty background space on all sides, "
    "character takes up only 40 percent of the image height, "
    "pastel soft gradient background fills the wide space, "
    "absolutely no text, no letters, no words, no watermark, "
    "no CJK, no Korean, no Japanese, high quality, vibrant"
)

print(f"\n[OG Image Generator - Cute Character Wide ver.] model: {MODEL}\n")

# S grade - 왕관 + 트로피 (골드)
gen(
    f"WIDE LANDSCAPE BANNER: A tiny cute chibi character wearing a golden crown, "
    f"holding a golden trophy, celebrating with arms up, "
    f"the small character is centered in a vast warm golden to peach gradient background, "
    f"gold coins, stars, confetti, and sparkles scattered across the wide space, "
    f"full body visible from head to toe, {base}",
    "og-S.png"
)

# A grade - 안경 + 다이아몬드 (블루)
gen(
    f"WIDE LANDSCAPE BANNER: A tiny cute chibi character with round glasses, "
    f"holding a glowing blue diamond gem, standing confidently, "
    f"the small character is centered in a vast soft blue to sky blue gradient background, "
    f"small sparkles and light particles floating across the wide space, "
    f"full body visible from head to toe, {base}",
    "og-A.png"
)

# B grade - 돈나무 키우기 (그린)
gen(
    f"WIDE LANDSCAPE BANNER: A tiny cute chibi character watering a small money tree, "
    f"the tree has coins on its branches, character holds a watering can, "
    f"the small character and tree are centered in a vast green to mint gradient background, "
    f"floating leaves and small coins scattered across the wide space, "
    f"full body visible from head to toe, {base}",
    "og-B.png"
)

# C grade - 책 읽기 (오렌지)
gen(
    f"WIDE LANDSCAPE BANNER: A tiny cute chibi character sitting and reading a big book, "
    f"a small glowing lightbulb floating above the head, "
    f"the small character is centered in a vast warm orange to yellow gradient background, "
    f"floating question marks and stars scattered across the wide space, "
    f"full body visible from head to toe, {base}",
    "og-C.png"
)

# D grade - 새싹 심기 (라벤더)
gen(
    f"WIDE LANDSCAPE BANNER: A tiny cute chibi character kneeling and planting a seed, "
    f"a small green sprout growing from the ground next to the character, "
    f"the small character is centered in a vast soft lavender to pink gradient background, "
    f"tiny butterflies and flower buds scattered across the wide space, "
    f"full body visible from head to toe, {base}",
    "og-D.png"
)

print(f"\nDone! Output: {out_dir}\n")

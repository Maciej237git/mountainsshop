from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "shop-gallery"
MAX_W = 1920
QUALITY = 82
THUMB = 160


def icloud2_inner():
    base = next(p for p in ROOT.iterdir() if p.name.endswith("iCloud (2)") and p.is_dir())
    return next(p for p in base.iterdir() if "iCloud" in p.name and p.is_dir())


def icloud3_inner():
    desktop = Path(r"c:\Users\Maciej\Desktop")
    base = next(p for p in desktop.iterdir() if p.name.endswith("iCloud (3)") and p.is_dir())
    return next(p for p in base.iterdir() if "iCloud" in p.name and p.is_dir())


def to_webp(src: Path, dest: Path, max_w=MAX_W):
    img = Image.open(src)
    if img.mode in ("P", "LA"):
        img = img.convert("RGBA")
    elif img.mode != "RGB":
        img = img.convert("RGB")
    w, h = img.size
    if w > max_w:
        img = img.resize((max_w, int(h * max_w / w)), Image.Resampling.LANCZOS)
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest, "WEBP", quality=QUALITY, method=6)


def thumb_from(dest: Path, thumb: Path):
    img = Image.open(dest)
    img.thumbnail((THUMB, THUMB), Image.Resampling.LANCZOS)
    img.save(thumb, "WEBP", quality=78, method=6)


def copy_existing(rel: str, out_name: str):
    src = ROOT / "assets" / rel
    dest = ASSETS / out_name
    if src.exists():
        if src.suffix.lower() == ".webp":
            dest.write_bytes(src.read_bytes())
        else:
            to_webp(src, dest)
        thumb_from(dest, ASSETS / out_name.replace(".webp", "-thumb.webp"))


VIBE_UUID = [
    "a9033543-a115-442a-ae01-1ad3ace4a8c5",
    "0814736f-dc64-4fcb-9f61-4d6c5fe92cc7",
    "f2d72b50-c489-43d4-8029-1b870cd83cdb",
    "8f93f99a-aa5f-4c13-99da-17ec0ec4e084",
    "5fd9d611-bf10-4701-8e67-4c4860fb46a4",
    "30f7264a-021f-414c-b1d2-81690dbd1d2c",
    "50871886-50ec-4d62-ab2e-4c426363b0ab",
    "c24b4347-a106-40bb-8da6-5aeef0ddf695",
    "3f57c197-e59e-4e93-b1d1-c555eaa113b1",
    "16933fc8-97fd-48ff-9c72-4e7eec306928",
]

SIMPLY_UUID = [
    "a8612aa1-0c48-475a-bb56-13a97d39713a",
    "df87a1f2-0975-4e37-bb0a-28b178a9f71e",
    "41127e1e-34a3-4c5c-ab43-23bc261526f7",
    "80cb43a3-76f5-49c3-8c61-7b2819a7de9b",
    "ca4a69b6-6794-4083-a3a8-9ec7ca5bc301",
    "d8815f51-e49d-4cd1-9dbc-7faa04e6efd2",
    "07eef065-31c2-4168-a990-d4e42d5f4153",
    "32257745-7c61-46f3-88c8-d2f54ceff91b",
    "aa2a23d7-c367-4767-8453-a7f038247a9e",
]

# Mountain Style — second exterior (window display, not duplicate sign)
STYLE_EXTERIOR_02_UUID = "afecb6f9-2fb4-402d-a9be-0952e5515977"

# Mountain Style interiors — no people (from iCloud 2)
STYLE_INTERIOR_UUID = [
    "5310c13f-8fe6-4f5e-aee6-cc0b8c378748",
    "636619d2-6e7d-475c-9e1e-1987c2955eed",
    "3c78d788-334a-4e58-b82a-c6f41997a64c",
    "3bb7caac-f0e2-4e48-8b3c-c18528aada90",
]

# Colorado Concept interiors — no people (from iCloud 2)
CONCEPT_INTERIOR_UUID = [
    "8cc1924e-8249-46fc-9169-8dc3d496b475",
    "552ab929-fd44-4a2c-b6b3-4b75fbd2aada",
    "c85b289f-9eb9-496d-bc35-f1b2500ec663",
]


def from_icloud(inner: Path, uuids, prefix: str, start_index: int = 1):
    for offset, uid in enumerate(uuids):
        src = inner / f"{uid}.jpg"
        if not src.exists():
            raise FileNotFoundError(src)
        n = start_index + offset
        name = f"{prefix}-{n:02d}.webp"
        dest = ASSETS / name
        to_webp(src, dest)
        thumb_from(dest, ASSETS / f"{prefix}-{n:02d}-thumb.webp")


def main():
    if ASSETS.exists():
        for p in ASSETS.glob("*"):
            p.unlink()
    else:
        ASSETS.mkdir(parents=True)

    for rel, name in [
        ("shop-style.webp", "style-01.webp"),
        ("style-storefront.webp", "style-03.webp"),
        ("photo-storefront-ms.webp", "style-04.webp"),
        ("shop-concept.webp", "concept-01.webp"),
        ("photo-concept-street.webp", "concept-02.webp"),
        ("bottom-main-street.webp", "concept-03.webp"),
    ]:
        copy_existing(rel, name)

    inner2 = icloud2_inner()
    from_icloud(inner2, [STYLE_EXTERIOR_02_UUID], "style", start_index=2)
    from_icloud(inner2, STYLE_INTERIOR_UUID, "style", start_index=5)
    from_icloud(inner2, CONCEPT_INTERIOR_UUID, "concept", start_index=4)

    inner3 = icloud3_inner()
    from_icloud(inner3, VIBE_UUID, "vibe")
    from_icloud(inner3, SIMPLY_UUID, "simply")

    to_webp(inner3 / f"{VIBE_UUID[0]}.jpg", ROOT / "assets" / "shop-vibe.webp")
    to_webp(inner3 / f"{SIMPLY_UUID[0]}.jpg", ROOT / "assets" / "shop-simply-storefront.webp")
    print("Done:", len(list(ASSETS.glob("*.webp"))), "files in shop-gallery")


if __name__ == "__main__":
    main()

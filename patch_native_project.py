#!/usr/bin/env python3
"""Apply Android-compatible launcher resources and dependency fix for NeoHack Arcade."""
from pathlib import Path
import subprocess
import sys

try:
    from PIL import Image, ImageOps
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "Pillow"])
    from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent
manifest_path = ROOT / "app/src/main/AndroidManifest.xml"
manifest = manifest_path.read_text()
if 'android:icon="@mipmap/ic_launcher"' not in manifest:
    old = "<application\n"
    new = (
        '<application\n'
        '        android:icon="@mipmap/ic_launcher"\n'
        '        android:roundIcon="@mipmap/ic_launcher"\n'
    )
    if old not in manifest:
        raise SystemExit("Android application element not found")
    manifest_path.write_text(manifest.replace(old, new, 1))

gradle_path = ROOT / "app/build.gradle"
gradle = gradle_path.read_text()
exclude = """configurations.configureEach {
    exclude group: 'org.jetbrains.kotlin', module: 'kotlin-stdlib-jdk7'
    exclude group: 'org.jetbrains.kotlin', module: 'kotlin-stdlib-jdk8'
}

"""
if "module: 'kotlin-stdlib-jdk8'" not in gradle:
    if "dependencies {" not in gradle:
        raise SystemExit("Gradle dependency block not found")
    gradle_path.write_text(gradle.replace("dependencies {", exclude + "dependencies {", 1))

icon_source = ROOT / "neohack-launcher-icon.jpg"
if not icon_source.is_file():
    raise SystemExit(f"Launcher image not found: {icon_source.name}")
source = Image.open(icon_source).convert("RGB")

# Preserve the full artwork and its proportions on a dark square background.
def make_icon(size: int) -> Image.Image:
    canvas = Image.new("RGB", (size, size), (8, 12, 24))
    art = ImageOps.contain(source, (size, size), method=Image.Resampling.LANCZOS)
    canvas.paste(art, ((size - art.width) // 2, (size - art.height) // 2))
    return canvas

# Legacy bitmap launcher icons are needed by older Android versions, including the J8.
for density, size in {
    "mdpi": 48,
    "hdpi": 72,
    "xhdpi": 96,
    "xxhdpi": 144,
    "xxxhdpi": 192,
}.items():
    out = ROOT / f"app/src/main/res/mipmap-{density}/ic_launcher.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    make_icon(size).save(out, format="PNG", optimize=True)

# Newer Android launchers require an adaptive icon; supply a compatible XML resource too.
foreground_size = 432
foreground = Image.new("RGBA", (foreground_size, foreground_size), (0, 0, 0, 0))
art = ImageOps.contain(source, (foreground_size, foreground_size), method=Image.Resampling.LANCZOS).convert("RGBA")
foreground.alpha_composite(art, ((foreground_size - art.width) // 2, (foreground_size - art.height) // 2))
foreground_path = ROOT / "app/src/main/res/mipmap-nodpi/ic_launcher_foreground.png"
foreground_path.parent.mkdir(parents=True, exist_ok=True)
foreground.save(foreground_path, format="PNG", optimize=True)

adaptive_dir = ROOT / "app/src/main/res/mipmap-anydpi-v26"
adaptive_dir.mkdir(parents=True, exist_ok=True)
(adaptive_dir / "ic_launcher.xml").write_text(
    '<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
    '    <background android:drawable="@android:color/black" />\n'
    '    <foreground android:drawable="@mipmap/ic_launcher_foreground" />\n'
    '</adaptive-icon>\n'
)
print("Applied density-specific PNG and adaptive launcher icons, preserving the artwork")

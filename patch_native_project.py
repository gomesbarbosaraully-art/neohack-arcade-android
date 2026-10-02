from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent
manifest_path = ROOT / "app/src/main/AndroidManifest.xml"
manifest = manifest_path.read_text()
if 'android:icon="@mipmap/ic_launcher"' not in manifest:
    old = '<application\n'
    new = ('<application\n'
           '        android:icon="@mipmap/ic_launcher"\n'
           '        android:roundIcon="@mipmap/ic_launcher"\n')
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
icon_target = ROOT / "app/src/main/res/mipmap-nodpi/ic_launcher.jpg"
icon_target.parent.mkdir(parents=True, exist_ok=True)
shutil.copyfile(icon_source, icon_target)
print("Applied Kotlin dependency exclusions and aspect-preserving launcher icon")

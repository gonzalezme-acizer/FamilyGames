#!/bin/zsh
set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
APP_DIR="$ROOT_DIR/Familia en Juego.app"
BUILD_DIR="$(mktemp -d /private/tmp/familia-en-juego-build.XXXXXX)"
BUILD_APP="$BUILD_DIR/Familia en Juego.app"
CONTENTS="$BUILD_APP/Contents"
trap 'rm -rf "$BUILD_DIR"' EXIT

mkdir -p "$CONTENTS/MacOS" "$CONTENTS/Resources"
clang "$ROOT_DIR/native/FamiliaEnJuego.m" \
  -o "$CONTENTS/MacOS/FamiliaEnJuego" \
  -fobjc-arc -fmodules-cache-path="$ROOT_DIR/.module-cache" \
  -framework Cocoa -framework WebKit

cp "$ROOT_DIR/native/Info.plist" "$CONTENTS/Info.plist"
cp "$ROOT_DIR/server.py" "$CONTENTS/Resources/server.py"
cp "$ROOT_DIR/desafios_catalog.py" "$CONTENTS/Resources/desafios_catalog.py"
cp "$ROOT_DIR/quien_dijo_catalog.py" "$CONTENTS/Resources/quien_dijo_catalog.py"
cp "$ROOT_DIR/quien_soy_catalog.py" "$CONTENTS/Resources/quien_soy_catalog.py"
cp "$ROOT_DIR/tres_verdades_catalog.py" "$CONTENTS/Resources/tres_verdades_catalog.py"
cp "$ROOT_DIR/just_sing_catalog.py" "$CONTENTS/Resources/just_sing_catalog.py"
cp "$ROOT_DIR/catalog_expansion.py" "$CONTENTS/Resources/catalog_expansion.py"
cp "$ROOT_DIR/incognito_catalog.py" "$CONTENTS/Resources/incognito_catalog.py"
cp "$ROOT_DIR/bomba_catalog.py" "$CONTENTS/Resources/bomba_catalog.py"
cp "$ROOT_DIR/content.json" "$CONTENTS/Resources/content.json"
cp "$ROOT_DIR/trivia-120.json" "$CONTENTS/Resources/trivia-120.json"
cp "$ROOT_DIR/trivia-expansion.json" "$CONTENTS/Resources/trivia-expansion.json"
cp "$ROOT_DIR/mimica-250.json" "$CONTENTS/Resources/mimica-250.json"
cp "$ROOT_DIR/extra-prompts.json" "$CONTENTS/Resources/extra-prompts.json"
mkdir -p "$CONTENTS/Resources/public"
cp -R "$ROOT_DIR/public/"* "$CONTENTS/Resources/public/"
chmod +x "$CONTENTS/MacOS/FamiliaEnJuego"
xattr -cr "$BUILD_APP"
codesign --force --deep --sign - "$BUILD_APP"
ditto "$BUILD_APP" "$APP_DIR"

echo ""
echo "✅ Familia en Juego.app fue creada correctamente."
echo "Ya podés cerrar esta ventana y abrir la aplicación."

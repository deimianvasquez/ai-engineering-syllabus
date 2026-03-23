#!/usr/bin/env bash
set -euo pipefail

# Generates a 1024x576 PNG from cover-template.html using Playwright CLI.
# Example:
# ./assets/cover/generate-cover.sh \
#   --title "My Project" \
#   --author "by @myuser" \
#   --image "./reference-right.png" \
#   --logo "./logo-placeholder.svg" \
#   --output "./assets/cover/my-project-cover.png"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

if [[ -d "$ROOT_DIR/assest/cover" ]]; then
  COVER_DIR="$ROOT_DIR/assest/cover"
elif [[ -d "$ROOT_DIR/assets/cover" ]]; then
  COVER_DIR="$ROOT_DIR/assets/cover"
else
  echo "No cover directory found. Expected assets/cover or assest/cover."
  exit 1
fi

TEMPLATE_FILE="$COVER_DIR/cover-template.html"
OUTPUT_FILE="$COVER_DIR/cover-output.png"
TITLE=""
AUTHOR=""
IMAGE=""
LOGO=""
BG=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --title)
      TITLE="${2:-}"
      shift 2
      ;;
    --author)
      AUTHOR="${2:-}"
      shift 2
      ;;
    --image)
      IMAGE="${2:-}"
      shift 2
      ;;
    --logo)
      LOGO="${2:-}"
      shift 2
      ;;
    --bg)
      BG="${2:-}"
      shift 2
      ;;
    --output)
      OUTPUT_FILE="${2:-}"
      shift 2
      ;;
    --help|-h)
      echo "Usage:"
      echo "  $0 [--title TEXT] [--author TEXT] [--image PATH] [--logo PATH] [--bg HEX] [--output PATH]"
      exit 0
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

if [[ ! -f "$TEMPLATE_FILE" ]]; then
  echo "Template not found: $TEMPLATE_FILE"
  exit 1
fi

if [[ "$OUTPUT_FILE" != /* ]]; then
  OUTPUT_FILE="$ROOT_DIR/$OUTPUT_FILE"
fi

mkdir -p "$(dirname "$OUTPUT_FILE")"

urlencode() {
  python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "$1"
}

QUERY=""
append_query_param() {
  local key="$1"
  local value="$2"
  if [[ -n "$value" ]]; then
    local encoded
    encoded="$(urlencode "$value")"
    if [[ -z "$QUERY" ]]; then
      QUERY="${key}=${encoded}"
    else
      QUERY="${QUERY}&${key}=${encoded}"
    fi
  fi
}

append_query_param "title" "$TITLE"
append_query_param "author" "$AUTHOR"
append_query_param "image" "$IMAGE"
append_query_param "logo" "$LOGO"
append_query_param "bg" "$BG"

PAGE_URL="file://${TEMPLATE_FILE}"
if [[ -n "$QUERY" ]]; then
  PAGE_URL="${PAGE_URL}?${QUERY}"
fi

echo "Rendering cover..."
echo "template_file: $TEMPLATE_FILE"
echo "output_file: $OUTPUT_FILE"

npx playwright screenshot \
  --viewport-size="1024,576" \
  "$PAGE_URL" \
  "$OUTPUT_FILE"

echo "Done. Cover generated at:"
echo "$OUTPUT_FILE"

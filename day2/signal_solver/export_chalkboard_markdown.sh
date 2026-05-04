#!/usr/bin/env zsh
set -euo pipefail

# Export the teacher script markdown to a print-friendly HTML file.
# Then print that HTML from your browser (Cmd+P) or Save as PDF.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$SCRIPT_DIR"

INPUT="signal_solver.md"
CSS="signal-solver.css"
OUTPUT="signal_solver.html"

pandoc "$INPUT" \
  --from=gfm \
  --to=html5 \
  --standalone \
  --css "$CSS" \
  --metadata title="Decode the Signal - Chalkboard Script" \
  --output "$OUTPUT"

echo "Created: $OUTPUT"

.PHONY: help list send record replay clean

help:
	@echo "MicroKORG MIDI Lab"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  list              List available MIDI ports"
	@echo "  send NOTES=...    Send a melody (e.g., make send NOTES='C4 D4 E4 G4')"
	@echo "  record DUR=...    Record performance (duration in seconds, default 8)"
	@echo "  replay            Replay the last recording"
	@echo "  save NOTES=...    Save a melody to file (e.g., make save NOTES='C4 D4 E4' FILE=hello.txt)"
	@echo "  load FILE=...     Load and display a melody (e.g., make load FILE=hello.txt)"
	@echo "  convert FILE=...  Convert recording to melody notation (e.g., make convert FILE=recording.json)"
	@echo "  clean             Remove recorded performances"
	@echo ""
	@echo "Examples:"
	@echo "  make list"
	@echo "  make send NOTES='C4 D4 E4 G4'"
	@echo "  make record DUR=10"
	@echo "  make replay"
	@echo "  make save NOTES='C4 D4 E4' FILE=mynote.txt"
	@echo "  make load FILE=mynote.txt"
	@echo "  make convert FILE=performance.json"

list:
	python driver.py list

send:
	@if [ -z "$(NOTES)" ]; then echo "Usage: make send NOTES='C4 D4 E4 G4'"; exit 1; fi
	python driver.py send --notes "$(NOTES)"

record:
	python driver.py record --duration $(DUR:-8)

replay:
	python driver.py replay

save:
	@if [ -z "$(NOTES)" ] || [ -z "$(FILE)" ]; then echo "Usage: make save NOTES='C4 D4 E4' FILE=melody.txt"; exit 1; fi
	python driver.py save --notes "$(NOTES)" --output-file "$(FILE)"

load:
	@if [ -z "$(FILE)" ]; then echo "Usage: make load FILE=melody.txt"; exit 1; fi
	python driver.py load --input-file "$(FILE)"

convert:
	@if [ -z "$(FILE)" ]; then echo "Usage: make convert FILE=recording.json"; exit 1; fi
	python driver.py convert --input-file "$(FILE)"

clean:
	rm -f performance.json recording.json test_melody.txt test_recording.json *.json *.txt 2>/dev/null || true

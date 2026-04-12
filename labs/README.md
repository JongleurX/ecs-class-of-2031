# MicroKORG MIDI Lab

This folder contains a Python MIDI lab for programming melodies and working with a MicroKORG synthesizer.

## Goals

- Send note/CC/Program Change data to a connected MicroKORG over USB-to-MIDI
- Switch easily between a virtual MIDI port and a real hardware port
- Record MIDI performances from the MicroKORG and replay them
- Provide both a simple command-line interface and a QML-based GUI

## Install

Use a Python virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r labs/requirements.txt
```

## Run the GUI

The GUI currently has Qt platform plugin issues on some macOS setups. **Use the CLI instead** — it is more direct and educational for students.

```bash
python labs/driver.py gui
```

## Run the CLI

Use the simple command-line interface. Optionally, use `make` for convenience:

```bash
# List available MIDI ports
python labs/driver.py list

# Send a melody
python labs/driver.py send --notes "C4 D4 E4 G4" --tempo 110 --port "IAC Driver Bus 1"

# Send a melody with chords
python labs/driver.py send --notes "[C4,E4,G4] [D4,F4,A4] [E4,G4,B4]" --port "IAC Driver Bus 1"

# Change the instrument patch before sending (0-127)
python labs/driver.py send --notes "C4 D4 E4 G4" --program 25 --port "IAC Driver Bus 1"

# Record a 10-second performance
python labs/driver.py record --input-port "IAC Driver Bus 1" --output-file performance.json --duration 10

# Replay the recording
python labs/driver.py replay --output-port "IAC Driver Bus 1" --input-file performance.json

# Save a melody to a file
python labs/driver.py save --notes "C4 D4 E4 G4" --output-file mymelody.txt

# Load a melody from a file
python labs/driver.py load --input-file mymelody.txt

# Convert a recorded GarageBand performance to melody text notation
python labs/driver.py convert --input-file performance.json --output-file melody_from_recording.txt
```

### Using Make for convenience

From the `labs/` directory:

```bash
# List ports
make list

# Send a melody
make send NOTES="C4 D4 E4 G4"

# Record a performance (default 8 seconds)
make record

# Record for 20 seconds
make record DUR=20

# Replay
make replay

# Save a melody to a file
make save NOTES="C4 D4 E4 G4" FILE="mymelody.txt"

# Load a melody from a file
make load FILE="mymelody.txt"

# Convert a recording to melody notation
make convert FILE="performance.json"

# Clean up recordings and saved files
make clean
```

### Workflow: Perform in GarageBand, edit in text

1. Open **GarageBand**
2. Set MIDI input to `IAC Driver Bus 1`
3. Record/play a performance
4. From Terminal, record the GarageBand output:
   ```bash
   python labs/driver.py record --input-port "GarageBand Virtual Out" --output-file perf.json --duration 20
   ```
5. Convert the recording to melody text:
   ```bash
   python labs/driver.py convert --input-file perf.json
   ```
6. Edit the output text to clean it up, remove wrong notes, etc.
7. Save it:
   ```bash
   python labs/driver.py save --notes "C4 D4 E4 F4 G4" --output-file mynote.txt
   ```
8. Replay it:
   ```bash
   python labs/driver.py send --notes "C4 D4 E4 F4 G4" --port "IAC Driver Bus 1"
   ```

### Changing MIDI output to a virtual device

1. List available output ports:

```bash
python labs/driver.py list --direction out
```

2. Find the name of your virtual MIDI port.
3. Pass that exact name to `--port` for send/replay, or `--input-port` for record.

Example for macOS:

```bash
python labs/driver.py send --notes "C4 D4 E4 G4" --port "IAC Driver Bus 1"
```

If you do not specify a port, the code will use the first available MIDI output port.

## Virtual MIDI testing on macOS

- Open `Audio MIDI Setup` from `/Applications/Utilities/Audio MIDI Setup.app`
- In the menu, choose `Window` → `Show MIDI Studio` if you do not see a MIDI window
- Double-click the `IAC Driver` icon
- Check `Device is online`
- If there is no bus, click the `+` button under `Ports` to add one
- Optionally rename the bus to something easy to type, for example `IAC Driver Bus 1`
- Close the dialog and then run:

```bash
python labs/driver.py list --direction out
```

- Use the exact bus name shown in the list for `--port` or `--input-port`
- Example:

```bash
python labs/driver.py send --notes "C4 D4 E4 G4" --port "IAC Driver Bus 1"
```

If the list still shows no output ports, make sure you are running the lab from the same Python environment where `python-rtmidi` and `mido` are installed.

## Melody Notation

Melodies can include notes, durations, chords, and rests:

**Single notes:**
```
C4 D4 E4 G4
```

**Notes with durations (in seconds):**
```
C4:1 D4:0.5 E4:0.25 G4:0.5
```

**Chords (simultaneous notes) using square brackets or parentheses:**
```
[C4,E4,G4] [D4,F4,A4] [E4,G4,B4]
```

**Chords with durations:**
```
[C4,E4,G4]:1 [D4,F4,A4]:0.5 [E4,G4,B4]:0.5
```

**Rests:**
```
C4 R:0.5 D4 REST:0.25 E4
```

**Mix everything together:**
```
[C4,E4,G4]:1 C4:0.5 R:0.25 [D4,F4,A4]:1 D4:0.5
```

### Important: Chords require a polyphonic synth

Chords will **only sound if your synthesizer or DAW is set to a polyphonic instrument**. If you hear only one note when playing a chord:

1. Check your synth/GarageBand patch — it may be set to a monophonic instrument (like a lead synthesizer or filtered bass)
2. Switch to a polyphonic instrument such as a piano, strings, pad, or organ
3. In GarageBand, choose a chord-capable instrument like "Keyboard" → "Piano"

### Program Change (Patch Selection)

You can use the `--program` flag to change the instrument patch before playing:

```bash
python labs/driver.py send --notes "[C4,E4,G4]:1" --program 0 --port "IAC Driver Bus 1"
```

Program numbers are 0-127 and map to standard General MIDI (GM) patches. Common patches include:
- 0-7: Pianos (best for chords!)
- 16-23: Organs
- 40-47: Strings
- 48-55: Ensembles
- 80-87: Synth leads

**⚠️ GarageBand Limitation:** GarageBand does not respond to incoming MIDI program changes. Program changes only work when routing MIDI to external hardware synthesizers or other DAWs. If you're using GarageBand as your destination, you need to manually select the instrument patch in GarageBand's interface—the program change flag won't affect it.

### GarageBand AppleScript patch automation

On macOS, you can use AppleScript to drive GarageBand's UI and try to select a patch by name. This is a best-effort helper that may require:

- GarageBand already running
- Terminal or Python to be granted Accessibility permissions
- the GarageBand library/search field to respond to keyboard input

Use the new command:

```bash
python labs/driver.py garageband-set-patch --name "Electric Grand Piano"
```

If the AppleScript helper does not behave consistently, fall back to selecting the patch manually inside GarageBand.

### GUI Instrument Selector

The QML GUI includes a visual instrument selector with:
- Quick-select category buttons (Piano, Organ, Strings, Synth, etc.)
- Search by instrument name (type "piano" or "strings" to find matching patches)
- Display of both the instrument name and its General MIDI program number
- Instant program change sending when you select an instrument

This helps students understand that instruments have numeric IDs (0-127) while learning instrument names in English.
### Qt GUI on macOS

If `python3 -m labs.driver gui` fails with `Could not find the Qt platform plugin "cocoa"`, this lab now sets the plugin path automatically in `labs/driver.py`. Make sure you are running it from the same virtual environment where `PySide6` is installed:

```bash
source .venv/bin/activate
python3 -m labs.driver gui
```
## Cross-platform notes

- macOS: use `IAC Driver` for virtual MIDI, or the MIDI port created by your USB-MIDI adapter.
- Windows: install a virtual MIDI driver such as `loopMIDI` or `loopBe1`, then use the port name shown by `python labs/driver.py list --direction out`.
- Linux: use ALSA/MIDI routing. The code should see ALSA MIDI ports when `python-rtmidi` is installed. Use `aconnect -l` to inspect available ports if needed.
- ChromeOS: native ChromeOS does not always expose Python/USB-MIDI. Use the Linux container (Crostini) if available and ensure the USB-MIDI device is shared into that container. The same `mido` + `python-rtmidi` code can work there if the Linux environment has access to the MIDI device.

## Notes

- This lab captures MIDI performance data, not audio.
- When you connect the MicroKORG via USB-to-MIDI DIN cable, select its MIDI port instead of the virtual port.

## Example Melodies

The `labs/examples/` folder contains ready-to-use melody files for students to learn from:

- **heart_and_soul.txt**: Classic "Heart and Soul" using chord notation
- **c_major_scale.txt**: C major scale with consistent rhythm
- **simple_rhythm.txt**: Example mixing single notes, rests, and chords

Try them with:

```bash
python labs/driver.py send --notes "$(cat labs/examples/heart_and_soul.txt)" --port "IAC Driver Bus 1"
python labs/driver.py send --notes "$(cat labs/examples/c_major_scale.txt)" --port "IAC Driver Bus 1"
python labs/driver.py send --notes "$(cat labs/examples/simple_rhythm.txt)" --program 0 --port "IAC Driver Bus 1"
```

Or save and edit them:

```bash
cp labs/examples/heart_and_soul.txt my_version.txt
# Edit my_version.txt in your editor
python labs/driver.py send --notes "$(cat my_version.txt)" --port "IAC Driver Bus 1"
```

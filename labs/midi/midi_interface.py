import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

try:
    import mido
    mido.set_backend("mido.backends.rtmidi")
except ImportError:
    mido = None  # type: ignore

DEFAULT_TEMPO = 120
DEFAULT_VELOCITY = 100
DEFAULT_CHANNEL = 1
DEFAULT_DURATION = 0.25

# General MIDI Instrument List (Program 0-127)
GM_INSTRUMENTS = {
    # Pianos (0-7)
    0: "Acoustic Grand Piano", 1: "Bright Acoustic Piano", 2: "Electric Grand Piano", 3: "Honky-tonk Piano",
    4: "Electric Piano 1", 5: "Electric Piano 2", 6: "Harpsichord", 7: "Clavichord",
    # Chromatic Percussion (8-15)
    8: "Celesta", 9: "Glockenspiel", 10: "Music Box", 11: "Vibraphone",
    12: "Marimba", 13: "Xylophone", 14: "Tubular Bell", 15: "Dulcimer",
    # Organ (16-23)
    16: "Drawbar Organ", 17: "Percussive Organ", 18: "Rock Organ", 19: "Church Organ",
    20: "Reed Organ", 21: "Accordion", 22: "Harmonica", 23: "Bandneon",
    # Guitar (24-31)
    24: "Nylon Guitar", 25: "Steel Guitar", 26: "Jazz Guitar", 27: "Clean Electric Guitar",
    28: "Muted Electric Guitar", 29: "Overdriven Guitar", 30: "Distortion Guitar", 31: "Guitar Harmonics",
    # Bass (32-39)
    32: "Acoustic Bass", 33: "Fingered Bass", 34: "Picked Bass", 35: "Fretless Bass",
    36: "Slap Bass 1", 37: "Slap Bass 2", 38: "Synth Bass 1", 39: "Synth Bass 2",
    # Strings (40-47)
    40: "Violin", 41: "Viola", 42: "Cello", 43: "Contrabass",
    44: "Tremolo Strings", 45: "Pizzicato Strings", 46: "Orchestral Harp", 47: "Timpani",
    # Ensemble (48-55) — Good for chords!
    48: "String Ensemble 1", 49: "String Ensemble 2", 50: "Synth Strings 1", 51: "Synth Strings 2",
    52: "Choir Aahs", 53: "Choir Oohs", 54: "Synth Voice", 55: "Orchestra Hit",
    # Brass (56-63)
    56: "Trumpet", 57: "Trombone", 58: "Tuba", 59: "Muted Trumpet",
    60: "French Horn", 61: "Brass Section", 62: "Synth Brass 1", 63: "Synth Brass 2",
    # Reed (64-71)
    64: "Soprano Saxophone", 65: "Alto Saxophone", 66: "Tenor Saxophone", 67: "Baritone Saxophone",
    68: "Oboe", 69: "English Horn", 70: "Bassoon", 71: "Clarinet",
    # Pipe (72-79)
    72: "Piccolo", 73: "Flute", 74: "Recorder", 75: "Pan Flute",
    76: "Blown Bottle", 77: "Shakuhachi", 78: "Whistle", 79: "Ocarina",
    # Synth Lead (80-87)
    80: "Lead 1 (Square)", 81: "Lead 2 (Sawtooth)", 82: "Lead 3 (Calliope)", 83: "Lead 4 (Chiff)",
    84: "Lead 5 (Charang)", 85: "Lead 6 (Voice)", 86: "Lead 7 (Fifths)", 87: "Lead 8 (Bass+Lead)",
    # Synth Pad (88-95)
    88: "Pad 1 (Warm)", 89: "Pad 2 (Cold)", 90: "Pad 3 (Polysynth)", 91: "Pad 4 (Choir)",
    92: "Pad 5 (Bowed)", 93: "Pad 6 (Metallic)", 94: "Pad 7 (Halo)", 95: "Pad 8 (Sweep)",
    # Synth Effects (96-103)
    96: "FX 1 (Rain)", 97: "FX 2 (Soundtrack)", 98: "FX 3 (Crystal)", 99: "FX 4 (Atmosphere)",
    100: "FX 5 (Brightness)", 101: "FX 6 (Goblins)", 102: "FX 7 (Echoes)", 103: "FX 8 (Sci-Fi)",
    # Ethnic (104-111)
    104: "Sitar", 105: "Banjo", 106: "Shamisen", 107: "Koto",
    108: "Kalimba", 109: "Bag Pipe", 110: "Fiddle", 111: "Shanai",
    # Percussive (112-119)
    112: "Tinkle Bell", 113: "Agogo", 114: "Steel Drums", 115: "Woodblock",
    116: "Taiko Drum", 117: "Melodic Tom", 118: "Synth Drum", 119: "Reverse Cymbal",
    # Sound Effects (120-127)
    120: "Guitar Fret Noise", 121: "Breath Noise", 122: "Seashore", 123: "Bird Tweet",
    124: "Telephone Ring", 125: "Helicopter", 126: "Applause", 127: "Gunshot",
}

# Popular instrument categories by program number for quick access
INSTRUMENT_CATEGORIES = {
    "Piano": [0, 1, 2, 3, 4, 5],
    "Organ": [16, 17, 18, 19, 20],
    "Guitar": [24, 25, 26, 27, 28],
    "Bass": [32, 33, 34, 35],
    "Strings": [40, 41, 42, 43, 44, 45],
    "Ensemble": [48, 49, 50, 51, 52, 53],
    "Brass": [56, 57, 58, 59, 60, 61],
    "Woodwind": [64, 65, 66, 68, 69, 70, 73],
    "Synth": [80, 81, 82, 88, 89, 90, 91],
}

# GarageBand uses patch names that do not always match GM names.
# This mapping provides search queries that are more likely to match GarageBand's library.
GARAGEBAND_PROGRAM_QUERY_MAP = {
    # Pianos
    0: "Grand Piano",
    1: "Bright Piano",
    2: "Electric Grand",
    3: "Honky Tonk Piano",
    4: "Classic Electric Piano",
    5: "Electric Piano",
    6: "Harpsichord",
    7: "Clav",
    # Organs
    16: "Hammond Organ",
    17: "Organ",
    18: "Rock Organ",
    19: "Church Organ",
    # Guitars
    24: "Classical Guitar",
    25: "Acoustic Guitar",
    26: "Jazz Guitar",
    27: "Clean Guitar",
    # Basses
    32: "Upright Bass",
    33: "Finger Bass",
    34: "Picked Bass",
    35: "Fretless Bass",
    38: "Synth Bass",
    39: "Synth Bass",
    # Strings / ensemble
    40: "Violin",
    41: "Viola",
    42: "Cello",
    43: "Contrabass",
    48: "String Ensemble",
    49: "String Ensemble",
    50: "Synth Strings",
    51: "Synth Strings",
    52: "Choir",
    53: "Choir",
    # Brass
    56: "Trumpet",
    57: "Trombone",
    58: "Tuba",
    60: "French Horn",
    61: "Brass Section",
    # Woodwind
    64: "Soprano Sax",
    65: "Alto Sax",
    66: "Tenor Sax",
    67: "Baritone Sax",
    68: "Oboe",
    69: "English Horn",
    70: "Bassoon",
    71: "Clarinet",
    73: "Flute",
    # Synth leads / pads
    80: "Square Lead",
    81: "Saw Lead",
    88: "Warm Pad",
    89: "Soft Pad",
    90: "Poly Synth Pad",
    91: "Choir Pad",
}

GARAGEBAND_PATCH_INDEX_DIRS = [
    Path("/Library/Application Support/GarageBand/Instrument Library/Plug-In Settings"),
    Path("/Library/Application Support/GarageBand/Instrument Library/Sampler/Sampler Instruments"),
    Path("/Library/Application Support/Logic/Plug-In Settings"),
    Path("/Library/Application Support/Logic/Sampler Instruments"),
    Path.home() / "Library/Audio/Presets",
]

GARAGEBAND_PATCH_FILE_EXTS = {".pst", ".exs", ".aupreset"}


def _garageband_patch_cache_path() -> Path:
    cache_dir = Path.home() / ".cache" / "microkorg-midi-lab"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / "garageband_patch_index.json"


def _garageband_patch_source_for_path(path: Path) -> str:
    path_str = str(path)
    if path_str.startswith("/Library/Application Support/GarageBand/"):
        return "GarageBand"
    if path_str.startswith("/Library/Application Support/Logic/"):
        return "Logic"
    if path_str.startswith(str(Path.home() / "Library/Audio/Presets")):
        return "User Presets"
    return "Other"


def _build_garageband_patch_index() -> Dict[str, Any]:
    patches: Dict[str, Dict[str, Any]] = {}
    scanned_dirs: List[str] = []

    for root in GARAGEBAND_PATCH_INDEX_DIRS:
        if not root.exists():
            continue
        scanned_dirs.append(str(root))
        for file_path in root.rglob("*"):
            if not file_path.is_file() or file_path.suffix.lower() not in GARAGEBAND_PATCH_FILE_EXTS:
                continue

            name = file_path.stem.replace("_", " ").strip()
            if not name:
                continue

            key = name.casefold()
            item = {
                "name": name,
                "kind": file_path.suffix.lower().lstrip("."),
                "source": _garageband_patch_source_for_path(file_path),
                "path": str(file_path),
                "folder": file_path.parent.name,
            }

            # Keep shortest path for duplicate names to reduce noise.
            existing = patches.get(key)
            if existing is None or len(item["path"]) < len(existing["path"]):
                patches[key] = item

    patch_list = sorted(patches.values(), key=lambda p: p["name"].casefold())
    return {
        "version": 1,
        "generated_at": int(time.time()),
        "scanned_dirs": scanned_dirs,
        "count": len(patch_list),
        "patches": patch_list,
    }


def load_garageband_patch_index(rebuild: bool = False) -> Dict[str, Any]:
    cache_path = _garageband_patch_cache_path()
    if not rebuild and cache_path.exists():
        try:
            return json.loads(cache_path.read_text())
        except Exception:
            pass

    index = _build_garageband_patch_index()
    cache_path.write_text(json.dumps(index, ensure_ascii=True, indent=2))
    return index


def search_garageband_patches(query: str = "", limit: int = 200, rebuild: bool = False) -> List[Dict[str, Any]]:
    index = load_garageband_patch_index(rebuild=rebuild)
    patches = index.get("patches", [])

    query_clean = (query or "").strip().casefold()
    if not query_clean:
        return patches[: max(1, int(limit))]

    results = [
        p for p in patches
        if query_clean in str(p.get("name", "")).casefold()
        or query_clean in str(p.get("folder", "")).casefold()
        or query_clean in str(p.get("source", "")).casefold()
    ]
    return results[: max(1, int(limit))]


def _garageband_query_for_program(program: int, gm_name: str) -> str:
    query = GARAGEBAND_PROGRAM_QUERY_MAP.get(program)
    if query:
        return query

    # Fallback: strip GM numbering/parentheses and normalize for search.
    simplified = re.sub(r"\s*\([^)]*\)", "", gm_name)
    simplified = re.sub(r"\b\d+\b", "", simplified)
    simplified = re.sub(r"\s+", " ", simplified).strip()
    return simplified or gm_name


def ensure_mido_installed() -> None:
    if mido is None:
        raise ModuleNotFoundError(
            "The 'mido' package is required. Install dependencies with 'pip install -r labs/requirements.txt'."
        )

NoteEvent = Tuple[Optional[int], float]


def _note_name_to_number(note_name: str) -> int:
    """Convert note name like 'C4' or 'D#5' to MIDI note number."""
    note_name = note_name.strip().upper()
    
    note_to_semitone = {
        'C': 0, 'D': 2, 'E': 4, 'F': 5,
        'G': 7, 'A': 9, 'B': 11
    }
    
    if not note_name or note_name[0] not in note_to_semitone:
        raise ValueError(f"Invalid note: {note_name}")
    
    note_char = note_name[0]
    rest = note_name[1:]
    
    semitone = note_to_semitone[note_char]
    octave = 0
    
    while rest and rest[0] in ('#', 'B'):
        if rest[0] == '#':
            semitone += 1
        elif rest[0] == 'B':
            semitone -= 1
        rest = rest[1:]
    
    if not rest or not rest.isdigit():
        raise ValueError(f"Invalid note: {note_name}")
    
    octave = int(rest)
    return (octave + 1) * 12 + semitone


def _number_to_note_name(note_number: int) -> str:
    """Convert MIDI note number back to note name like 'C4' or 'D#5'."""
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    octave = (note_number // 12) - 1
    semitone = note_number % 12
    return f"{note_names[semitone]}{octave}"


def _recording_json_to_melody(json_data: Dict[str, Any], min_velocity: int = 10) -> str:
    """Convert a recorded MIDI JSON to simple melody text notation.
    
    Filters out very quiet notes and returns melody as "C4 D4 E4 G4" format.
    """
    events = json_data.get("events", [])
    
    # Build a dict of note_on/note_off pairs to get durations
    notes_playing: Dict[int, Tuple[float, int]] = {}  # note_number -> (start_time, velocity)
    melody_notes: List[Tuple[float, int, float]] = []  # (start_time, note_number, duration)
    
    for event in events:
        event_time = float(event.get("time", 0.0))
        msg_dict = event.get("message", {})
        msg_type = msg_dict.get("type")
        
        if msg_type == "note_on":
            note = msg_dict.get("note")
            velocity = msg_dict.get("velocity", 64)
            if note is not None and velocity >= min_velocity:
                notes_playing[note] = (event_time, velocity)
        
        elif msg_type == "note_off":
            note = msg_dict.get("note")
            if note is not None and note in notes_playing:
                start_time, velocity = notes_playing.pop(note)
                duration = event_time - start_time
                if duration > 0.01:  # Ignore very short notes
                    melody_notes.append((start_time, note, duration))
    
    # Sort by start time and convert to notation
    melody_notes.sort(key=lambda x: x[0])
    
    melody_text_parts = []
    for start_time, note_number, duration in melody_notes:
        note_name = _number_to_note_name(note_number)
        duration_rounded = round(duration * 4) / 4  # Round to nearest 16th note
        if duration_rounded < 0.5:
            duration_rounded = 0.25
        melody_text_parts.append(f"{note_name}:{duration_rounded:.2g}")
    
    return " ".join(melody_text_parts) if melody_text_parts else ""


def search_instruments(query: str) -> List[Dict[str, Any]]:
    """Search for instruments by name substring (case-insensitive).
    
    Returns list of dicts with 'program', 'name' keys, sorted by relevance.
    """
    query_lower = query.strip().lower()
    results = []
    
    for program, name in GM_INSTRUMENTS.items():
        if query_lower in name.lower():
            results.append({
                "program": program,
                "name": name,
            })
    
    # Sort by exact match first, then alphabetically
    results.sort(key=lambda x: (
        x["name"].lower() != query_lower,  # Exact matches first
        x["program"]  # Then by program number
    ))
    return results


def get_instrument_categories() -> Dict[str, List[Dict[str, Any]]]:
    """Get instruments organized by category for quick selection.
    
    Returns dict of category -> list of dicts with 'program', 'name' keys.
    """
    categories = {}
    for category, programs in INSTRUMENT_CATEGORIES.items():
        categories[category] = [
            {"program": p, "name": GM_INSTRUMENTS[p]}
            for p in programs
        ]
    return categories


def _osascript_available() -> bool:
    return shutil.which("osascript") is not None


def _escape_applescript_string(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _run_osascript(script: str, timeout_seconds: float = 15.0) -> str:
    if not _osascript_available():
        raise RuntimeError("osascript is not available on this system.")

    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"AppleScript failed: {result.stderr.strip() or result.stdout.strip()}"
        )
    return result.stdout.strip()


def _garageband_automation_prerequisites() -> None:
    if sys.platform != "darwin":
        raise RuntimeError("GarageBand AppleScript support is only available on macOS.")
    if not _osascript_available():
        raise RuntimeError("osascript is not available on this system.")


def stop_garageband_playback(assume_playing: bool = True) -> None:
    """
    Stop GarageBand playback by simulating spacebar (play/pause toggle).
    
    Note: GarageBand does not expose playback state via AppleScript, and the
    toolbar play button is not accessible via standard UI automation.
    
    Args:
        assume_playing: If True (default), press spacebar to toggle playback.
                       This is safe when you KNOW playback is active (e.g., during Ctrl+C).
                       If False, this function does nothing (reserved for future use).
    """
    if not assume_playing:
        return
    
    _garageband_automation_prerequisites()

    script = '''
    tell application "GarageBand"
        activate
        delay 0.1
    end tell
    
    tell application "System Events"
        tell process "GarageBand"
            set frontmost to true
            delay 0.1
            -- Press spacebar to toggle play/pause
            -- Only safe when playback is definitely active
            key code 49
            delay 0.2
        end tell
    end tell
    '''
    _run_osascript(script)


def set_garageband_patch(patch_name: str, track_number: int = 1, retries: int = 2) -> None:
    _garageband_automation_prerequisites()

    escaped_name = _escape_applescript_string(patch_name)
    track_number = max(1, int(track_number))
    script = f'''
    tell application "GarageBand" to activate
    delay 0.4
    tell application "System Events"
        tell process "GarageBand"
            set frontmost to true
            -- Best-effort track selection by index before opening the browser.
            try
                set focused of first window to true
                tell front window
                    repeat {track_number} - 1 times
                        key code 125
                        delay 0.05
                    end repeat
                end tell
            end try

            set searchField to missing value

            -- First see whether the Search Sounds field is already present.
            set elems to entire contents of front window
            repeat with e in elems
                try
                    if role of e is "AXTextField" then
                        try
                            set d to description of e
                        on error
                            set d to ""
                        end try
                        if d contains "search text field" then
                            set searchField to e
                            exit repeat
                        end if
                    end if
                end try
            end repeat

            -- If not present, toggle browser open and search again.
            if searchField is missing value then
                key code 16
                delay 0.45
                set elems to entire contents of front window
                repeat with e in elems
                    try
                        if role of e is "AXTextField" then
                            try
                                set d to description of e
                            on error
                                set d to ""
                            end try
                            if d contains "search text field" then
                                set searchField to e
                                exit repeat
                            end if
                        end if
                    end try
                end repeat
            end if

            if searchField is missing value then
                error "GarageBand Search Sounds field not found"
            end if

            set focused of searchField to true
            delay 0.1
            keystroke "a" using command down
            key code 51
            keystroke "{escaped_name}"
            delay 0.35
            key code 125
            delay 0.1
            key code 36
        end tell
    end tell
    '''

    attempts = max(1, int(retries) + 1)
    last_error: Optional[Exception] = None
    for attempt in range(1, attempts + 1):
        try:
            _run_osascript(script)
            return
        except Exception as exc:
            last_error = exc
            if attempt < attempts:
                time.sleep(0.25)

    raise RuntimeError(f"Unable to set GarageBand patch '{patch_name}': {last_error}")


def set_garageband_patch_by_program(program: int, track_number: int = 1, retries: int = 2) -> str:
    program_clamped = max(0, min(127, int(program)))
    gm_name = GM_INSTRUMENTS.get(program_clamped)
    if gm_name is None:
        raise ValueError(f"Unknown GM program number: {program}")
    query = _garageband_query_for_program(program_clamped, gm_name)
    set_garageband_patch(query, track_number=track_number, retries=retries)
    return query


class MidiInterface:
    @staticmethod
    def load_garageband_patch_index(rebuild: bool = False) -> Dict[str, Any]:
        return load_garageband_patch_index(rebuild=rebuild)

    @staticmethod
    def search_garageband_patches(query: str = "", limit: int = 200, rebuild: bool = False) -> List[Dict[str, Any]]:
        return search_garageband_patches(query=query, limit=limit, rebuild=rebuild)

    @staticmethod
    def stop_garageband_playback(assume_playing: bool = True) -> None:
        stop_garageband_playback(assume_playing=assume_playing)

    @staticmethod
    def set_garageband_patch(patch_name: str, track_number: int = 1, retries: int = 2) -> None:
        set_garageband_patch(patch_name, track_number=track_number, retries=retries)

    @staticmethod
    def set_garageband_patch_by_program(program: int, track_number: int = 1, retries: int = 2) -> str:
        return set_garageband_patch_by_program(program, track_number=track_number, retries=retries)

    @staticmethod
    def _send_panic_messages(port: Any, channels: Optional[Sequence[int]] = None) -> None:
        channel_list = list(channels) if channels is not None else list(range(16))
        for ch in channel_list:
            # Sustain off, all sound off, all notes off.
            port.send(mido.Message("control_change", control=64, value=0, channel=ch))
            port.send(mido.Message("control_change", control=120, value=0, channel=ch))
            port.send(mido.Message("control_change", control=123, value=0, channel=ch))

    @staticmethod
    def panic(output_port: Optional[str] = None, channel: Optional[int] = None) -> None:
        ensure_mido_installed()
        port_name = MidiInterface.resolve_port(output_port, MidiInterface.list_output_ports())
        channels: Optional[List[int]] = None
        if channel is not None:
            channels = [max(0, min(15, channel - 1))]

        with mido.open_output(port_name) as port:
            MidiInterface._send_panic_messages(port, channels)

    @staticmethod
    def duration_to_seconds(duration_whole_note: float, tempo: int) -> float:
        if tempo <= 0:
            raise ValueError("Tempo must be greater than 0 BPM.")
        # Duration values are fractions of a whole note: 1.0=whole, 0.5=half, 0.25=quarter.
        return duration_whole_note * (240.0 / float(tempo))

    @staticmethod
    def list_output_ports() -> List[str]:
        ensure_mido_installed()
        return mido.get_output_names()

    @staticmethod
    def list_input_ports() -> List[str]:
        ensure_mido_installed()
        return mido.get_input_names()

    @staticmethod
    def resolve_port(name: Optional[str], available_ports: Sequence[str]) -> str:
        if name:
            return name
        if available_ports:
            return available_ports[0]
        raise RuntimeError("No MIDI ports found.")

    @staticmethod
    def parse_melody(melody_text: str) -> List[NoteEvent]:
        ensure_mido_installed()

        # Strip comments while preserving sharps in note names (e.g. C#4).
        melody_text = "\n".join(
            re.sub(r"(^|\s)#.*$", "", line).strip()
            for line in melody_text.splitlines()
        )
        
        # First pass: protect chords from being split by replacing commas inside them
        import re as regex
        
        # Find all chords [note,note,...] and (note,note,...)
        chord_pattern = r'[\[\(][A-G#b0-9, ]+[\]\)](?::[0-9.]+)?'
        chords = regex.findall(chord_pattern, melody_text, regex.IGNORECASE)
        chord_placeholders = {}
        
        protected_text = melody_text
        for i, chord in enumerate(chords):
            placeholder = f"__CHORD_{i}__"
            chord_placeholders[placeholder] = chord
            protected_text = protected_text.replace(chord, placeholder, 1)
        
        # Now tokenize safely
        tokens = [token.strip() for token in regex.split(r"[\s,;]+", protected_text.strip()) if token.strip()]
        
        # Restore chords
        tokens = [chord_placeholders.get(t, t) for t in tokens]
        
        notes: List[NoteEvent] = []

        for token in tokens:
            if not token:
                continue

            duration = DEFAULT_DURATION
            
            # Extract duration if present: note:duration or [chord]:duration format
            if ":" in token:
                colon_idx = token.rfind(":")
                token_part = token[:colon_idx]
                value = token[colon_idx+1:]
                try:
                    duration = float(value)
                except ValueError:
                    raise ValueError(f"Invalid duration in token '{token}'")
                token = token_part

            token_upper = token.upper()
            
            # Handle chords: [C4,E4,G4] or (C4,E4,G4)
            if (token_upper.startswith('[') and token_upper.endswith(']')) or \
               (token_upper.startswith('(') and token_upper.endswith(')')):
                chord_notes = token[1:-1].split(',')
                chord_numbers = []
                for chord_note in chord_notes:
                    chord_note = chord_note.strip()
                    try:
                        note_number = _note_name_to_number(chord_note)
                        chord_numbers.append(note_number)
                    except ValueError as exc:
                        raise ValueError(f"Unable to parse chord note '{chord_note}'") from exc
                # Store chord as negative note number to distinguish from single notes
                # Use -1 as marker and store the list separately in the duration tuple
                notes.append((-1, duration, chord_numbers))  # Special format for chords
                continue
            
            # Handle rests
            if token_upper in ("R", "REST", "_"):
                notes.append((None, duration))
                continue

            # Handle single notes
            try:
                note_number = _note_name_to_number(token)
            except ValueError as exc:
                raise ValueError(f"Unable to parse note '{token}'") from exc

            notes.append((note_number, duration))

        return notes

    @staticmethod
    def send_melody(
        melody_text: str,
        output_port: Optional[str] = None,
        tempo: int = DEFAULT_TEMPO,
        channel: int = DEFAULT_CHANNEL,
        velocity: int = DEFAULT_VELOCITY,
    ) -> None:
        ensure_mido_installed()
        if not melody_text or not melody_text.strip():
            raise ValueError("No notes were provided. Pass note text (e.g. 'C4 D4 E4') or use a valid file path with shell substitution.")
        notes = MidiInterface.parse_melody(melody_text)
        if not notes:
            raise ValueError("No playable notes were parsed from --notes.")
        port_name = MidiInterface.resolve_port(output_port, MidiInterface.list_output_ports())
        midi_channel = max(0, min(15, channel - 1))

        print(f"Playing melody on port: {port_name}")
        with mido.open_output(port_name) as port:
            try:
                for i, event in enumerate(notes):
                    # Handle chords (3-tuple format)
                    if len(event) == 3:
                        note_marker, duration_whole, chord_notes = event
                        duration_seconds = MidiInterface.duration_to_seconds(duration_whole, tempo)
                        note_names = [_number_to_note_name(n) for n in chord_notes]
                        chord_str = "[" + ",".join(note_names) + "]"
                        print(f"  [{i}] {chord_str} {duration_whole:g} ({duration_seconds:.3g}s)")
                        
                        # Send all note_on messages
                        for note in chord_notes:
                            msg = mido.Message(
                                "note_on",
                                note=note,
                                velocity=velocity,
                                channel=midi_channel,
                            )
                            port.send(msg)
                        
                        # Hold for duration
                        time.sleep(duration_seconds)
                        
                        # Send all note_off messages
                        for note in chord_notes:
                            msg = mido.Message(
                                "note_off",
                                note=note,
                                velocity=0,
                                channel=midi_channel,
                            )
                            port.send(msg)
                        continue
                    
                    # Handle single notes and rests (2-tuple format)
                    note, duration_whole = event
                    duration_seconds = MidiInterface.duration_to_seconds(duration_whole, tempo)
                    if note is None:
                        print(f"  [{i}] Rest {duration_whole:g} ({duration_seconds:.3g}s)")
                        time.sleep(duration_seconds)
                        continue

                    note_on = mido.Message(
                        "note_on",
                        note=note,
                        velocity=velocity,
                        channel=midi_channel,
                    )
                    note_off = mido.Message(
                        "note_off",
                        note=note,
                        velocity=0,
                        channel=midi_channel,
                    )

                    note_name = _number_to_note_name(note)
                    print(f"  [{i}] {note_name} {duration_whole:g} ({duration_seconds:.3g}s)")
                    port.send(note_on)
                    time.sleep(duration_seconds)
                    port.send(note_off)
            except KeyboardInterrupt:
                print("\nInterrupted. Sending all-notes-off...")
                MidiInterface._send_panic_messages(port)
                if sys.platform == "darwin":
                    try:
                        # We know playback is active during send_melody
                        MidiInterface.stop_garageband_playback(assume_playing=True)
                        print("Sent GarageBand stop playback command.")
                    except Exception as exc:
                        print(f"GarageBand stop command failed: {exc}")
                raise
        
        print("Done!")

    @staticmethod
    def send_program_change(
        program: int,
        output_port: Optional[str] = None,
        channel: int = DEFAULT_CHANNEL,
    ) -> None:
        ensure_mido_installed()
        port_name = MidiInterface.resolve_port(output_port, MidiInterface.list_output_ports())
        with mido.open_output(port_name) as port:
            port.send(
                mido.Message(
                    "program_change",
                    program=max(0, min(127, program)),
                    channel=max(0, min(15, channel - 1)),
                )
            )

    @staticmethod
    def send_control_change(
        control: int,
        value: int,
        output_port: Optional[str] = None,
        channel: int = DEFAULT_CHANNEL,
    ) -> None:
        ensure_mido_installed()
        port_name = MidiInterface.resolve_port(output_port, MidiInterface.list_output_ports())
        with mido.open_output(port_name) as port:
            port.send(
                mido.Message(
                    "control_change",
                    control=max(0, min(127, control)),
                    value=max(0, min(127, value)),
                    channel=max(0, min(15, channel - 1)),
                )
            )

    @staticmethod
    def record_performance(
        input_port: Optional[str] = None,
        output_file: str = "performance.json",
        duration: Optional[float] = None,
    ) -> Dict[str, Any]:
        ensure_mido_installed()
        port_name = MidiInterface.resolve_port(input_port, MidiInterface.list_input_ports())
        events: List[Dict[str, Any]] = []
        start_time = time.time()

        def callback(message: Any) -> None:
            events.append(
                {
                    "time": round(time.time() - start_time, 6),
                    "message": message.dict(),
                }
            )

        with mido.open_input(port_name, callback=callback):
            stop_at = time.time() + duration if duration is not None else None
            try:
                while stop_at is None or time.time() < stop_at:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                pass

        result = {"port": port_name, "events": events}
        with open(output_file, "w", encoding="utf-8") as handle:
            json.dump(result, handle, indent=2)

        return result

    @staticmethod
    def replay_performance(
        input_file: str,
        output_port: Optional[str] = None,
    ) -> None:
        ensure_mido_installed()
        with open(input_file, "r", encoding="utf-8") as handle:
            data = json.load(handle)

        events = data.get("events", [])
        port_name = MidiInterface.resolve_port(output_port, MidiInterface.list_output_ports())
        with mido.open_output(port_name) as port:
            last_time = 0.0
            for event in events:
                event_time = float(event.get("time", 0.0))
                delay = max(0.0, event_time - last_time)
                time.sleep(delay)
                message_dict = dict(event.get("message", {}))
                message_dict.pop("time", None)
                try:
                    message = mido.Message.from_dict(message_dict)
                except (TypeError, ValueError) as exc:
                    raise ValueError(f"Invalid recorded message: {message_dict}") from exc
                port.send(message)
                last_time = event_time

    @staticmethod
    def save_melody(melody_text: str, output_file: str) -> None:
        """Save a melody text to a file."""
        with open(output_file, "w", encoding="utf-8") as handle:
            handle.write(melody_text.strip())

    @staticmethod
    def load_melody(input_file: str) -> str:
        """Load a melody text from a file."""
        with open(input_file, "r", encoding="utf-8") as handle:
            return handle.read().strip()

    @staticmethod
    def recording_to_melody_text(input_file: str) -> str:
        """Convert a recorded MIDI JSON to simple melody text notation.
        
        Useful for capturing performances from GarageBand and converting
        them to editable text format.
        """
        with open(input_file, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return _recording_json_to_melody(data)

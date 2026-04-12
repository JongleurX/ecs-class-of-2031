import argparse
import importlib.util
import os
import sys
from pathlib import Path


def _find_qt_platform_plugin_path() -> str | None:
    spec = importlib.util.find_spec("PySide6")
    if spec is None or spec.origin is None:
        return None

    package_dir = Path(spec.origin).resolve().parent
    plugins_root = package_dir / "Qt" / "plugins"
    platforms_dir = plugins_root / "platforms"
    if platforms_dir.exists():
        return str(plugins_root)
    if plugins_root.exists():
        return str(plugins_root)
    return None

qt_plugins = _find_qt_platform_plugin_path()
if qt_plugins:
    os.environ.setdefault("QT_QPA_PLATFORM_PLUGIN_PATH", qt_plugins)
    os.environ.setdefault("QT_PLUGIN_PATH", qt_plugins)

try:
    from labs.midi_interface import MidiInterface
except ImportError:
    from midi_interface import MidiInterface


def run_gui() -> int:
    try:
        from PySide6.QtGui import QGuiApplication
        from PySide6.QtQml import QQmlApplicationEngine
        from PySide6.QtCore import QCoreApplication
    except ModuleNotFoundError:
        print("PySide6 is not installed. Install the requirements and try again.")
        return 1

    # Force Qt plugin paths in environment and ensure they're not overridden
    plugin_path = _find_qt_platform_plugin_path()
    if plugin_path:
        os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = plugin_path
        os.environ["QT_PLUGIN_PATH"] = plugin_path
        os.environ["QT_PLUGIN_OPTIONFLAGS"] = ""
    
    # Set library paths in code
    if plugin_path:
        QCoreApplication.setLibraryPaths([plugin_path])
    
    # Set the platform to 'cocoa' explicitly on macOS
    if sys.platform == "darwin":
        os.environ["QT_QPA_PLATFORM"] = "cocoa"

    try:
        from labs.midi_app import MidiApp
    except ImportError:
        from midi_app import MidiApp

    try:
        app = QGuiApplication(sys.argv)
    except Exception as e:
        print(f"Failed to create QGuiApplication: {e}")
        print(f"Plugin path: {plugin_path}")
        print(f"QT_QPA_PLATFORM_PLUGIN_PATH: {os.environ.get('QT_QPA_PLATFORM_PLUGIN_PATH')}")
        return 1
    
    engine = QQmlApplicationEngine()
    backend = MidiApp()
    engine.rootContext().setContextProperty("backend", backend)

    qml_file = Path(__file__).resolve().parent / "qml" / "Main.qml"
    engine.load(str(qml_file))
    if not engine.rootObjects():
        print("Failed to load QML interface.")
        return 1

    return app.exec()


def list_ports(direction: str) -> None:
    if direction in ("out", "both"):
        outputs = MidiInterface.list_output_ports()
        print("MIDI output ports:")
        for port in outputs:
            print(f"  {port}")
        if not outputs:
            print("  (no output ports found)")

    if direction in ("in", "both"):
        inputs = MidiInterface.list_input_ports()
        print("MIDI input ports:")
        for port in inputs:
            print(f"  {port}")
        if not inputs:
            print("  (no input ports found)")


def main() -> int:
    parser = argparse.ArgumentParser(description="MicroKORG MIDI lab driver")
    subparsers = parser.add_subparsers(dest="command")

    list_parser = subparsers.add_parser("list", help="List available MIDI ports")
    list_parser.add_argument("--direction", choices=["in", "out", "both"], default="both")

    send_parser = subparsers.add_parser("send", help="Send a melody to a MIDI output port")
    send_parser.add_argument("--notes", required=True, help="Melody notes, e.g. \"C4 D4 E4 G4\" or \"[C4,E4,G4]\"")
    send_parser.add_argument("--port", default=None, help="Output port name")
    send_parser.add_argument("--tempo", type=int, default=120, help="Tempo in BPM")
    send_parser.add_argument("--channel", type=int, default=1, help="MIDI channel (1-16)")
    send_parser.add_argument("--velocity", type=int, default=100, help="Note velocity (0-127)")
    send_parser.add_argument("--program", type=int, help="MIDI program change (0-127, optional)")

    gb_parser = subparsers.add_parser("garageband-set-patch", help="Set a GarageBand patch via AppleScript")
    gb_parser.add_argument("--name", required=True, help="Name of the GarageBand patch to select")
    gb_parser.add_argument("--track", type=int, default=1, help="GarageBand track number (optional)")

    record_parser = subparsers.add_parser("record", help="Record MIDI performance from an input port")
    record_parser.add_argument("--input-port", default=None, help="MIDI input port name")
    record_parser.add_argument("--output-file", default="performance.json", help="File path to save the recording")
    record_parser.add_argument("--duration", type=float, default=10.0, help="Recording duration in seconds")

    replay_parser = subparsers.add_parser("replay", help="Replay a recorded MIDI performance")
    replay_parser.add_argument("--output-port", default=None, help="MIDI output port name")
    replay_parser.add_argument("--input-file", default="performance.json", help="Recorded performance JSON file")

    save_parser = subparsers.add_parser("save", help="Save a melody to a text file")
    save_parser.add_argument("--notes", required=True, help="Melody notes, e.g. \"C4 D4 E4 G4\"")
    save_parser.add_argument("--output-file", required=True, help="File path to save the melody")

    load_parser = subparsers.add_parser("load", help="Load and display a melody from a text file")
    load_parser.add_argument("--input-file", required=True, help="Melody file to load")

    convert_parser = subparsers.add_parser("convert", help="Convert a recorded MIDI performance to melody text notation")
    convert_parser.add_argument("--input-file", default="performance.json", help="Recorded performance JSON file")
    convert_parser.add_argument("--output-file", default=None, help="Optional file to save the converted melody text")

    gui_parser = subparsers.add_parser("gui", help="Launch the QML GUI")

    parser.set_defaults(command="gui")
    args = parser.parse_args()

    if args.command == "list":
        list_ports(args.direction)
        return 0

    if args.command == "send":
        if args.program is not None:
            print(f"Sending program change to patch {args.program}...")
            MidiInterface.send_program_change(
                program=args.program,
                output_port=args.port,
                channel=args.channel,
            )
        
        MidiInterface.send_melody(
            melody_text=args.notes,
            output_port=args.port,
            tempo=args.tempo,
            channel=args.channel,
            velocity=args.velocity,
        )
        return 0

    if args.command == "garageband-set-patch":
        print(f"Setting GarageBand patch to {args.name} on track {args.track}...")
        MidiInterface.set_garageband_patch(args.name, args.track)
        print("GarageBand patch automation command sent.")
        return 0

    if args.command == "record":
        print(f"Recording performance to {args.output_file}...")
        MidiInterface.record_performance(
            input_port=args.input_port,
            output_file=args.output_file,
            duration=args.duration,
        )
        print("Recording finished.")
        return 0

    if args.command == "replay":
        print(f"Replaying performance from {args.input_file}...")
        MidiInterface.replay_performance(
            input_file=args.input_file,
            output_port=args.output_port,
        )
        print("Replay finished.")
        return 0

    if args.command == "save":
        MidiInterface.save_melody(
            melody_text=args.notes,
            output_file=args.output_file,
        )
        print(f"Melody saved to {args.output_file}")
        return 0

    if args.command == "load":
        melody = MidiInterface.load_melody(args.input_file)
        print(f"Loaded melody from {args.input_file}:")
        print(melody)
        return 0

    if args.command == "convert":
        melody = MidiInterface.recording_to_melody_text(args.input_file)
        if args.output_file:
            MidiInterface.save_melody(melody, args.output_file)
            print(f"Converted and saved to {args.output_file}:")
        else:
            print(f"Converted melody from {args.input_file}:")
        print(melody)
        return 0

    if args.command == "gui":
        return run_gui()

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

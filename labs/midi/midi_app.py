import threading
from pathlib import Path
from typing import List

from PySide6.QtCore import QObject, Property, Signal, Slot

try:
    from labs.midi.midi_interface import MidiInterface, search_instruments, get_instrument_categories, GM_INSTRUMENTS
except ImportError:
    from midi_interface import MidiInterface, search_instruments, get_instrument_categories, GM_INSTRUMENTS


class MidiApp(QObject):
    outputPortsChanged = Signal()
    inputPortsChanged = Signal()
    statusTextChanged = Signal()

    def __init__(self):
        super().__init__()
        self._output_ports = MidiInterface.list_output_ports()
        self._input_ports = MidiInterface.list_input_ports()
        self._status_text = "Ready"

    @Property("QStringList", notify=outputPortsChanged)
    def outputPorts(self) -> List[str]:
        return self._output_ports

    @Property("QStringList", notify=inputPortsChanged)
    def inputPorts(self) -> List[str]:
        return self._input_ports

    @Property(str, notify=statusTextChanged)
    def statusText(self) -> str:
        return self._status_text

    @Slot()
    def refreshPorts(self) -> None:
        self._output_ports = MidiInterface.list_output_ports()
        self._input_ports = MidiInterface.list_input_ports()
        self.outputPortsChanged.emit()
        self.inputPortsChanged.emit()
        self.setStatus("MIDI ports refreshed")

    @Slot(str, str, int, int, int)
    def sendMelody(self, melody_text: str, port_name: str, tempo: int, channel: int, velocity: int) -> None:
        try:
            MidiInterface.send_melody(
                melody_text=melody_text,
                output_port=port_name or None,
                tempo=tempo,
                channel=channel,
                velocity=velocity,
            )
            self.setStatus(f"Melody sent to {port_name or 'default port'}")
        except Exception as exc:
            self.setStatus(f"Send failed: {exc}")

    @Slot(str, str, float)
    def recordPerformance(self, input_port: str, output_file: str, duration: float) -> None:
        output_path = output_file or "performance.json"

        def task() -> None:
            try:
                result = MidiInterface.record_performance(
                    input_port=input_port or None,
                    output_file=output_path,
                    duration=duration if duration > 0 else None,
                )
                self.setStatus(f"Recorded {len(result['events'])} events to {output_path}")
            except Exception as exc:
                self.setStatus(f"Record failed: {exc}")

        thread = threading.Thread(target=task, daemon=True)
        thread.start()
        self.setStatus("Recording started")

    @Slot(str, str)
    def replayPerformance(self, output_port: str, input_file: str) -> None:
        input_path = input_file or "performance.json"

        def task() -> None:
            try:
                MidiInterface.replay_performance(input_file=input_path, output_port=output_port or None)
                self.setStatus(f"Replayed performance from {input_path}")
            except Exception as exc:
                self.setStatus(f"Replay failed: {exc}")

        thread = threading.Thread(target=task, daemon=True)
        thread.start()
        self.setStatus("Replay started")

    @Slot(str)
    def setStatus(self, text: str) -> None:
        self._status_text = text
        self.statusTextChanged.emit()

    @Slot(str, result=str)
    def searchInstruments(self, query: str) -> str:
        """Search for instruments by name substring. Returns JSON string."""
        import json
        results = search_instruments(query)
        return json.dumps(results)

    @Slot(result=str)
    def getInstrumentCategories(self) -> str:
        """Get instruments organized by category. Returns JSON string."""
        import json
        return json.dumps(get_instrument_categories())

    @Slot(int, str, int)
    def sendProgramChange(self, program: int, port_name: str, channel: int) -> None:
        """Send a program change message."""
        try:
            MidiInterface.send_program_change(
                program=program,
                output_port=port_name or None,
                channel=channel,
            )
            instrument_name = GM_INSTRUMENTS.get(program, "Unknown")
            self.setStatus(f"Program change to {program} ({instrument_name})")
        except Exception as exc:
            self.setStatus(f"Program change failed: {exc}")

    @Slot(str)
    def setGarageBandPatch(self, patch_name: str) -> None:
        """Set a GarageBand patch via AppleScript."""
        try:
            MidiInterface.set_garageband_patch(patch_name)
            self.setStatus(f"GarageBand patch set to {patch_name}")
        except Exception as exc:
            self.setStatus(f"GarageBand patch failed: {exc}")

    @Slot(int)
    def setGarageBandPatchByProgram(self, program: int) -> None:
        """Set a GarageBand patch by GM program number using a GB-friendly query mapping."""
        try:
            query_used = MidiInterface.set_garageband_patch_by_program(program)
            gm_name = GM_INSTRUMENTS.get(program, "Unknown")
            self.setStatus(f"GarageBand patch set for GM {program} ({gm_name}) via '{query_used}'")
        except Exception as exc:
            self.setStatus(f"GarageBand patch-by-program failed: {exc}")

    @Slot(str, int, bool, result=str)
    def searchGarageBandPatches(self, query: str, limit: int = 200, rebuild: bool = False) -> str:
        """Search dynamic GarageBand patch index. Returns JSON array."""
        import json
        results = MidiInterface.search_garageband_patches(query=query, limit=limit, rebuild=rebuild)
        return json.dumps(results)

    @Slot(result=str)
    def rebuildGarageBandPatchIndex(self) -> str:
        """Rebuild cached GarageBand patch index and return status text."""
        try:
            index = MidiInterface.load_garageband_patch_index(rebuild=True)
            count = int(index.get("count", 0))
            self.setStatus(f"Rebuilt GarageBand patch index ({count} patches)")
            return f"ok:{count}"
        except Exception as exc:
            self.setStatus(f"GarageBand patch index rebuild failed: {exc}")
            return f"error:{exc}"

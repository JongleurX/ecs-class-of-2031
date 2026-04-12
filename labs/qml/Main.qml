import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    visible: true
    width: 900
    height: 850
    title: "MicroKORG MIDI Lab"

    property int selectedProgramNumber: -1
    property string selectedInstrumentName: "None"

    Component.onCompleted: {
        backend.refreshPorts()
        instrumentModel.refresh()
    }

    ListModel {
        id: instrumentModel
        function refresh() {
            clear()
            var categories = JSON.parse(backend.getInstrumentCategories())
            for (var cat in categories) {
                for (var i = 0; i < categories[cat].length; i++) {
                    var instr = categories[cat][i]
                    append({
                        category: cat,
                        name: instr.name,
                        program: instr.program
                    })
                }
            }
        }
    }

    ListModel {
        id: searchResultsModel
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 12

        Text {
            text: "MicroKORG MIDI Lab"
            font.pixelSize: 28
            font.bold: true
        }

        RowLayout {
            spacing: 10
            Button {
                text: "Refresh ports"
                onClicked: backend.refreshPorts()
            }
            Text {
                text: "Select MIDI ports, choose an instrument, and program melodies."
                wrapMode: Text.Wrap
                Layout.fillWidth: true
            }
        }

        GridLayout {
            columns: 2
            rowSpacing: 8
            columnSpacing: 12
            Layout.fillWidth: true

            Text { text: "MIDI output port:" }
            ComboBox {
                id: outputPortCombo
                model: backend.outputPorts
                Layout.fillWidth: true
            }

            Text { text: "MIDI input port:" }
            ComboBox {
                id: inputPortCombo
                model: backend.inputPorts
                Layout.fillWidth: true
            }

            Text { text: "Tempo (BPM):" }
            Slider {
                id: tempoSlider
                from: 40
                to: 240
                value: 120
                stepSize: 1
                Layout.fillWidth: true
            }
            Text { text: tempoSlider.value.toFixed(0) }

            Text { text: "Channel:" }
            SpinBox {
                id: channelSpin
                from: 1
                to: 16
                value: 1
                Layout.fillWidth: true
            }

            Text { text: "Velocity:" }
            SpinBox {
                id: velocitySpin
                from: 1
                to: 127
                value: 100
                Layout.fillWidth: true
            }
        }

        GroupBox {
            title: "Instrument Selection"
            Layout.fillWidth: true
            ColumnLayout {
                spacing: 10
                anchors.fill: parent
                anchors.margins: 10

                // Search field
                RowLayout {
                    spacing: 10
                    TextField {
                        id: instrumentSearchField
                        placeholderText: "Search instruments by name... (e.g., Piano, Strings, Organ)"
                        Layout.fillWidth: true
                        onTextChanged: {
                            if (text.length > 0) {
                                var results = JSON.parse(backend.searchInstruments(text))
                                searchResultsModel.clear()
                                for (var i = 0; i < results.length; i++) {
                                    searchResultsModel.append(results[i])
                                }
                            } else {
                                searchResultsModel.clear()
                            }
                        }
                    }
                    Text {
                        text: "Program: " + (selectedProgramNumber >= 0 ? selectedProgramNumber : "none")
                        font.bold: true
                        color: "#1976d2"
                    }
                }

                // Selected instrument display
                Rectangle {
                    color: "#e3f2fd"
                    border.color: "#1976d2"
                    border.width: 2
                    radius: 4
                    Layout.fillWidth: true
                    height: 32
                    visible: selectedProgramNumber >= 0
                    Text {
                        anchors.centerIn: parent
                        text: "Selected: " + selectedInstrumentName + " (GM Program " + selectedProgramNumber + ")"
                        font.pixelSize: 14
                    }
                }

                // Quick instrument presets
                Text {
                    text: "Primary instruments:"
                    font.bold: true
                }
                Flow {
                    spacing: 8
                    Layout.fillWidth: true
                    Repeater {
                        model: [
                            {icon: "🎹", label: "Piano", name: "Acoustic Grand Piano", program: 0},
                            {icon: "🎸", label: "Guitar", name: "Clean Electric Guitar", program: 27},
                            {icon: "🎻", label: "Strings", name: "String Ensemble 1", program: 48},
                            {icon: "🥁", label: "Percussion", name: "Synth Drum", program: 118},
                            {icon: "🔊", label: "Synth", name: "Pad 3 (Polysynth)", program: 90},
                            {icon: "🎺", label: "Brass", name: "Trumpet", program: 56}
                        ]
                        Button {
                            text: modelData.icon + " " + modelData.label
                            onClicked: {
                                selectedProgramNumber = modelData.program
                                selectedInstrumentName = modelData.name
                                backend.sendProgramChange(modelData.program, outputPortCombo.currentText, channelSpin.value)
                            }
                        }
                    }
                }

                // Quick category buttons
                Text {
                    text: "Search by category:"
                    font.bold: true
                }
                Flow {
                    spacing: 8
                    Layout.fillWidth: true
                    Repeater {
                        model: ["Piano", "Organ", "Guitar", "Bass", "Strings", "Ensemble", "Brass", "Woodwind", "Synth"]
                        Button {
                            text: modelData
                            onClicked: {
                                instrumentSearchField.text = modelData
                            }
                        }
                    }
                }

                // Search results
                Text {
                    text: "Search results (" + searchResultsModel.count + "):"
                    visible: searchResultsModel.count > 0
                    font.bold: true
                }
                ScrollView {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 120
                    visible: searchResultsModel.count > 0
                    GridView {
                        cellWidth: parent.width
                        cellHeight: 28
                        model: searchResultsModel
                        delegate: Rectangle {
                            width: parent.width
                            height: 28
                            color: mouse.containsMouse ? "#f0f0f0" : "white"
                            border.color: "#e0e0e0"
                            Text {
                                anchors.fill: parent
                                anchors.margins: 4
                                text: model.name + " (" + model.program + ")"
                                verticalAlignment: Text.AlignVCenter
                                elide: Text.ElideRight
                            }
                            MouseArea {
                                id: mouse
                                anchors.fill: parent
                                hoverEnabled: true
                                onClicked: {
                                    selectedProgramNumber = model.program
                                    selectedInstrumentName = model.name
                                    backend.sendProgramChange(model.program, outputPortCombo.currentText, channelSpin.value)
                                }
                            }
                        }
                    }
                }

                Button {
                    text: "Send Program Change"
                    enabled: selectedProgramNumber >= 0
                    Layout.fillWidth: true
                    onClicked: backend.sendProgramChange(selectedProgramNumber, outputPortCombo.currentText, channelSpin.value)
                }
                Button {
                    text: "Apply patch to GarageBand"
                    enabled: selectedProgramNumber >= 0
                    Layout.fillWidth: true
                    onClicked: backend.setGarageBandPatch(selectedInstrumentName)
                }
            }
        }

        GroupBox {
            title: "Melody Programming"
            Layout.fillWidth: true
            ColumnLayout {
                spacing: 10
                TextArea {
                    id: melodyTextArea
                    placeholderText: "Enter notes like: C4 D4 E4 G4\nWith durations: C4:0.5 D4:1\nWith chords: [C4,E4,G4]:1 [D4,F4,A4]:0.5\nRests: R:0.5 or REST:0.25"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 120
                    text: "C4 D4 E4 G4"
                }
                Button {
                    text: "Send Melody"
                    Layout.fillWidth: true
                    onClicked: {
                        if (selectedProgramNumber >= 0) {
                            backend.sendProgramChange(selectedProgramNumber, outputPortCombo.currentText, channelSpin.value)
                        }
                        backend.sendMelody(melodyTextArea.text, outputPortCombo.currentText, tempoSlider.value, channelSpin.value, velocitySpin.value)
                    }
                }
            }
        }

        GroupBox {
            title: "Performance Capture"
            Layout.fillWidth: true
            ColumnLayout {
                spacing: 10
                RowLayout {
                    spacing: 10
                    TextField {
                        id: recordFileField
                        placeholderText: "recording.json"
                        text: "recording.json"
                        Layout.fillWidth: true
                    }
                    Button {
                        text: "Record 8 sec"
                        onClicked: backend.recordPerformance(inputPortCombo.currentText, recordFileField.text, 8)
                    }
                }
                Button {
                    text: "Replay from file"
                    Layout.fillWidth: true
                    onClicked: backend.replayPerformance(outputPortCombo.currentText, recordFileField.text)
                }
            }
        }

        Rectangle {
            color: "#f4f4f4"
            radius: 6
            border.color: "#cccccc"
            Layout.fillWidth: true
            height: 50
            Text {
                anchors.fill: parent
                anchors.margins: 8
                text: backend.statusText
                wrapMode: Text.Wrap
                verticalAlignment: Text.AlignVCenter
            }
        }
    }
}


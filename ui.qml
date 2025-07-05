import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

import QtQuick.Layouts 1.15

ApplicationWindow {

    // Force Material style (optional if set via env var)
    Material.theme: Material.Light
    Material.accent: Material.Blue


    id: mainWindow
    title: qsTr("Pdf Split Tool")  // Window title with translation support
    width: 800
    height: 600
    visible: true
    
    // Optional window properties
    minimumWidth: 400
    minimumHeight: 300
    color: "#f0f0f0"  // Window background color

    ColumnLayout {

        anchors.fill: parent
        spacing: 10
        
        Label {
            text: qsTr(" Pdf Split Tool :")
            font.bold: true
            font.pixelSize: 16
        }

        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            ScrollBar.vertical.policy: ScrollBar.AlwaysOn

            TextArea {
                id: consoleBox

                readOnly: true
                wrapMode: TextArea.Wrap
                text: "Console Output:\n"
                font.family: "monospace"
            }
        
        }


        RowLayout {
            spacing: 10
            Layout.alignment: Qt.AlignHCenter

            Button {
                id: selectBtn
                text: "Select"
                onClicked: backend.select_file()
            }

            SpinBox {
                id: spinBox
                from: 1
                to: 100
                value: 5
                stepSize: 1
                editable: true
                wrap: true
                property string prefix: "Split Size: "
                property string suffix: " MB"


                textFromValue: function(value, locale) {
                    return prefix + Number(value).toLocaleString(locale, 'f', 0) + suffix
                }

                valueFromText: function(text, locale) {
                    let re = /\D*(-?\d*\.?\d*)\D*/
                    return Number.fromLocaleString(locale, re.exec(text)[1])
                }
            }

            Button {
                id: runBtn
                text: "Split"
                onClicked: backend.run(spinBox.value)
            }
        }
    }

    Connections {
        target: backend

        function onMessage(msg) {
            consoleBox.text += msg + "\n"
        }
    }
}

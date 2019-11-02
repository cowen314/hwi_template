import QtQuick 2.0
import QtQuick.Window 2.0
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.13

ApplicationWindow {
    id: rootWindow

    width: 1080
    height: 480
    visible: true

    title: "Qt for Python with QML"

    RowLayout {
        id: mainLayout
        anchors.fill: parent

        Rectangle {
            id: spacer1
            Layout.fillHeight: true
            Layout.fillWidth: true
        }

        ColumnLayout {
            id: textColumnLayout

            Layout.fillHeight: true

            Rectangle {
                id: spacer3
                Layout.fillHeight: true
            }

            Label {
                id: helloWorld

                text: "Hello, world!"
                font.bold: controller.bold
                font.italic: controller.italic
                font.underline: controller.underline
                font.pointSize: controller.size
            }

            Rectangle {
                id: spacer4
                Layout.fillHeight: true
            }

        }

        Rectangle {
            id: spacer2
            Layout.fillHeight: true
            Layout.fillWidth: true
        }

        ColumnLayout {
            id: styleControlLayout

            Slider {
                id: fontSizeSlider
                from: 4
                to: 64
                value: 32

                Binding {
                    target: controller
                    property: "size"
                    value: fontSizeSlider.value
                }
            }

            RowLayout {
                id: fontStyleButtonRow

                Button {
                    text: "Italic"
                    onClicked: controller.toggleItalic()
                }

                Button {
                    text: "Bold"
                    onClicked: controller.toggleBold()
                }

                Button {
                    text: "Underline"
                    onClicked: controller.toggleUnderline()
                }

                Button {
                    text: "None"
                    onClicked: controller.clearStyle()
                }
            }

            ButtonGroup {
                id: colorRadioGroup
            }

            // These could probably be replaced with a repeater pretty easily
            RadioButton {
                id: redRadio
                text: "Red"
                onToggled: {
                    helloWorld.color = controller.getColor(this.text)
                }
                ButtonGroup.group: colorRadioGroup
            }

            RadioButton {
                id: greenRadio
                text: "Green"
                onToggled: {
                    helloWorld.color = controller.getColor(this.text)
                }
                ButtonGroup.group: colorRadioGroup
            }

            RadioButton {
                id: blueRadio
                text: "Blue"
                onToggled: {
                    helloWorld.color = controller.getColor(this.text)
                }
                ButtonGroup.group: colorRadioGroup
            }

            RadioButton {
                id: blackRadio
                text: "Black"
                checked: true
                onToggled: {
                    helloWorld.color = controller.getColor(this.text)
                }
                ButtonGroup.group: colorRadioGroup
            }



        } // styleControlLayout
    } // mainLayout
}

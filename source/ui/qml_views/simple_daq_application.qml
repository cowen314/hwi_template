import QtQuick 2.0
import QtQuick.Window 2.0
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.13

ApplicationWindow {
    id: rootWindow

    width: 1080
    height: 480
    visible: true

    title: "A simple DAQ application"

    RowLayout {
        id: mainLayout
        anchors.fill: parent // what is this?

//        Rectangle {
//            id: spacer1
//            Layout.fillHeight: true
//            Layout.fillWidth: true
//        }

        RowLayout {

            Button {
                text: "Login"
            }

            TextField {
                placeholderText: "Enter username"
            }

        }

//        Rectangle {
//            id: spacer2
//            Layout.fillHeight: true
//            Layout.fillWidth: true
//        }
    }
}

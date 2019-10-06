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
        anchors.fill: parent

        Rectangle {
//            anchors.fill: parent

            Loader {
                id: mainLoader
                anchors.fill: parent
                source: "simple_login_screen.qml"
            }
        }

        Button {
            text: "Log"
            onClicked: controller.log("log from the app window")
        }

        // create connections to signals from other views
        Connections {
            target: mainLoader.item
            onStateChanged: controller.log("state changed")
        }

    }
}

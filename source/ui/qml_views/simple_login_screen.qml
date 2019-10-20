import QtQuick 2.0
import QtQuick.Window 2.0
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.13

// be sure to change Item to ApplicationWindow if running as top level view
Rectangle {
    id: loginItem

    width: 1080
    height: 480
    visible: true

//    title: "A login screen"

//    signal stateChanged()

    RowLayout {
        id: mainLoginLayout
        anchors.fill: parent

        Button {
            text: "Login"
            onClicked: controller.loginRequested(userNameEntry.text)
        }

        Button {
            text: "Log"
            onClicked: {
                console.error("This is a test")
                console.warn("test")
                console.exception("Test")
                console.debug("dtest")
                console.log("log")
                controller.log("log from the login window")
            }
        }

        Button {
            text: "Test signal"
            onClicked: {
                controller.log("test signal button clicked")
                controller.testSlot()
            }
        }

        TextField {
            id: userNameEntry
            placeholderText: "Enter username"
        }

        Label {
            text: controller.statusText
        }
    }
}

import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Dialog  {
    id: deviceEarthDialog
    width: 264
    height: 146
    visible: false
    modal: true
    x: firstOrbitaWindow.width / 2 - width / 2
    y: firstOrbitaWindow.height / 2 - height / 2

    GridLayout {
        anchors.fill: parent
        columns: 2
        rows: 5

        Text {
            id: deviceEarthText
            Layout.preferredWidth: parent.width * 0.5
            Layout.preferredHeight: 23
            text: "Устройство"
            Layout.row: 0
            Layout.column: 0
        }

        ComboBox {
            id: deviceEarthBox
            Layout.preferredWidth: parent.width * 0.5
            Layout.preferredHeight: 23
            Layout.row: 0
            Layout.column: 1
            editable: false
            model: ListModel {
                id: modelDevice
                ListElement { text: "test" }
            }
            onAccepted: {
                if (find(editText) === -1)
                    model.append({text: editText})
            }
        }

        Text {
            Layout.preferredWidth: parent.width * 0.5
            Layout.preferredHeight: 23
            text: "Нач. состояние"
            Layout.row: 1
            Layout.column: 0
        }

        ComboBox {
            id: startStateEarthBox
            Layout.preferredWidth: parent.width * 0.5
            Layout.preferredHeight: 23
            Layout.row: 1
            Layout.column: 1
            editable: false
            model: ListModel {
                id: modelStates
                ListElement { text: "ON" }
                ListElement { text: "OFF" }
            }
            onAccepted: {
                if (find(editText) === -1)
                    model.append({text: editText})
            }
        }

        Button {
            height: 23
            width: parent.width
            Layout.preferredHeight: 23
            Layout.preferredWidth: parent.width * 0.5
            Layout.column: 0
            Layout.row: 4
            text: "ОК"
            onClicked: {
                probe.devices.append({
                                         name: deviceEarthBox.currentValue,
                                         number: `${probe.devices.count === 0 ? 1 : probe.devices.count + 1}`,
                                         type: "none",
                                         startState: startStateEarthBox.currentValue
                                     })
                listViewDevices.currentIndex = probe.devices.count - 1

                deviceEarthDialog.accepted()
                deviceEarthDialog.close()
            }

        }

        Button {
            height: 23
            width: parent.width
            Layout.preferredHeight: 23
            Layout.preferredWidth: parent.width * 0.5
            Layout.column: 1
            Layout.row: 4
            text: "Отмена"
            onClicked: {
                deviceEarthDialog.rejected()
                deviceEarthDialog.close()
            }

        }


    }

}

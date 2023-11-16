import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

import PlanetsDevicesModel 1.0

Dialog  {
    id: deviceDialog
    width: 450
    height: 146
    visible: false
    modal: true
    x: mainWindow.width / 2 - width / 2
    y: mainWindow.height / 2 - height / 2

    ColumnLayout {
        anchors.fill: parent
        width: parent.width
        height: parent.height

        RowLayout {
            width: parent.width
            height: parent.height * 0.2
            Layout.preferredWidth: parent.width
            Layout.preferredHeight: parent.height * 0.2
            Text {
                id: deviceText
                Layout.preferredWidth: parent.width * 0.3
                Layout.preferredHeight: 23
                text: "Устройство"
            }

            ComboBox {
                id: deviceBox
                Layout.preferredWidth: parent.width * 0.7
                Layout.preferredHeight: 23
                editable: false
                model: PlanetsDevicesModel {
                    list: planetDevicesItems
                }
                currentIndex: 0
                onAccepted: {
                    if (find(editText) === -1)
                        model.append({type: editText})
                        currentIndex = find(editText)
                }
            }
        }

        GridLayout {
            width: parent.width
            height: parent.height * 0.8
            Layout.preferredWidth: parent.width
            Layout.preferredHeight: parent.height * 0.8
            columns: 2
            rows: 4

            Text {
                Layout.preferredWidth: parent.width * 0.5
                Layout.preferredHeight: 23
                text: "Нач. состояние"
                Layout.row: 1
                Layout.column: 0
            }

            ComboBox {
                id: startStateBox
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

            Text {
                Layout.preferredWidth: parent.width * 0.5
                Layout.preferredHeight: 23
                text: "Safe Mode"
                Layout.row: 2
                Layout.column: 0
            }

            ComboBox {
                id: safeModeBox
                Layout.preferredWidth: parent.width * 0.5
                Layout.preferredHeight: 23
                Layout.row: 2
                Layout.column: 1
                editable: false
                model: ListModel {
                    id: modelCommands
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
                Layout.row: 3
                text: "ОК"
                onClicked: {
                    var deviceCode = planetDevicesItems.getDeviceCode(deviceBox.currentValue)
                    var deviceEngName = planetDevicesItems.getDeviceEngName(deviceBox.currentValue)

                    devicesItems.appendDevicesItem(
                                probes,
                                listViewProbes.currentIndex,
                                deviceBox.currentValue,
                                deviceCode,
                                deviceEngName,
                                startStateBox.currentValue,
                                safeModeBox.currentIndex === 1 ? false : true)

                    tableViewDevices.currentRow = devicesItems.size()

                    deviceBox.currentIndex = 0
                    startStateBox.currentIndex = 0
                    safeModeBox.currentIndex = 0
                    deviceDialog.accepted()
                    deviceDialog.close()
                }

            }

            Button {
                height: 23
                width: parent.width
                Layout.preferredHeight: 23
                Layout.preferredWidth: parent.width * 0.5
                Layout.column: 1
                Layout.row: 3
                text: "Отмена"
                onClicked: {
                    deviceBox.currentIndex = 0
                    startStateBox.currentIndex = 0
                    safeModeBox.currentIndex = 0
                    deviceDialog.rejected()
                    deviceDialog.close()
                }

            }


        }
    }

}

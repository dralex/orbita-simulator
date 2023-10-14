import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import ComboBoxEarthDevices 1.0

Dialog  {
    id: earthDiagrammDialog
    width: 400
    height: 120
    visible: false
    modal: true
    ErrorMessage {id: errorDialog}

    x: mainWindow.width / 2 - width / 2
    y: mainWindow.height / 2 - height / 2

    ColumnLayout {
        anchors.fill: parent

        RowLayout {
            width: parent.width
            height: parent.height * 0.5
            Layout.preferredWidth: width
            Layout.preferredHeight: height
            ComboBox {
                id: earthDevicesBox
                Layout.preferredWidth: parent.width
                Layout.preferredHeight: 23
                editable: false
                currentIndex: 0
                model: ComboBoxEarthDevices {
                    id: earthModelDevices
                    list: earthProbeSystems
                }
                onAccepted: {
                    if (find(editText) === -1)
                        model.append({name: editText})
                }
            }
        }

        RowLayout {
            width: parent.width
            height: parent.height * 0.5
            Layout.preferredWidth: width
            Layout.preferredHeight: height
            Button {
                height: 23
                width: parent.width
                Layout.preferredHeight: 23
                Layout.preferredWidth: parent.width * 0.5
                text: "Добавить"
                onClicked: {appendEarthSystem
                    diagrammSystemName = earthDevicesBox.currentValue;
                    diagrammFileDialog.open()

                    earthDiagrammDialog.accepted()
                    earthDiagrammDialog.close()
                }
            }


            Button {
                height: 23
                width: parent.width
                Layout.preferredHeight: 23
                Layout.preferredWidth: parent.width * 0.5
                text: "Удалить"
                onClicked: {

                    earthDiagrammDialog.rejected()
                    earthDiagrammDialog.close()
                }
            }
        }
    }
}



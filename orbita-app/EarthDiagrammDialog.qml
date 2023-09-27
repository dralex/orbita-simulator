import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import ComboBoxEarthDevices 1.0

Dialog  {
    id: earthDiagrammDialog
    width: 400
    height: 179
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
                    list: earthProbeDevices
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
                onClicked: {
                    if (devicesBox.currentValue) {
                        if (!timeInput.text) {
                            errorDialog.textOfError = "Укажите время!"
                            errorDialog.open()
                            return
                        }

                        if (whatIsWindow) {
                            stepsLandingItems.appendItem(probes,
                                                         whatIsWindow,
                                                         listViewProbes.currentIndex,
                                                         listViewDevices.currentItem.devicesModelData.deviceNumber,
                                                         timeInput.text,
                                                         devicesBox.currentValue,
                                                         commandsBox.currentValue,
                                                         argumentInput.text);
                            listViewStepsLanding.currentIndex = stepsLandingItems.size() - 1
                        } else {
                            stepsActivityItems.appendItem(probes,
                                                          whatIsWindow,
                                                          listViewProbes.currentIndex,
                                                          listViewDevices.currentItem.devicesModelData.deviceNumber,
                                                          timeInput.text,
                                                          devicesBox.currentValue,
                                                          commandsBox.currentValue,
                                                          argumentInput.text);
                            listViewStepsPlanetActivity.currentIndex = stepsActivityItems.size() - 1
                        }




                        timeInput.text = ""
                        argumentInput.text = ""
                        commandsBox.currentIndex = 0
                        devicesBox.currentIndex = 0
                        earthDiagrammDialog.accepted()
                        earthDiagrammDialog.close()
                    } else {
                        errorDialog.textOfError = "Выберите устройство!"
                        errorDialog.open()
                        return
                    }

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


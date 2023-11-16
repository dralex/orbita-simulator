import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import EarthMissionsModel 1.0
import ImagesModel 1.0

Window  {
    id: earthCalculatorWindow
    width: 1100
    height: 610
    visible: false
    flags: Qt.Window | Qt.WindowFixedSize
    title: qsTr("Гравитационный кальулятор")
    ErrorMessage {id: errorDialog}

    onClosing: {
        simulationController.clearInfo()
        simulationController.clearImages()
        mainWindow.visible = true
        earthCalculatorWindow.visible = false
    }

    ColumnLayout {
        anchors.fill: parent
        width: parent.width
        height: parent.height

        GroupBox {
            id: cParametrs
            title: qsTr("Параметры модели")
            width: parent.width
            height: parent.height * 0.3
            Layout.preferredWidth: width
            Layout.preferredHeight: height

            GridLayout {
                anchors.fill: parent
                columns: 6
                rows: 5
                Text {
                    width: 80
                    height: 23
                    Layout.row: 0
                    Layout.column: 0
                    Layout.alignment: Qt.AlignTop
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    text: "Угловая скорость: "
                }

                TextInput {
                    id: angularVelocityInput
                    width: 80
                    height: 23
                    Layout.alignment: Qt.AlignTop
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    Layout.row: 0
                    Layout.column: 1
                    text: "0"

                    onTextChanged: {
                        if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(angularVelocityInput.text)) {
                            angularVelocityInput.text = angularVelocityInput.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                        }
                    }

                    property string placeholderText: "Введите число..."

                    Text {
                        text: angularVelocityInput.placeholderText
                        color: "#aaa"
                        visible: !angularVelocityInput.text
                    }
                }

                Text {
                    width: 80
                    height: 23
                    Layout.row: 0
                    Layout.column: 2
                    Layout.alignment: Qt.AlignTop
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    text: "Длительность: "
                }

                TextInput {
                    id: durationInput
                    width: 80
                    height: 23
                    Layout.alignment: Qt.AlignTop
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    Layout.row: 0
                    Layout.column: 3
                    text: "0"

                    onTextChanged: {
                        if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(durationInput.text)) {
                            durationInput.text = durationInput.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                        }
                    }

                    property string placeholderText: "Введите число..."

                    Text {
                        text: durationInput.placeholderText
                        color: "#aaa"
                        visible: !durationInput.text
                    }
                }

                Text {
                    width: 80
                    height: 23
                    Layout.row: 0
                    Layout.column: 4
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    text: "Масса: "
                }

                TextInput {
                    id: massInput
                    width: 80
                    height: 23
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    Layout.row: 0
                    Layout.column: 5
                    text: "0"

                    onTextChanged: {
                        if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(massInput.text)) {
                            massInput.text = massInput.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                        }
                    }

                    property string placeholderText: "Введите число..."

                    Text {
                        text: massInput.placeholderText
                        color: "#aaa"
                        visible: !massInput.text
                    }
                }

                Text {
                    width: 90
                    height: 23
                    Layout.row: 1
                    Layout.column: 0
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    text: "Ориентацион. угол: "
                }

                TextInput {
                    id: orientAngleInput
                    width: 80
                    height: 23
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    Layout.row: 1
                    Layout.column: 1
                    text: "0"

                    onTextChanged: {
                        if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(orientAngleInput.text)) {
                            orientAngleInput.text = orientAngleInput.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                        }
                    }

                    property string placeholderText: "Введите число..."

                    Text {
                        text: orientAngleInput.placeholderText
                        color: "#aaa"
                        visible: !orientAngleInput.text
                    }
                }

                Text {
                    width: 80
                    height: 23
                    Layout.row: 1
                    Layout.column: 2
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    text: "Момент: "
                    wrapMode: Text.WordWrap
                }

                TextInput {
                    id: momentInput
                    width: 80
                    height: 23
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    Layout.row: 1
                    Layout.column: 3
                    text: "0"

                    onTextChanged: {
                        if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(momentInput.text)) {
                            momentInput.text = momentInput.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                        }
                    }

                    property string placeholderText: "Введите число..."

                    Text {
                        text: momentInput.placeholderText
                        color: "#aaa"
                        visible: !momentInput.text
                    }
                }

                Text {
                    width: 80
                    height: 23
                    Layout.row: 1
                    Layout.column: 4
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    text: "Шаг (сек): "
                }

                TextInput {
                    id: tickInput
                    width: 80
                    height: 23
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    Layout.row: 1
                    Layout.column: 5
                    text: "10"

                    onTextChanged: {
                        if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(tickInput.text)) {
                            tickInput.text = tickInput.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                        }
                    }

                    property string placeholderText: "Введите число..."

                    Text {
                        text: tickInput.placeholderText
                        color: "#aaa"
                        visible: !tickInput.text
                    }
                }

                Text {
                    width: 80
                    height: 23
                    Layout.row: 2
                    Layout.column: 0
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    text: "Cкорость X (м/с): "
                }

                TextInput {
                    id: xVTextInput
                    width: 80
                    height: 23
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    Layout.row: 2
                    Layout.column: 1
                    text: "0"

                    onTextChanged: {
                        if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(xVTextInput.text)) {
                            xVTextInput.text = xVTextInput.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                        }
                    }

                    property string placeholderText: "Введите число..."

                    Text {
                        text: xVTextInput.placeholderText
                        color: "#aaa"
                        visible: !yVTextInput.text
                    }
                }

                Text {
                    width: 80
                    height: 23
                    Layout.row: 2
                    Layout.column: 2
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    text: "Cкорость Y (м/с): "
                }

                TextInput {
                    id: yVTextInput
                    width: 80
                    height: 23
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    Layout.row: 2
                    Layout.column: 3
                    text: "0"

                    onTextChanged: {
                        if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(yVTextInput.text)) {
                            yVTextInput.text = yVTextInput.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                        }
                    }

                    property string placeholderText: "Введите число..."

                    Text {
                        text: yVTextInput.placeholderText
                        color: "#aaa"
                        visible: !yVTextInput.text
                    }
                }

                Text {
                    width: 80
                    height: 23
                    Layout.row: 2
                    Layout.column: 4
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    text: "X : "
                }

                TextInput {
                    id: xTextInput
                    width: 80
                    height: 23
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    Layout.row: 2
                    Layout.column: 5
                    text: "0"

                    onTextChanged: {
                        if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(xTextInput.text)) {
                            xTextInput.text = xTextInput.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                        }
                    }

                    property string placeholderText: "Введите число..."

                    Text {
                        text: xTextInput.placeholderText
                        color: "#aaa"
                        visible: !xTextInput.text
                    }
                }

                Text {
                    width: 80
                    height: 23
                    Layout.row: 3
                    Layout.column: 0
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    text: "Высота Y: "
                }

                TextInput {
                    id: yTextInput
                    width: 80
                    height: 23
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    Layout.row: 3
                    Layout.column: 1
                    text: "0"

                    onTextChanged: {
                        if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(yTextInput.text)) {
                            yTextInput.text = yTextInput.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                        }
                    }

                    property string placeholderText: "Введите число..."

                    Text {
                        text: yTextInput.placeholderText
                        color: "#aaa"
                        visible: !yTextInput.text
                    }
                }

                Text {
                    width: 110
                    height: 23
                    Layout.row: 3
                    Layout.column: 2
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    text: "Длительность импульса: "
                }

                TextInput {
                    id: impulseDurationInput
                    width: 80
                    height: 23
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    Layout.row: 3
                    Layout.column: 3
                    text: "0"

                    onTextChanged: {
                        if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(impulseDurationInput.text)) {
                            impulseDurationInput.text = impulseDurationInput.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                        }
                    }

                    property string placeholderText: "Введите число..."

                    Text {
                        text: impulseDurationInput.placeholderText
                        color: "#aaa"
                        visible: !impulseDurationInput.text
                    }
                }

                Text {
                    width: 80
                    height: 23
                    Layout.row: 3
                    Layout.column: 4
                    Layout.alignment: Qt.AlignBottom
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    text: "Скорость импульса: "
                }

                TextInput {
                    id: impulseSpeedInput
                    width: 80
                    height: 23
                    Layout.alignment: Qt.AlignBottom
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    Layout.row: 3
                    Layout.column: 5
                    text: "0"

                    onTextChanged: {
                        if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(impulseSpeedInput.text)) {
                            impulseSpeedInput.text = impulseSpeedInput.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                        }
                    }

                    property string placeholderText: "Введите число..."

                    Text {
                        text: impulseSpeedInput.placeholderText
                        color: "#aaa"
                        visible: !impulseSpeedInput.text
                    }
                }

                Text {
                    width: 80
                    height: 23
                    Layout.row: 4
                    Layout.column: 0
                    Layout.alignment: Qt.AlignBottom
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    text: "Время импульса: "
                }

                TextInput {
                    id: impulseTimeInput
                    width: 80
                    height: 23
                    Layout.alignment: Qt.AlignBottom
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    Layout.row: 4
                    Layout.column: 1
                    text: "0"

                    onTextChanged: {
                        if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(impulseTimeInput.text)) {
                            impulseTimeInput.text = impulseTimeInput.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                        }
                    }

                    property string placeholderText: "Введите число..."

                    Text {
                        text: impulseTimeInput.placeholderText
                        color: "#aaa"
                        visible: !impulseTimeInput.text
                    }
                }


                Text {
                    width: 80
                    height: 23
                    Layout.row: 4
                    Layout.column: 2
                    Layout.alignment: Qt.AlignBottom
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    text: "Импульсная тяга: "
                }

                TextInput {
                    id: impulseTractionInput
                    width: 80
                    height: 23
                    Layout.alignment: Qt.AlignBottom
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    Layout.row: 4
                    Layout.column: 3
                    text: "0"

                    onTextChanged: {
                        if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(impulseTractionInput.text)) {
                            impulseTractionInput.text = impulseTractionInput.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                        }
                    }

                    property string placeholderText: "Введите число..."

                    Text {
                        text: impulseTractionInput.placeholderText
                        color: "#aaa"
                        visible: !impulseTractionInput.text
                    }
                }

            }

        }

        RowLayout {
           height: parent.height * 0.6 - buttonsLayout.height
           width: parent.width
           Layout.preferredHeight: height
           Layout.preferredWidth: width

           GroupBox {
               title: qsTr("Журнал полёта")
               width: parent.width
               height: parent.height
               Layout.preferredHeight: parent.height
               Layout.preferredWidth: parent.width * 0.5

               ScrollView {
                   width: parent.width
                   height: parent.height
                   Layout.preferredWidth: width
                   Layout.preferredHeight: height

                   TextArea {
                       id: missionInfo
                       anchors.fill: parent
                       readOnly: true
                       text: simulationController.telemetryLogContents
                   }
               }
           }

           GroupBox {
               title: qsTr("Графики")
               Layout.preferredHeight: parent.height
               Layout.preferredWidth: parent.width * 0.5
               ListView {
                   id: imageListView
                   width: parent.width
                   height: parent.height
                   clip: true

                   model: ImagesModel {
                        list: simulationController
                   }

                   ScrollBar.vertical: ScrollBar {
                       id: probesScrollBar
                       anchors {
                           right: parent.right
                           top: parent.top
                           bottom: parent.bottom
                           margins: 0
                       }
                   }

                   delegate: Item {
                       width: imageListView.width
                       height: imageListView.height

                       Image {
                           width: parent.width
                           height: parent.height
                           fillMode: Image.PreserveAspectFit

                           source: model.imageSource
                       }
                   }
               }


           }
        }


        RowLayout {
            id: buttonsLayout
            width: parent.width
            height: 23
            Layout.preferredHeight: height
            Layout.preferredWidth: width

            Button {
                width: parent.width * 0.2
                height: 23
                Layout.preferredHeight: height
                Layout.preferredWidth: width
                Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter
                text: "Cтарт!"
                onClicked: {
                    if (
                        angularVelocityInput.text &&
                        durationInput.text &&
                        massInput.text &&
                        orientAngleInput.text &&
                        momentInput.text &&
                        tickInput.text &&
                        xVTextInput.text &&
                        yVTextInput.text &&
                        impulseDurationInput.text &&
                        impulseSpeedInput.text &&
                        impulseTimeInput.text &&
                        impulseTractionInput.text &&
                        xTextInput.text &&
                        yTextInput.text
                            ) {
                    simulationController.addEarthCalculatorData(angularVelocityInput.text,
                                                                durationInput.text,
                                                                impulseDurationInput.text,
                                                                impulseSpeedInput.text,
                                                                impulseTimeInput.text,
                                                                impulseTractionInput.text,
                                                                massInput.text ,
                                                                momentInput.text,
                                                                orientAngleInput.text,
                                                                tickInput.text,
                                                                xVTextInput.text,
                                                                yVTextInput.text,
                                                                xTextInput.text,
                                                                yTextInput.text
                                                                 )

                    simulationController.startCalculatorSimulation(settingsManager, typeMission)
                    } else {
                        errorDialog.textOfError = "Вы заполнили не все данные!"
                        errorDialog.open()
                    }
                }
            }

            Button {
                width: parent.width * 0.2
                height: 23
                Layout.preferredHeight: height
                Layout.preferredWidth: width
                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                text: "Закрыть"
                onClicked: {
                    simulationController.clearInfo()
                    simulationController.clearImages()
                    mainWindow.visibility = 1
                    earthCalculatorWindow.visibility = 0
                }
            }
        }
    }

}

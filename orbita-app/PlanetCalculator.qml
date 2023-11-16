import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

import PlanetsModel 1.0
import ImagesModel 1.0

Window  {
    id: planetCalculatorWindow
    width: 819
    height: 610
    visible: false
    flags: Qt.Window | Qt.WindowFixedSize
    title: qsTr("Гравитационный кальулятор")
    ErrorMessage {id: errorDialog}

    onClosing: {
        simulationController.clearInfo()
        simulationController.clearImages()
        mainWindow.visible = true
        planetCalculatorWindow.visible = false
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
                rows: 3
                Text {
                    width: 80
                    height: 23
                    Layout.row: 0
                    Layout.column: 0
                    Layout.alignment: Qt.AlignTop
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    text: "Планета: "
                }

                ComboBox {
                    id: planetsBox
                    width: 110
                    height: 23
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    Layout.alignment: Qt.AlignTop
                    Layout.row: 0
                    Layout.column: 1
                    editable: false
                    model: PlanetsModel {
                        id: modelMissions
                        list: planetsItems
                    }
                    currentIndex: 0
                    onAccepted: {
                        if (find(editText) === -1)
                            model.append({text: editText})
                    }
                }

                Text {
                    width: 80
                    height: 23
                    Layout.row: 1
                    Layout.column: 0
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    text: "Площадь (м^2): "
                }

                TextInput {
                    id: squareTextInput
                    width: 80
                    height: 23
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    Layout.row: 1
                    Layout.column: 1
                    text: "0"

                    onTextChanged: {
                        if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(squareTextInput.text)) {
                            squareTextInput.text = squareTextInput.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                        }
                    }

                    property string placeholderText: "Введите число..."

                    Text {
                        text: squareTextInput.placeholderText
                        color: "#aaa"
                        visible: !squareTextInput.text
                    }
                }

                Text {
                    width: 80
                    height: 23
                    Layout.row: 2
                    Layout.column: 0
                    Layout.alignment: Qt.AlignBottom
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    text: "Масса кг: "
                }

                TextInput {
                    id: massTextInput
                    width: 80
                    height: 23
                    Layout.alignment: Qt.AlignBottom
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    Layout.row: 2
                    Layout.column: 1
                    text: "0"

                    onTextChanged: {
                        if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(massTextInput.text)) {
                            massTextInput.text = massTextInput.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                        }
                    }

                    property string placeholderText: "Введите число..."

                    Text {
                        text: massTextInput.placeholderText
                        color: "#aaa"
                        visible: !massTextInput.text
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
                    text: "Y высота (м): "
                }

                TextInput {
                    id: hTextInput
                    width: 80
                    height: 23
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    Layout.row: 1
                    Layout.column: 3
                    text: "0"

                    onTextChanged: {
                        if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(hTextInput.text)) {
                            hTextInput.text = hTextInput.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                        }
                    }

                    property string placeholderText: "Введите число..."

                    Text {
                        text: hTextInput.placeholderText
                        color: "#aaa"
                        visible: !hTextInput.text
                    }
                }

                Text {
                    width: 80
                    height: 23
                    Layout.row: 2
                    Layout.column: 2
                    Layout.alignment: Qt.AlignBottom
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    text: "X (м): "
                }

                TextInput {
                    id: xTextInput
                    width: 80
                    height: 23
                    Layout.alignment: Qt.AlignBottom
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    Layout.row: 2
                    Layout.column: 3
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
                    Layout.row: 0
                    Layout.column: 4
                    Layout.alignment: Qt.AlignTop
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    text: "Шаг (сек): "
                }

                ComboBox {
                    id: tickComboBox
                    width: 80
                    height: 23
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    Layout.alignment: Qt.AlignTop
                    Layout.row: 0
                    Layout.column: 5
                    editable: false
                    model: ListModel {
                        id: modelTicks
                        ListElement {text: "10"}
                        ListElement {text: "20"}
                        ListElement {text: "30"}
                        ListElement {text: "40"}
                        ListElement {text: "50"}
                        ListElement {text: "60"}
                        ListElement {text: "70"}
                        ListElement {text: "80"}
                        ListElement {text: "90"}
                        ListElement {text: "100"}
                    }
                    currentIndex: 0
                    onAccepted: {
                        if (find(editText) === -1)
                            model.append({text: editText})
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
                    text: "Аэродинам. коэфф.: "
                    wrapMode: Text.WordWrap
                }

                TextInput {
                    id: coeffTextInput
                    width: 80
                    height: 23
                    Layout.alignment: Qt.AlignTop
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    Layout.row: 0
                    Layout.column: 3
                    text: "0.47"

                    onTextChanged: {
                        if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(coeffTextInput.text)) {
                            coeffTextInput.text = coeffTextInput.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                        }
                    }

                    property string placeholderText: "Введите число..."

                    Text {
                        text: coeffTextInput.placeholderText
                        color: "#aaa"
                        visible: !coeffTextInput.text
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
                    text: "Cкорость Y (м/с): "
                }

                TextInput {
                    id: yVTextInput
                    width: 80
                    height: 23
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    Layout.row: 1
                    Layout.column: 5
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
                    Layout.alignment: Qt.AlignBottom
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    text: "Cкорость X (м/с): "
                }

                TextInput {
                    id: xVTextInput
                    width: 80
                    height: 23
                    Layout.alignment: Qt.AlignBottom
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    Layout.row: 2
                    Layout.column: 5
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
                    if (squareTextInput.text &&
                            massTextInput.text &&
                            hTextInput.text &&
                            xTextInput.text &&
                            xVTextInput.text &&
                            yVTextInput.text &&
                            coeffTextInput.text) {
                    simulationController.addPlanetCalculatorData(planetsBox.currentValue,
                                                                 tickComboBox.currentValue,
                                                                 squareTextInput.text,
                                                                 massTextInput.text,
                                                                 hTextInput.text,
                                                                 xTextInput.text,
                                                                 xVTextInput.text,
                                                                 yVTextInput.text,
                                                                 coeffTextInput.text
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
                    planetCalculatorWindow.visibility = 0
                }
            }
        }
    }

}

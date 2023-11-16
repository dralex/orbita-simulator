import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

import PlanetsModel 1.0

Window  {
    id: planetCalculatorWindow
    width: 819
    height: 610
    visible: false
    flags: Qt.Window | Qt.WindowFixedSize
    title: qsTr("Гравитационный кальулятор")

    onClosing: {
        mainWindow.visible = true
        planetCalculatorWindow.visible = false
    }

    ColumnLayout {
        anchors.fill: parent

        GroupBox {
            id: cParametrs
            title: qsTr("Параметры модели")
            width: parent.width
            height: parent.height * 0.3
            Layout.preferredHeight: width
            Layout.preferredWidth: height

            GridLayout {
                width: parent.width
                height: parent.height
                columns: 6
                rows: 3
                Text {
                    Layout.row: 0
                    Layout.column: 0
                    Layout.alignment: Qt.AlignTop
                    Layout.preferredWidth: parent.width * 0.1
                    Layout.preferredHeight: 23
                    text: "Планета: "
                }

                ComboBox {
                    id: deviceBox
                    Layout.preferredWidth: parent.width * 0.2
                    Layout.preferredHeight: 23
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
                    Layout.row: 1
                    Layout.column: 0
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: parent.width * 0.1
                    Layout.preferredHeight: 23
                    text: "Площадь (м^2): "
                }

                TextInput {
                    id: squareTextInput
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: parent.width * 0.1
                    Layout.preferredHeight: 23
                    Layout.row: 1
                    Layout.column: 1

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
                    Layout.row: 2
                    Layout.column: 0
                    Layout.alignment: Qt.AlignBottom
                    Layout.preferredWidth: parent.width * 0.1
                    Layout.preferredHeight: 23
                    text: "Масса кг: "
                }

                TextInput {
                    id: massTextInput
                    Layout.alignment: Qt.AlignBottom
                    Layout.preferredWidth: parent.width * 0.1
                    Layout.preferredHeight: 23
                    Layout.row: 2
                    Layout.column: 1

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
                    Layout.row: 1
                    Layout.column: 2
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: parent.width * 0.1
                    Layout.preferredHeight: 23
                    text: "Y высота (м): "
                }

                TextInput {
                    id: hTextInput
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: parent.width * 0.1
                    Layout.preferredHeight: 23
                    Layout.row: 1
                    Layout.column: 3

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
                    Layout.row: 2
                    Layout.column: 2
                    Layout.alignment: Qt.AlignBottom
                    Layout.preferredWidth: parent.width * 0.1
                    Layout.preferredHeight: 23
                    text: "X (м): "
                }

                TextInput {
                    id: xTextInput
                    Layout.alignment: Qt.AlignBottom
                    Layout.preferredWidth: parent.width * 0.1
                    Layout.preferredHeight: 23
                    Layout.row: 2
                    Layout.column: 3

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
                    Layout.row: 0
                    Layout.column: 4
                    Layout.alignment: Qt.AlignTop
                    Layout.preferredWidth: parent.width * 0.1
                    Layout.preferredHeight: 23
                    text: "Шаг (сек): "
                }

                ComboBox {
                    id: tickComboBox
                    Layout.preferredWidth: parent.width * 0.1
                    Layout.preferredHeight: 23
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
                    Layout.row: 1
                    Layout.column: 4
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: parent.width * 0.1
                    Layout.preferredHeight: 23
                    text: "Cкорость Y (м/с): "
                }

                TextInput {
                    id: xVTextInput
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: parent.width * 0.1
                    Layout.preferredHeight: 23
                    Layout.row: 1
                    Layout.column: 5

                    onTextChanged: {
                        if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(xVTextInput.text)) {
                            xVTextInput.text = xVTextInput.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                        }
                    }

                    property string placeholderText: "Введите число..."

                    Text {
                        text: xVTextInput.placeholderText
                        color: "#aaa"
                        visible: !xVTextInput.text
                    }
                }

                Text {
                    Layout.row: 2
                    Layout.column: 4
                    Layout.alignment: Qt.AlignBottom
                    Layout.preferredWidth: parent.width * 0.1
                    Layout.preferredHeight: 23
                    text: "Cкорость X (м/с): "
                }

                TextInput {
                    id: yVTextInput
                    Layout.alignment: Qt.AlignBottom
                    Layout.preferredWidth: parent.width * 0.1
                    Layout.preferredHeight: 23
                    Layout.row: 2
                    Layout.column: 5

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

            }

        }

        GroupBox {
            id: journalOfFlyGB
            width: parent.width
            height: parent.height * 0.6
            Layout.preferredHeight: height
            Layout.preferredWidth: width
            title: qsTr("Журнал полёта")
            ScrollView {
                Layout.preferredWidth: parent.width
                Layout.preferredHeight: parent.height

                TextArea {
                    id: missionInfo
                    anchors.fill: parent
                    readOnly: true
                }
            }
        }

        RowLayout {
            width: parent.width
            height: parent.height * 0.1
            Layout.preferredHeight: height
            Layout.preferredWidth: width

            Button {
                width: parent.width * 0.2
                height: 23
                Layout.preferredHeight: height
                Layout.preferredWidth: width
                Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter
                text: "Cтарт!"
            }

            Button {
                width: parent.width * 0.2
                height: 23
                Layout.preferredHeight: height
                Layout.preferredWidth: width
                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                text: "Закрыть"
                onClicked: {
                    mainWindow.visibility = 1
                    planetCalculatorWindow.visibility = 0
                }
            }
        }
    }

}

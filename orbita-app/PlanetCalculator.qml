import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

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
        width: parent.width
        height: parent.height
        Layout.preferredHeight: width
        Layout.preferredWidth: height

        GroupBox {
            id: cParametrs
            title: qsTr("Параметры модели")
            width: parent.width
            height: parent.height * 0.3
            Layout.preferredHeight: width
            Layout.preferredWidth: height

            GridLayout {
                anchors.fill: parent
                columns: 6
                rows: 3
                Text {
                    width: parent.width * 0.1
                    height: 23
                    Layout.row: 0
                    Layout.column: 0
                    Layout.alignment: Qt.AlignTop
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    text: "Планета: "
                }

                ComboBox {
                    id: deviceBox
                    width: parent.width * 0.2
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
                    width: parent.width * 0.1
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
                    width: parent.width * 0.1
                    height: 23
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
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
                    width: parent.width * 0.1
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
                    width: parent.width * 0.1
                    height: 23
                    Layout.alignment: Qt.AlignBottom
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
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
                    width: parent.width * 0.1
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
                    width: parent.width * 0.1
                    height: 23
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
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
                    width: parent.width * 0.1
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
                    width: parent.width * 0.1
                    height: 23
                    Layout.alignment: Qt.AlignBottom
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
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
                    width: parent.width * 0.1
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
                    width: parent.width * 0.1
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
                    width: parent.width * 0.1
                    height: 23
                    Layout.row: 1
                    Layout.column: 4
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    text: "Cкорость Y (м/с): "
                }

                TextInput {
                    id: xVTextInput
                    width: parent.width * 0.1
                    height: 23
                    Layout.alignment: Qt.AlignVCenter
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
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
                    width: parent.width * 0.1
                    height: 23
                    Layout.row: 2
                    Layout.column: 4
                    Layout.alignment: Qt.AlignBottom
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
                    text: "Cкорость X (м/с): "
                }

                TextInput {
                    id: yVTextInput
                    width: parent.width * 0.1
                    height: 23
                    Layout.alignment: Qt.AlignBottom
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height
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
                width: parent.width
                height: parent.height
                Layout.preferredWidth: width
                Layout.preferredHeight: width

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

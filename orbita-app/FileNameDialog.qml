import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12


Dialog  {
    id: fileNameDialog
    width: 287
    height: 179
    visible: false
    modal: true
    title: qsTr("Введите название файла")

    x: mainWindow.width / 2 - width / 2
    y: mainWindow.height / 2 - height / 2

    GridLayout {
        anchors.fill: parent
        columns: 2
        rows: 2

        Text {
            id: fileName
            Layout.preferredWidth: parent.width * 0.3
            Layout.preferredHeight: 23
            text: "Название файла:"
            Layout.row: 0
            Layout.column: 0
        }

        TextInput {
            id: fileNameInput
            Layout.row: 0
            Layout.column: 1
            Layout.preferredWidth: parent.width * 0.6
            Layout.preferredHeight: 23

            property string placeholderText: "Введите название"

            Text {
                text: fileNameInput.placeholderText
                color: "#aaa"
                visible: !fileNameInput.text
            }
        }

        Button {
            height: 23
            width: parent.width
            Layout.preferredHeight: 23
            Layout.preferredWidth: parent.width * 0.5
            Layout.column: 0
            Layout.row: 1
            text: "ОК"
            onClicked: {
                fileNameFromDialog =  fileNameInput.text
                pathToSaveDialog.open()
                fileNameInput.text = ""

                fileNameDialog.accepted()
                fileNameDialog.close()
            }

        }

        Button {
            height: 23
            width: parent.width
            Layout.preferredHeight: 23
            Layout.preferredWidth: parent.width * 0.5
            Layout.column: 1
            Layout.row: 1
            text: "Отмена"
            onClicked: {
                fileNameInput.text = ""
                fileNameFromDialog = ""
                fileNameDialog.rejected()
                fileNameDialog.close()
            }

        }
    }
}


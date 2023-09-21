import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15


Dialog  {
    id: settingsDialog
    width: 450
    height: 146
    visible: false
    modal: true
    x: mainWindow.width / 2 - width / 2
    y: mainWindow.height / 2 - height / 2
    GridLayout {
        anchors.fill: parent
        width: parent.width
        height: parent.height * 0.8
        Layout.preferredWidth: parent.width
        Layout.preferredHeight: parent.height * 0.8
        rowSpacing: 20
        columns: 2
        rows: 3

        Text {
            Layout.preferredWidth: parent.width * 0.5
            Layout.preferredHeight: 23
            text: "Симулятор: " + folderSimulation
            Layout.row: 1
            Layout.column: 0
            wrapMode: Text.WordWrap
        }

        Button {
            id: addSimulationPathButton
            Layout.preferredWidth: parent.width * 0.5
            Layout.preferredHeight: 23
            Layout.row: 1
            Layout.column: 1
            text: "Добавить путь симулятора"
            onClicked: {
                simulationPathDialog.open()
            }
        }

        Text {
            Layout.preferredWidth: parent.width * 0.5
            Layout.preferredHeight: 23
            text: "Аппараты: " + folderProbesPath
            Layout.row: 2
            Layout.column: 0
            wrapMode: Text.WordWrap
        }

        Button {
            id: addProbePathButton
            Layout.preferredWidth: parent.width * 0.5
            Layout.preferredHeight: 23
            Layout.row: 2
            Layout.column: 1
            text: "Добавить путь к аппаратам"
            onClicked: {
                checkAction = false
                pathToSaveDialog.open()
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
                settingsDialog.accepted()
                settingsDialog.close()
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
                folderSimulation = "None"
                settingsManager.setSimulationPath(folderSimulation);
                settingsManager.setDevicesPath(folderSimulation + "/devices-ru.xml");
                settingsManager.setPlanetsPath(folderSimulation + "/planets.xml");
                settingsDialog.rejected()
                settingsDialog.close()
            }

        }


    }
}



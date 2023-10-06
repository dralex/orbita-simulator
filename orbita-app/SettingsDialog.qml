import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15


Dialog  {
    id: settingsDialog
    width: 450
    height: 200
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
        rows: 4

        Text {
            Layout.preferredWidth: parent.width * 0.5
            Layout.preferredHeight: 23
            text: "Симулятор: " + settingsFolderSimulation
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
            text: "Аппараты: " + settingsFolderProbesPath
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

        Text {
            Layout.preferredWidth: parent.width * 0.5
            Layout.preferredHeight: 23
            text: "Калькулятор: " + settingsFolderCalculatorPath
            Layout.row: 3
            Layout.column: 0
            wrapMode: Text.WordWrap
        }

        Button {
            height: 23
            width: parent.width
            Layout.preferredHeight: 23
            Layout.preferredWidth: parent.width * 0.5
            Layout.column: 1
            Layout.row: 3
            text: "Добавить путь к калькулятору"
            onClicked: {
                calculatorFileDialog.open()
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
                if (typeMission) {
                    folderSimulation = settingsManager.getSimulationPath()
                    folderCalculatorPath = settingsManager.getPlanetsCalculatorPath()
                    settingsManager.setSimulationPath(folderSimulation);
                    settingsManager.setDevicesPath(folderSimulation + "/devices-ru.xml")
                    settingsManager.setPlanetsPath(folderSimulation + "/planets.xml")
                    settingsManager.setPlanetsCalculatorPath(folderCalculatorPath)
                    settingsManager.saveSettingsToFile("planets_settings.txt", typeMission)
                    planetsItems.loadPlanets(settingsManager.getPlanetsPath())
                    planetDevicesItems.loadDevices(settingsManager.getDevicesPath())
                } else {
                    earthFolderSimulation = settingsManager.getEarthSimulationPath()
                    earthFolderCalculatorPath = settingsManager.getEarthCalculatorPath()
                    settingsManager.setEarthSimulationPath(earthFolderSimulation);
                    settingsManager.setEarthSystemsPath(earthFolderSimulation + "/devices-ru.xml")
                    settingsManager.setMissionsPath(earthFolderSimulation + "/missions-ru.xml")
                    settingsManager.setEarthCalculatorPath(earthFolderCalculatorPath)
                    settingsManager.saveSettingsToFile("earth_settings.txt", typeMission)
                }

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
            Layout.row: 4
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



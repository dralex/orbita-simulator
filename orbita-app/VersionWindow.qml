import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

Dialog  {
    id: versionWindow
    width: 400
    height: 200
    visible: false
    modal: true
    x: mainWindow.width / 2 - width / 2
    y: mainWindow.height / 2 - height / 2
    title: qsTr("Выберите версию Орбиты")

    ColumnLayout {
        anchors.fill: parent
        RowLayout {
            height: parent.height * 0.2
            width: parent.width
            Layout.preferredWidth: width
            Layout.preferredHeight: height
            ComboBox {
                id: versionSelect
                width: parent.width
                height: parent.height
                Layout.preferredWidth: width
                Layout.preferredHeight: height
                editable: false
                model: ListModel {
                    id: modelVersions
                    ListElement { text: "Орбита 1.0" }
                    ListElement { text: "Орбита 2.0" }
                }
                onAccepted: {
                    if (find(editText) === -1)
                        model.append({text: editText})
                }
            }
        }

        RowLayout {
            height: 23
            width: parent.width
            Layout.preferredHeight: 23
            Layout.preferredWidth: parent.width
            Button {
                Layout.preferredHeight: 23
                Layout.preferredWidth: parent.width * 0.5
                text: "ОК"
                onClicked: {
                    modelSolutions.clear()
                    if (versionSelect.currentIndex === 0 ) {
                        if (!probes.size())
                            itemsEnabled = false
                        else
                            itemsEnabled = true
                        probeNameText.text = ""
                        modelSolutions.append({text: "Таблица"})
                        typeMission = true
                        settingsManager.loadSettingsFromFile("planets_settings.txt", typeMission);
                        pathToSave = settingsManager.getPlanetsProbesPath()
                        pathToLoad = settingsManager.getPlanetsProbesPath()

                        pathToLoadDialog.folder = pathToLoad !== "None" ? "file://" + pathToLoad : Qt.resolvedUrl("~")
                        pathToSaveDialog.folder = pathToSave !== "None" ? "file://" + pathToSave : Qt.resolvedUrl("~")

                        settingsFolderSimulation = settingsManager.getSimulationPath()
                        settingsFolderProbesPath = pathToSave
                        settingsFolderCalculatorPath = settingsManager.getPlanetsCalculatorPath()

                        if (!planetsItems.size())
                            planetsItems.loadPlanets(settingsManager.getPlanetsPath());
                        if (!planetDevicesItems.size())
                            planetDevicesItems.loadDevices(settingsManager.getDevicesPath());

                        versionWindow.visible = false
                        earthElementsVisible = false
                        planetsElementsVisible = true
                        showDiagrammButton = false
                        gBEPythonCode.visible = false

                    } else {
                        if (!earthProbes.size())
                            itemsEnabled = false
                        else
                            itemsEnabled = true

                        probeNameText.text = ""
                        typeMission = false
                        modelSolutions.append({text: "Диаграмма"})
                        settingsManager.loadSettingsFromFile("earth_settings.txt", typeMission)

                        earthPathToLoad = settingsManager.getEarthProbesPath();
                        earthPathToSave = settingsManager.getEarthProbesPath();
                        if (!earthMissions.size())
                            earthMissions.loadMissions(settingsManager.getMissionsPath());
                        if (!systems.size())
                            systems.loadSystems((settingsManager.getEarthSystemsPath()));

                        settingsFolderSimulation = settingsManager.getEarthSimulationPath()
                        settingsFolderProbesPath = earthPathToLoad
                        settingsFolderCalculatorPath = settingsManager.getEarthCalculatorPath()

                        earthPathToLoad = settingsManager.getEarthProbesPath()
                        earthPathToSave = settingsManager.getEarthProbesPath()

                        pathToLoadDialog.folder = earthPathToLoad !== "None" ? "file://" + earthPathToLoad : Qt.resolvedUrl("~")
                        pathToSaveDialog.folder = earthPathToSave !== "None" ? "file://" + earthPathToSave : Qt.resolvedUrl("~")

                        showPlanetsElems = false
                        showPlanetsDevices = false
                        showPythonArea = false

                        versionWindow.visible = false
                        planetsElementsVisible = false
                        earthElementsVisible = true


                    }
                    modelSolutions.append({text: "Python"})
                    newProbeButton.enabled = true
                    loadProbeButton.enabled = true
                    settingsButton.enabled = true
                    runCalculatorButton.enabled = true

                }
            }

            Button {
                Layout.preferredHeight: 23
                Layout.preferredWidth: parent.width * 0.5
                text: "Отмена"
                onClicked: {
                    versionWindow.visible = false
                }
            }
        }
    }
}

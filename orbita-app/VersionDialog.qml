import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Dialog  {
    id: versionDialog
    width: 264
    height: 146
    visible: false
    modal: true

    title: qsTr("Выберите версию Орбиты")
    x: mainWindow.width / 2 - width / 2
    y: mainWindow.height / 2 - height / 2
    ColumnLayout {
        anchors.fill: parent
        RowLayout {
            height: parent.height * 0.3
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
                    if (versionSelect.currentIndex === 0 ) {
                        modelSolutions.clear()
                        modelSolutions.append({text: "Таблица"})
                        mainWindow.typeMission = true
                        settingsManager.loadSettingsFromFile("planets_settings.txt");
                        pathToSave = settingsManager.getProbesPath()
                        pathToLoad = settingsManager.getProbesPath()
                        planetsItems.loadPlanets(settingsManager.getPlanetsPath());
                        planetDevicesItems.loadDevices(settingsManager.getDevicesPath());
                    } else {
                        modelSolutions.clear()
                        modelSolutions.append({text: "Диаграмма"})
                        mainWindow.typeMission = false
                    }
                    modelSolutions.append({text: "Python"})
                    newProbeButton.enabled = true
                    loadProbeButton.enabled = true
                    versionSelect.currentIndex = 0

                    settingsButton.enabled = true;
                    versionDialog.accepted()
                    versionDialog.close()
                }
            }

            Button {
                Layout.preferredHeight: 23
                Layout.preferredWidth: parent.width * 0.5
                text: "Отмена"
                onClicked: {
                    versionSelect.currentIndex = 0
                    versionDialog.rejected()
                    versionDialog.close()
                }
            }
        }
    }
}

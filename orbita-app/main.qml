import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow  {
    id: versionWindow
    width: 800
    height: 600
    visible: true
    flags: Qt.Window | Qt.WindowFixedSize
    title: qsTr("Выберите версию Орбиты")
    FirstOrbitaWindow {id: firstOrbitaWindow}
    SecondOrbitaWindow {id: secondOrbitaWindow}
    property ListModel modelSolutions: ListModel {}

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
                        modelSolutions.append({text: "Таблица"})
                        settingsManager.loadSettingsFromFile("planets_settings.txt");
                        firstOrbitaWindow.pathToSave = settingsManager.getPlanetsProbesPath()
                        firstOrbitaWindow.pathToLoad = settingsManager.getPlanetsProbesPath()
                        if (!planetsItems.size())
                            planetsItems.loadPlanets(settingsManager.getPlanetsPath());
                        if (!planetDevicesItems.size())
                            planetDevicesItems.loadDevices(settingsManager.getDevicesPath());

                        firstOrbitaWindow.visible = true
                        versionWindow.visible = false
                    } else {
                        modelSolutions.append({text: "Диаграмма"})
                        secondOrbitaWindow.visible = true
                        versionWindow.visible = false
                    }
                    modelSolutions.append({text: "Python"})
                    versionSelect.currentIndex = 0


                }
            }

            Button {
                Layout.preferredHeight: 23
                Layout.preferredWidth: parent.width * 0.5
                text: "Отмена"
                onClicked: {
                    versionSelect.currentIndex = 0
                }
            }
        }
    }
}

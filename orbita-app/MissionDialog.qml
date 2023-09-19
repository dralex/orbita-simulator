import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import PlanetsModel 1.0


Dialog  {
    id: missionDialog
    width: 264
    height: 146
    visible: false
    modal: true
    ErrorMessage {id: errorDialog}
    property ListModel clear: ListModel {}

    title: qsTr("Выберите миссию")
    x: firstOrbitaWindow.width / 2 - width / 2
    y: firstOrbitaWindow.height / 2 - height / 2
    ColumnLayout {
        anchors.fill: parent
        RowLayout {
            height: parent.height * 0.3
            width: parent.width
            Layout.preferredWidth: width
            Layout.preferredHeight: height
            ComboBox {
                id: missonSelect
                width: parent.width * 0.45
                height: parent.height
                Layout.preferredWidth: width
                Layout.preferredHeight: height
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

            ComboBox {
                id: solutionSelect
                width: parent.width * 0.55
                height: parent.height
                Layout.preferredWidth: width
                Layout.preferredHeight: height
                editable: false
                model: modelSolutions
                currentIndex: 0
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
                    probeNameText.text = ""
                    firstNumber.text = ""
                    secondNumber.text = ""
                    if (!missonSelect.currentText) {
                        errorDialog.textOfError = "Вы не выбрали миссию"
                        errorDialog.open()
                        return
                    } else if (!solutionSelect.currentText) {
                        errorDialog.textOfError = "Вы не выбрали способ решения"
                        errorDialog.open()
                        return
                    } else if (solutionSelect.currentText && missonSelect.currentText) {
                        if (missonSelect.currentText === "Moon" || missonSelect.currentText === "Mars") {
                            if (solutionSelect.currentText === "Таблица") {
                                showPlanetsElems = true
                                showPlanetsDevices = true
                                showPythonArea = false
                                showDiagrammButton = false
                                showPythonArea.text = ""

                                probes.loadFromXml(`${settingsManager.getSimulationPath()}/planets probes templates/${missonSelect.currentText}-Template.xml`, planetDevicesItems, settingsManager)
                                listViewProbes.currentIndex = probes.size() - 1
                                currentProbe = listViewProbes.currentItem.probesModelData

                                probeNameText.text = `${currentProbe.probeName}`
                                devicesItems.changeDevices(probes, listViewProbes.currentIndex)
                                stepsActivityItems.changeSteps(probes, listViewProbes.currentIndex)
                                stepsLandingItems.changeSteps(probes, listViewProbes.currentIndex)

                            } else if (solutionSelect.currentText === "Python") {
                                showPlanetsElems = false
                                showPlanetsDevices = true
                                showPythonArea = true
                                showDiagrammButton = false

                                probes.loadFromXml(`${settingsManager.getSimulationPath()}/planets probes templates/${missonSelect.currentText}-Python-Template.xml`, planetDevicesItems, settingsManager)
                                listViewProbes.currentIndex = probes.size() - 1
                                currentProbe = listViewProbes.currentItem.probesModelData

                                probeNameText.text = `${currentProbe.probeName}`
                                devicesItems.changeDevices(probes, listViewProbes.currentIndex)
                                stepsActivityItems.changeSteps(probes, listViewProbes.currentIndex)
                                stepsLandingItems.changeSteps(probes, listViewProbes.currentIndex)
                                pythonCodeTextArea.text = currentProbe.pythonCode
                            }
                        } else {
                            if (solutionSelect.currentText === "Таблица") {
                                showPlanetsElems = true
                                showPlanetsDevices = true
                                showPythonArea = false
                                showDiagrammButton = false
                                showPythonArea.text = ""

                                probes.appendProbe("probe", missonSelect.currentText, 0, 0, "", settingsManager.getPlanetsProbesPath() + "/probe.xml")

                                listViewProbes.currentIndex = probes.size() - 1
                                currentProbe = listViewProbes.currentItem.probesModelData
                                devicesItems.changeDevices(probes, listViewProbes.currentIndex)
                                stepsActivityItems.changeSteps(probes, listViewProbes.currentIndex)
                                stepsLandingItems.changeSteps(probes, listViewProbes.currentIndex)
                            }

                            if (solutionSelect.currentText === "Python") {
                                showPlanetsElems = false
                                showPlanetsDevices = true

                                showPythonArea = true
                                showDiagrammButton = false

                                probes.appendProbe("probe", missonSelect.currentText, 0, 0, "print('Hello World!')", settingsManager.getPlanetsProbesPath() + "/probe.xml")

                                listViewProbes.currentIndex = probes.size() - 1
                                currentProbe = listViewProbes.currentItem.probesModelData
                                devicesItems.changeDevices(probes, listViewProbes.currentIndex)
                                pythonCodeProperty = currentProbe.pythonCode

                            }

                            if (solutionSelect.currentText === "Диаграмма") {
                                showPlanetsElems = false
                                showPlanetsDevices = true
                                showPythonArea = false
                                showDiagrammButton = true
                                showPythonArea.text = ""
                            }
                        }

                        missionIndex = missonSelect.currentIndex

                        probeNameText.text = `${currentProbe.probeName}`

                        firstNumber.text = `${currentProbe.innerRadius}`
                        secondNumber.text = `${currentProbe.outerRadius}`

                        itemsEnabled = true

                        missonSelect.currentIndex = 0
                        solutionSelect.currentIndex = 0

                        missionDialog.accepted()
                        missionDialog.close()
                    }
                }
            }

            Button {
                Layout.preferredHeight: 23
                Layout.preferredWidth: parent.width * 0.5
                text: "Отмена"
                onClicked: {
                    missonSelect.currentIndex = 0
                    solutionSelect.currentIndex = 0
                    missionDialog.rejected()
                    missionDialog.close()
                }
            }
        }
    }
}

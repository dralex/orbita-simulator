import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

import PlanetsModel 1.0
import EarthMissionsModel 1.0


Dialog  {
    id: missionDialog
    width: 354
    height: 146
    visible: false
    modal: true
    ErrorMessage {id: errorDialog}
    property ListModel clear: ListModel {}

    title: qsTr("Выберите миссию")
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
                id: missonSelect
                width: parent.width * 0.6
                height: parent.height
                Layout.preferredWidth: width
                Layout.preferredHeight: height
                editable: false
                visible: planetsElementsVisible
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
                id: earthMissonSelect
                width: parent.width * 0.6
                height: parent.height
                Layout.preferredWidth: width
                Layout.preferredHeight: height
                editable: false
                visible: earthElementsVisible
                currentIndex: 0
                model: EarthMissionsModel {
                    list: earthMissions
                }
                onAccepted: {
                    if (find(editText) === -1)
                        model.append({text: editText})
                }
            }

            ComboBox {
                id: solutionSelect
                width: parent.width * 0.4
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
                    if ((!missonSelect.currentText && typeMission) || (!earthMissonSelect.currentText && !typeMission)) {
                        errorDialog.textOfError = "Вы не выбрали миссию"
                        errorDialog.open()
                        return
                    } else if (!solutionSelect.currentText) {
                        errorDialog.textOfError = "Вы не выбрали способ решения"
                        errorDialog.open()
                        return
                    } else if ((solutionSelect.currentText && missonSelect.currentText) || (earthMissonSelect.currentText && solutionSelect.currentText)) {
                        if ((missonSelect.currentText === "Moon" || missonSelect.currentText === "Mars") && typeMission) {
                            if (solutionSelect.currentText === "Таблица") {
                                showPlanetsElems = true
                                showPlanetsDevices = true
                                showPythonArea = false
                                showDiagrammButton = false
                                showPythonArea.text = ""

                                probes.loadFromXml(`../orbita-app/planets_probes_templates/${missonSelect.currentText}-Template.xml`,
                                                   planetDevicesItems,
                                                   settingsManager)
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

                                    probes.loadFromXml(`../orbita-app/planets_probes_templates/${missonSelect.currentText}-Python-Template.xml`,
                                                       planetDevicesItems,
                                                       settingsManager)
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
                                if (typeMission) {
                                    showPlanetsElems = false
                                    showPlanetsDevices = true

                                    showPythonArea = true
                                    showDiagrammButton = false

                                    probes.appendProbe("probe", missonSelect.currentText, 0, 0, "print('Hello World!')", settingsManager.getPlanetsProbesPath() + "/probe.xml")

                                    listViewProbes.currentIndex = probes.size() - 1
                                    currentProbe = listViewProbes.currentItem.probesModelData
                                    devicesItems.changeDevices(probes, listViewProbes.currentIndex)
                                    pythonCodeProperty = currentProbe.pythonCode
                                } else {
                                    if (earthMissions.getMissionEngName(earthMissonSelect.currentText).includes("test"))
                                        earthProbes.loadEarthProbeFromXml(`../orbita-app/earth_probes_templates/${earthMissions.getMissionEngName(earthMissonSelect.currentText)}.xml`,
                                                                          systems,
                                                                          earthMissions,
                                                                          settingsManager)
                                    else
                                        earthProbes.appendEarthProbe("earth probe", earthMissonSelect.currentText, "print('Hello World!')", "");
                                    listViewEarthProbes.currentIndex = earthProbes.size() - 1
                                    currentProbe = listViewEarthProbes.currentItem.earthProbesModelData

                                    probeNameText.text = `${currentProbe.probeName}`
                                    fuelTextInput.text = `${currentProbe.fuel}`
                                    voltageTextInput.text = `${currentProbe.voltage}`
                                    xz_yz_solar_id.text = `${currentProbe.xz_yz_solar}`
                                    xz_yz_radiator_id.text = `${currentProbe.xz_yz_radiator}`
                                    xy_radiator_id.text = `${currentProbe.xy_radiator}`
                                    earthProbeSystems.changeEarthSystems(earthProbes, listViewEarthProbes.currentIndex)

                                    gBEPythonCode.visible = true
                                    earthPythonCodeProperty = currentProbe.pythonCode
                                    showDiagrammButton = false
                                }


                            }

                            if (solutionSelect.currentText === "Диаграмма") {
                                if (earthMissions.getMissionEngName(earthMissonSelect.currentText).includes("test"))
                                    earthProbes.loadEarthProbeFromXml(`../orbita-app/earth_probes_templates/${earthMissions.getMissionEngName(earthMissonSelect.currentText)}sm.xml`,
                                                                      systems,
                                                                      earthMissions,
                                                                      settingsManager
                                                                      )
                                else
                                    earthProbes.appendEarthProbe("earth probe", earthMissonSelect.currentText, "", "");
                                listViewEarthProbes.currentIndex = earthProbes.size() - 1
                                currentProbe = listViewEarthProbes.currentItem.earthProbesModelData

                                probeNameText.text = `${currentProbe.probeName}`
                                fuelTextInput.text = `${currentProbe.fuel}`
                                voltageTextInput.text = `${currentProbe.voltage}`
                                xz_yz_solar_id.text = `${currentProbe.xz_yz_solar}`

                                xz_yz_radiator_id.text = `${currentProbe.xz_yz_radiator}`

                                xy_radiator_id.text = `${currentProbe.xy_radiator}`
                                earthProbeSystems.changeEarthSystems(earthProbes, listViewEarthProbes.currentIndex)

                                gBEPythonCode.visible = false
                                showDiagrammButton = true
                                earthPythonCodeProperty = ""

                            }
                        }

                        missionIndex = missonSelect.currentIndex
                        earthMissionIndex = earthMissonSelect.currentIndex

                        probeNameText.text = `${currentProbe.probeName}`

                        if (typeMission) {
                            firstNumber.text = `${currentProbe.innerRadius}`
                            secondNumber.text = `${currentProbe.outerRadius}`
                        }


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

import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import Qt.labs.settings 1.0

import ProbeModel 1.0
import DevicesModel 1.0
import StepsActivityModel 1.0
import StepsLandingModel 1.0
import PlanetsProbesDevicesModel 1.0

import DevicesTableModel 1.0

import EarthProbesModel 1.0
import SystemsProbeModel 1.0

ApplicationWindow  {
    id: mainWindow
    width: 773
    height: 745
    visible: true
    title: qsTr("Орбита")
    flags: Qt.Window | Qt.WindowFixedSize
    MissionDialog {id: missionDialog}
    DeviceDialog {id: deviceDialog}
    CommandDialog {id: commandDialog}
    RunWindow {id: runWindow}
    ErrorMessage {id: errorDialog}
    SuccessMessage {id: successDialog}
    DeviceForEarthDialog {id: deviceEarthDialog}
    PathToSaveDialog {id: pathToSaveDialog}
    PathToLoadDialog {id: pathToLoadDialog}
    SettingsDialog  {id: settingsDialog}
    SimulationPathDialog {id: simulationPathDialog}
    PlanetCalculator {id: planetCalculatorWindow}
    VersionWindow {id: versionWindow}
    FileNameDialog {id: fileNameDialog }
    CalculatorFileDialog {id: calculatorFileDialog}
    EarthDiagrammDialog {id: earthDiagrammDialog}
    DiagrammFileDialog {id: diagrammFileDialog}
    EarthCalculator {id: earthCalculatorWindow}
    property string fileNameFromDialog;
    property ListModel modelSolutions: ListModel {}
    property bool itemsEnabled: false
    property bool showPlanetsDevices: false
    property bool showPlanetsElems: false
    property bool showPythonArea: false
    property bool showDiagrammButton: false
    property bool whatIsWindow: false
    property bool typePathDialog: true
    property var currentProbe: undefined
    property int missionIndex: 0
    property string pythonCodeProperty: ""
    property string earthPythonCodeProperty: ""

    property string folderProbesPath: ""
    property string folderSimulation: ""
    property string folderCalculatorPath: ""
    property string pathToSave: ""
    property string pathToLoad: ""

    property string earthPathToSave: ""
    property string earthPathToLoad: ""
    property string earthFolderProbesPath: ""
    property string earthFolderSimulation: ""
    property string earthFolderCalculatorPath: ""
    property int earthMissionIndex: 0

    property string diagrammSystemName: ""

    property string settingsFolderSimulation: ""
    property string settingsFolderProbesPath: ""
    property string settingsFolderCalculatorPath: ""

    property bool planetsElementsVisible: false
    property bool earthElementsVisible: false
    property bool checkAction: false
    property bool typeMission: true

    Connections {
        target: earthProbes
        function onErrorOccurred(errorMessage) {
            errorDialog.textOfError = errorMessage;
            errorDialog.open();
        }
    }

    Connections {
        target: probes
        function onErrorOccurred(errorMessage) {
            errorDialog.textOfError = errorMessage;
            errorDialog.open();
        }
    }



    RowLayout {
        anchors.fill: parent
        x: 9
        GroupBox {
            id: groupBoxProbe
            title: qsTr("Cписок аппаратов")
            Layout.preferredWidth: 280
            Layout.fillHeight: true

            ListView {
                id: listViewProbes
                anchors.fill: parent
                width: parent.width
                height: parent.height - newProbeButton.height
                anchors.bottomMargin: 182
                clip: true
                enabled: itemsEnabled
                visible: planetsElementsVisible
                model: ProbeModel {
                    list: probes
                }

                ScrollBar.vertical: ScrollBar {
                    id: probesScrollBar
                    anchors {
                        right: parent.right
                        top: parent.top
                        bottom: parent.bottom
                        margins: 0
                    }
                }

                delegate: Item {
                    property variant probesModelData: model

                    width: listViewProbes.width
                    height: 50

                    Rectangle {
                        width: parent.width - probesScrollBar.width
                        height: parent.height - 5
                        color: listViewProbes.currentIndex === index && listViewProbes.enabled? "lightblue" : "white"
                        border.color: "grey"


                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                listViewProbes.currentIndex = index
                                currentProbe = listViewProbes.currentItem.probesModelData

                                probeNameText.text = `${model.probeName}`
                                firstNumber.text = `${model.outerRadius}`
                                secondNumber.text = `${model.innerRadius}`
                                devicesItems.changeDevices(probes, index)

                                if (currentProbe.pythonCode) {
                                    showPlanetsElems = false
                                    showPlanetsDevices = true
                                    showPythonArea = true
                                    pythonCodeProperty = currentProbe.pythonCode
                                    showDiagrammButton = false
                                } else {
                                    showPlanetsElems = true
                                    showPlanetsDevices = true
                                    showPythonArea = false
                                    showDiagrammButton = false
                                    pythonCodeProperty = ""
                                    stepsActivityItems.changeSteps(probes, index)
                                    stepsLandingItems.changeSteps(probes, index)
                                }

                            }
                        }
                    }

                    Column {
                        anchors.fill: parent
                        anchors.leftMargin: 5
                        anchors.topMargin: 5
                        spacing: 5
                        Text {
                            text: index >= 0 && index < listViewProbes.count ? '<b>Аппарат:</b> ' + model.probeName : ""
                        }

                        Text {
                            text: index >= 0 && index < listViewProbes.count ? '<b>Миссия:</b> ' + model.missionName : ""
                        }
                    }
                }
            }

            ListView {
                id: listViewEarthProbes
                anchors.fill: parent
                width: parent.width
                height: parent.height - newProbeButton.height
                anchors.bottomMargin: 182
                clip: true
                enabled: itemsEnabled
                visible: earthElementsVisible
                model: EarthProbesModel {
                    list: earthProbes
                }
                ScrollBar.vertical: ScrollBar {
                    id: probesEarthScrollBar
                    anchors {
                        right: parent.right
                        top: parent.top
                        bottom: parent.bottom
                        margins: 0
                    }
                }

                delegate: Item {
                    property variant earthProbesModelData: model

                    width: listViewEarthProbes.width
                    height: 65

                    Rectangle {
                        width: parent.width - probesScrollBar.width
                        height: parent.height - 5
                        color: listViewEarthProbes.currentIndex === index && listViewEarthProbes.enabled? "lightblue" : "white"
                        border.color: "grey"


                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                listViewEarthProbes.currentIndex = index
                                currentProbe = listViewEarthProbes.currentItem.earthProbesModelData

                                probeNameText.text = `${model.probeName}`
                                earthProbeSystems.changeEarthSystems(earthProbes, index)

                                if (currentProbe.pythonCode) {
                                    gBEPythonCode.visible = true
                                    earthPythonCodeProperty = currentProbe.pythonCode
                                    showDiagrammButton = false
                                } else {
                                    gBEPythonCode.visible = false
                                    showDiagrammButton = true
                                    earthPythonCodeProperty = ""
                                }
                            }
                        }
                    }

                    Column {
                        anchors.fill: parent
                        anchors.leftMargin: 5
                        anchors.topMargin: 5
                        spacing: 5
                        Text {
                            text: index >= 0 && index < listViewEarthProbes.count ? '<b>Аппарат:</b> ' + model.probeName : ""
                        }

                        Text {
                            width: listViewEarthProbes.width - probesScrollBar.width
                            text: index >= 0 && index < listViewEarthProbes.count ? '<b>Миссия:</b> ' + model.missionName : ""
                            wrapMode: Text.WordWrap
                        }
                    }
                }
            }


            Button {
                id: selectVersionButton

                width: parent.width; height: 23
                text: "Выбрать версию"
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 154
                onClicked: {
                    versionWindow.visible = true
                }
            }

            Button {
                id: newProbeButton
                width: parent.width; height: 23
                text: "Создать новый"
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 125
                enabled: false
                onClicked: {
                    if (typeMission) {
                        if (planetsItems.size()) {
                            missionDialog.open()
                        } else {
                            errorDialog.textOfError = "Выберите папку с симулятором в настройках."
                            errorDialog.open()
                        }
                    } else {
                        if(earthMissions.size()) {
                            missionDialog.open()
                        } else {
                            errorDialog.textOfError = "Выберите папку с симулятором в настройках."
                            errorDialog.open()
                        }
                    }
                }
            }

            Button {
                id: saveProbeButton
                width: parent.width; height: 23
                text: "Сохранить"
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 96
                enabled: itemsEnabled
                onClicked: {
                    checkAction = true
                    if (!currentProbe.probeFilePath) {
                        fileNameDialog.open()
                    } else {
                        if (typeMission) {
                            probes.saveProbe(listViewProbes.currentIndex,
                                             probeNameText.text,
                                             firstNumber.text,
                                             secondNumber.text,
                                             pythonCodeProperty,
                                             currentProbe.probeFilePath)

                            probes.saveToXml(listViewProbes.currentIndex,
                                             planetsItems,
                                             missionIndex,
                                             currentProbe.probeFilePath,
                                             )
                        } else {
                            earthProbes.saveEarthProbe(listViewEarthProbes.currentIndex,
                                                       probeNameText.text,
                                                       fuelTextInput.text,
                                                       voltageTextInput.text,
                                                       xz_yz_solar_id.text,
                                                       xz_yz_radiator_id.text,
                                                       xy_radiator_id.text,
                                                       currentProbe.probeFilePath);

                            earthProbes.saveEarthProbeToXml(listViewEarthProbes.currentIndex,
                                                            earthMissions,
                                                            systems,
                                                            earthMissionIndex,
                                                            currentProbe.probeFilePath,
                                                            )
                        }
                    }
                }
            }

            Button {
                id: loadProbeButton
                width: parent.width; height: 23
                text: "Загрузить"
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 67
                enabled: false
                onClicked: {
                    if (typeMission) {
                        settingsManager.loadSettingsFromFile("planets_settings.txt", typeMission);
                        pathToSave = settingsManager.getPlanetsProbesPath()
                        pathToLoad = settingsManager.getPlanetsProbesPath()
                        folderCalculatorPath = settingsManager.getPlanetsCalculatorPath()
                        if (!planetsItems.size())
                            planetsItems.loadPlanets(settingsManager.getPlanetsPath());
                        if (!planetDevicesItems.size())
                            planetDevicesItems.loadDevices(settingsManager.getDevicesPath());

                        if (planetsItems.size() > 0) {
                            pathToLoadDialog.open()
                        } else {
                            errorDialog.textOfError = "Выберите папку с симулятором в настройках."
                            errorDialog.open()
                        }
                    } else {
                        settingsManager.loadSettingsFromFile("earth_settings.txt", typeMission);
                        earthPathToLoad = settingsManager.getEarthProbesPath()
                        earthPathToSave = settingsManager.getEarthProbesPath()
                        folderCalculatorPath = settingsManager.getEarthCalculatorPath()

                        if (!earthMissions.size())
                            earthMissions.loadMissions(settingsManager.getMissionsPath());
                        if (!systems.size())
                            systems.loadSystems((settingsManager.getEarthSystemsPath()));

                        if (systems.size() > 0) {
                            pathToLoadDialog.open()
                        } else {
                            errorDialog.textOfError = "Выберите папку с симулятором в настройках."
                            errorDialog.open()
                        }
                    }
                }
            }

            Button {
                id: runButton
                width: parent.width; height: 23
                text: "Запустить"
                anchors.bottom: parent.bottom
                enabled: itemsEnabled
                anchors.bottomMargin: 30
                onClicked: {
                    if (typeMission) {
                        if (settingsManager.checkSimulationFile(settingsManager.getSimulationPath() + "/simulation.py")) {
                            probes.saveProbe(listViewProbes.currentIndex, probeNameText.text, firstNumber.text, secondNumber.text, pythonCodeProperty, currentProbe.probeFilePath)
                            if (probes.checkFileChanges(listViewProbes.currentIndex, planetDevicesItems)) {
                                settingsManager.saveSettingsToFile("planets_settings.txt", typeMission);
                                pathToSave = settingsManager.getPlanetsProbesPath()
                                pathToLoad = settingsManager.getPlanetsProbesPath()
                            } else {
                                errorDialog.textOfError = "Вы не сохранили изменения в аппарате!"
                                errorDialog.open()
                                return
                            }
                        } else {
                            errorDialog.textOfError = "В данной директории отсутствуют файлы симулятора."
                            errorDialog.open()
                            folderSimulation = "None"
                        }
                    } else {
                        if (settingsManager.checkSimulationFile(settingsManager.getEarthSimulationPath() + "/simulation.py")) {
                            earthProbes.saveEarthProbe(listViewEarthProbes.currentIndex, probeNameText.text, fuelTextInput.text, voltageTextInput.text,
                                                       xz_yz_solar_id.text, xz_yz_radiator_id.text, xy_radiator_id.text, currentProbe.probeFilePath);
                            if (earthProbes.checkFileChanges(systems, listViewEarthProbes.currentIndex)) {
                                settingsManager.saveSettingsToFile("earth_settings.txt", typeMission);
                                earthPathToSave = settingsManager.getEarthProbesPath()
                                earthPathToLoad = settingsManager.getEarthProbesPath()
                            } else {
                                errorDialog.textOfError = "Вы не сохранили изменения в аппарате!"
                                errorDialog.open()
                                return
                            }
                        } else {
                            errorDialog.textOfError = "В данной директории отсутствуют файлы симулятора."
                            errorDialog.open()
                            folderSimulation = "None"
                        }
                    }
                    runWindow.visibility = 1
                    mainWindow.visibility = 0
                }
            }

            Button {
                id: runCalculatorButton
                width: parent.width; height: 23
                text: "Запустить калькулятор"
                anchors.bottom: parent.bottom
                enabled: false
                onClicked: {
                    if (typeMission) {
                        if (settingsManager.checkSimulationFile(settingsManager.getPlanetsCalculatorPath() + "/simulation.py")) {
                            mainWindow.visibility = 0
                            planetCalculatorWindow.visibility = 1

                        } else {
                            errorDialog.textOfError = "В данной директории отсутствуют файлы симулятора."
                            errorDialog.open()
                            folderSimulation = "None"
                        }
                    } else {
                        if (settingsManager.checkSimulationFile(settingsManager.getEarthCalculatorPath() + "/simulation.py")) {
                            mainWindow.visibility = 0
                            earthCalculatorWindow.visibility = 1

                        } else {
                            errorDialog.textOfError = "В данной директории отсутствуют файлы симулятора."
                            errorDialog.open()
                            folderSimulation = "None"
                        }
                    }
                }
            }
        }

        GroupBox {
            id: probesConstructor
            Layout.preferredWidth: parent.width - groupBoxProbe.width - 10
            Layout.fillHeight: true
            title: qsTr("Аппарат")
            ColumnLayout {
                anchors.fill: parent
                RowLayout {
                    Layout.preferredHeight: 20
                    Text {
                        height: probeNameText.implicitHeight
                        text: "Название:"
                    }
                    TextInput {
                        id: probeNameText
                        width: 200
                        height: 10
                        enabled: itemsEnabled
                        onTextChanged: {
                            if (probeNameText.text.length > 30) {
                                probeNameText.text = probeNameText.text.substring(0, 30);
                            }
                        }

                        property string placeholderText: "Введите название..."

                        Text {
                            text: probeNameText.placeholderText
                            color: "#aaa"
                            visible: !probeNameText.text
                        }
                    }
                }

                GroupBox {
                    Layout.preferredWidth: parent.width
                    Layout.preferredHeight: 100
                    title: qsTr("Общие параметры")
                    visible: planetsElementsVisible

                    GridLayout {
                        height: parent.height
                        columns: 2
                        rows: 2

                        Text {
                            text: "Внутренний радиус (м)"
                            Layout.row: 0
                            Layout.column: 0
                        }

                        TextInput {
                            id: firstNumber
                            Layout.row: 0
                            Layout.column: 1
                            width: 200
                            height: 10
                            enabled: itemsEnabled

                            onTextChanged: {
                                if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(firstNumber.text)) {
                                    firstNumber.text = firstNumber.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                                }
                            }

                            property string placeholderText: "Введите число..."

                            Text {
                                text: firstNumber.placeholderText
                                color: "#aaa"
                                visible: !firstNumber.text
                            }
                        }

                        Text {
                            text: "Внешний радиус (м)"
                            Layout.row: 1
                            Layout.column: 0
                        }

                        TextInput {
                            id: secondNumber
                            Layout.row: 1
                            Layout.column: 1
                            width: 200
                            height: 10
                            enabled: itemsEnabled

                            onTextChanged: {
                                if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(secondNumber.text)) {
                                    secondNumber.text = secondNumber.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                                }
                            }

                            property string placeholderText: "Введите число..."

                            Text {
                                text: secondNumber.placeholderText
                                color: "#aaa"
                                visible: !secondNumber.text
                            }
                        }
                    }
                }

                GroupBox {
                    Layout.preferredWidth: parent.width
                    Layout.preferredHeight: 140
                    visible: planetsElementsVisible
                    title: qsTr("Устройства")

                    RowLayout {
                        anchors.fill: parent
                        ListView {
                            id: listViewDevices
                            width: parent.width - devicesButtons.width
                            height: parent.height
                            clip: true
                            enabled: itemsEnabled
                            visible: showPlanetsDevices
                            model: DevicesModel {
                                list: devicesItems
                            }



                            ScrollBar.vertical: ScrollBar {
                                id: devicesScrollBar
                                anchors {
                                    right: parent.right
                                    top: parent.top
                                    bottom: parent.bottom
                                    margins: 0
                                }
                            }

                            delegate: Item {
                                property variant devicesModelData: model

                                width: listViewDevices.width
                                height: 100
                                Rectangle {
                                    width: parent.width - devicesScrollBar.width
                                    height: parent.height - 5
                                    color: listViewDevices.currentIndex === index ** listViewDevices.enabled? "lightblue" : "white"
                                    border.color: "grey"

                                    MouseArea {
                                        anchors.fill: parent
                                        onClicked: {
                                            listViewDevices.currentIndex = index
                                        }
                                    }
                                }

                                Column {
                                    anchors.fill: parent
                                    anchors.leftMargin: 5
                                    anchors.topMargin: 15

                                    Text { text: '<b>Номер:</b> ' + model.deviceNumber  }

                                    Text { text: index >= 0 && index < listViewDevices.count && model.deviceName ? '<b>Название:</b> ' + model.deviceName : "<b>Название:</b> None" }

                                    Text { text: index >= 0 && index < listViewDevices.count && model.startState ? '<b>Начальное состояние:</b> ' + model.startState : "<b>Начальное состояние:</b> None" }

                                    Text {
                                        text: index >= 0 && index < listViewDevices.count ? '<b>Safe Mode:</b> ' + model.inSafeMode : ""
                                    }

                                }
                            }
                        }

                        ColumnLayout {
                            id: devicesButtons
                            Layout.preferredHeight: 23
                            Layout.preferredWidth: 80
                            Layout.alignment: Qt.AlignRight | Qt.AlignTop
                            Button {
                                id: buttonAddDevice
                                Layout.preferredHeight: 23
                                Layout.preferredWidth: 80
                                text: "Добавить"
                                enabled: itemsEnabled
                                onClicked: {
                                    if (planetDevicesItems.size()) {
                                        deviceDialog.open()
                                    } else {
                                        errorDialog.textOfError = "Выберите папку с симулятором в настройках."
                                        errorDialog.open()
                                    }
                                }
                            }

                            Button {
                                id: buttonDeleteDevice
                                Layout.preferredHeight: 23
                                Layout.preferredWidth: 80
                                text: "Удалить"
                                enabled: itemsEnabled
                                onClicked: {
                                    if (devicesItems.size()) {
                                        successDialog.message = `Успешно удалено устройство ${listViewDevices.currentItem.devicesModelData.deviceName}`
                                        devicesItems.removeDevicesItem(probes, stepsActivityItems, stepsLandingItems, listViewProbes.currentIndex, listViewDevices.currentIndex)
                                        successDialog.open()
                                    }

                                }
                            }
                        }

                    }


                }

                GroupBox {
                    Layout.preferredWidth: parent.width
                    Layout.preferredHeight: 90
                    title: qsTr("Общие параметры")
                    visible: earthElementsVisible
                    GridLayout {
                        height: parent.height
                        columns: 2
                        rows: 2

                        Text {
                            text: "Кол-во топлива:"
                            Layout.row: 0
                            Layout.column: 0
                        }

                        TextInput {
                            id: fuelTextInput
                            Layout.row: 0
                            Layout.column: 1
                            width: 200
                            height: 10
                            enabled: itemsEnabled

                            onTextChanged: {
                                if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(fuelTextInput.text)) {
                                    fuelTextInput.text = fuelTextInput.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                                }
                            }

                            property string placeholderText: "Введите число..."

                            Text {
                                text: fuelTextInput.placeholderText
                                color: "#aaa"
                                visible: !fuelTextInput.text
                            }
                        }

                        Text {
                            text: "Вольтаж:"
                            Layout.row: 1
                            Layout.column: 0
                        }

                        TextInput {
                            id: voltageTextInput
                            Layout.row: 1
                            Layout.column: 1
                            width: 200
                            height: 10
                            enabled: itemsEnabled

                            onTextChanged: {
                                if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(voltageTextInput.text)) {
                                    voltageTextInput.text = voltageTextInput.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                                }
                            }

                            property string placeholderText: "Введите число..."

                            Text {
                                text: voltageTextInput.placeholderText
                                color: "#aaa"
                                visible: !voltageTextInput.text
                            }
                        }

                    }

                }

                GroupBox {
                    Layout.preferredWidth: parent.width
                    Layout.preferredHeight: 120
                    title: qsTr("Общие параметры долей")
                    visible: earthElementsVisible

                    GridLayout {
                        height: parent.height
                        columns: 2
                        rows: 3

                        Text {
                            text: "Солнечная панель (Ось: XZ YZ):"
                            Layout.row: 0
                            Layout.column: 0
                        }

                        TextInput {
                            id: xz_yz_solar_id
                            Layout.row: 0
                            Layout.column: 1
                            width: 200
                            height: 10
                            enabled: itemsEnabled

                            onTextChanged: {
                                if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(xz_yz_solar_id.text)) {
                                    xz_yz_solar_id.text = xz_yz_solar_id.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                                }
                            }

                            property string placeholderText: "Введите число..."

                            Text {
                                text: xz_yz_solar_id.placeholderText
                                color: "#aaa"
                                visible: !xz_yz_solar_id.text
                            }
                        }

                        Text {
                            text: "Радиатор (Ось: XZ YZ):"
                            Layout.row: 1
                            Layout.column: 0
                        }

                        TextInput {
                            id: xz_yz_radiator_id
                            Layout.row: 1
                            Layout.column: 1
                            width: 200
                            height: 10
                            enabled: itemsEnabled

                            onTextChanged: {
                                if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(xz_yz_radiator_id.text)) {
                                    xz_yz_radiator_id.text = xz_yz_radiator_id.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                                }
                            }

                            property string placeholderText: "Введите число..."

                            Text {
                                text: xz_yz_radiator_id.placeholderText
                                color: "#aaa"
                                visible: !xz_yz_radiator_id.text
                            }
                        }

                        Text {
                            text: "Радиатор (Ось: XY):"
                            Layout.row: 2
                            Layout.column: 0
                        }

                        TextInput {
                            id: xy_radiator_id
                            Layout.row: 2
                            Layout.column: 1
                            width: 200
                            height: 10
                            enabled: itemsEnabled

                            onTextChanged: {
                                if (!/^[-]?[0-9]*[.]?[0-9]*$/.test(xy_radiator_id.text)) {
                                    xy_radiator_id.text = xy_radiator_id.text.replace(new RegExp("[^\\d.\\-]", "g"), "");
                                }
                            }

                            property string placeholderText: "Введите число..."

                            Text {
                                text: xy_radiator_id.placeholderText
                                color: "#aaa"
                                visible: !xy_radiator_id.text
                            }
                        }
                    }
                }


                GroupBox {
                    Layout.preferredWidth: parent.width
                    Layout.preferredHeight: 140
                    visible: earthElementsVisible
                    title: qsTr("Подсистемы")

                    RowLayout {
                        anchors.fill: parent
                        ListView {
                            id: listViewEarthSystems
                            width: parent.width - devicesButtons.width
                            height: parent.height
                            clip: true
                            enabled: itemsEnabled
                            visible: earthElementsVisible
                            model: SystemsProbeModel {
                                list: earthProbeSystems
                            }


                            ScrollBar.vertical: ScrollBar {
                                id: earthDevicesScrollBar
                                anchors {
                                    right: parent.right
                                    top: parent.top
                                    bottom: parent.bottom
                                    margins: 0
                                }
                            }

                            delegate: Item {
                                property variant systemsModelData: model

                                width: listViewEarthSystems.width - earthDevicesScrollBar.width
                                height: model.diagramPath ? 95 : 80
                                Rectangle {
                                    width: parent.width - devicesScrollBar.width
                                    height: parent.height - 5
                                    color: listViewEarthSystems.currentIndex === index ** listViewEarthSystems.enabled? "lightblue" : "white"
                                    border.color: "grey"

                                    MouseArea {
                                        anchors.fill: parent
                                        onClicked: {
                                            listViewEarthSystems.currentIndex = index
                                        }
                                    }
                                }

                                Column {
                                    anchors.fill: parent
                                    anchors.leftMargin: 5
                                    anchors.topMargin: 10


                                    Text {
                                        width: listViewEarthSystems.width - systemsEarthButtons.width
                                        text: index >= 0 && index < listViewEarthSystems.count && model.systemName ? '<b>Название:</b> ' + model.systemName : "<b>Название:</b> None"
                                        wrapMode: Text.WordWrap
                                    }

                                    Text { text: index >= 0 && index < listViewEarthSystems.count && model.mass ? '<b>Масса:</b> ' + model.mass : "<b>Масса:</b> None" }

                                    Text {
                                        text: index >= 0 && index < listViewEarthSystems.count ? '<b>Начальное состояние:</b> ' + model.startMode : ""
                                    }

                                    Text {
                                        width: listViewEarthSystems.width - systemsEarthButtons.width
                                        text: index >= 0 && index < listViewEarthSystems.count && model.diagramPath ? '<b>Путь к файлу:</b> ' + model.diagramPath : ""
                                        wrapMode: Text.WordWrap
                                    }

                                }
                            }
                        }

                        ColumnLayout {
                            id: systemsEarthButtons
                            visible: earthElementsVisible
                            Layout.preferredHeight: 23
                            Layout.preferredWidth: 80
                            Layout.alignment: Qt.AlignRight | Qt.AlignTop
                            Button {
                                id: buttonAddEarthSystem
                                Layout.preferredHeight: 23
                                Layout.preferredWidth: 80
                                text: "Добавить"
                                enabled: itemsEnabled
                                onClicked: {
                                    if (systems.size()) {
                                        deviceEarthDialog.open()
                                    } else {
                                        errorDialog.textOfError = "Выберите папку с симулятором в настройках."
                                        errorDialog.open()
                                    }
                                }
                            }

                            Button {
                                id: buttonDeleteEarthSystem
                                Layout.preferredHeight: 23
                                Layout.preferredWidth: 80
                                text: "Удалить"
                                enabled: itemsEnabled
                                onClicked: {
                                    if (systems.size()) {
                                        successDialog.message = `Успешно удалена подсистема: ${listViewEarthSystems.currentItem.systemsModelData.systemName}`
                                        earthProbeSystems.removeEarthSystem(earthProbes, listViewEarthProbes.currentIndex, listViewEarthSystems.currentIndex)
                                        successDialog.open()
                                    }

                                }
                            }
                        }

                    }


                }


                GroupBox {
                    id: commandsGroupBox
                    width: parent.width
                    height: 400
                    Layout.preferredWidth: parent.width
                    Layout.preferredHeight: 400
                    visible: showPlanetsElems
                    title: qsTr("Команды")

                    ColumnLayout {
                        anchors.fill: parent

                        GroupBox {
                            id: stepsLandingGroupBox
                            Layout.preferredWidth: parent.width
                            Layout.preferredHeight: parent.height * 0.5
                            title: qsTr("Этап приземления")
                            RowLayout {
                                anchors.fill: parent
                                ListView {
                                    id: listViewStepsLanding
                                    width: parent.width - sLButton.width
                                    height: parent.height
                                    clip: true
                                    enabled: itemsEnabled
                                    visible: showPlanetsElems
                                    model: StepsLandingModel {
                                        list: stepsLandingItems
                                    }


                                    ScrollBar.vertical: ScrollBar {
                                        id: stepsLandingScrollBar
                                        anchors {
                                            right: parent.right
                                            top: parent.top
                                            bottom: parent.bottom
                                            margins: 0
                                        }
                                    }

                                    delegate: Item {
                                        width: listViewStepsLanding.width
                                        height: model.argument ? 85 : 80
                                        Rectangle {
                                            width: parent.width - stepsLandingScrollBar.width
                                            height: parent.height - 5
                                            color: listViewStepsLanding.currentIndex === index && listViewStepsLanding.enabled? "lightblue" : "white"
                                            border.color: "grey"

                                            MouseArea {
                                                anchors.fill: parent
                                                onClicked: {
                                                    listViewStepsLanding.currentIndex = index
                                                }
                                            }
                                        }

                                        Column {
                                            anchors.fill: parent
                                            anchors.leftMargin: 5
                                            anchors.topMargin: model.argument ? 2 : 5

                                            Text { text: index >= 0 && index < listViewStepsLanding.count && model.deviceNumber? '<b>Номер устройства:</b> ' + model.deviceNumber : "<b>Номер устройства:</b> None" }

                                            Text { text: index >= 0 && index < listViewStepsLanding.count && model.time >= 0 ? '<b>Время:</b> ' + model.time : "<b>Время:</b> None" }

                                            Text { text: index >= 0 && index < listViewStepsLanding.count && model.device ? '<b>Тип:</b> ' + model.device : "<b>Тип:</b> None" }

                                            Text { text: index >= 0 && index < listViewStepsLanding.count && model.command ? '<b>Команда:</b> ' + model.command : "<b>Команда:</b> None" }

                                            Text { text: index >= 0 && index < listViewStepsLanding.count && model.argument ? '<b>Параметр:</b> ' + model.argument : "" }
                                        }
                                    }
                                }


                                ColumnLayout {
                                    id: sLButton
                                    height: 23
                                    Layout.alignment: Qt.AlignRight | Qt.AlignTop
                                    Button {
                                        id: buttonAddSL
                                        Layout.preferredHeight: 23
                                        text: "Добавить"
                                        enabled: itemsEnabled
                                        onClicked: {
                                            whatIsWindow = true
                                            commandDialog.open()
                                        }
                                    }

                                    Button {
                                        id: buttonDeleteSL
                                        Layout.preferredHeight: 23
                                        text: "Удалить"
                                        enabled: itemsEnabled
                                        onClicked: {
                                            if (stepsLandingItems.size()) {
                                                successDialog.message = "Успшено удалено"
                                                stepsLandingItems.removeItem(probes, true, listViewProbes.currentIndex, listViewStepsLanding.currentIndex)
                                                successDialog.open()
                                            }
                                        }

                                    }
                                }
                            }
                        }

                        GroupBox {
                                id: stepsPlanetActivityGroupBox
                                title: qsTr("Этапы Планетарной активности")
                                Layout.preferredWidth: parent.width
                                Layout.preferredHeight: parent.height * 0.5
                                RowLayout {
                                    anchors.fill: parent
                                    ListView {
                                        id: listViewStepsPlanetActivity
                                        width: parent.width - sPAButtons.width
                                        height: parent.height
                                        clip: true
                                        enabled: itemsEnabled
                                        visible: showPlanetsElems
                                        model: StepsActivityModel {
                                            list: stepsActivityItems
                                        }


                                        ScrollBar.vertical: ScrollBar {
                                            id: stepsPlanetActivityScrollBar
                                            anchors {
                                                right: parent.right
                                                top: parent.top
                                                bottom: parent.bottom
                                                margins: 0
                                            }
                                        }

                                        delegate: Item {
                                            width: listViewStepsPlanetActivity.width
                                            height: model.argument ? 85 : 80
                                            Rectangle {
                                                width: parent.width - stepsPlanetActivityScrollBar.width
                                                height: parent.height - 5
                                                color: listViewStepsPlanetActivity.currentIndex === index && listViewStepsPlanetActivity.enabled? "lightblue" : "white"
                                                border.color: "grey"

                                                MouseArea {
                                                    anchors.fill: parent
                                                    onClicked: {
                                                        listViewStepsPlanetActivity.currentIndex = index
                                                    }
                                                }
                                            }

                                            Column {
                                                anchors.fill: parent
                                                anchors.leftMargin: 5
                                                anchors.topMargin: 3

                                                Text { text: index >= 0 && index < listViewStepsLanding.count && model.deviceNumber ? '<b>Номер устройства:</b> ' + model.deviceNumber : "<b>Номер устройства:</b> None" }

                                                Text { text: index >= 0 && index < listViewStepsPlanetActivity.count && model.time >= 0 ? '<b>Время:</b> ' + model.time : "<b>Время:</b> None" }

                                                Text { text: index >= 0 && index < listViewStepsPlanetActivity.count && model.device ? '<b>Тип:</b> ' + model.device : "<b>Тип:</b> None" }

                                                Text { text: index >= 0 && index < listViewStepsPlanetActivity.count && model.command ? '<b>Команда:</b>' + model.command : "<b>Команда:</b> None" }

                                                Text { text: index >= 0 && index < listViewStepsPlanetActivity.count && model.argument ? '<b>Параметр:</b> ' + model.argument : "" }
                                            }
                                        }
                                    }


                                    ColumnLayout {
                                        id: sPAButtons
                                        Layout.preferredHeight: 23
                                        Layout.alignment: Qt.AlignRight | Qt.AlignTop
                                        Button {
                                            id: buttonAddSPA
                                            Layout.preferredHeight: 23
                                            text: "Добавить"
                                            enabled: itemsEnabled
                                            onClicked: {
                                                whatIsWindow = false
                                                commandDialog.open()
                                            }
                                        }

                                        Button {
                                            id: buttonDeleteSPA
                                            Layout.preferredHeight: 23
                                            text: "Удалить"
                                            enabled: itemsEnabled
                                            onClicked: {
                                                if (stepsActivityItems.size()) {
                                                    successDialog.message = "Успешно удалено"
                                                    stepsActivityItems.removeItem(probes, false, listViewProbes.currentIndex, listViewStepsPlanetActivity.currentIndex)
                                                    successDialog.open()
                                                }

                                            }
                                        }
                                    }
                                }
                            }

                    }


                }

                GroupBox {
                    width: parent.width
                    height: 400
                    Layout.preferredWidth: parent.width
                    Layout.preferredHeight: 400
                    visible: showPythonArea
                    title: qsTr("Вставьте Python код:")

                    ScrollView {
                        anchors.fill: parent
                        TextArea {
                            id: pythonCodeTextArea
                            width: parent.width
                            height: parent.height
                            enabled: itemsEnabled
                            text: pythonCodeProperty

                            onTextChanged: {
                                pythonCodeProperty = text;
                            }

                            Keys.onPressed: {
                                if (event.key === Qt.Key_Tab) {
                                    event.accepted = true;
                                    var cursorPos = cursorPosition;
                                    text = text.slice(0, cursorPos) + "    " + text.slice(cursorPos);
                                    cursorPosition = cursorPos + 4;
                                }
                            }
                        }
                    }
                }


                GroupBox {
                    id: gBEPythonCode
                    width: parent.width
                    height: 300
                    Layout.preferredWidth: parent.width
                    Layout.preferredHeight: 300
                    visible: false
                    title: qsTr("Вставьте Python код:")

                    ScrollView {
                        anchors.fill: parent
                        TextArea {
                            id: earthPythonCodeTextArea
                            width: parent.width
                            height: parent.height

                            text: earthPythonCodeProperty

                            onTextChanged: {
                                earthPythonCodeProperty = text;
                            }

                            Keys.onPressed: {
                                if (event.key === Qt.Key_Tab) {
                                    event.accepted = true;
                                    var cursorPos = cursorPosition;
                                    text = text.slice(0, cursorPos) + "    " + text.slice(cursorPos);
                                    cursorPosition = cursorPos + 4;
                                }
                            }
                        }
                    }
                }


                Button {
                    id: settingsButton
                    width: parent.width * 0.4
                    height: 23
                    Layout.preferredHeight: height
                    Layout.preferredWidth: width
                    Layout.alignment: Qt.AlignBottom | Qt.AlignRight
                    enabled: false
                    text: "Настройки"
                    onClicked: {
                        folderProbesPath = settingsManager.getPlanetsProbesPath()
                        folderSimulation = settingsManager.getSimulationPath()
                        settingsDialog.open()
                    }
                }

                ColumnLayout {
                    Layout.preferredHeight: 500
                    width: parent.width
                    Button {
                        text: "Загрузить диаграмму"
                        height: 23
                        width: parent.width
                        Layout.alignment: Qt.AlignRight | Qt.AlignTop
                        Layout.preferredHeight: height
                        Layout.preferredWidth: width
                        enabled: itemsEnabled
                        visible: showDiagrammButton
                        onClicked: {
                            if (earthProbeSystems.size()) {
                                earthDiagrammDialog.open()
                            } else {
                                errorDialog.textOfError = "Добавьте подсистемы!"
                                errorDialog.open()
                            }

                        }

                    }
                }
            }
        }
    }
}

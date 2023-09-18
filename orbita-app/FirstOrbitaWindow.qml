import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import Qt.labs.settings 1.0

import ProbeModel 1.0
import DevicesModel 1.0
import StepsActivityModel 1.0
import StepsLandingModel 1.0

Window  {
    id: firstOrbitaWindow
    width: 773
    height: 745
    visible: false
    title: qsTr("Орбита 1.0")
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
    property bool itemsEnabled: false
    property bool showPlanetsDevices: false
    property bool showPlanetsElems: false
    property bool showPythonArea: false
    property bool showDiagrammButton: false
    property bool whatIsWindow: false
    property bool typePathDialog: true
    property var currentProbe: undefined
    property string pathToSave: ""
    property string pathToLoad: ""
    property int missionIndex: 0
    property string pythonCodeProperty: ""
    property string folderProbesPath: ""
    property string folderSimulation: ""

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
                anchors.bottomMargin: 158
                clip: true
                enabled: itemsEnabled
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

            Button {
                id: selectVersionButton

                width: parent.width; height: 23
                text: "Сменить версию"
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 125
                onClicked: {
                    versionWindow.visible = true
                    firstOrbitaWindow.visible = false
                }
            }

            Button {
                id: newProbeButton
                width: parent.width; height: 23
                text: "Cоздать новый"
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 96

                onClicked: {
                    if (planetsItems.size() > 0) {
                        missionDialog.open()
                    } else {
                        errorDialog.textOfError = "Выберите папку с симулятором в настройках."
                        errorDialog.open()
                    }
                }
            }

            Button {
                id: saveProbeButton
                width: parent.width; height: 23
                text: "Сохранить"
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 67
                enabled: itemsEnabled
                onClicked: {
                    if (!currentProbe.probeFilePath) {
                        pathToSaveDialog.open()
                    } else {
                        probes.saveProbe(listViewProbes.currentIndex, probeNameText.text, firstNumber.text, secondNumber.text, pythonCodeProperty, currentProbe.probeFilePath)
                        probes.saveToXml(listViewProbes.currentIndex, planetsItems, missionIndex, currentProbe.probeFilePath)
                    }
                }
            }

            Button {
                id: loadProbeButton
                width: parent.width; height: 23
                text: "Загрузить"
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 38
                onClicked: {
                    settingsManager.loadSettingsFromFile("planets_settings.txt");
                    firstOrbitaWindow.pathToSave = settingsManager.getProbesPath()
                    firstOrbitaWindow.pathToLoad = settingsManager.getProbesPath()
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

                }
            }

            Button {
                id: runButton
                width: parent.width; height: 23
                text: "Запустить"
                anchors.bottom: parent.bottom
                enabled: itemsEnabled
                onClicked: {
                    if (settingsManager.checkSimulationFile(settingsManager.getSimulationPath() + "/simulation.py")) {
                        settingsManager.saveSettingsToFile("planets_settings.txt");
                        pathToSave = settingsManager.getProbesPath()
                        pathToLoad = settingsManager.getProbesPath()
                        runWindow.visible = true
                        firstOrbitaWindow.visible = false
                    } else {
                        errorDialog.textOfError = "В данной директории отсутствуют файлы симулятора."
                        errorDialog.open()
                        folderSimulation = "None"
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
                                        height: 85
                                        Rectangle {
                                            width: parent.width - devicesScrollBar.width
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
                                            anchors.topMargin: 2

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
                                            height: 85
                                            Rectangle {
                                                width: parent.width - devicesScrollBar.width
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
                                                anchors.topMargin: 2

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
                    TextArea {
                        id: pythonCodeTextArea
                        anchors.fill: parent
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

                Button {
                    id: settingsButton
                    width: parent.width * 0.4
                    height: 23
                    Layout.preferredHeight: height
                    Layout.preferredWidth: width
                    Layout.alignment: Qt.AlignBottom | Qt.AlignRight
                    text: "Настройки"
                    onClicked: {
                        folderProbesPath = settingsManager.getProbesPath()
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

                    }

                    Text {
                        Layout.alignment: Qt.AlignTop
                        text: "Вы не выбрали диаграмму"
                        visible: showDiagrammButton

                    }
                }
            }

        }
    }
}

import QtQuick.Dialogs 1.3

FileDialog {
    id: fileToLoadDialog
    title: 'Выберите файл для загрузки'
    selectFolder: false
    selectMultiple: false
    width: 264
    height: 146
    visible: false
    folder: ""

    onAccepted: {
        var filePath = fileToLoadDialog.fileUrl.toString()
        var folderPath = fileToLoadDialog.folder.toString()

        if (filePath.startsWith("file://") || folderPath.startsWith("file://")) {
            pathToLoad = folderPath.substring(7)
            var fileToLoad= filePath.substring(7)
        }

        if (typeMission) {
            probes.loadFromXml(fileToLoad, planetDevicesItems, settingsManager)
            listViewProbes.currentIndex = probes.size() - 1
            currentProbe = listViewProbes.currentItem.probesModelData

            devicesItems.changeDevices(probes, listViewProbes.currentIndex)
            stepsActivityItems.changeSteps(probes, listViewProbes.currentIndex)
            stepsLandingItems.changeSteps(probes, listViewProbes.currentIndex)

            probeNameText.text = `${currentProbe.probeName}`

            firstNumber.text = `${currentProbe.innerRadius}`
            secondNumber.text = `${currentProbe.outerRadius}`
            if (currentProbe.pythonCode) {
                showPlanetsElems = false
                showPlanetsDevices = true
                showPythonArea = true
                showDiagrammButton = false
                pythonCodeTextArea.text = currentProbe.pythonCode
            } else {
                showPlanetsElems = true
                showPlanetsDevices = true
                showPythonArea = false
                showDiagrammButton = false
            }
        } else {
            earthProbes.loadEarthProbeFromXml(fileToLoad, systems, earthMissions, settingsManager);
            listViewEarthProbes.currentIndex = earthProbes.size() - 1
            currentProbe = listViewEarthProbes.currentItem.earthProbesModelData

            earthProbeSystems.changeEarthSystems(earthProbes, listViewEarthProbes.currentIndex)
            probeNameText.text = `${currentProbe.probeName}`
            fuelTextInput.text = `${currentProbe.fuel}`
            voltageTextInput.text = `${currentProbe.voltage}`
            xz_yz_solar_id.text = `${currentProbe.xz_yz_solar}`
            xz_yz_radiator_id.text = `${currentProbe.xz_yz_radiator}`
            xy_radiator_id.text = `${currentProbe.xy_radiator}`

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


        itemsEnabled = true
    }
}

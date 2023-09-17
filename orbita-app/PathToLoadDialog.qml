import QtQuick.Dialogs 1.3

FileDialog {
    id: fileToLoadDialog
    title: 'Выберите файл для загрузки'
    selectFolder: false
    selectMultiple: false
    width: 264
    height: 146
    visible: false
    folder: "file://" + pathToLoad
    onAccepted: {
        var filePath = fileToLoadDialog.fileUrl.toString()
        var folderPath = fileToLoadDialog.folder.toString()

        if (filePath.startsWith("file://") || folderPath.startsWith("file://")) {
            pathToLoad = folderPath.substring(7)
            var fileToLoad= filePath.substring(7)
        }

        probes.loadFromXml(fileToLoad, planetDevicesItems)
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

        itemsEnabled = true
    }
}

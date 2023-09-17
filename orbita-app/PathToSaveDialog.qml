import QtQuick.Dialogs 1.3
import QtQuick.Controls 2.5

FileDialog {
    id: fileToSaveDialog
    title: 'Выберите файл для сохранения'
    folder: "file://" + pathToSave
    selectFolder: false
    selectMultiple: false
    width: 264
    height: 200
    visible: false

    onAccepted: {
        var filePath = fileToSaveDialog.fileUrl.toString()
        folderProbesPath = fileToSaveDialog.folder.toString()

        if (filePath.startsWith("file://") || folderProbesPath.startsWith("file://")) {
            var fileToSave = filePath.substring(7)
            folderProbesPath = folderProbesPath.substring(7)

        }

        settingsManager.setProbesPath(folderProbesPath)
        settingsManager.saveSettingsToFile("planets_settings.txt");
        pathToSave = settingsManager.getProbesPath()
        pathToLoad = settingsManager.getProbesPath()
        if (fileToSave) {
            probes.saveProbe(listViewProbes.currentIndex, probeNameText.text, firstNumber.text, secondNumber.text, pythonCodeProperty, fileToSave)
            probes.saveToXml(listViewProbes.currentIndex, planetsItems, missionIndex, fileToSave)
        } else {
            probes.saveProbe(listViewProbes.currentIndex, probeNameText.text, firstNumber.text, secondNumber.text, pythonCodeProperty, folderProbesPath + `/${currentProbe.probeName}.xml`)
            probes.saveToXml(listViewProbes.currentIndex, planetsItems, missionIndex, folderProbesPath + `/${currentProbe.probeName}.xml`)
        }
    }
}

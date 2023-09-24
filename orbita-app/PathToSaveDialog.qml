import QtQuick.Dialogs 1.3
import QtQuick.Controls 2.5

FileDialog {
    id: fileToSaveDialog
    title: 'Выберите файл для сохранения'
    folder: "file://" + pathToSave
    selectFolder: true
    selectMultiple: false
    width: 264
    height: 200
    visible: false
    onAccepted: {
        var filePath = fileToSaveDialog.fileUrl.toString()
        folderProbesPath = fileToSaveDialog.folder.toString()

        if (filePath.startsWith("file://") || folderProbesPath.startsWith("file://")) {
            var fileToSave = filePath.substring(7)
            if (fileNameFromDialog)
                if (!fileNameFromDialog.endsWith(".xml"))
                fileToSave = filePath.substring(7) + `/${fileNameFromDialog}.xml`
            folderProbesPath = folderProbesPath.substring(7)

        }

        if (typeMission) {
            settingsManager.setProbesPath(folderProbesPath)
            settingsManager.saveSettingsToFile("planets_settings.txt", typeMission);
            pathToSave = settingsManager.getPlanetsProbesPath()
            pathToLoad = settingsManager.getPlanetsProbesPath()
            settingsFolderProbesPath = pathToSave
            if (checkAction) {
                if (fileToSave) {
                    probes.saveProbe(listViewProbes.currentIndex, probeNameText.text, firstNumber.text, secondNumber.text, pythonCodeProperty, fileToSave)
                    probes.saveToXml(listViewProbes.currentIndex, planetsItems, missionIndex, fileToSave)
                } else {
                    probes.saveProbe(listViewProbes.currentIndex, probeNameText.text, firstNumber.text, secondNumber.text, pythonCodeProperty, folderProbesPath + `/${currentProbe.probeName}.xml`)
                    probes.saveToXml(listViewProbes.currentIndex, planetsItems, missionIndex, folderProbesPath + `/${currentProbe.probeName}.xml`)
                }
            }
        }
        else {
            settingsManager.setEarthProbesPath(folderProbesPath)
            settingsManager.saveSettingsToFile("earth_settings.txt", typeMission);
            earthPathToSave = settingsManager.getEarthProbesPath()
            earthPathToLoad = settingsManager.getEarthProbesPath()
            settingsFolderProbesPath = earthPathToLoad
        }



    }
}

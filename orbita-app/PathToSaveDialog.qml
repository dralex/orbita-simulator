import QtQuick.Dialogs 1.3
import QtQuick.Controls 2.5

FileDialog {
    id: fileToSaveDialog
    title: 'Выберите файл для сохранения'
    folder: typeMission ? "file://" + pathToSave : "file://" + earthPathToSave
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
            pathToSave = settingsManager.getPlanetsProbesPath()
            pathToLoad = settingsManager.getPlanetsProbesPath()
            if (!systems.size())
                systems.loadSystems((settingsManager.getEarthSystemsPath()));
            if (checkAction) {

                if (fileToSave) {
                    probes.saveProbe(listViewProbes.currentIndex, probeNameText.text, firstNumber.text, secondNumber.text, pythonCodeProperty, fileToSave)
                    probes.saveToXml(listViewProbes.currentIndex, planetsItems, missionIndex, fileToSave)
                } else {
                    probes.saveProbe(listViewProbes.currentIndex, probeNameText.text, firstNumber.text, secondNumber.text, pythonCodeProperty, folderProbesPath + `/${currentProbe.probeName}.xml`)
                    probes.saveToXml(listViewProbes.currentIndex, planetsItems, missionIndex, folderProbesPath + `/${currentProbe.probeName}.xml`)
                }
            } else {
                settingsManager.setProbesPath(folderProbesPath)
                settingsManager.saveSettingsToFile("planets_settings.txt", typeMission);
                settingsFolderProbesPath = pathToSave
            }
        }
        else {
            earthPathToLoad = settingsManager.getEarthProbesPath()
            earthPathToSave = settingsManager.getEarthProbesPath()
            if (!earthMissions.size())
                earthMissions.loadMissions(settingsManager.getMissionsPath());

            if (checkAction) {
                earthPathToSave = settingsManager.getEarthProbesPath()
                earthPathToLoad = settingsManager.getEarthProbesPath()
                if (fileToSave) {
                    earthProbes.saveEarthProbe(listViewEarthProbes.currentIndex, probeNameText.text, fuelTextInput.text, voltageTextInput.text,
                                               xz_yz_solar_id.text, xz_yz_radiator_id.text, xy_radiator_id.text);
                    earthProbes.saveEarthProbeToXml(listViewEarthProbes.currentIndex, earthMissions, earthMissionIndex, fileToSave)
                } else {
                    earthProbes.saveEarthProbe(listViewEarthProbes.currentIndex, probeNameText.text, fuelTextInput.text, voltageTextInput.text,
                                               xz_yz_solar_id.text, xz_yz_radiator_id.text, xy_radiator_id.text, folderProbesPath + `/${currentProbe.probeName}.xml`);
                    earthProbes.saveEarthProbeToXml(listViewEarthProbes.currentIndex, earthMissions, earthMissionIndex, folderProbesPath + `/${currentProbe.probeName}.xml`)

                }
            } else {
                settingsManager.setEarthProbesPath(folderProbesPath)
                settingsManager.saveSettingsToFile("earth_settings.txt", typeMission);
                settingsFolderProbesPath = earthPathToLoad
            }
        }



    }
}

import QtQuick.Dialogs 1.3
import QtQuick.Controls 2.5

FileDialog {
    id: calculatorFileDialog
    title: 'Выберите файл для сохранения'
    folder: "file://" + folderCalculatorPath
    selectFolder: true
    selectMultiple: false
    width: 264
    height: 200
    visible: false
    onAccepted: {
        var folderCalculator = calculatorFileDialog.folder.toString()
        if (folderCalculator.startsWith("file://")) {
        folderCalculator = folderCalculator.substring(7)
        }
        if (typeMission) {
            if (settingsManager.checkSimulationFile(folderCalculator + "/simulation.py") && folderCalculator.includes("planets_gravity")) {
                settingsManager.setPlanetsCalculatorPath(folderCalculator);
                folderCalculatorPath = settingsManager.getPlanetsCalculatorPath()
            } else {
                errorDialog.textOfError = "В данной директории отсутствуют файлы симулятора планет."
                errorDialog.open()
                folderCalculatorPath = "None"
                return;
            }
            settingsFolderCalculatorPath = folderCalculator
        } else {
            if (settingsManager.checkSimulationFile(folderCalculator + "/simulation.py") && folderCalculator.includes("earth_gravity")) {
                settingsManager.setEarthCalculatorPath(folderCalculator);
                earthFolderCalculatorPath = settingsManager.getPlanetsCalculatorPath()
            } else {
                errorDialog.textOfError = "В данной директории отсутствуют файлы симулятора Земли."
                errorDialog.open()
                folderCalculatorPath = "None"
                return;
            }
            settingsFolderCalculatorPath = folderCalculator
        }
    }
}

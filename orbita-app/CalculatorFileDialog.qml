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
        if (settingsManager.checkSimulationFile(folderCalculator + "/simulation.py")) {
            settingsManager.setPlanetsCalculatorPath(folderCalculator);
            folderCalculatorPath = settingsManager.getPlanetsCalculatorPath()
        } else {
            errorDialog.textOfError = "В данной директории отсутствуют файлы симулятора."
            errorDialog.open()
            folderSimulation = ""
        }
    }
}

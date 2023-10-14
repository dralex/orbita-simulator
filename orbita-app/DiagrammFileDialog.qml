import QtQuick.Dialogs 1.3

FileDialog {
    id: fileToLoadDialog
    title: 'Выберите файл для загрузки'
    selectFolder: false
    selectMultiple: false
    width: 264
    height: 146
    visible: false
    folder: shortcuts.home

    onAccepted: {
        var filePath = fileToLoadDialog.fileUrl.toString()
        var folderPath = fileToLoadDialog.folder.toString()

        if (filePath.startsWith("file://") || folderPath.startsWith("file://")) {
            var fileToLoad= filePath.substring(7)
        }

        earthProbes.appendDiagramm(listViewEarthProbes.currentIndex, diagrammSystemName, fileToLoad);
        diagrammSystemName = ""
    }
}

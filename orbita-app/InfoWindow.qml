import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Dialog  {
    id: infoWindow
    width: 264
    height: 146
    visible: false
    modal: true
    property string textOfInfo: ""
    title: qsTr("Подробная информация")
    x: parent.width / 2 - width / 2
    y: parent.height / 2 - height / 2

    ColumnLayout {
        anchors.fill: parent
        Text {
            height: parent.height - 23
            width: parent.width
            Layout.preferredHeight: height
            Layout.preferredWidth: width
            text: textOfInfo
            wrapMode: Text.WordWrap
        }

        Button {
            height: 23
            width: parent.width * 0.5
            Layout.preferredHeight: height
            Layout.preferredWidth: width
            text: "Закрыть"
            Layout.alignment: Qt.AlignRight
            onClicked: {
                textOfInfo = ""
                infoWindow.accepted()
                infoWindow.close()
            }
        }
    }

}

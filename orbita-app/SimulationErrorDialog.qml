import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

Dialog  {
    id: simulationErrorDialog
    width: 464
    height: 346
    visible: false
    modal: true
    property string textOfError: ""
    title: qsTr("Ошибка!")
    x: parent.width / 2 - width / 2
    y: parent.height / 2 - height / 2

    ColumnLayout {
        anchors.fill: parent

        ScrollView {
            width: parent.width
            height: parent.height - 23
            Layout.preferredWidth: width
            Layout.preferredHeight: height

            TextArea {
                id: missionInfo
                anchors.fill: parent
                readOnly: true
                text: textOfError
            }
        }
        Button {
            height: 23
            width: parent.width * 0.5
            Layout.preferredHeight: height
            Layout.preferredWidth: width
            text: "ОК"
            onClicked: {

                textOfError = ""
                simulationErrorDialog.accepted()
                simulationErrorDialog.close()
            }
        }
    }

}

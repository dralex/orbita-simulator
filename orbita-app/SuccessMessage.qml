import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

Dialog  {
    id: successDialog
    width: 264
    height: 146
    visible: false
    modal: true
    property string message: ""
    title: qsTr("Успешно!")
    x: parent.width / 2 - width / 2
    y: parent.height / 2 - height / 2

    ColumnLayout {
        anchors.fill: parent

        Text {
            height: parent.height - 23
            width: parent.width
            Layout.preferredHeight: height
            Layout.preferredWidth: width
            wrapMode: Text.WordWrap
            text: message
        }

        Button {
            height: 23
            width: parent.width * 0.5
            Layout.preferredHeight: height
            Layout.preferredWidth: width
            text: "ОК"
            onClicked: {


                successDialog.accepted()
                successDialog.close()
            }
        }
    }

}

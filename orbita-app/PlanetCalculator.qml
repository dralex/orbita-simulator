import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Window  {
    id: planetCalculatorWindow
    width: 819
    height: 610
    visible: true
    flags: Qt.Window | Qt.WindowFixedSize
    title: qsTr("Гравитационный кальулятор")
    RowLayout {
        anchors.fill: parent

        GroupBox {
            id: cParametrs
            title: qsTr("Параметры модели")
            width: 801
            height: 125
            Layout.preferredHeight: 125
            Layout.preferredWidth: 801

            GridLayout {
                columns: 6
                rows: 3


            }
        }
    }

}

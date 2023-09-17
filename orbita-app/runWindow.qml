import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Window  {
    width: 798
    height: 610
    visible: true
    flags: Qt.Window | Qt.WindowFixedSize

    ColumnLayout {
        anchors.fill: parent


        Text {
            Layout.preferredHeight: 20
            Layout.preferredWidth: parent.width
            Layout.topMargin: 5
            text: "<b>Аппарат:</b "
        }


        RowLayout {
           Layout.preferredHeight: 531
           Layout.preferredWidth: parent.width

           GroupBox {
               title: qsTr("Журнал полёта")
               Layout.preferredHeight: parent.height
               Layout.preferredWidth: parent.width * 0.5

               ColumnLayout {
                   anchors.fill: parent

                   Column {
                       Layout.preferredWidth: parent.width
                       Layout.preferredHeight: 15
                       Text {text: "Миссия: "}
                   }

                   TextField {
                       Layout.preferredWidth: parent.width
                       Layout.preferredHeight: 381
                       id: missionInfo
                       readOnly: true
                   }

                   Button {
                       Layout.preferredHeight: 23
                       Layout.preferredWidth: parent.width
                       id: startButton
                       text: "Cтарт!"


                   }
                   Button {
                       Layout.preferredHeight: 23
                       Layout.preferredWidth: parent.width
                       id: stopButton
                       text: "Остановить"

                   }
                   Button {
                       Layout.preferredHeight: 23
                       Layout.preferredWidth: parent.width
                       id: printButton
                       text: "Распечатать..."

                   }
               }

           }

           GroupBox {
               title: qsTr("Полный журнал полёта")
               Layout.preferredHeight: parent.height
               Layout.preferredWidth: parent.width * 0.5
               TextField {
                   anchors.fill: parent
                   id: missionFullInfo
                   readOnly: true
               }
           }
        }

          Button {
              id: closeButton
              Layout.preferredHeight: 23
              Layout.preferredWidth: 80
              Layout.alignment: Qt.AlignRight | Qt.AlignTop
              Layout.rightMargin: 5
              Layout.bottomMargin: 10
              text: "Закрыть"

          }


    }
}

#include "earthdevices.h"

EarthDevices::EarthDevices(QObject *parent)
    : QObject{parent}
{

}

void EarthDevices::loadDevices(const QString &filePath) {
    QFile file(filePath);

    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        qDebug() << "Не удалость открыть XML файл.";
        return;
    }

    QXmlStreamReader xmlReader(&file);

    while (!xmlReader.atEnd() && !xmlReader.hasError()) {
        xmlReader.readNext();
        if (xmlReader.name() == "choices") {
            while (!xmlReader.atEnd() && !xmlReader.hasError()) {
                xmlReader.readNext();

                if (xmlReader.isStartElement() && xmlReader.name() == "device") {
                    EarthDevicesItem devicesItemXml;

                    QXmlStreamAttributes attributes = xmlReader.attributes();
                    devicesItemXml.id = mItems.size();
                    devicesItemXml.deviceEngName = attributes.value("name").toString();
                    devicesItemXml.deviceName = attributes.value("full_name").toString();

                    while (!(xmlReader.isEndElement() && xmlReader.name() == "device")) {
                        xmlReader.readNext();

                        if (xmlReader.isStartElement()) {
                            if (xmlReader.name() == "mass") {
                                devicesItemXml.mass = xmlReader.readElementText().toDouble();
                            }
                        }
                    }

                    emit preEarthDeviceAppended();

                    mItems.append(devicesItemXml);

                    emit postEarthDeviceAppended();


                    while (!(xmlReader.isEndElement() && xmlReader.name() == "device")) {
                        xmlReader.readNext();
                    }
                } else if (xmlReader.isEndElement() && xmlReader.name() == "choices") {
                    break;
                }
            }

        }
    }

    if (xmlReader.hasError()) {
        qDebug() << "XML parsing error: " << xmlReader.errorString();
    }

    file.close();
}

void EarthDevices::showDevices()
{
    for (int i = 0; i < mItems.size(); ++i) {
        qDebug()<<"Названия:"<<mItems[i].deviceName;
        qDebug()<<"Масса:"<<mItems[i].mass;
    }
}

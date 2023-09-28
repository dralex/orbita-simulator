#include "earthdevices.h"

EarthDevices::EarthDevices(QObject *parent)
    : QObject{parent}
{

}

QVector<EarthDevicesItem> EarthDevices::items() const
{
    return mItems;
}

bool EarthDevices::setEarthDevices(int index, const EarthDevicesItem &item)
{
    if (index < 0 || index >= mItems.size())
        return false;

    const EarthDevicesItem &olditem = mItems.at(index);
    if (item.id == olditem.id)
        return false;

    mItems[index] = item;
    return true;
}

void EarthDevices::loadDevices(const QString &filePath) {
    QFile file(filePath);

    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        qDebug() << "Не удалось открыть XML файл.";
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
                            } else if (xmlReader.name() == "type") {
                                devicesItemXml.type = xmlReader.readElementText();
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

QString EarthDevices::getDeviceEngName(QString deviceName)
{
    for (int i = 0; i < mItems.size(); ++i) {
        if (mItems[i].deviceName == deviceName)
            return mItems[i].deviceEngName;
    }
    return "None";
}

QString EarthDevices::getType(QString deviceName)
{
    for (int i = 0; i < mItems.size(); ++i) {
        if (mItems[i].deviceName == deviceName)
            return mItems[i].type;
    }
    return "None";
}

double EarthDevices::getMass(QString deviceName)
{
    for (int i = 0; i < mItems.size(); ++i) {
        if (mItems[i].deviceName == deviceName)
            return mItems[i].mass;
    }
    return 0.0;
}

int EarthDevices::size()
{
    return mItems.size();
}

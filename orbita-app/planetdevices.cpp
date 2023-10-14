#include "planetdevices.h"

PlanetDevices::PlanetDevices(QObject *parent)
    : QObject{parent}
{
}



QVector<PlanetDeviceItems> PlanetDevices::items() const
{
    return mItems;
}

bool PlanetDevices::setPlanetDevices(int index, const PlanetDeviceItems &item)
{
    if (index < 0 || index >= mItems.size())
        return false;

    const PlanetDeviceItems &olditem = mItems.at(index);
    if (item.id == olditem.id)
        return false;

    mItems[index] = item;
    return true;
}

void PlanetDevices::loadDevices(const QString &filePath)
{
    QFile file(filePath);
    if (!file.open(QFile::ReadOnly | QFile::Text))
    {
        qDebug() << "Не удалось открыть файл устройств";
        return;
    }

    QXmlStreamReader xmlReader(&file);

    while (!xmlReader.atEnd() && !xmlReader.hasError())
    {
        QXmlStreamReader::TokenType token = xmlReader.readNext();

        if (token == QXmlStreamReader::StartElement && xmlReader.name() == "device")
        {
            PlanetDeviceItems device;
            device.id = mItems.size();
            device.deviceEngName = xmlReader.attributes().value("name").toString();
            device.deviceName = xmlReader.attributes().value("full_name").toString();
            device.deviceCode = xmlReader.attributes().value("code").toString();

            emit prePlanetDeviceAppended();

            mItems.append(device);

            emit postPlanetDeviceAppended();
        }
    }

    if (xmlReader.hasError())
        return;

    file.close();
}

int PlanetDevices::size()
{
    return mItems.size();
}

QString PlanetDevices::getDeviceCode(QString deviceName)
{
    for (int i = 0; i < mItems.size(); ++i) {
        if (mItems[i].deviceName == deviceName)
            return mItems[i].deviceCode;
    }
    return "None";
}

QString PlanetDevices::getDeviceEngName(QString deviceName)
{
    for (int i = 0; i < mItems.size(); ++i) {
        if (mItems[i].deviceName == deviceName)
            return mItems[i].deviceEngName;
    }
    return "None";
}

QString PlanetDevices::getDeviceName(QString deviceEngName)
{
    for (int i = 0; i < mItems.size(); ++i) {
        if (mItems[i].deviceEngName == deviceEngName)
            return mItems[i].deviceName;
    }
    return "None";
}

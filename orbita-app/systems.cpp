#include "systems.h"

Systems::Systems(QObject *parent)
    : QObject{parent}
{

}

QVector<EarthSystemItem> Systems::items() const
{
    return mItems;
}

bool Systems::setEarthSystems(int index, const EarthSystemItem &item)
{
    if (index < 0 || index >= mItems.size())
        return false;

    const EarthSystemItem &olditem = mItems.at(index);
    if (item.id == olditem.id)
        return false;

    mItems[index] = item;
    return true;
}

void Systems::loadSystems(const QString &filePath) {
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
                    EarthSystemItem devicesItemXml;

                    QXmlStreamAttributes attributes = xmlReader.attributes();
                    devicesItemXml.id = mItems.size();
                    devicesItemXml.systemEngName = attributes.value("name").toString();
                    devicesItemXml.systemName = attributes.value("full_name").toString();

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

                    emit preEarthSystemAppended();

                    mItems.append(devicesItemXml);

                    emit postEarthSystemAppended();

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


void Systems::showSystems()
{
    for (int i = 0; i < mItems.size(); ++i) {
        qDebug()<<"Названия:"<<mItems[i].systemName;
        qDebug()<<"Масса:"<<mItems[i].mass;
    }
}

QString Systems::getSystemsEngName(QString systemName)
{
    for (int i = 0; i < mItems.size(); ++i) {
        if (mItems[i].systemName == systemName)
            return mItems[i].systemEngName;
    }
    return "None";
}

QString Systems::getSystemNameByEng(QString systemEngName)
{
    for (int i = 0; i < mItems.size(); ++i) {
        if (mItems[i].systemEngName == systemEngName)
            return mItems[i].systemName;
    }
    return "None";
}

QString Systems::getType(QString systemName)
{
    for (int i = 0; i < mItems.size(); ++i) {
        if (mItems[i].systemName == systemName)
            return mItems[i].type;
    }
    return "None";
}

double Systems::getMass(QString systemName)
{
    for (int i = 0; i < mItems.size(); ++i) {
        if (mItems[i].systemName == systemName)
            return mItems[i].mass;
    }
    return 0.0;
}

int Systems::size()
{
    return mItems.size();
}

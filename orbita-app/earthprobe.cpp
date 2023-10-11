#include "earthprobe.h"

EarthProbe::EarthProbe(QObject *parent)
    : QObject{parent}
{

}

QVector<EarthProbeItem> EarthProbe::items() const
{
    return mItems;
}

bool EarthProbe::setEarthProbe(int index, const EarthProbeItem &item)
{
    if (index < 0 || index >= mItems.size())
        return false;

    const EarthProbeItem &olditem = mItems.at(index);
    if (item.probeNumber == olditem.probeNumber)
        return false;

    mItems[index] = item;
    return true;
}

void EarthProbe::appendEarthProbe(QString probeName, QString missionName, QString pythonCode, QString filePath)
{
    emit preEarthProbeAppended();

    mItems.append({mItems.size(), probeName, missionName, 0.0, 0.0, 0.0, 0.0, 0.0, {}, pythonCode, {}, filePath});

    emit postEarthProbeAppended();
}

void EarthProbe::appendEarthDevice(int probeIndex, QString systemEngName, QString systemName,  QString type, double mass, bool startMode)
{
    emit preEarthSystemAppended();

    mItems[probeIndex].systems.append({mItems[probeIndex].systems.size(), systemEngName, systemName, type, mass, startMode});

    emit postEarthSystemAppended();
}

void EarthProbe::removeEarthDevice(int probeIndex, int index)
{
    emit preEarthSystemRemoved(index);

    mItems[probeIndex].systems.removeAt(index);

    emit postEarthSystemRemoved();
}

void EarthProbe::saveEarthProbe(int probeIndex, QString probeName,  double fuel, double voltage,
                                double xz_yz_solar_panel_fraction, double xz_yz_radiator_fraction, double xy_radiator_fraction)
{
    mItems[probeIndex].probeName = probeName;
    mItems[probeIndex].fuel = fuel;
    mItems[probeIndex].voltage = voltage;
    mItems[probeIndex].xz_yz_solar_panel_fraction = xz_yz_solar_panel_fraction;
    mItems[probeIndex].xz_yz_radiator_fraction = xz_yz_radiator_fraction;
    mItems[probeIndex].xy_radiator_fraction = xy_radiator_fraction;
}

void EarthProbe::appendDiagramm(int probeIndex, QString systemEngName, QString path)
{
    mItems[probeIndex].diagrammPathes.append({mItems[probeIndex].diagrammPathes.size(), systemEngName, path});
}

void EarthProbe::removeDiagramm(int probeIndex, QString systemEngName)
{
    for (int i = 0; i < mItems[probeIndex].diagrammPathes.size(); ++i) {
        if (mItems[probeIndex].diagrammPathes[i].systemEngName == systemEngName)
            mItems[probeIndex].diagrammPathes.removeAt(i);
    }
}

int EarthProbe::size()
{
    return mItems.size();
}

void EarthProbe::saveEarthProbeToXml(int probeIndex, EarthMissions *missions, int missionIndex, const QString &filename)
{
    QFile file(filename);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text))
    {
        return;
    }

    EarthMissionsItem missionItem = missions->items()[missionIndex];

    QXmlStreamWriter xmlWriter(&file);
    xmlWriter.setAutoFormatting(true);

    xmlWriter.writeStartDocument();
    xmlWriter.writeStartElement("v:probe");

    xmlWriter.writeAttribute("name", mItems[probeIndex].probeName);
    xmlWriter.writeNamespace("venus", "v");

    xmlWriter.writeStartElement("flight");

    xmlWriter.writeTextElement("tournament", "tournament");

    xmlWriter.writeStartElement("planet");
    xmlWriter.writeAttribute("name", "Earth");
    xmlWriter.writeEndElement();

    xmlWriter.writeStartElement("time");
    xmlWriter.writeAttribute("start", "2015-01-01 00:00:00");
    xmlWriter.writeEndElement();

    xmlWriter.writeTextElement("T_start", "290.000000");


    xmlWriter.writeStartElement("mission");
    xmlWriter.writeAttribute("type", missionItem.missionEngName);

    xmlWriter.writeStartElement("control_stations");
    for (int i = 0; i < missionItem.controlStations.size(); ++i) {
        xmlWriter.writeStartElement("control_station");
        xmlWriter.writeAttribute("name", missionItem.controlStations[i].name);

        xmlWriter.writeTextElement("location_angle", generateDoubleData(missionItem.controlStations[i].fromToNumbers));

        xmlWriter.writeEndElement();
    }
    xmlWriter.writeEndElement();

    xmlWriter.writeEndElement();
    xmlWriter.writeTextElement("duration",  QString::number(missionItem.duration));

    if (missionItem.onewayMessages.size()) {
        for (int i = 0; i < missionItem.onewayMessages.size(); ++i) {
            xmlWriter.writeStartElement("oneway_message");

            xmlWriter.writeAttribute("text", generateRandomString());

            xmlWriter.writeEndElement();
        }
    }

    if (missionItem.message.number) {
        xmlWriter.writeStartElement("messages");
        QList<EarthMessage> elemMessages = generateRandomMessages(missionItem.controlStations.size());
        for (int i = 0; i < missionItem.message.number; ++i) {
            xmlWriter.writeStartElement("message");

            xmlWriter.writeAttribute("order", QString::number(i + 1));
            xmlWriter.writeAttribute("msgfrom", QString::number(elemMessages[i].msgfrom));
            xmlWriter.writeAttribute("msgto", QString::number(elemMessages[i].msgto));
            xmlWriter.writeAttribute("data", generateIntData(missionItem.message.data));
            xmlWriter.writeAttribute("duration", generateIntData(missionItem.message.timeout));

            xmlWriter.writeEndElement();
        }

        xmlWriter.writeEndElement();
    }

    if (missionItem.missiles.size()) {
        xmlWriter.writeStartElement("missiles");

        for (int i = 0; i < missionItem.missiles.size(); ++i) {
            xmlWriter.writeStartElement("missile");
            xmlWriter.writeAttribute("index", QString::number(missionItem.missiles[i].id + 1));

            xmlWriter.writeTextElement("location_angle",
                                       generateDoubleData(missionItem.missiles[i].locatonAngle));
            xmlWriter.writeTextElement("launch_time",
                                       generateIntData(missionItem.missiles[i].launchTime));
            xmlWriter.writeEndElement();
        }

        xmlWriter.writeEndElement();
    }

    if (missionItem.orbitData.size())
        xmlWriter.writeTextElement("orbit", generateIntData(missionItem.orbitData));

    if (missionItem.precision.size())
        xmlWriter.writeTextElement("precision", generateDoubleData(missionItem.precision));

    if (missionItem.resolution.size())
        xmlWriter.writeTextElement("resolution", generateDoubleData(missionItem.resolution));

    xmlWriter.writeTextElement("start_angular_velocity", "1.0");

    if (missionItem.targetOrbit.size())
      xmlWriter.writeTextElement("target_orbit", generateIntData(missionItem.targetOrbit));

    if (missionItem.targetAngle.size())
        xmlWriter.writeTextElement("target_angle", generateDoubleData(missionItem.targetAngle));


    xmlWriter.writeEndElement();

    xmlWriter.writeStartElement("construction");

    xmlWriter.writeTextElement("fuel", QString::number(mItems[probeIndex].fuel));
    xmlWriter.writeTextElement("voltage", QString::number(mItems[probeIndex].voltage));
    xmlWriter.writeTextElement("xz_yz_solar_panel_fraction", QString::number(mItems[probeIndex].xz_yz_solar_panel_fraction));
    xmlWriter.writeTextElement("xz_yz_radiator_fraction", QString::number(mItems[probeIndex].xz_yz_radiator_fraction));
    xmlWriter.writeTextElement("xy_radiator_fraction", QString::number(mItems[probeIndex].xy_radiator_fraction));

    xmlWriter.writeEndElement();

    xmlWriter.writeStartElement("systems");

    if (mItems[probeIndex].systems.size()) {
        for (const SystemItem &systems : mItems[probeIndex].systems)
        {
            xmlWriter.writeStartElement("system");
            xmlWriter.writeAttribute("name", QString(systems.systemEngName));
            if (systems.startMode)
                xmlWriter.writeAttribute("start_mode", "ON");
            if (mItems[probeIndex].diagrammPathes.size()) {
                for (int i = 0; i < mItems[probeIndex].diagrammPathes.size(); ++i) {
                    if (mItems[probeIndex].diagrammPathes[i].systemEngName == systems.systemEngName) {
                        xmlWriter.writeStartElement("hsm_diagram");
                        xmlWriter.writeAttribute("type", "yEd");
                        xmlWriter.writeAttribute("path", mItems[probeIndex].diagrammPathes[i].path);
                        xmlWriter.writeEndElement();
                    }
                }
            }
            xmlWriter.writeEndElement();
        }
    }


    xmlWriter.writeEndElement();

    if (!mItems[probeIndex].pythonCode.isEmpty()) {
        xmlWriter.writeStartElement("python_code");
        xmlWriter.writeCDATA("\n" + mItems[probeIndex].pythonCode + "\n");
        xmlWriter.writeEndElement();
    }

    xmlWriter.writeEndElement();
    xmlWriter.writeEndDocument();

    file.close();
}

void EarthProbe::loadEarthProbeFromXml(const QString &path, Systems *systems, EarthMissions *missions) {
    QFile file(path);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        qDebug() << "Не удалось открыть XML файл для чтения: " << file.errorString();
        return;
    }

    QXmlStreamReader xmlReader(&file);

    EarthProbeItem probeItem;
    QVector<DiagrammPathes> diagrammPathes;
    QString pythonCode;
    QVector<SystemItem> systemsItems;

    while (!xmlReader.atEnd() && !xmlReader.hasError()) {
        xmlReader.readNext();

        if (xmlReader.isStartElement()) {
            QString elementName = xmlReader.name().toString();

            if (elementName == "probe") {
                probeItem.probeName = xmlReader.attributes().value("name").toString();
            } else if (elementName == "mission") {
                probeItem.missionName = missions->getMissionName(xmlReader.attributes().value("type").toString());
            } else if (elementName == "construction") {
                while (!(xmlReader.isEndElement() && xmlReader.name() == "construction")) {
                    xmlReader.readNext();

                    if (xmlReader.isStartElement()) {
                        if (xmlReader.name() == "fuel") {
                            probeItem.fuel = xmlReader.readElementText().toDouble();
                        } else if (xmlReader.name() == "voltage") {
                            probeItem.voltage = xmlReader.readElementText().toDouble();
                        } else if (xmlReader.name() == "xz_yz_solar_panel_fraction") {
                            probeItem.xz_yz_solar_panel_fraction = xmlReader.readElementText().toDouble();
                        } else if (xmlReader.name() == "xz_yz_radiator_fraction") {
                            probeItem.xz_yz_radiator_fraction = xmlReader.readElementText().toDouble();
                        } else if (xmlReader.name() == "xy_radiator_fraction") {
                            probeItem.xy_radiator_fraction = xmlReader.readElementText().toDouble();
                        }
                    }
                }
            } else if (elementName == "systems") {
                while (!(xmlReader.isEndElement() && xmlReader.name() == "systems")) {
                    xmlReader.readNext();

                    if (xmlReader.isStartElement() && xmlReader.name() == "system") {
                        SystemItem systemItem;

                        QXmlStreamAttributes attributes = xmlReader.attributes();
                        systemItem.systemEngName = attributes.value("name").toString();
                        systemItem.systemName = systems->getSystemNameByEng(systemItem.systemEngName);
                        systemItem.type = systems->getType(systemItem.systemName);
                        systemItem.mass = systems->getMass(systemItem.systemName);

                        if (attributes.value("start_mode").toString() == "ON")
                            systemItem.startMode = true;
                        else
                            systemItem.startMode = false;

                        systemsItems.append(systemItem);

                        while (!(xmlReader.isEndElement() && xmlReader.name() == "system")) {
                            xmlReader.readNext();
                            if (xmlReader.isCDATA()) {
                                pythonCode = xmlReader.text().toString();
                            }
                        }
                    }
                }
            }
        }
    }

    if (xmlReader.hasError()) {
        qDebug() << "Ошибка при разборе XML файла: " << xmlReader.errorString();
    }

    file.close();

    probeItem.diagrammPathes = diagrammPathes;
    probeItem.pythonCode = pythonCode;
    probeItem.filePath = path;
    probeItem.probeNumber = mItems.size();

    emit preEarthProbeAppended();

    mItems.append(probeItem);
    mItems[probeItem.probeNumber].systems = systemsItems;

    emit postEarthProbeAppended();
}

QString EarthProbe::generateIntData(QVector<int> data) {
    int fromValue = data[0];
    int toValue = data[1];

    return QString::number(QRandomGenerator::global()->generate() % (static_cast<qint64>(toValue) - static_cast<qint64>(fromValue) + 1) + static_cast<qint64>(fromValue)) + ".000000";
}

QString EarthProbe::generateDoubleData(QVector<double> data) {
    double fromValue = data[0];
    double toValue = data[1];

    double randomValue = QRandomGenerator::global()->generateDouble();
    double scaledValue = randomValue * (toValue - fromValue) + fromValue;

    scaledValue = qRound(scaledValue * 1e6) / 1e6;

    return QString::number(scaledValue);
}



QString EarthProbe::generateRandomString()
{
    QRandomGenerator::securelySeeded();
    int length = QRandomGenerator::global()->bounded(23, 28);

    QString randomString;
    for (int i = 0; i < length; ++i) {
        int choice = QRandomGenerator::global()->bounded(3);

        if (choice == 0) {
            QChar randomChar = QChar('a' + QRandomGenerator::global()->bounded(26));
            randomString.append(randomChar);
        } else if (choice == 1) {
            QChar randomChar = QChar('A' + QRandomGenerator::global()->bounded(26));
            randomString.append(randomChar);
        } else {
            QChar randomChar = QChar('0' + QRandomGenerator::global()->bounded(10));
            randomString.append(randomChar);
        }
    }

    return randomString;
}


QList<EarthMessage> EarthProbe::generateRandomMessages(int stationCount)
{
    QList<EarthMessage> messages;
    QRandomGenerator::securelySeeded();

    QList<int> stations;
    for (int i = 0; i <= stationCount; ++i) {
        stations.append(i);
    }

    for (int i = 0; i < 5; ++i) {
        int msgfromIndex = QRandomGenerator::global()->bounded(stations.size());
        int msgfrom = stations[msgfromIndex];
        stations.removeAt(msgfromIndex);

        int msgtoIndex = QRandomGenerator::global()->bounded(stations.size());
        int msgto = stations[msgtoIndex];
        stations.removeAt(msgtoIndex);

        EarthMessage message;
        message.msgfrom = msgfrom;
        message.msgto = msgto;

        messages.append(message);
    }

    return messages;
}


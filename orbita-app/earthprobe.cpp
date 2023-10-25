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

    mItems[probeIndex].systems.append({mItems[probeIndex].systems.size(), systemEngName, systemName, type, mass, startMode, ""});

    emit postEarthSystemAppended();
}

void EarthProbe::removeEarthDevice(int probeIndex, int index)
{
    emit preEarthSystemRemoved(index);

    mItems[probeIndex].systems.removeAt(index);

    emit postEarthSystemRemoved();
}

void EarthProbe::saveEarthProbe(int probeIndex, QString probeName,  double fuel, double voltage,
                                double xz_yz_solar_panel_fraction, double xz_yz_radiator_fraction, double xy_radiator_fraction,
                                QString filePath)
{
    mItems[probeIndex].probeName = probeName;
    mItems[probeIndex].fuel = fuel;
    mItems[probeIndex].voltage = voltage;
    mItems[probeIndex].xz_yz_solar_panel_fraction = xz_yz_solar_panel_fraction;
    mItems[probeIndex].xz_yz_radiator_fraction = xz_yz_radiator_fraction;
    mItems[probeIndex].xy_radiator_fraction = xy_radiator_fraction;
    mItems[probeIndex].filePath = filePath;
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

void EarthProbe::saveEarthProbeToXml(int probeIndex, EarthMissions *missions,
                                     Systems *earthSystems, int missionIndex, const QString &filename) {
    EarthMissionsItem missionItem = missions->items()[missionIndex];
    QFile file(filename);
    bool isNewFile = true;

    QString missionType;
    QString onewayMessageText = "";
    QVector<StationData> controlStationsData;
    QVector<MessageData> messagesData;
    QVector<MissileData> missilesData;
    int missionDuration = 0;
    double missionPrecision = 0;
    int missionOrbit = 0;
    int missionResolution = 0;
    double missionTargetOrbit = 0;
    double missionTargetAngle = 0;

    if (file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        isNewFile = false;
        QXmlStreamReader xmlReader(&file);

        while (!xmlReader.atEnd() && !xmlReader.hasError()) {
            xmlReader.readNext();

            if (xmlReader.isStartElement() && xmlReader.name() == "mission") {
                missionType = xmlReader.attributes().value("type").toString();
            } else if (xmlReader.isStartElement()) {
                QString elementName = xmlReader.name().toString();
                if (elementName == "control_station") {
                    StationData station;
                    station.name = xmlReader.attributes().value("name").toString();
                    while (!(xmlReader.isEndElement() && xmlReader.name() == "control_station")) {
                        xmlReader.readNext();
                        if (xmlReader.isStartElement()) {
                            QString innerElementName = xmlReader.name().toString();
                            if (innerElementName == "location_angle") {
                                station.locationAngle = xmlReader.readElementText().toDouble();
                            }
                        }
                    }
                    controlStationsData.append(station);
                } else if (elementName == "duration") {
                    missionDuration = xmlReader.readElementText().toInt();
                } else if (elementName == "orbit") {
                    missionOrbit = xmlReader.readElementText().toDouble();
                } else if (elementName == "resolution") {
                    missionResolution = xmlReader.readElementText().toDouble();
                } else if (elementName == "target_orbit") {
                    missionTargetOrbit = xmlReader.readElementText().toDouble();
                } else if (elementName == "target_angle") {
                    missionTargetAngle = xmlReader.readElementText().toDouble();
                } else if (elementName == "missile") {
                    MissileData missile;
                    missile.index = xmlReader.attributes().value("index").toInt();
                    while (!(xmlReader.isEndElement() && xmlReader.name() == "missile")) {
                        xmlReader.readNext();
                        if (xmlReader.isStartElement()) {
                            QString missileElementName = xmlReader.name().toString();
                            if (missileElementName == "location_angle") {
                                missile.locationAngle = xmlReader.readElementText().toDouble();
                            } else if (missileElementName == "launch_time") {
                                missile.launchTime = xmlReader.readElementText().toDouble();
                            }
                        }
                    }
                    missilesData.append(missile);
                } else if (elementName == "messages") {
                    while (!(xmlReader.isEndElement() && xmlReader.name() == "messages")) {
                        xmlReader.readNext();
                        if (xmlReader.isStartElement() && xmlReader.name() == "message") {
                            MessageData message;
                            message.order = xmlReader.attributes().value("order").toInt();
                            message.msgFrom = xmlReader.attributes().value("msgfrom").toInt();
                            message.msgTo = xmlReader.attributes().value("msgto").toInt();
                            message.data = xmlReader.attributes().value("data").toDouble();
                            message.duration = xmlReader.attributes().value("duration").toDouble();
                            messagesData.append(message);
                        }
                    }
                } else if (elementName == "precision") {
                    missionPrecision = xmlReader.readElementText().toDouble();
                }
            }
        }
        file.close();
    }

    if (file.open(QIODevice::WriteOnly | QIODevice::Text)) {
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

        if (isNewFile) {
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
        } else {
            xmlWriter.writeStartElement("mission");
            xmlWriter.writeAttribute("type", missionItem.missionEngName);

            xmlWriter.writeStartElement("control_stations");
            for (int i = 0; i < controlStationsData.size(); ++i) {
                xmlWriter.writeStartElement("control_station");
                xmlWriter.writeAttribute("name", controlStationsData[i].name);

                xmlWriter.writeTextElement("location_angle", QString::number(controlStationsData[i].locationAngle));

                xmlWriter.writeEndElement();
            }
            xmlWriter.writeEndElement();

            xmlWriter.writeEndElement();
            xmlWriter.writeTextElement("duration",  QString::number(missionDuration));

            if (onewayMessageText.length()) {
                xmlWriter.writeStartElement("oneway_message");
                xmlWriter.writeAttribute("text", onewayMessageText);
                xmlWriter.writeEndElement();
            }

            if (messagesData.size()) {
                xmlWriter.writeStartElement("messages");
                for (int i = 0; i < messagesData.size(); ++i) {
                    xmlWriter.writeStartElement("message");

                    xmlWriter.writeAttribute("order", QString::number(messagesData[i].order));
                    xmlWriter.writeAttribute("msgfrom", QString::number(messagesData[i].msgFrom));
                    xmlWriter.writeAttribute("msgto", QString::number(messagesData[i].msgTo));
                    xmlWriter.writeAttribute("data", QString::number(messagesData[i].data));
                    xmlWriter.writeAttribute("duration", QString::number(messagesData[i].duration));

                    xmlWriter.writeEndElement();
                }

                xmlWriter.writeEndElement();
            }

            if (missilesData.size()) {
                xmlWriter.writeStartElement("missiles");

                for (int i = 0; i < missilesData.size(); ++i) {
                    xmlWriter.writeStartElement("missile");
                    xmlWriter.writeAttribute("index", QString::number(missilesData[i].index));

                    xmlWriter.writeTextElement("location_angle", QString::number(missilesData[i].locationAngle));
                    xmlWriter.writeTextElement("launch_time", QString::number(missilesData[i].launchTime));
                    xmlWriter.writeEndElement();
                }

                xmlWriter.writeEndElement();
            }

            if (missionOrbit)
                xmlWriter.writeTextElement("orbit", QString::number(missionOrbit));

            if (missionPrecision)
                xmlWriter.writeTextElement("precision", QString::number(missionPrecision));

            if (missionResolution)
                xmlWriter.writeTextElement("resolution", QString::number(missionResolution));

            xmlWriter.writeTextElement("start_angular_velocity", "1.0");

            if (missionTargetOrbit)
              xmlWriter.writeTextElement("target_orbit", QString::number(missionTargetOrbit));

            if (missionTargetAngle)
                xmlWriter.writeTextElement("target_angle", QString::number(missionTargetAngle));


            xmlWriter.writeEndElement();
        }

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
                if (systems.startMode && earthSystems->getAllowState(systems.systemName))
                    xmlWriter.writeAttribute("start_mode", "ON");
                else if (!systems.startMode && earthSystems->getAllowState(systems.systemName))
                    xmlWriter.writeAttribute("start_mode", "OFF");

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

    }
    file.close();
}

void EarthProbe::loadEarthProbeFromXml(const QString &path, Systems *systems, EarthMissions *missions,
                                       SettingsManager *settingsManager) {
    QString probeFilename = path;
    QFile file(path);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        QString errorMessage =  "Не удалось открыть XML файл для чтения: " + file.errorString();
        emit errorOccurred(errorMessage);
        return;
    }

//    QXmlSchema schema;
//    schema.load(settingsManager->getEarthSimulationPath() + "/xml-schemas/probe.xsd");
//    if(!schema.isValid()) {
//        qDebug()<<"Плохой файл xml-схемы аппарата";
//        return;
//    }

//    QXmlSchemaValidator validator(schema);
//    if(!validator.validate(settingsManager->getEarthSimulationPath() + "/xml-schemas/probe.xsd")) {
//        qDebug() << "Файл аппарата " << path << " не соответствует схеме";
//        return;
//    }


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
                            if (xmlReader.isStartElement() && xmlReader.name() == "hsm_diagram")
                                diagrammPathes.append({diagrammPathes.size(), systemItem.systemEngName, xmlReader.attributes().value("path").toString()});
                            else if (xmlReader.isCDATA())
                                pythonCode = xmlReader.text().toString();
                        }
                    }
                }
            }
        }
    }

    if (xmlReader.hasError()) {
        QString errorMessage = "Ошибка при разборе XML файла: " + xmlReader.errorString();
        emit errorOccurred(errorMessage);
        return;
    }

    file.close();

    probeItem.diagrammPathes = diagrammPathes;
    probeItem.pythonCode = pythonCode;
    if (path.contains("earth_probes_templates")) {
        probeFilename = "";
    }
    probeItem.filePath = probeFilename;
    probeItem.probeNumber = mItems.size();
    probeItem.systems = systemsItems;

    for (int i = 0; i < probeItem.systems.size(); ++i) {
        for (int j = 0; j < probeItem.diagrammPathes.size(); ++j) {
            if (probeItem.diagrammPathes[j].systemEngName == probeItem.systems[i].systemEngName) {
                probeItem.systems[i].diagramPath = probeItem.diagrammPathes[j].path;
                break;
            }
        }
    }
    emit preEarthProbeAppended();

    mItems.append(probeItem);

    emit postEarthProbeAppended();
}

bool EarthProbe::checkFileChanges(Systems *systems, int probeIndex)
{
    QFile file(mItems[probeIndex].filePath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        QString errorMessage =  "Не удалось открыть XML файл для чтения: " + file.errorString();
        emit errorOccurred(errorMessage);
        return 0;
    }

    QXmlStreamReader xmlReader(&file);

    QVector<DiagrammPathes> diagrammPathes;
    QString pythonCode;
    QVector<SystemItem> systemsItems;

    while (!xmlReader.atEnd() && !xmlReader.hasError()) {
        xmlReader.readNext();

        if (xmlReader.isStartElement()) {
            QString elementName = xmlReader.name().toString();

            if (elementName == "probe") {

                if (xmlReader.attributes().value("name").toString() != mItems[probeIndex].probeName) {
                    file.close();
                    return false;
                }
            } else if (elementName == "construction") {
                while (!(xmlReader.isEndElement() && xmlReader.name() == "construction")) {
                    xmlReader.readNext();

                    if (xmlReader.isStartElement()) {
                        if (xmlReader.name() == "fuel") {

                            if (xmlReader.readElementText().toDouble() != mItems[probeIndex].fuel) {
                                file.close();
                                return false;
                            }
                        } else if (xmlReader.name() == "voltage") {
                            if (xmlReader.readElementText().toDouble() != mItems[probeIndex].voltage) {
                                file.close();
                                return false;
                            }
                        } else if (xmlReader.name() == "xz_yz_solar_panel_fraction") {

                            if (xmlReader.readElementText().toDouble() != mItems[probeIndex].xz_yz_solar_panel_fraction) {
                                file.close();
                                return false;
                            }
                        } else if (xmlReader.name() == "xz_yz_radiator_fraction") {
                            if (xmlReader.readElementText().toDouble() != mItems[probeIndex].xz_yz_radiator_fraction) {
                                file.close();
                                return false;
                            }
                        } else if (xmlReader.name() == "xy_radiator_fraction") {
                            if (xmlReader.readElementText().toDouble() != mItems[probeIndex].xy_radiator_fraction) {
                                file.close();
                                return false;
                            }
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
                            if (xmlReader.isStartElement() && xmlReader.name() == "hsm_diagram")
                                diagrammPathes.append({diagrammPathes.size(), systemItem.systemEngName, xmlReader.attributes().value("path").toString()});
                            else if (xmlReader.isCDATA())
                                if (mItems[probeIndex].pythonCode != xmlReader.text().toString()) {
                                    file.close();
                                    return false;
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

    if (mItems[probeIndex].systems.size() != systemsItems.size()) {
        return false;
    } else {
        for (int i = 0; i < mItems[probeIndex].systems.size(); ++i) {
            if (mItems[probeIndex].systems.size()) {
                if (mItems[probeIndex].systems[i].systemEngName != systemsItems[i].systemEngName ||
                    mItems[probeIndex].systems[i].systemName != systemsItems[i].systemName ||
                    mItems[probeIndex].systems[i].type != systemsItems[i].type ||
                    mItems[probeIndex].systems[i].mass != systemsItems[i].mass ||
                    mItems[probeIndex].systems[i].startMode != systemsItems[i].startMode) {
                    return false;
                }
            }
        }
    }

    if (mItems[probeIndex].diagrammPathes.size() != diagrammPathes.size()) {
        return false;
    } else {
        if (mItems[probeIndex].diagrammPathes.size()) {
            for (int i = 0; i < mItems[probeIndex].diagrammPathes.size(); ++i) {
                if (mItems[probeIndex].diagrammPathes[i].systemEngName != diagrammPathes[i].systemEngName ||
                    mItems[probeIndex].diagrammPathes[i].path != diagrammPathes[i].path) {
                    return false;
                }
            }
        }
    }


    return true;
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


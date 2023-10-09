#include "earthmissions.h"

EarthMissions::EarthMissions(QObject *parent)
    : QObject{parent}
{

}

QVector<EarthMissionsItem> EarthMissions::items() const
{
    return mItems;
}

bool EarthMissions::setMissions(int index, const EarthMissionsItem &item)
{
    if (index < 0 || index >= mItems.size())
        return false;

    const EarthMissionsItem &olditem = mItems.at(index);
    if (item.id == olditem.id)
        return false;

    mItems[index] = item;
    return true;
}

void EarthMissions::loadMissions(const QString &filePath) {
    QFile file(filePath);

    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        qDebug() << "Не удалось открыть XML файл.";
        return;
    }

    QXmlStreamReader xmlReader(&file);
    EarthMissionsItem missionItem;
    while (!xmlReader.atEnd() && !xmlReader.hasError()) {
        xmlReader.readNext();

        if (xmlReader.isStartElement() && xmlReader.name() == "mission") {
            missionItem = {};
            QXmlStreamAttributes attributes = xmlReader.attributes();
            missionItem.id = mItems.size();
            missionItem.missionEngName = attributes.value("name").toString();
            missionItem.missionName = attributes.value("full_name").toString();
            missionItem.duration = attributes.value("duration").toDouble();

            while (!(xmlReader.isEndElement() && xmlReader.name() == "description")) {
                xmlReader.readNext();
                if (xmlReader.isCharacters()) {
                    missionItem.missionDescription = xmlReader.text().toString();
                }
            }

            while (!(xmlReader.isEndElement() && xmlReader.name() == "generator")) {
                xmlReader.readNext();
                if (xmlReader.isStartElement()) {
                    if (xmlReader.name() == "control_stations") {
                        QVector<ControlStations> controlStationsData;

                        while (!(xmlReader.isEndElement() && xmlReader.name() == "control_stations")) {
                            xmlReader.readNext();
                            if (xmlReader.isStartElement() && xmlReader.name() == "control_station") {
                                ControlStations controlStation;
                                QXmlStreamAttributes controlStationAttributes = xmlReader.attributes();
                                controlStation.id = controlStationsData.size();
                                controlStation.name = controlStationAttributes.value("name").toString();

                                while (!(xmlReader.isEndElement() && xmlReader.name() == "control_station")) {
                                    xmlReader.readNext();
                                    if (xmlReader.isStartElement()) {
                                        if (xmlReader.name() == "location_angle") {
                                            QVector<double> locationAngleData;

                                            while (!(xmlReader.isEndElement() && xmlReader.name() == "location_angle")) {
                                                xmlReader.readNext();
                                                if (xmlReader.isStartElement() && xmlReader.name() == "frm") {
                                                    xmlReader.readNext();
                                                    locationAngleData.append(xmlReader.text().toDouble());
                                                } else if (xmlReader.isStartElement() && xmlReader.name() == "to") {
                                                    xmlReader.readNext();
                                                    locationAngleData.append(xmlReader.text().toDouble());
                                                }
                                            }

                                            controlStation.fromToNumbers = locationAngleData;
                                        }
                                    }
                                }

                                controlStationsData.append(controlStation);
                            }
                        }
                        missionItem.controlStations = controlStationsData;
                        controlStationsData.clear();

                    } else if (xmlReader.name() == "orbit") {
                        QVector<int> orbitData;
                        while (!(xmlReader.isEndElement() && xmlReader.name() == "orbit")) {
                            xmlReader.readNext();
                            if (xmlReader.isStartElement() && xmlReader.name() == "frm") {
                                xmlReader.readNext();
                                orbitData.append(xmlReader.text().toDouble());
                            } else if (xmlReader.isStartElement() && xmlReader.name() == "to") {
                                xmlReader.readNext();
                                orbitData.append(xmlReader.text().toDouble());
                            }
                        }
                      missionItem.orbitData = orbitData;
                      orbitData.clear();
                    } else if (xmlReader.name() == "precision") {
                        QVector<double> precision;
                        while (!(xmlReader.isEndElement() && xmlReader.name() == "precision")) {
                            xmlReader.readNext();
                            if (xmlReader.isStartElement() && xmlReader.name() == "frm") {
                                xmlReader.readNext();
                                precision.append(xmlReader.text().toDouble());
                            } else if (xmlReader.isStartElement() && xmlReader.name() == "to") {
                                xmlReader.readNext();
                                precision.append(xmlReader.text().toDouble());
                            }
                        }
                        missionItem.precision = precision;
                        precision.clear();
                    } else if (xmlReader.name() == "resolution") {
                        QVector<double> resolutionData;
                        while (!(xmlReader.isEndElement() && xmlReader.name() == "resolution")) {
                            xmlReader.readNext();
                            if (xmlReader.isStartElement() && xmlReader.name() == "frm") {
                                xmlReader.readNext();
                                resolutionData.append(xmlReader.text().toDouble());
                            } else if (xmlReader.isStartElement() && xmlReader.name() == "to") {
                                xmlReader.readNext();
                                resolutionData.append(xmlReader.text().toDouble());
                            }
                        }
                        missionItem.resolution = resolutionData;
                        resolutionData.clear();
                    } else if (xmlReader.name() == "target") {
                        QVector<int> targetOrbit;
                        QVector<double> targetAngle;

                        while (!(xmlReader.isEndElement() && xmlReader.name() == "target")) {
                            xmlReader.readNext();

                            if (xmlReader.isStartElement()) {
                                if (xmlReader.name() == "orbit") {
                                    while (!(xmlReader.isEndElement() && xmlReader.name() == "orbit")) {
                                        xmlReader.readNext();

                                        if (xmlReader.isStartElement()) {
                                            if (xmlReader.name() == "frm") {
                                                xmlReader.readNext();
                                                targetOrbit.append(xmlReader.text().toDouble());
                                            } else if (xmlReader.name() == "to") {
                                                xmlReader.readNext();
                                                targetOrbit.append(xmlReader.text().toDouble());
                                            }
                                        }
                                    }
                                } else if (xmlReader.name() == "location_angle") {
                                    while (!(xmlReader.isEndElement() && xmlReader.name() == "location_angle")) {
                                        xmlReader.readNext();

                                        if (xmlReader.isStartElement()) {
                                            if (xmlReader.name() == "frm") {
                                                xmlReader.readNext();
                                                targetAngle.append(xmlReader.text().toDouble());
                                            } else if (xmlReader.name() == "to") {
                                                xmlReader.readNext();
                                                targetAngle.append(xmlReader.text().toDouble());
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        missionItem.targetOrbit = targetOrbit;
                        missionItem.targetAngle = targetAngle;
                        targetOrbit.clear();
                        targetAngle.clear();
                    } else if (xmlReader.name() == "oneway_message") {
                        QVector<OnewayMessage> onewayMessages;

                        while (!(xmlReader.isEndElement() && xmlReader.name() == "oneway_message")) {
                            xmlReader.readNext();
                            if (xmlReader.isStartElement() && xmlReader.name() == "length") {
                                QVector<double> onewayMessageData;

                                while (!(xmlReader.isEndElement() && xmlReader.name() == "length")) {
                                    xmlReader.readNext();
                                    if (xmlReader.isStartElement() && xmlReader.name() == "frm") {
                                        xmlReader.readNext();
                                        onewayMessageData.append(xmlReader.text().toDouble());
                                    } else if (xmlReader.isStartElement() && xmlReader.name() == "to") {
                                        xmlReader.readNext();
                                        onewayMessageData.append(xmlReader.text().toDouble());
                                    }
                                }

                                onewayMessages.append({onewayMessages.size(), onewayMessageData});
                            }
                        }

                        missionItem.onewayMessages = onewayMessages;
                        onewayMessages.clear();
                    } else if (xmlReader.name() == "messages") {
                        Message message;
                        int number = xmlReader.attributes().value("number").toInt();

                        while (!(xmlReader.isEndElement() && xmlReader.name() == "messages")) {
                            xmlReader.readNext();

                            if (xmlReader.isStartElement()) {
                                QString elementName = xmlReader.name().toString();

                                if (elementName == "data") {
                                    while (!(xmlReader.isEndElement() && xmlReader.name() == "data")) {
                                        xmlReader.readNext();
                                        if (xmlReader.isStartElement()) {
                                            if (xmlReader.name() == "frm") {
                                                message.data.append(xmlReader.readElementText().toDouble());
                                            } else if (xmlReader.name() == "to") {
                                                message.data.append(xmlReader.readElementText().toDouble());
                                            }
                                        }
                                    }
                                } else if (elementName == "timeout") {
                                    while (!(xmlReader.isEndElement() && xmlReader.name() == "timeout")) {
                                        xmlReader.readNext();
                                        if (xmlReader.isStartElement()) {
                                            if (xmlReader.name() == "frm") {
                                                message.timeout.append(xmlReader.readElementText().toDouble());
                                            } else if (xmlReader.name() == "to") {
                                                message.timeout.append(xmlReader.readElementText().toDouble());
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        message.number = number;
                        missionItem.message = message;
                    } else if (xmlReader.name() == "missiles") {
                        QVector<Missiles> missiles;
                        int number = xmlReader.attributes().value("number").toInt();

                        while (!(xmlReader.isEndElement() && xmlReader.name() == "missiles")) {
                            xmlReader.readNext();

                            if (xmlReader.isStartElement()) {
                                if (xmlReader.name() == "location_angle") {
                                    double fromLA = 0.0, toLA = 0.0;
                                    int fromLT = 0, toLT = 0, cooldown = 0
;

                                    while (!(xmlReader.isEndElement() && xmlReader.name() == "location_angle")) {
                                        xmlReader.readNext();

                                        if (xmlReader.isStartElement()) {
                                            if (xmlReader.name() == "frm") {
                                                xmlReader.readNext();
                                                fromLA = xmlReader.text().toDouble();
                                            } else if (xmlReader.name() == "to") {
                                                xmlReader.readNext();
                                                toLA = xmlReader.text().toDouble();
                                            }
                                        }
                                    }

                                    xmlReader.readNext();
                                    if (xmlReader.name() == "launch_time") {
                                        while (!(xmlReader.isEndElement() && xmlReader.name() == "launch_time")) {
                                            xmlReader.readNext();

                                            if (xmlReader.isStartElement()) {
                                                if (xmlReader.name() == "frm") {
                                                    xmlReader.readNext();
                                                    fromLT = xmlReader.text().toDouble();
                                                } else if (xmlReader.name() == "to") {
                                                    xmlReader.readNext();
                                                    toLT = xmlReader.text().toDouble();
                                                }
                                            }
                                        }
                                    }

                                    xmlReader.readNext();
                                    if (xmlReader.name() == "cooldown") {
                                        xmlReader.readNext();
                                        cooldown = xmlReader.text().toInt();
                                    }

                                    missiles.append({missiles.size(), number, {fromLA, toLA}, {fromLT, toLT}, cooldown});
                                }
                            }
                        }

                        missionItem.missiles = missiles;
                        missiles.clear();
                    }
                }
            }




            emit preEarthMissionsItemAppended();

            mItems.append(missionItem);

            emit postEarthMissionsItemAppended();
        }
    }

    if (xmlReader.hasError()) {
        qDebug() << "Ошибка чтения XML файла: " << xmlReader.errorString();
    }

    file.close();
}


QString EarthMissions::getMissionEngName(QString missionName)
{
    for (int i = 0; i < mItems.size(); ++i)
        if (mItems[i].missionName == missionName)
            return mItems[i].missionEngName;

    return "None";
}
int EarthMissions::size()
{
    return mItems.size();
}

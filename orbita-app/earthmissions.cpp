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
                        QVector<double> orbitData;
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
                        QVector<double> targetOrbit;
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
                        QVector<Messages> messages;
                        int number = xmlReader.attributes().value("number").toInt();
                        while (!(xmlReader.isEndElement() && xmlReader.name() == "messages")) {
                            xmlReader.readNext();

                            if (xmlReader.isStartElement() && xmlReader.name() == "data") {
                                double fromData = 0.0, toData = 0.0, fromTimeout = 0.0, toTimeout = 0.0;
                                int msgto = 0, msgfrom = 0;

                                while (!(xmlReader.isEndElement() && xmlReader.name() == "data")) {
                                    xmlReader.readNext();
                                    if (xmlReader.isStartElement() && xmlReader.name() == "frm") {
                                        xmlReader.readNext();
                                        fromData = xmlReader.text().toDouble();
                                    } else if (xmlReader.isStartElement() && xmlReader.name() == "to") {
                                        xmlReader.readNext();
                                        toData = xmlReader.text().toDouble();
                                    }
                                }

                                xmlReader.readNext();
                                if (xmlReader.name() == "timeout") {
                                    while (!(xmlReader.isEndElement() && xmlReader.name() == "timeout")) {
                                        xmlReader.readNext();
                                        if (xmlReader.isStartElement() && xmlReader.name() == "frm") {
                                            xmlReader.readNext();
                                            fromTimeout = xmlReader.text().toDouble();
                                        } else if (xmlReader.isStartElement() && xmlReader.name() == "to") {
                                            xmlReader.readNext();
                                            toTimeout = xmlReader.text().toDouble();
                                        }
                                    }
                                }

                                xmlReader.readNext();
                                if (xmlReader.name() == "msgto") {
                                    msgto = xmlReader.readElementText().toInt();
                                }

                                xmlReader.readNext();
                                if (xmlReader.name() == "msgfrom") {
                                    msgfrom = xmlReader.readElementText().toInt();
                                }

                                messages.append({messages.size(), number, {fromData, toData}, {fromTimeout, toTimeout}, msgto, msgfrom});
                            }
                        }

                        missionItem.messages = messages;
                        messages.clear();
                    } else if (xmlReader.name() == "missiles") {
                        QVector<Missiles> missiles;
                        int number = xmlReader.attributes().value("number").toInt();

                        while (!(xmlReader.isEndElement() && xmlReader.name() == "missiles")) {
                            xmlReader.readNext();

                            if (xmlReader.isStartElement()) {
                                if (xmlReader.name() == "location_angle") {
                                    double fromLA = 0.0, toLA = 0.0;
                                    double fromLT = 0.0, toLT = 0.0;
                                    int cooldown = 0;

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
                    } else if (xmlReader.name() == "start_angular_velocity") {
                        QVector<double> startAngularVelocity;
                        while (!(xmlReader.isEndElement() && xmlReader.name() == "start_angular_velocity")) {
                            xmlReader.readNext();
                            if (xmlReader.isStartElement() && xmlReader.name() == "frm") {
                                xmlReader.readNext();
                                startAngularVelocity.append(xmlReader.text().toDouble());
                            } else if (xmlReader.isStartElement() && xmlReader.name() == "to") {
                                xmlReader.readNext();
                                startAngularVelocity.append(xmlReader.text().toDouble());
                            }
                        }
                        missionItem.startAngularVelocity = startAngularVelocity;
                    } else if (xmlReader.name() == "channel") {
                        QVector<double> channel;
                        while (!(xmlReader.isEndElement() && xmlReader.name() == "channel")) {
                            xmlReader.readNext();
                            if (xmlReader.isStartElement() && xmlReader.name() == "frm") {
                                xmlReader.readNext();
                                channel.append(xmlReader.text().toDouble());
                            } else if (xmlReader.isStartElement() && xmlReader.name() == "to") {
                                xmlReader.readNext();
                                channel.append(xmlReader.text().toDouble());
                            }
                        }
                        missionItem.channel = channel;
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

void EarthMissions::showMissions()
{
    for (const EarthMissionsItem &missionItem : mItems) {
        qDebug() << "Mission Name: " << missionItem.missionName;
        qDebug() << "Mission Eng Name: " << missionItem.missionEngName;
        qDebug() << "Duration: " << missionItem.duration;
        qDebug() << "Mission Description: " << missionItem.missionDescription;

        qDebug() << "Control Stations:";
        for (const ControlStations &station : missionItem.controlStations) {
            qDebug() << "  ID: " << station.id;
            qDebug() << "  Name: " << station.name;
            qDebug() << "  From-To Numbers: " << station.fromToNumbers;
        }

        qDebug() << "Orbit Data: " << missionItem.orbitData;
        qDebug() << "Precision: " << missionItem.precision;

        qDebug() << "Oneway Messages:";
        for (const OnewayMessage &message : missionItem.onewayMessages) {
            qDebug() << "  ID: " << message.id;
            qDebug() << "  Length: " << message.length;
        }

        qDebug() << "Missiles:";
        for (const Missiles &missile : missionItem.missiles) {
            qDebug() << "  ID: " << missile.id;
            qDebug() << "  Number: " << missile.number;
            qDebug() << "  Location Angle: " << missile.locatonAngle;
            qDebug() << "  Launch Time: " << missile.launchTime;
            qDebug() << "  Cooldown: " << missile.cooldown;
        }

        qDebug() << "Messages:";
        for (const Messages &message : missionItem.messages) {
            qDebug() << "  ID: " << message.id;
            qDebug() << "  Number: " << message.number;
            qDebug() << "  Data: " << message.data;
            qDebug() << "  Timeout: " << message.timeout;
            qDebug() << "  Msg To: " << message.msgto;
            qDebug() << "  Msg From: " << message.msgfrom;
        }

        qDebug() << "Resolution: " << missionItem.resolution;
        qDebug() << "Start Angular Velocity: " << missionItem.startAngularVelocity;
        qDebug() << "Target Angle: " << missionItem.targetAngle;
        qDebug() << "Target Orbit: " << missionItem.targetOrbit;
        qDebug() << "Channel: " << missionItem.channel;

        qDebug() << "\n";
        qDebug() << "-----------------------------------------------------------------";
        qDebug() << "\n";
    }
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

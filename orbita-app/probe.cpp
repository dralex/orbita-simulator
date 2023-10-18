#include "probe.h"
#include <QDebug>

Probe::Probe(QObject *parent)
    : QObject{parent}
{
}

QVector<ProbeItem> Probe::items() const
{
    return mItems;
}

bool Probe::setProbe(int index, const ProbeItem &item)
{
    if (index < 0 || index >= mItems.size())
        return false;

    const ProbeItem &olditem = mItems.at(index);
    if (item.probeNumber == olditem.probeNumber)
        return false;

    mItems[index] = item;
    return true;
}

void Probe::appendProbe(QString probeName, QString missionName, double outerRadius, double innerRadius, QString pythonCode)
{
    emit preProbeAppended();

    mItems.append({mItems.size(), probeName, missionName, outerRadius, innerRadius, {}, {},{},  pythonCode, ""});

    emit postProbeAppended();
}


void Probe::appendDevicesItem(int probeIndex, int deviceNumber, QString deviceName, QString deviceCode, QString deviceEngName, QString startState, bool inSafeMode)
{
    emit preDevicesItemAppended();

    mItems[probeIndex].devices.append({mItems[probeIndex].devices.size(), deviceNumber, deviceName, deviceCode, deviceEngName, startState, inSafeMode});

    emit postDevicesItemAppended();
}

void Probe::removeDevicesItem(int probeIndex, int index)
{
    emit preDevicesItemRemoved(index);

    mItems[probeIndex].devices.removeAt(index);

    emit postDevicesItemRemoved();
}

void Probe::appendActivityAndLandingItem(int probeIndex, bool typeCommand, int deviceNumber, double time, QString device, QString command, int argument)
{
    emit preActivityAndLandingItemAppended();

    if (typeCommand)
        mItems[probeIndex].stepsLanding.append({mItems[probeIndex].stepsActivity.size(), deviceNumber, time, device, command, argument});
    else
        mItems[probeIndex].stepsActivity.append({mItems[probeIndex].stepsActivity.size(), deviceNumber, time, device, command, argument});

    emit postActivityAndLandingItemAppended();
}

void Probe::removeActivityAndLandingItem(int probeIndex, bool typeCommand, int index)
{
    emit preActivityAndLandingItemRemoved(index);

    if (typeCommand)
        mItems[probeIndex].stepsLanding.removeAt(index);
    else
        mItems[probeIndex].stepsActivity.removeAt(index);

    emit postActivityAndLandingItemRemoved();

}

void Probe::saveToXml(int probeIndex, Planets *planetsData, int planetIndex, const QString &filename)
{
    QFile file(filename);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text))
    {
        return;
    }

    QXmlStreamWriter xmlWriter(&file);
    xmlWriter.setAutoFormatting(true);

    xmlWriter.writeStartDocument();
    xmlWriter.writeStartElement("v:probe");

    xmlWriter.writeAttribute("name", mItems[probeIndex].probeName);
    xmlWriter.writeNamespace("venus", "v");

    xmlWriter.writeStartElement("flight");

    xmlWriter.writeStartElement("mission");
    xmlWriter.writeAttribute("name", planetsData->items()[planetIndex].planetName);
    xmlWriter.writeEndElement();

    xmlWriter.writeTextElement("start_height", QString::number(planetsData->items()[planetIndex].height));

    xmlWriter.writeEndElement();


    xmlWriter.writeStartElement("parameters");
    xmlWriter.writeTextElement("radius_external", QString::number(mItems[probeIndex].outerRadius));
    xmlWriter.writeTextElement("radius_internal", QString::number(mItems[probeIndex].innerRadius));
    if (planetsData->items()[planetIndex].planetName == "Mercury" || planetsData->items()[planetIndex].planetName == "Venus") {
        xmlWriter.writeTextElement("absorber", "ON");
        xmlWriter.writeTextElement("isolator", "ON");
    } else {
        xmlWriter.writeTextElement("absorber", "OFF");
        xmlWriter.writeTextElement("isolator", "OFF");
    }


    xmlWriter.writeEndElement();

    xmlWriter.writeStartElement("devices");

    if (mItems[probeIndex].devices.size()) {
        for (const DevicesItem &deviceItem : mItems[probeIndex].devices)
        {
            xmlWriter.writeStartElement("device");
            xmlWriter.writeAttribute("number", QString::number(deviceItem.deviceNumber));
            xmlWriter.writeAttribute("name", QString(deviceItem.deviceEngName));
            xmlWriter.writeAttribute("start_state", QString(deviceItem.startState));
            if (deviceItem.inSafeMode) {
                xmlWriter.writeAttribute("in_safe_mode", "ON");
            } else {
                xmlWriter.writeAttribute("in_safe_mode", "OFF");
            }
            xmlWriter.writeEndElement();
        }
    }


    xmlWriter.writeEndElement();

    if (mItems[probeIndex].stepsLanding.size() || mItems[probeIndex].stepsActivity.size()) {
        xmlWriter.writeStartElement("program");
        if (mItems[probeIndex].stepsLanding.size()) {
            xmlWriter.writeStartElement("stage");
            xmlWriter.writeAttribute("id", "Landing");
            for (const StepsLandingItem &stepsLanding : mItems[probeIndex].stepsLanding)
            {
                xmlWriter.writeStartElement("command");
                xmlWriter.writeAttribute("time", QString::number(stepsLanding.time));
                xmlWriter.writeAttribute("device", QString(stepsLanding.device + stepsLanding.deviceNumber));
                xmlWriter.writeAttribute("action", QString(stepsLanding.command));
                xmlWriter.writeAttribute("argument", QString::number(stepsLanding.argument));
                xmlWriter.writeEndElement();
            }
            xmlWriter.writeEndElement();
        }

        if (mItems[probeIndex].stepsActivity.size()) {
            xmlWriter.writeStartElement("stage");
            xmlWriter.writeAttribute("id", "Surface activity");

            for (const StepsActivityItem &stepsActivity : mItems[probeIndex].stepsActivity)
            {
                xmlWriter.writeStartElement("command");
                xmlWriter.writeAttribute("time", QString::number(stepsActivity.time));
                xmlWriter.writeAttribute("device", QString(stepsActivity.device + stepsActivity.deviceNumber));
                xmlWriter.writeAttribute("action", QString(stepsActivity.command));
                xmlWriter.writeAttribute("argument", QString::number(stepsActivity.argument));
                xmlWriter.writeEndElement();
            }
            xmlWriter.writeEndElement();
        }

        xmlWriter.writeEndElement();
    } else if (!mItems[probeIndex].pythonCode.isEmpty()) {
        xmlWriter.writeStartElement("python_code");
        xmlWriter.writeCDATA("\n" + mItems[probeIndex].pythonCode + "\n");
        xmlWriter.writeEndElement();
    }

    xmlWriter.writeEndElement();
    xmlWriter.writeEndDocument();

    file.close();
}

void Probe::loadFromXml(QString filename, PlanetDevices *planetDevicesData) {
    QString probeFilename = filename;
    QFile file(filename);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        return;
    }

    QXmlStreamReader xmlReader(&file);

    ProbeItem probeXmlItem;
    probeXmlItem.pythonCode = "";
    QVector<DevicesItem> devicesItems;
    QVector<StepsLandingItem> stepsLandingItems;
    QVector<StepsActivityItem> stepsActivityItems;

    while (!xmlReader.atEnd() && !xmlReader.hasError()) {
        xmlReader.readNext();

        if (xmlReader.isStartElement()) {
            QString elementName = xmlReader.name().toString();
            if (elementName == "probe") {
                probeXmlItem.probeName = xmlReader.attributes().value("name").toString();
            } else if (elementName == "mission") {
                probeXmlItem.missionName = xmlReader.attributes().value("name").toString();
            } else if (elementName == "radius_external") {
                xmlReader.readNext();
                probeXmlItem.outerRadius = xmlReader.text().toDouble();
            } else if (xmlReader.name() == "radius_internal") {
                xmlReader.readNext();
                probeXmlItem.innerRadius = xmlReader.text().toDouble();
            } else if (xmlReader.name() == "devices") {
                while (!xmlReader.atEnd() && !xmlReader.hasError()) {
                    xmlReader.readNext();

                    if (xmlReader.isStartElement() && xmlReader.name() == "device") {
                        DevicesItem deviceItem;

                        QXmlStreamAttributes attributes = xmlReader.attributes();
                        deviceItem.deviceNumber = attributes.value("number").toInt();
                        deviceItem.deviceEngName = attributes.value("name").toString();
                        deviceItem.deviceName = planetDevicesData->getDeviceName(deviceItem.deviceEngName);
                        deviceItem.deviceCode = planetDevicesData->getDeviceCode(deviceItem.deviceName);

                        deviceItem.startState = attributes.value("start_state").toString();
                        deviceItem.inSafeMode = (attributes.value("in_safe_mode").toString() == "ON");

                        devicesItems.append(deviceItem);


                        while (!(xmlReader.isEndElement() && xmlReader.name() == "device")) {
                            xmlReader.readNext();
                        }
                    } else if (xmlReader.isEndElement() && xmlReader.name() == "devices") {
                        break;
                    }
                }

            } else if (xmlReader.name() == "program") {
                while (!xmlReader.atEnd() && !xmlReader.hasError()) {
                    xmlReader.readNext();

                    if (xmlReader.isStartElement() && (xmlReader.name() == "stage")) {
                        QString stageId = xmlReader.attributes().value("id").toString();

                        while (!xmlReader.atEnd() && !xmlReader.hasError()) {
                            xmlReader.readNext();

                            if (xmlReader.isStartElement() && (xmlReader.name() == "command")) {
                                QRegExp rx("([A-Za-z]+)(\\d+)");
                                StepsLandingItem landingItem;
                                StepsActivityItem activityItem;

                                int time = xmlReader.attributes().value("time").toInt();
                                QString device = xmlReader.attributes().value("device").toString();
                                QString action = xmlReader.attributes().value("action").toString();
                                int argument = xmlReader.attributes().value("argument").toInt();

                                if (stageId == "Landing") {
                                    landingItem.device = device;
                                    if (rx.indexIn(device) != -1) {
                                        landingItem.deviceNumber = rx.cap(2).toInt();
                                    }

                                    landingItem.id = stepsLandingItems.size();
                                    landingItem.time = time;
                                    landingItem.command = action;
                                    landingItem.argument = argument;
                                    stepsLandingItems.append(landingItem);
                                } else if (stageId == "Surface activity") {
                                    activityItem.device = device;
                                    if (rx.indexIn(device) != -1) {
                                        activityItem.deviceNumber = rx.cap(2).toInt();
                                    }
                                    activityItem.id = stepsActivityItems.size();
                                    activityItem.time = time;
                                    activityItem.command = action;
                                    activityItem.argument = argument;
                                    stepsActivityItems.append(activityItem);
                                }

                                while (!(xmlReader.isEndElement() && xmlReader.name() == "command")) {
                                    xmlReader.readNext();
                                }
                            } else if (xmlReader.isEndElement() && xmlReader.name() == "stage") {
                                break;
                            }
                        }
                    } else if (xmlReader.isEndElement() && xmlReader.name() == "program") {
                        break;
                    }
                }
            } else if (elementName == "python_code") {
                xmlReader.readNext();
                if (xmlReader.isCDATA()) {
                    probeXmlItem.pythonCode = xmlReader.text().toString();
                }
            }
        }
    }

    if (xmlReader.hasError()) {
        return;
    }

    emit preProbeAppended();

    int probeIndex = mItems.size();

    if (filename.contains("planets_probes_templates")) {
        probeFilename = "";
    }

    mItems.append({probeIndex,
                   probeXmlItem.probeName,
                   probeXmlItem.missionName,
                   probeXmlItem.outerRadius,
                   probeXmlItem.innerRadius,
                   {},
                   {},
                   {},
                   probeXmlItem.pythonCode,
                   probeFilename,
                  });

    emit postProbeAppended();

    if (devicesItems.size()) {
        for (int i = 0; i < devicesItems.size(); ++i) {
            emit preDevicesItemAppended();

            mItems[probeIndex].devices.append(devicesItems[i]);

            emit postDevicesItemAppended();
        }
    }


    if (stepsActivityItems.size()) {
        for (int i = 0; i < stepsActivityItems.size(); ++i) {
            emit preActivityAndLandingItemAppended();

            mItems[probeIndex].stepsActivity.append(stepsActivityItems[i]);

            emit postActivityAndLandingItemRemoved();
        }
    }

    if (stepsLandingItems.size()) {
        for (int i = 0; i < stepsLandingItems.size(); ++i) {
            emit preActivityAndLandingItemAppended();

            mItems[probeIndex].stepsLanding.append(stepsLandingItems[i]);

            emit postActivityAndLandingItemRemoved();
        }
    }


    file.close();
}

bool Probe::checkFileChanges(int probeIndex, PlanetDevices *planetDevicesData)
{
    QFile file(mItems[probeIndex].filePath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        return false;
    }

    QXmlStreamReader xmlReader(&file);

    QVector<DevicesItem> devicesItems;
    QVector<StepsLandingItem> stepsLandingItems;
    QVector<StepsActivityItem> stepsActivityItems;

    while (!xmlReader.atEnd() && !xmlReader.hasError()) {
        xmlReader.readNext();

        if (xmlReader.isStartElement()) {
            QString elementName = xmlReader.name().toString();
            if (elementName == "probe") {
                if (xmlReader.attributes().value("name").toString() != mItems[probeIndex].probeName) {
                    file.close();
                    return false;
                }
            } else if (elementName == "radius_external") {
                xmlReader.readNext();
                if (xmlReader.text().toDouble() != mItems[probeIndex].outerRadius) {
                    file.close();
                    return false;
                }
            } else if (xmlReader.name() == "radius_internal") {
                xmlReader.readNext();
                if (xmlReader.text().toDouble() != mItems[probeIndex].innerRadius) {
                    file.close();
                    return false;
                }
            } else if (xmlReader.name() == "devices") {
                while (!xmlReader.atEnd() && !xmlReader.hasError()) {
                    xmlReader.readNext();

                    if (xmlReader.isStartElement() && xmlReader.name() == "device") {
                        DevicesItem deviceItem;

                        QXmlStreamAttributes attributes = xmlReader.attributes();
                        deviceItem.deviceNumber = attributes.value("number").toInt();
                        deviceItem.deviceEngName = attributes.value("name").toString();
                        deviceItem.deviceName = planetDevicesData->getDeviceName(deviceItem.deviceEngName);
                        deviceItem.deviceCode = planetDevicesData->getDeviceCode(deviceItem.deviceName);

                        deviceItem.startState = attributes.value("start_state").toString();
                        deviceItem.inSafeMode = (attributes.value("in_safe_mode").toString() == "ON");

                        devicesItems.append(deviceItem);


                        while (!(xmlReader.isEndElement() && xmlReader.name() == "device")) {
                            xmlReader.readNext();
                        }
                    } else if (xmlReader.isEndElement() && xmlReader.name() == "devices") {
                        break;
                    }
                }

            } else if (xmlReader.name() == "program") {
                while (!xmlReader.atEnd() && !xmlReader.hasError()) {
                    xmlReader.readNext();

                    if (xmlReader.isStartElement() && (xmlReader.name() == "stage")) {
                        QString stageId = xmlReader.attributes().value("id").toString();

                        while (!xmlReader.atEnd() && !xmlReader.hasError()) {
                            xmlReader.readNext();

                            if (xmlReader.isStartElement() && (xmlReader.name() == "command")) {
                                QRegExp rx("([A-Za-z]+)(\\d+)");
                                StepsLandingItem landingItem;
                                StepsActivityItem activityItem;

                                int time = xmlReader.attributes().value("time").toInt();
                                QString device = xmlReader.attributes().value("device").toString();
                                QString action = xmlReader.attributes().value("action").toString();
                                int argument = xmlReader.attributes().value("argument").toInt();

                                if (stageId == "Landing") {
                                    landingItem.device = device;
                                    if (rx.indexIn(device) != -1) {
                                        landingItem.deviceNumber = rx.cap(2).toInt();
                                    }

                                    landingItem.id = stepsLandingItems.size();
                                    landingItem.time = time;
                                    landingItem.command = action;
                                    landingItem.argument = argument;
                                    stepsLandingItems.append(landingItem);
                                } else if (stageId == "Surface activity") {
                                    activityItem.device = device;
                                    if (rx.indexIn(device) != -1) {
                                        activityItem.deviceNumber = rx.cap(2).toInt();
                                    }
                                    activityItem.id = stepsActivityItems.size();
                                    activityItem.time = time;
                                    activityItem.command = action;
                                    activityItem.argument = argument;
                                    stepsActivityItems.append(activityItem);
                                }

                                while (!(xmlReader.isEndElement() && xmlReader.name() == "command")) {
                                    xmlReader.readNext();
                                }
                            } else if (xmlReader.isEndElement() && xmlReader.name() == "stage") {
                                break;
                            }
                        }
                    } else if (xmlReader.isEndElement() && xmlReader.name() == "program") {
                        break;
                    }
                }
            } else if (elementName == "python_code") {
                xmlReader.readNext();
                if (xmlReader.isCDATA()) {
                    if (xmlReader.text().toString() != mItems[probeIndex].pythonCode) {
                        file.close();
                        return false;
                    }
                }
            }
        }
    }

    if (xmlReader.hasError()) {
        return false;
    }

    file.close();
    if (mItems[probeIndex].devices.size() != devicesItems.size()) {
        return false;
    } else {
        for (int i = 0; i < mItems[probeIndex].devices.size(); ++i) {
            if (mItems[probeIndex].devices.size()) {
                if (mItems[probeIndex].devices[i].deviceNumber != devicesItems[i].deviceNumber ||
                    mItems[probeIndex].devices[i].deviceName != devicesItems[i].deviceName ||
                    mItems[probeIndex].devices[i].deviceCode != devicesItems[i].deviceCode ||
                    mItems[probeIndex].devices[i].deviceEngName != devicesItems[i].deviceEngName ||
                    mItems[probeIndex].devices[i].startState != devicesItems[i].startState ||
                    mItems[probeIndex].devices[i].inSafeMode != devicesItems[i].inSafeMode) {
                    return false;
                }
            }
        }
    }


    if (mItems[probeIndex].stepsLanding.size() != stepsLandingItems.size()) {
        return false;
    } else {
        for (int i = 0; i < mItems[probeIndex].stepsLanding.size(); ++i) {
            if (mItems[probeIndex].stepsLanding.size()) {
                if (mItems[probeIndex].stepsLanding[i].deviceNumber != stepsLandingItems[i].deviceNumber ||
                    mItems[probeIndex].stepsLanding[i].time != stepsLandingItems[i].time ||
                    mItems[probeIndex].stepsLanding[i].device != stepsLandingItems[i].device ||
                    mItems[probeIndex].stepsLanding[i].command != stepsLandingItems[i].command ||
                    mItems[probeIndex].stepsLanding[i].argument != stepsLandingItems[i].argument) {
                    return false;
                }
            }
        }
    }


    if (mItems[probeIndex].stepsActivity.size() != stepsActivityItems.size()) {
        return false;
    } else {
        for (int i = 0; i < mItems[probeIndex].stepsActivity.size(); ++i) {
            if (mItems[probeIndex].stepsActivity.size()) {
                if (mItems[probeIndex].stepsActivity[i].deviceNumber != stepsActivityItems[i].deviceNumber ||
                    mItems[probeIndex].stepsActivity[i].time != stepsActivityItems[i].time ||
                    mItems[probeIndex].stepsActivity[i].device != stepsActivityItems[i].device ||
                    mItems[probeIndex].stepsActivity[i].command != stepsActivityItems[i].command ||
                    mItems[probeIndex].stepsActivity[i].argument != stepsActivityItems[i].argument) {
                    return false;
                }
            }
        }
    }


    return true;
}


void Probe::saveProbe(int probeIndex, QString probeName, double innerRadius, double outerRadius, QString pythonCode, const QString &filePath)
{
    mItems[probeIndex].probeName = probeName;
    mItems[probeIndex].outerRadius = outerRadius;
    mItems[probeIndex].innerRadius = innerRadius;
    mItems[probeIndex].filePath = filePath;
    if (!pythonCode.isEmpty())
        mItems[probeIndex].pythonCode = pythonCode;
}

int Probe::size()
{
    return mItems.size();
}

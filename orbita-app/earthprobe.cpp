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

void EarthProbe::appendEarthDevice(int probeIndex, QString deviceEngName, QString deviceName,  QString type, double mass, bool startMode)
{
    emit preEarthDeviceAppended();

    mItems[probeIndex].devices.append({mItems[probeIndex].devices.size(), deviceEngName, deviceName, type, mass, startMode});

    emit postEarthDeviceAppended();
}

void EarthProbe::removeEarthDevice(int probeIndex, int index)
{
    emit preEarthDeviceRemoved(index);

    mItems[probeIndex].devices.removeAt(index);

    emit postEarthDeviceRemoved();
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

void EarthProbe::appendDiagramm(int probeIndex, QString deviceEngName, QString path)
{
    mItems[probeIndex].diagrammPathes.append({mItems[probeIndex].diagrammPathes.size(), deviceEngName, path});
}

void EarthProbe::removeDiagramm(int probeIndex, QString deviceEngName)
{
    for (int i = 0; i < mItems[probeIndex].diagrammPathes.size(); ++i) {
        if (mItems[probeIndex].diagrammPathes[i].deviceEngName == deviceEngName)
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
    xmlWriter.writeAttribute("type", missions->items()[missionIndex].missionEngName);

    xmlWriter.writeStartElement("control_stations");

    // here needs a for cycle for set data of control stations
    xmlWriter.writeStartElement("control_station");
    xmlWriter.writeTextElement("location_angle", "data");
    xmlWriter.writeEndElement();

    xmlWriter.writeEndElement();
    xmlWriter.writeTextElement("duration", "data");
    xmlWriter.writeTextElement("orbit", "data");
    xmlWriter.writeTextElement("precision", "data");
    xmlWriter.writeTextElement("start_angular_velocity", "1.0");
    xmlWriter.writeTextElement("target_angle", "data");
    xmlWriter.writeTextElement("target_angle", "data");

    xmlWriter.writeEndElement();

    xmlWriter.writeStartElement("construction");

    xmlWriter.writeTextElement("fuel", QString::number(mItems[probeIndex].fuel));
    xmlWriter.writeTextElement("voltage", QString::number(mItems[probeIndex].voltage));
    xmlWriter.writeTextElement("xz_yz_solar_panel_fraction", QString::number(mItems[probeIndex].xz_yz_solar_panel_fraction));
    xmlWriter.writeTextElement("xz_yz_radiator_fraction", QString::number(mItems[probeIndex].xz_yz_radiator_fraction));
    xmlWriter.writeTextElement("xy_radiator_fraction", QString::number(mItems[probeIndex].xy_radiator_fraction));

    xmlWriter.writeEndElement();

    xmlWriter.writeStartElement("systems");

    if (mItems[probeIndex].devices.size()) {
        for (const EarthProbeDeviceItem &systems : mItems[probeIndex].devices)
        {
            xmlWriter.writeStartElement("system");
            xmlWriter.writeAttribute("name", QString(systems.deviceEngName));
            if (systems.startMode)
                xmlWriter.writeAttribute("start_mode", "ON");
            if (mItems[probeIndex].diagrammPathes.size()) {
                for (int i = 0; i < mItems[probeIndex].diagrammPathes.size(); ++i) {
                    if (mItems[probeIndex].diagrammPathes[i].deviceEngName == systems.deviceEngName) {
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

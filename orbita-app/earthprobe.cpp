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

    mItems.append({mItems.size(), probeName, missionName, {}, pythonCode, {}, filePath});

    emit postEarthProbeAppended();
}

void EarthProbe::appendEarthDevice(int probeIndex, QString deviceEngName, QString deviceName, double mass, bool startMode)
{
    emit preEarthDeviceAppended();

    mItems[probeIndex].devices.append({mItems[probeIndex].devices.size(), deviceEngName, deviceName, mass, startMode});

    emit postEarthDeviceAppended();
}

void EarthProbe::removeEarthDevice(int probeIndex, int index)
{
    emit preEarthDeviceRemoved(index);

    mItems[probeIndex].devices.removeAt(index);

    emit postEarthDeviceRemoved();
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

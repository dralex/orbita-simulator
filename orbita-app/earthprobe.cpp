#include "earthprobe.h"

EarthProbe::EarthProbe(QObject *parent)
    : QObject{parent}
{

}

QVector<EarthProbeItem> EarthProbe::items() const
{
    return mItems;
}

void EarthProbe::appendEarthProbe(QString probeName, QString missionName, QString filePath)
{
    emit preEarthProbeAppended();

    mItems.append({mItems.size(), probeName, missionName, {}, "", "", filePath});

    emit postEarthProbeAppended();
}

void EarthProbe::appendEarthDevice(int probeIndex, QString deviceEngName, QString deviceName, double mass)
{
    emit preEarthDeviceAppended();

    mItems[probeIndex].devices.append({mItems[probeIndex].devices.size(), deviceEngName, deviceName, mass});

    emit postEarthDeviceAppended();
}

void EarthProbe::removeEarthDevice(int probeIndex, int index)
{
    emit preEarthDeviceRemoved(index);

    mItems[probeIndex].devices.removeAt(index);

    emit postEarthDeviceRemoved();
}

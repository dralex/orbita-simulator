#include "earthprobedevices.h"

EarthProbeDevices::EarthProbeDevices(QObject *parent)
    : QObject{parent}
{
}

QVector<EarthProbeDeviceItem> EarthProbeDevices::items() const
{
    return mItems;
}

bool EarthProbeDevices::setEarthProbesDevices(int index, const EarthProbeDeviceItem &item)
{
    if (index < 0 || index >= mItems.size())
        return false;

    const EarthProbeDeviceItem &olditem = mItems.at(index);
    if (item.id == olditem.id)
        return false;
    mItems[index] = item;
    return true;
}

void EarthProbeDevices::appendEarthDevice(EarthProbe *earthProbe, int probeIndex, QString deviceEngName, QString deviceName, double mass, bool startMode)
{
    emit preEarthProbeDeviceAppended();

    mItems.append({mItems.size(), deviceEngName, deviceName, mass, startMode});
    earthProbe->appendEarthDevice(probeIndex, deviceEngName, deviceName, mass, startMode);

    emit postEarthProbeDeviceAppended();
}

void EarthProbeDevices::removeEarthDevice(EarthProbe *earthProbe, int probeIndex, int index)
{
    emit preEarthProbeDeviceRemoved(index);

    mItems.removeAt(index);
    earthProbe->removeEarthDevice(probeIndex, index);

    emit postEarthProbeDeviceRemoved();
}

void EarthProbeDevices::changeEarthDevices(EarthProbe *earthProbe, int probeIndex)
{
    for (int i = mItems.size() - 1; i >= 0; --i) {
        emit preEarthProbeDeviceRemoved(i);
        mItems.removeAt(i);
        emit postEarthProbeDeviceRemoved();
    }

    for (int i = 0; i < earthProbe->items()[probeIndex].devices.size(); ++i) {
        emit preEarthProbeDeviceAppended();

        mItems.append({mItems.size(),
                       earthProbe->items()[probeIndex].devices[i].deviceEngName,
                       earthProbe->items()[probeIndex].devices[i].deviceName,
                       earthProbe->items()[probeIndex].devices[i].mass,
                       earthProbe->items()[probeIndex].devices[i].startMode
                      });

        emit postEarthProbeDeviceAppended();
    }
}

int EarthProbeDevices::size()
{
    return mItems.size();
}

#include "earthprobedevices.h"

EarthProbeDevices::EarthProbeDevices(QObject *parent)
    : QObject{parent}
{

}

void EarthProbeDevices::appendEarthDevice(EarthProbe *earthProbe, int probeIndex, QString deviceEngName, QString deviceName, double mass)
{
    emit preEarthProbeDeviceAppended();

    mItems.append({mItems.size(), deviceEngName, deviceName, mass});
    earthProbe->appendEarthDevice(probeIndex, deviceEngName, deviceName, mass);

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
                       earthProbe->items()[probeIndex].devices[i].mass
                      });

        emit postEarthProbeDeviceAppended();
    }
}

int EarthProbeDevices::size()
{
    return mItems.size();
}

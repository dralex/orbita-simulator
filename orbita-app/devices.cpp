#include "devices.h"

Devices::Devices(QObject *parent)
    : QObject{parent}
{
}

QVector<DevicesItem> Devices::items() const
{
    return mItems;
}

bool Devices::setDevicesItem(int index, const DevicesItem &item)
{
    if (index < 0 || index >= mItems.size())
        return false;

    const DevicesItem &olditem = mItems.at(index);
    if (item.id == olditem.id)
        return false;
    mItems[index] = item;
    return true;
}

void Devices::appendDevicesItem(Probe* probe, int probeIndex, QString deviceName, QString deviceCode, QString deviceEngName, QString startState, bool inSafeMode)
{
    emit preDevicesItemAppended();

    int numberDevice = 1;

    for (int i = 0; i < mItems.size(); ++i)
    {
        if (mItems[i].deviceName == deviceName)
        {
            numberDevice++;
        }
    }
    mItems.append({mItems.size(), numberDevice, deviceName, deviceCode, deviceEngName, startState, inSafeMode});
    probe->appendDevicesItem(probeIndex, numberDevice, deviceName, deviceCode, deviceEngName, startState, inSafeMode);

    emit postDevicesItemAppended();

}

void Devices::removeDevicesItem(Probe* probe, StepsActivity* stepsActivity, StepsLanding* stepsLanding, int probeIndex, int index)
{
    emit preDevicesItemRemoved(index);

    int deviceNumberToRemove = mItems[index].deviceNumber;

    if (stepsActivity->items().size()) {
        for (int i = stepsActivity->items().size() - 1; i >= 0; --i)
        {
            if (stepsActivity->items()[i].deviceNumber == deviceNumberToRemove)
            {
                stepsActivity->removeItem(probe, false, probeIndex, i);
                break;
            }
        }
    }

    if (stepsLanding->items().size()) {
        for (int i = stepsLanding->items().size() - 1; i >= 0; --i)
        {
            if (stepsLanding->items()[i].deviceNumber == deviceNumberToRemove)
            {
                stepsLanding->removeItem(probe, true, probeIndex, i);
                break;
            }
        }
    }

    mItems.removeAt(index);
    probe->removeDevicesItem(probeIndex, index);

    emit postDevicesItemRemoved();
}


void Devices::changeDevices(Probe *probe, int probeIndex)
{

    for (int i = mItems.size() - 1; i >= 0; --i) {
        emit preDevicesItemRemoved(i);
        mItems.removeAt(i);
        emit postDevicesItemRemoved();
    }

    for (int i = 0; i < probe->items()[probeIndex].devices.size(); ++i) {
        emit preDevicesItemAppended();

        mItems.append({mItems.size(),
                       probe->items()[probeIndex].devices[i].deviceNumber,
                       probe->items()[probeIndex].devices[i].deviceName,
                       probe->items()[probeIndex].devices[i].deviceCode,
                       probe->items()[probeIndex].devices[i].deviceEngName,
                       probe->items()[probeIndex].devices[i].startState,
                       probe->items()[probeIndex].devices[i].inSafeMode
                      });

        emit postDevicesItemAppended();
    }
}

int Devices::size()
{
    return mItems.size();
}

QString Devices::getDeviceName(int index)
{
    for (int i = 0; i < mItems.size(); ++i)
        if (i == index)
            return mItems[i].deviceName;

    return "None";
}

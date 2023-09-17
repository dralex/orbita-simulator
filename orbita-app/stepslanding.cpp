#include "stepslanding.h"

StepsLanding::StepsLanding(QObject *parent)
    : QObject{parent}
{

}

const QVector<StepsLandingItem> StepsLanding::items() const
{
    return mItems;
}

bool StepsLanding::setItem(int index, const StepsLandingItem &item)
{
    if (index < 0 || index >= mItems.size())
        return false;

    const StepsLandingItem &olditem = mItems.at(index);
    if (item.id == olditem.id)
        return false;
    mItems[index] = item;
    return true;
}

void StepsLanding::appendItem(Probe *probe, bool typeCommand, int probeIndex, int deviceNumber, double time, QString device, QString command, int argument)
{
    emit preItemAppended();

    mItems.append({mItems.size(), deviceNumber, time, device, command, argument});

    probe->appendActivityAndLandingItem(probeIndex, typeCommand, deviceNumber, time, device, command, argument);

    emit postItemAppended();
}

void StepsLanding::removeItem(Probe *probe, bool typeCommand, int probeIndex, int index)
{
    emit preItemRemoved(index);

    mItems.removeAt(index);

    probe->removeActivityAndLandingItem(probeIndex, typeCommand, index);

    emit postItemRemoved();
}

void StepsLanding::changeSteps(Probe *probe, int probeIndex)
{
    for (int i = mItems.size() - 1; i >= 0; --i) {
        emit preItemRemoved(i);
        mItems.removeAt(i);
        emit postItemRemoved();
    }

    for (int i = 0; i < probe->items()[probeIndex].stepsLanding.size(); ++i) {
        emit preItemAppended();

        mItems.append({mItems.size(),
                       probe->items()[probeIndex].stepsLanding[i].deviceNumber,
                       probe->items()[probeIndex].stepsLanding[i].time,
                       probe->items()[probeIndex].stepsLanding[i].device,
                       probe->items()[probeIndex].stepsLanding[i].command,
                       probe->items()[probeIndex].stepsLanding[i].argument
                      });

        emit postItemAppended();
    }
}

int StepsLanding::size()
{
    return mItems.size();
}

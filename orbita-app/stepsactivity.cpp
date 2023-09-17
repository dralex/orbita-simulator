#include "stepsactivity.h"

StepsActivity::StepsActivity(QObject *parent)
    : QObject{parent}
{

}

const QVector<StepsActivityItem> StepsActivity::items() const
{
    return mItems;
}

bool StepsActivity::setItem(int index, const StepsActivityItem &item)
{
    if (index < 0 || index >= mItems.size())
        return false;

    const StepsActivityItem &olditem = mItems.at(index);
    if (item.id == olditem.id)
        return false;
    mItems[index] = item;
    return true;
}

void StepsActivity::appendItem(Probe *probe, bool typeCommand, int probeIndex, int deviceNumber, double time, QString device, QString command, int argument)
{
    emit preItemAppended();

    mItems.append({mItems.size(), deviceNumber, time, device, command, argument});

    probe->appendActivityAndLandingItem(probeIndex, typeCommand, deviceNumber, time, device, command, argument);

    emit postItemAppended();
}

void StepsActivity::removeItem(Probe *probe, bool typeCommand, int probeIndex, int index)
{
    emit preItemRemoved(index);

    mItems.removeAt(index);

    probe->removeActivityAndLandingItem(probeIndex, typeCommand, index);

    emit postItemRemoved();
}

void StepsActivity::changeSteps(Probe *probe, int probeIndex)
{
    for (int i = mItems.size() - 1; i >= 0; --i) {
        emit preItemRemoved(i);
        mItems.removeAt(i);
        emit postItemRemoved();
    }

    for (int i = 0; i < probe->items()[probeIndex].stepsActivity.size(); ++i) {
        emit preItemAppended();

        mItems.append({mItems.size(),
                       probe->items()[probeIndex].stepsActivity[i].deviceNumber,
                       probe->items()[probeIndex].stepsActivity[i].time,
                       probe->items()[probeIndex].stepsActivity[i].device,
                       probe->items()[probeIndex].stepsActivity[i].command,
                       probe->items()[probeIndex].stepsActivity[i].argument
                      });

        emit postItemAppended();
    }
}

int StepsActivity::size()
{
    return mItems.size();
}

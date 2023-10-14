#include "stepsitems.h"

StepsActivityAndLanding::StepsActivityAndLanding(QObject *parent)
    : QObject{parent}
{

}

const QVector<StepsActivityAndLandingItem> StepsActivityAndLanding::activityItems() const
{
    return mActivityItems;
}


bool StepsActivityAndLanding::setActivityItem(int index, const StepsActivityAndLandingItem &item)
{
    if (index < 0 || index >= mActivityItems.size())
        return false;

    const StepsActivityAndLandingItem &olditem = mActivityItems.at(index);
    if (item.id == olditem.id)
        return false;
    mActivityItems[index] = item;
    return true;
}

void StepsActivityAndLanding::appendItem(Probe* probe, bool typeCommand, int probeIndex, double time,
                                         QString device, QString command, QString argument)
{
    emit preItemAppended();
    if (typeCommand)
        mLandingItems.append({mLandingItems.size(), time, device, command, argument});
    else
        mActivityItems.append({mActivityItems.size(), time, device, command, argument});

    probe->appendActivityAndLandingItem(probeIndex, typeCommand, time, device, command, argument);

    emit postItemAppended();
}

void StepsActivityAndLanding::removeItem(Probe* probe, bool typeCommand, int probeIndex, int index)
{
    emit preItemRemoved(index);

    if (typeCommand)
        mLandingItems.removeAt(index);
    else
        mActivityItems.removeAt(index);

    probe->removeActivityAndLandingItem(probeIndex, typeCommand, index);

    emit postItemRemoved();
}

void StepsActivityAndLanding::changeSteps(Probe *probe, bool typeCommand, int probeIndex)
{
    if (typeCommand) {
        for (int i = mLandingItems.size() - 1; i >= 0; --i) {
            emit preItemRemoved(i);
            mLandingItems.removeAt(i);
            emit postItemRemoved();
        }

        for (int i = 0; i < probe->items()[probeIndex].stepsLanding.size(); ++i) {
            emit preItemAppended();

            mLandingItems.append({mLandingItems.size(), probe->items()[probeIndex].stepsLanding[i].time,
                                   probe->items()[probeIndex].stepsLanding[i].device,
                                   probe->items()[probeIndex].stepsLanding[i].command,
                                   probe->items()[probeIndex].stepsLanding[i].argument
                          });

            emit postItemAppended();
        }
    } else {
        for (int i = mActivityItems.size() - 1; i >= 0; --i) {
            emit preItemRemoved(i);
            mActivityItems.removeAt(i);
            emit postItemRemoved();
        }

        for (int i = 0; i < probe->items()[probeIndex].stepsActivity.size(); ++i) {
            emit preItemAppended();

            mActivityItems.append({mActivityItems.size(), probe->items()[probeIndex].stepsActivity[i].time,
                                   probe->items()[probeIndex].stepsActivity[i].device,
                                   probe->items()[probeIndex].stepsActivity[i].command,
                                   probe->items()[probeIndex].stepsActivity[i].argument
                          });

            emit postItemAppended();

        }
    }

}

int StepsActivityAndLanding::size(bool typeCommand)
{
    if (typeCommand)
        return mLandingItems.size();
    else
        return mActivityItems.size();
}

const QVector<StepsActivityAndLandingItem> StepsActivityAndLanding::landingItems() const
{
    return mLandingItems;
}

bool StepsActivityAndLanding::setLandingItems(int index, const StepsActivityAndLandingItem &item)
{
    if (index < 0 || index >= mLandingItems.size())
        return false;

    const StepsActivityAndLandingItem &olditem = mLandingItems.at(index);
    if (item.id == olditem.id)
        return false;
    mLandingItems[index] = item;
    return true;
}


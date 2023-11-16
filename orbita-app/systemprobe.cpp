#include "systemprobe.h"

SystemProbe::SystemProbe(QObject *parent)
    : QObject{parent}
{
}

QVector<SystemItem> SystemProbe::items() const
{
    return mItems;
}

bool SystemProbe::setEarthProbesSystems(int index, const SystemItem &item)
{
    if (index < 0 || index >= mItems.size())
        return false;

    const SystemItem &olditem = mItems.at(index);
    if (item.id == olditem.id)
        return false;
    mItems[index] = item;
    return true;
}

void SystemProbe::appendEarthSystem(EarthProbe *earthProbe, int probeIndex, QString systemEngName, QString systemName,  QString type, double mass, bool startMode)
{
    emit preEarthProbeSystemsAppended();

    mItems.append({mItems.size(), systemEngName, systemName, type, mass, startMode, ""});
    earthProbe->appendEarthDevice(probeIndex, systemEngName, systemName, type, mass, startMode);

    emit postEarthProbeSystemsAppended();
}

void SystemProbe::removeEarthSystem(EarthProbe *earthProbe, int probeIndex, int index)
{
    emit preEarthProbeSystemsRemoved(index);

    mItems.removeAt(index);
    earthProbe->removeEarthDevice(probeIndex, index);

    emit postEarthProbeSystemsRemoved();
}

void SystemProbe::appendDiagramPath(QString systemEngName, QString diagramPath)
{
    for (int i = 0; i < mItems.size(); ++i)
        if (mItems[i].systemEngName == systemEngName)
            mItems[i].diagramPath = diagramPath;
}

QString SystemProbe::getText(int row, int column)
{
    return (row >= 0 && row < mItems.size()) ? ((column == 0) ? mItems[row].systemName : ((column == 3) ? mItems[row].diagramPath : QString())) : QString();
}

bool SystemProbe::checkUniqueType(QString type)
{
    for (int i = 0; i < mItems.size(); ++i)
        if (mItems[i].type == type)
            return true;
    return false;
}

void SystemProbe::changeEarthSystems(EarthProbe *earthProbe, int probeIndex)
{
    for (int i = mItems.size() - 1; i >= 0; --i) {
        emit preEarthProbeSystemsRemoved(i);
        mItems.removeAt(i);
        emit postEarthProbeSystemsRemoved();
    }

    for (int i = 0; i < earthProbe->items()[probeIndex].systems.size(); ++i) {
        emit preEarthProbeSystemsAppended();

        mItems.append({mItems.size(),
                       earthProbe->items()[probeIndex].systems[i].systemEngName,
                       earthProbe->items()[probeIndex].systems[i].systemName,
                       earthProbe->items()[probeIndex].systems[i].type,
                       earthProbe->items()[probeIndex].systems[i].mass,
                       earthProbe->items()[probeIndex].systems[i].startMode,
                       earthProbe->items()[probeIndex].systems[i].diagramPath,
                      });

        emit postEarthProbeSystemsAppended();
    }
}

int SystemProbe::size()
{
    return mItems.size();
}

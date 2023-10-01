#include "earthprobesmodel.h"

EarthProbesModel::EarthProbesModel(QObject *parent)
    : QAbstractListModel(parent)
{
}

int EarthProbesModel::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid() || !mList)
        return 0;

    return mList->items().size();
}

QVariant EarthProbesModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || !mList)
        return QVariant();
    const EarthProbeItem item = mList->items().at(index.row());
    switch (role) {
    case probeNumberRole:
        return QVariant(item.probeNumber);
    case probeNameRole:
        return QVariant(item.probeName);
    case missionRole:
        return QVariant(item.missionName);
    case fuelRole:
        return QVariant(item.fuel);
    case voltageRole:
        return QVariant(item.voltage);
    case xz_yz_solarRole:
        return QVariant(item.xz_yz_solar_panel_fraction);
    case xz_yz_radiatorRole:
        return QVariant(item.xz_yz_radiator_fraction);
    case xy_radiatorRole:
        return QVariant(item.xy_radiator_fraction);
    case pythonCodeRole:
        return QVariant(item.pythonCode);
    case filePathRole:
        return QVariant(item.filePath);
    }


    return QVariant();
}

bool EarthProbesModel::setData(const QModelIndex &index, const QVariant &value, int role)
{
    if (!mList)
        return false;

    EarthProbeItem item = mList->items().at(index.row());

    switch (role) {
    case probeNumberRole:
        item.probeNumber = value.toInt();
        break;
    case probeNameRole:
        item.probeName = value.toString();
        break;
    case missionRole:
        item.missionName = value.toString();
        break;
    case fuelRole:
        item.fuel = value.toDouble();
    case voltageRole:
        item.voltage = value.toDouble();
        break;
    case xz_yz_solarRole:
        item.xz_yz_solar_panel_fraction = value.toDouble();
        break;
    case xz_yz_radiatorRole:
        item.xz_yz_radiator_fraction = value.toDouble();
        break;
    case xy_radiatorRole:
        item.xy_radiator_fraction = value.toDouble();
        break;
    case pythonCodeRole:
        item.pythonCode = value.toString();
        break;
    case filePathRole:
        item.filePath = value.toString();
        break;
    }
    if (mList->setEarthProbe(index.row(), item)) {
        emit dataChanged(index, index, QVector<int>() << role);
        return true;
    }
    return false;
}

Qt::ItemFlags EarthProbesModel::flags(const QModelIndex &index) const
{
    if (!index.isValid())
        return Qt::NoItemFlags;

    return Qt::ItemIsEditable;
}

QHash<int, QByteArray> EarthProbesModel::roleNames() const
{
    QHash<int, QByteArray> names;
    names[probeNumberRole] = "probeNumber";
    names[probeNameRole] = "probeName";
    names[missionRole] = "missionName";
    names[fuelRole] = "fuel";
    names[voltageRole] = "voltage";
    names[xz_yz_solarRole] = "xz_yz_solar";
    names[xz_yz_radiatorRole] = "xz_yz_radiator";
    names[xy_radiatorRole] = "xy_radiator";
    names[pythonCodeRole] = "pythonCode";
    names[filePathRole] = "probeFilePath";
    return names;
}

EarthProbe *EarthProbesModel::list() const
{
    return mList;
}

void EarthProbesModel::setList(EarthProbe *list)
{
    beginResetModel();

    if (mList)
        mList->disconnect(this);

    mList = list;

    if (mList) {
        connect(mList, &EarthProbe::preEarthProbeAppended, this, [=] () {
            const int index = mList->items().size();
            beginInsertRows(QModelIndex(), index, index);
        });
        connect(mList, &EarthProbe::postEarthProbeAppended, this, [=] () {
            endInsertRows();
        });

        connect(mList, &EarthProbe::preEarthProbeRemoved, this, [=] (int index) {
            beginRemoveRows(QModelIndex(), index, index);
        });
        connect(mList, &EarthProbe::postEarthProbeRemoved, this, [=] () {
            endRemoveRows();
        });
    }
    endResetModel();
}

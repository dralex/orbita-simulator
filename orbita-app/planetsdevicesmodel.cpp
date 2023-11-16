#include "planetsdevicesmodel.h"

PlanetsDevicesModel::PlanetsDevicesModel(QObject *parent)
    : QAbstractListModel(parent), mList(NULL)
{
}

int PlanetsDevicesModel::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid() || !mList)
        return 0;

    return mList->items().size();
}

QVariant PlanetsDevicesModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || !mList)
        return QVariant();

    const PlanetDeviceItems item = mList->items().at(index.row());

    switch (role) {
    case textRole:
        return QVariant(item.deviceName);
    }


    return QVariant();
}

bool PlanetsDevicesModel::setData(const QModelIndex &index, const QVariant &value, int role)
{
    if (!mList)
        return false;

    PlanetDeviceItems item = mList->items().at(index.row());

    switch (role) {
    case textRole:
        item.deviceName = value.toString();
        break;
    }

    if (mList->setPlanetDevices(index.row(), item)) {
        emit dataChanged(index, index, QVector<int>() << role);
        return true;
    }
    return false;
}

Qt::ItemFlags PlanetsDevicesModel::flags(const QModelIndex &index) const
{
    if (!index.isValid())
        return Qt::NoItemFlags;

    return Qt::ItemIsEditable;
}

QHash<int, QByteArray> PlanetsDevicesModel::roleNames() const
{
    QHash<int, QByteArray> names;
    names[textRole] = "text";
    return names;
}

PlanetDevices *PlanetsDevicesModel::list() const
{
    return mList;
}

void PlanetsDevicesModel::setList(PlanetDevices *list)
{
    beginResetModel();

    if (mList)
        mList->disconnect(this);

    mList = list;

    if (mList) {
        connect(mList, &PlanetDevices::prePlanetDeviceAppended, this, [=] () {
            const int index = mList->items().size();
            beginInsertRows(QModelIndex(), index, index);
        });
        connect(mList, &PlanetDevices::postPlanetDeviceAppended, this, [=] () {
            endInsertRows();
        });

        connect(mList, &PlanetDevices::prePlanetDeviceRemoved, this, [=] (int index) {
            beginRemoveRows(QModelIndex(), index, index);
        });
        connect(mList, &PlanetDevices::postPlanetDeviceRemoved, this, [=] () {
            endRemoveRows();
        });
    }
    endResetModel();
}

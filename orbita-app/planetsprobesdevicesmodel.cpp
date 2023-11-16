#include "planetsprobesdevicesmodel.h"

PlanetsProbesDevicesModel::PlanetsProbesDevicesModel(QObject *parent)
    : QAbstractTableModel(parent)
    , mList(nullptr)
{
}

int PlanetsProbesDevicesModel::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid() || !mList)
        return 0;

    return mList->items().size();
}

int PlanetsProbesDevicesModel::columnCount(const QModelIndex &parent) const
{
    if (parent.isValid() || !mList)
        return 0;

    return 4;
}

QVariant PlanetsProbesDevicesModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || !mList)
        return QVariant();

    const DevicesItem item = mList->items().at(index.row());

    switch (role) {
    case deviceNumberRole:
        return QVariant(item.deviceNumber);
    case deviceNameRole:
        return QVariant(item.deviceName);
    case startStateRole:
        return QVariant(item.startState);
    case inSafeModeRole:
        return QVariant(item.inSafeMode);

    }


    return QVariant();
}

bool PlanetsProbesDevicesModel::setData(const QModelIndex &index, const QVariant &value, int role)
{
    if (!mList)
        return false;

    DevicesItem item = mList->items().at(index.row());
    switch (role) {
    case deviceNumberRole:
        item.deviceNumber = value.toInt();
        break;
    case deviceNameRole:
        item.deviceName = value.toString();
        break;
    case startStateRole:
        item.startState = value.toString();
        break;
    case inSafeModeRole:
        item.inSafeMode = value.toBool();
        break;
    }

    if (mList->setDevicesItem(index.row(), item)) {
        emit dataChanged(index, index, QVector<int>() << role);
        return true;
    }
    return false;
}

Qt::ItemFlags PlanetsProbesDevicesModel::flags(const QModelIndex &index) const
{
    if (!index.isValid())
        return Qt::NoItemFlags;

    return Qt::ItemIsEditable;
}

QHash<int, QByteArray> PlanetsProbesDevicesModel::roleNames() const
{
    QHash<int, QByteArray> names;
    names[deviceNumberRole] = "deviceNumber";
    names[deviceNameRole] = "deviceName";
    names[startStateRole] = "startState";
    names[inSafeModeRole] = "inSafeMode";
    return names;
}

Devices *PlanetsProbesDevicesModel::list() const
{
    return mList;
}

void PlanetsProbesDevicesModel::setList(Devices *list)
{
    beginResetModel();

    if (mList)
        mList->disconnect(this);

    mList = list;

    if (mList) {
        connect(mList, &Devices::preDevicesItemAppended, this, [=] () {
            const int index = mList->items().size();
            beginInsertRows(QModelIndex(), index, index);
        });
        connect(mList, &Devices::postDevicesItemAppended, this, [=] () {
            endInsertRows();
        });

        connect(mList, &Devices::preDevicesItemRemoved, this, [=] (int index) {
            beginRemoveRows(QModelIndex(), index, index);
        });
        connect(mList, &Devices::postDevicesItemRemoved, this, [=] () {
            endRemoveRows();
        });
    }
    endResetModel();
}

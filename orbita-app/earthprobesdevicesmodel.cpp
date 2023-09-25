#include "earthprobesdevicesmodel.h"

EarthProbesDevicesModel::EarthProbesDevicesModel(QObject *parent)
    : QAbstractListModel(parent)
    , mList (nullptr)
{
}

int EarthProbesDevicesModel::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid() || !mList)
        return 0;

    return mList->items().size();
}

QVariant EarthProbesDevicesModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || !mList)
        return QVariant();

    const EarthProbeDeviceItem item = mList->items().at(index.row());

    switch (role) {
    case deviceNameRole:
        return QVariant(item.deviceName);
    case massRole:
        return QVariant(item.mass);
    case startModeRole:
        return QVariant(item.startMode);

    }


    return QVariant();
}

bool EarthProbesDevicesModel::setData(const QModelIndex &index, const QVariant &value, int role)
{
    if (!mList)
        return false;

    EarthProbeDeviceItem item = mList->items().at(index.row());
    switch (role) {
    case deviceNameRole:
        item.deviceName = value.toString();
        break;
    case massRole:
        item.mass = value.toDouble();
        break;
    case startModeRole:
        item.startMode = value.toBool();
        break;
    }

    if (mList->setEarthProbesDevices(index.row(), item)) {
        emit dataChanged(index, index, QVector<int>() << role);
        return true;
    }
    return false;
}

Qt::ItemFlags EarthProbesDevicesModel::flags(const QModelIndex &index) const
{
    if (!index.isValid())
        return Qt::NoItemFlags;

    return Qt::ItemIsEditable;
}

QHash<int, QByteArray> EarthProbesDevicesModel::roleNames() const
{
    QHash<int, QByteArray> names;
    names[deviceNameRole] = "deviceName";
    names[massRole] = "mass";
    names[startModeRole] = "startMode";
    return names;
}

EarthProbeDevices *EarthProbesDevicesModel::list() const
{
    return mList;
}

void EarthProbesDevicesModel::setList(EarthProbeDevices *list)
{
    beginResetModel();

    if (mList)
        mList->disconnect(this);

    mList = list;

    if (mList) {
        connect(mList, &EarthProbeDevices::preEarthProbeDeviceAppended, this, [=] () {
            const int index = mList->items().size();
            beginInsertRows(QModelIndex(), index, index);
        });
        connect(mList, &EarthProbeDevices::postEarthProbeDeviceAppended, this, [=] () {
            endInsertRows();
        });

        connect(mList, &EarthProbeDevices::preEarthProbeDeviceRemoved, this, [=] (int index) {
            beginRemoveRows(QModelIndex(), index, index);
        });
        connect(mList, &EarthProbeDevices::postEarthProbeDeviceRemoved, this, [=] () {
            endRemoveRows();
        });
    }
    endResetModel();
}

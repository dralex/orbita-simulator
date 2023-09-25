#include "earthdevicesmodel.h"

EarthDevicesModel::EarthDevicesModel(QObject *parent)
    : QAbstractListModel(parent)
    , mList(nullptr)
{
}

int EarthDevicesModel::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid() || !mList)
        return 0;

    return mList->items().size();
}

QVariant EarthDevicesModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || !mList)
        return QVariant();

    const EarthDevicesItem item = mList->items().at(index.row());

    switch (role) {
    case textRole:
        return QVariant(item.deviceName);
    }


    return QVariant();
}

bool EarthDevicesModel::setData(const QModelIndex &index, const QVariant &value, int role)
{
    if (!mList)
        return false;

    EarthDevicesItem item = mList->items().at(index.row());

    switch (role) {
    case textRole:
        item.deviceName = value.toString();
        break;
    }

    if (mList->setEarthDevices(index.row(), item)) {
        emit dataChanged(index, index, QVector<int>() << role);
        return true;
    }
    return false;
}

Qt::ItemFlags EarthDevicesModel::flags(const QModelIndex &index) const
{
    if (!index.isValid())
        return Qt::NoItemFlags;

    return Qt::ItemIsEditable;
}

QHash<int, QByteArray> EarthDevicesModel::roleNames() const
{
    QHash<int, QByteArray> names;
    names[textRole] = "text";
    return names;
}

EarthDevices *EarthDevicesModel::list() const
{
    return mList;
}

void EarthDevicesModel::setList(EarthDevices *list)
{
    beginResetModel();

    if (mList)
        mList->disconnect(this);

    mList = list;

    if (mList) {
        connect(mList, &EarthDevices::preEarthDeviceAppended, this, [=] () {
            const int index = mList->items().size();
            beginInsertRows(QModelIndex(), index, index);
        });
        connect(mList, &EarthDevices::postEarthDeviceAppended, this, [=] () {
            endInsertRows();
        });

        connect(mList, &EarthDevices::preEarthDeviceRemoved, this, [=] (int index) {
            beginRemoveRows(QModelIndex(), index, index);
        });
        connect(mList, &EarthDevices::postEarthDeviceRemoved, this, [=] () {
            endRemoveRows();
        });
    }
    endResetModel();
}

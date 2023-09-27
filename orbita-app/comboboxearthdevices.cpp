#include "comboboxearthdevices.h"

ComboBoxEarthDevices::ComboBoxEarthDevices(QObject *parent)
    : QAbstractListModel(parent)
    , mList(nullptr)
{
}

int ComboBoxEarthDevices::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid() || !mList)
        return 0;
    return mList->items().size();
}

QVariant ComboBoxEarthDevices::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || !mList)
        return QVariant();

    const EarthProbeDeviceItem item = mList->items().at(index.row());

    switch (role) {
    case textRole:
        return QVariant(item.deviceName);
    }


    return QVariant();
}

bool ComboBoxEarthDevices::setData(const QModelIndex &index, const QVariant &value, int role)
{
    if (!mList)
        return false;

    EarthProbeDeviceItem item = mList->items().at(index.row());

    switch (role) {
    case textRole:
        item.deviceName = value.toString();
        break;
    }

    if (mList->setEarthProbesDevices(index.row(), item)) {
        emit dataChanged(index, index, QVector<int>() << role);
        return true;
    }
    return false;
}

Qt::ItemFlags ComboBoxEarthDevices::flags(const QModelIndex &index) const
{
    if (!index.isValid())
        return Qt::NoItemFlags;

    return Qt::ItemIsEditable;
}

QHash<int, QByteArray> ComboBoxEarthDevices::roleNames() const
{
    QHash<int, QByteArray> names;
    names[textRole] = "text";
    return names;
}

EarthProbeDevices *ComboBoxEarthDevices::list() const
{
    return mList;
}

void ComboBoxEarthDevices::setList(EarthProbeDevices *list)
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

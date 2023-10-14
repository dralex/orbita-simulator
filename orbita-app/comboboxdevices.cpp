#include "comboboxdevices.h"

ComboBoxDevices::ComboBoxDevices(QObject *parent)
    : QAbstractListModel(parent)
    , mList(nullptr)
{
}

int ComboBoxDevices::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid() || !mList)
        return 0;

    return mList->items().size();
}


QVariant ComboBoxDevices::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || !mList)
        return QVariant();

    const DevicesItem item = mList->items().at(index.row());
    QString deviceNumber = QString::number(item.deviceNumber);

    switch (role) {
    case textRole:
        return QVariant(item.deviceCode + deviceNumber);
    }


    return QVariant();
}

bool ComboBoxDevices::setData(const QModelIndex &index, const QVariant &value, int role)
{
    if (!mList)
        return false;

    DevicesItem item = mList->items().at(index.row());
    QString deviceNumber = QString::number(item.deviceNumber);

    switch (role) {
    case textRole:
        item.deviceCode = value.toString() + deviceNumber;
        break;
    }

    if (mList->setDevicesItem(index.row(), item)) {
        emit dataChanged(index, index, QVector<int>() << role);
        return true;
    }
    return false;
}

Qt::ItemFlags ComboBoxDevices::flags(const QModelIndex &index) const
{
    if (!index.isValid())
        return Qt::NoItemFlags;

    return Qt::ItemIsEditable;
}

QHash<int, QByteArray> ComboBoxDevices::roleNames() const
{
    QHash<int, QByteArray> names;
    names[textRole] = "text";
    return names;
}

Devices *ComboBoxDevices::list() const
{
    return mList;
}

void ComboBoxDevices::setList(Devices *list)
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

#include "devicestablemodel.h"

DevicesTableModel::DevicesTableModel(QObject *parent)
    : QAbstractTableModel(parent)
    , mList(nullptr)
{
    table.append({"Номер", "Название", "Начальное состояние", "Safe Mode"});
}

int DevicesTableModel::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid() || !mList)
        return 0;

    return table.size() + mList->items().size();
}

int DevicesTableModel::columnCount(const QModelIndex &parent) const
{
    if (parent.isValid() || !mList)
        return 0;

    return table.at(0).size();
}

QVariant DevicesTableModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || !mList)
        return QVariant();

    if (role == tableDataRole) {
        if (index.row() == 0) {
            return table.at(index.row()).at(index.column());
        } else {
            int dataIndex = index.row() - 1;
            if (dataIndex < mList->items().size()) {
                const DevicesItem item = mList->items().at(dataIndex);
                if (index.column() == 0) {
                    return item.deviceNumber;
                } else if (index.column() == 1) {
                    return item.deviceName;
                } else if (index.column() == 2) {
                    return item.startState;
                } else if (index.column() == 3) {
                    return item.inSafeMode;
                }
            }
        }
    } else if (role == headingRole) {
        return index.row() == 0;
    }

    return QVariant();
}



bool DevicesTableModel::setData(const QModelIndex &index, const QVariant &value, int role)
{
    if (!mList)
        return false;

    if (role == tableDataRole && index.row() > 0) {
        int dataIndex = index.row() - 1;
        if (dataIndex < mList->items().size()) {
            DevicesItem item = mList->items()[dataIndex];
            if (index.column() == 0) {
                item.deviceNumber = value.toInt();
            } else if (index.column() == 1) {
                item.deviceName = value.toString();
            } else if (index.column() == 2) {
                item.startState = value.toString();
            } else if (index.column() == 3) {
                item.inSafeMode = value.toBool();
            }
            mList->setDevicesItem(dataIndex, item);
            emit dataChanged(index, index, QVector<int>() << role);
            return true;
        }
    }

    return false;
}

Qt::ItemFlags DevicesTableModel::flags(const QModelIndex &index) const
{
    if (!index.isValid())
        return Qt::NoItemFlags;

    return Qt::ItemIsEditable;
}

QHash<int, QByteArray> DevicesTableModel::roleNames() const
{
    QHash<int, QByteArray> names;
    names[tableDataRole] = "tableData";
    names[headingRole] = "heading";
    return names;
}

Devices *DevicesTableModel::list() const
{
    return mList;
}

void DevicesTableModel::setList(Devices *list)
{
    beginResetModel();

    if (mList)
        mList->disconnect(this);

    mList = list;

    if (mList) {
        connect(mList, &Devices::preDevicesItemAppended, this, [=]() {
            const int index = mList->items().size();
            beginInsertRows(QModelIndex(), index, index);
        });
        connect(mList, &Devices::postDevicesItemAppended, this, [=]() {
            endInsertRows();
        });

        connect(mList, &Devices::preDevicesItemRemoved, this, [=](int index) {
            beginRemoveRows(QModelIndex(), index, index);
        });
        connect(mList, &Devices::postDevicesItemRemoved, this, [=]() {
            endRemoveRows();
        });
    }

    endResetModel();
}

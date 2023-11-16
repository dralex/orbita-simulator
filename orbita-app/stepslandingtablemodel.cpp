#include "stepslandingtablemodel.h"

StepsLandingTableModel::StepsLandingTableModel(QObject *parent)
    : QAbstractTableModel(parent)
    , mList(nullptr)
{
    table.append({"Номер", "Время", "Тип", "Команда", "Параметр"});
}

int StepsLandingTableModel::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid() || !mList)
        return 0;

    return table.size() + mList->items().size();
}

int StepsLandingTableModel::columnCount(const QModelIndex &parent) const
{
    if (parent.isValid() || !mList)
        return 0;

    return table.at(0).size();
}


QVariant StepsLandingTableModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || !mList)
        return QVariant();

    if (role == tableDataRole) {
        if (index.row() == 0) {
             return table.at(index.row()).at(index.column());
         } else {
            int dataIndex = index.row() - 1;
            if (dataIndex < mList->items().size()) {
                const StepsLandingItem item = mList->items().at(dataIndex);
                if (index.column() == 0) {
                    return item.deviceNumber;
                } else if (index.column() == 1) {
                    return item.time;
                } else if (index.column() == 2) {
                    return item.device;
                } else if (index.column() == 3) {
                    return item.command;
                } else if (index.column() == 4) {
                    return item.argument;
                }
            }
        }
    } else if (role == headingRole) {
        return index.row() == 0;
    }

    return QVariant();
}


bool StepsLandingTableModel::setData(const QModelIndex &index, const QVariant &value, int role)
{
    if (!mList)
        return false;

    if (role == tableDataRole && index.row() > 0) {
        int dataIndex = index.row() - 1;
        if (dataIndex < mList->items().size()) {
            StepsLandingItem item = mList->items()[dataIndex];

            if (index.column() == 0) {
                item.deviceNumber = value.toInt();
            } else if (index.column() == 1) {
                item.time = value.toDouble();
            } else if (index.column() == 2) {
                item.device = value.toString();
            } else if (index.column() == 3) {
                item.command = value.toString();
            } else if (index.column() == 4) {
                item.argument = value.toInt();
            }
            mList->setItem(dataIndex, item);
            emit dataChanged(index, index, QVector<int>() << role);
            return true;
        }
    }

    return false;
}


Qt::ItemFlags StepsLandingTableModel::flags(const QModelIndex &index) const
{
    if (!index.isValid())
        return Qt::NoItemFlags;

    return Qt::ItemIsEditable;
}

QHash<int, QByteArray> StepsLandingTableModel::roleNames() const
{
    QHash<int, QByteArray> names;
    names[tableDataRole] = "tableData";
    names[headingRole] = "heading";
    return names;
}

StepsLanding *StepsLandingTableModel::list() const
{
    return mList;
}

void StepsLandingTableModel::setList(StepsLanding *list)
{
    beginResetModel();

    if (mList)
        mList->disconnect(this);

    mList = list;

    if (mList) {
        connect(mList, &StepsLanding::preItemAppended, this, [=]() {
            const int index = mList->items().size();
            beginInsertRows(QModelIndex(), index, index);
        });
        connect(mList, &StepsLanding::postItemAppended, this, [=]() {
            endInsertRows();
        });

        connect(mList, &StepsLanding::preItemRemoved, this, [=](int index) {
            beginRemoveRows(QModelIndex(), index, index);
        });
        connect(mList, &StepsLanding::postItemRemoved, this, [=]() {
            endRemoveRows();
        });
    }

    endResetModel();
}

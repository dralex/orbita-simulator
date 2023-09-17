#include "stepsactivitymodel.h"

StepsActivityModel::StepsActivityModel(QObject *parent)
    : QAbstractListModel(parent)
    , mList(nullptr)
{
}

int StepsActivityModel::rowCount(const QModelIndex &parent) const
{
    // For list models only the root node (an invalid parent) should return the list's size. For all
    // other (valid) parents, rowCount() should return 0 so that it does not become a tree model.
    if (parent.isValid() || !mList)
        return 0;

    return mList->items().size();
}

QVariant StepsActivityModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid())
        return QVariant();
    const StepsActivityItem item = mList->items().at(index.row());
    switch (role) {
    case idRole:
        return QVariant(item.id);
    case deviceNumberRole:
        return QVariant(item.deviceNumber);
    case timeRole:
        return QVariant(item.time);
    case deviceRole:
        return QVariant(item.device);
    case commandRole:
        return QVariant(item.command);
    case argumentRole:
        return QVariant(item.argument);
    }

    return QVariant();
}

bool StepsActivityModel::setData(const QModelIndex &index, const QVariant &value, int role)
{
    if (!mList) {
        return false;
    }

    StepsActivityItem item = mList->items().at(index.row());

    switch (role) {
    case idRole:
        item.id = value.toInt();
        break;
    case deviceNumberRole:
        item.deviceNumber = value.toInt();
        break;
    case timeRole:
        item.time = value.toDouble();
        break;
    case deviceRole:
        item.device = value.toString();
        break;
    case commandRole:
        item.command = value.toString();
        break;
    case argumentRole:
        item.argument = value.toInt();
        break;
    }

    if (mList->setItem(index.row(), item)) {
        emit dataChanged(index, index, QVector<int>() << role);
        return true;
    }
    return false;
}

Qt::ItemFlags StepsActivityModel::flags(const QModelIndex &index) const
{
    if (!index.isValid())
        return Qt::NoItemFlags;

    return Qt::ItemIsEditable;
}

QHash<int, QByteArray> StepsActivityModel::roleNames() const
{
    QHash<int, QByteArray> names;
    names[idRole] = "id";
    names[deviceNumberRole] = "deviceNumber";
    names[timeRole] = "time";
    names[deviceRole] = "device";
    names[commandRole] = "command";
    names[argumentRole] = "argument";
    return names;
}

StepsActivity *StepsActivityModel::list() const
{
    return mList;
}

void StepsActivityModel::setList(StepsActivity *list)
{
    beginResetModel();
    if (mList)
        mList->disconnect(this);

    mList = list;

    if (mList) {
        connect(mList, &StepsActivity::preItemAppended, this, [=] () {
            const int index = mList->items().size();
            beginInsertRows(QModelIndex(), index, index);
        });
        connect(mList, &StepsActivity::postItemAppended, this, [=] () {
            endInsertRows();
        });

        connect(mList, &StepsActivity::preItemRemoved, this, [=] (int index) {
            beginRemoveRows(QModelIndex(), index, index);
        });
        connect(mList, &StepsActivity::postItemRemoved, this, [=] () {
            endRemoveRows();
        });
    }
    endResetModel();
}

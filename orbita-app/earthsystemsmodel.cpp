#include "earthsystemsmodel.h"

EarthSystemsModel::EarthSystemsModel(QObject *parent)
    : QAbstractListModel(parent)
    , mList(nullptr)
{
}

int EarthSystemsModel::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid() || !mList)
        return 0;

    return mList->items().size();
}

QVariant EarthSystemsModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || !mList)
        return QVariant();

    const EarthSystemItem item = mList->items().at(index.row());

    switch (role) {
    case textRole:
        return QVariant(item.systemName);
    }


    return QVariant();
}

bool EarthSystemsModel::setData(const QModelIndex &index, const QVariant &value, int role)
{
    if (!mList)
        return false;

    EarthSystemItem item = mList->items().at(index.row());

    switch (role) {
    case textRole:
        item.systemName = value.toString();
        break;
    }

    if (mList->setEarthSystems(index.row(), item)) {
        emit dataChanged(index, index, QVector<int>() << role);
        return true;
    }
    return false;
}

Qt::ItemFlags EarthSystemsModel::flags(const QModelIndex &index) const
{
    if (!index.isValid())
        return Qt::NoItemFlags;

    return Qt::ItemIsEditable;
}

QHash<int, QByteArray> EarthSystemsModel::roleNames() const
{
    QHash<int, QByteArray> names;
    names[textRole] = "text";
    return names;
}

Systems *EarthSystemsModel::list() const
{
    return mList;
}

void EarthSystemsModel::setList(Systems *list)
{
    beginResetModel();

    if (mList)
        mList->disconnect(this);

    mList = list;

    if (mList) {
        connect(mList, &Systems::preEarthSystemAppended, this, [=] () {
            const int index = mList->items().size();
            beginInsertRows(QModelIndex(), index, index);
        });
        connect(mList, &Systems::postEarthSystemAppended, this, [=] () {
            endInsertRows();
        });

        connect(mList, &Systems::preEarthSystemsRemoved, this, [=] (int index) {
            beginRemoveRows(QModelIndex(), index, index);
        });
        connect(mList, &Systems::postEarthSystemsRemoved, this, [=] () {
            endRemoveRows();
        });
    }
    endResetModel();
}

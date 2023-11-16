#include "earthmissionsmodel.h"

EarthMissionsModel::EarthMissionsModel(QObject *parent)
    : QAbstractListModel(parent)
    , mList(nullptr)
{
}

int EarthMissionsModel::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid() || !mList)
        return 0;

    return mList->items().size();
}

QVariant EarthMissionsModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || !mList)
        return QVariant();

    const EarthMissionsItem item = mList->items().at(index.row());

    switch (role) {
    case textRole:
        return QVariant(item.missionName);
    }


    return QVariant();
}

bool EarthMissionsModel::setData(const QModelIndex &index, const QVariant &value, int role)
{
    if (!mList)
        return false;

    EarthMissionsItem item = mList->items().at(index.row());

    switch (role) {
    case textRole:
        item.missionName = value.toString();
        break;
    }

    if (mList->setMissions(index.row(), item)) {
        emit dataChanged(index, index, QVector<int>() << role);
        return true;
    }
    return false;
}

Qt::ItemFlags EarthMissionsModel::flags(const QModelIndex &index) const
{
    if (!index.isValid())
        return Qt::NoItemFlags;

    return Qt::ItemIsEditable;
}

QHash<int, QByteArray> EarthMissionsModel::roleNames() const
{
    QHash<int, QByteArray> names;
    names[textRole] = "text";
    return names;
}

EarthMissions *EarthMissionsModel::list() const
{
    return mList;
}

void EarthMissionsModel::setList(EarthMissions *list)
{
    beginResetModel();

    if (mList)
        mList->disconnect(this);

    mList = list;

    if (mList) {
        connect(mList, &EarthMissions::preEarthMissionsItemAppended, this, [=] () {
            const int index = mList->items().size();
            beginInsertRows(QModelIndex(), index, index);
        });
        connect(mList, &EarthMissions::postEarthMissionsItemAppended, this, [=] () {
            endInsertRows();
        });

        connect(mList, &EarthMissions::preEarthMissionsItemRemoved, this, [=] (int index) {
            beginRemoveRows(QModelIndex(), index, index);
        });
        connect(mList, &EarthMissions::postEarthMissionsItemRemoved, this, [=] () {
            endRemoveRows();
        });
    }
    endResetModel();
}

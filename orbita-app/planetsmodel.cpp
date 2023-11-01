#include "planetsmodel.h"

PlanetsModel::PlanetsModel(QObject *parent)
    : QAbstractListModel(parent)
{
}

int PlanetsModel::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid() || !mList)
        return 0;

    return mList->items().size();
}

QVariant PlanetsModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || !mList)
        return QVariant();

    const PlanetsItem item = mList->items().at(index.row());

    switch (role) {
    case textRole:
        return QVariant(item.planetName);
    }


    return QVariant();
}

bool PlanetsModel::setData(const QModelIndex &index, const QVariant &value, int role)
{
    if (!mList)
        return false;

    PlanetsItem item = mList->items().at(index.row());

    switch (role) {
    case textRole:
        item.planetName = value.toString();
        break;
    }

    if (mList->setPlanets(index.row(), item)) {
        emit dataChanged(index, index, QVector<int>() << role);
        return true;
    }
    return false;
}

Qt::ItemFlags PlanetsModel::flags(const QModelIndex &index) const
{
    if (!index.isValid())
        return Qt::NoItemFlags;

    return Qt::ItemIsEditable;
}

QHash<int, QByteArray> PlanetsModel::roleNames() const
{
    QHash<int, QByteArray> names;
    names[textRole] = "text";
    return names;
}

Planets *PlanetsModel::list() const
{
    return mList;
}

void PlanetsModel::setList(Planets *list)
{
    beginResetModel();

    if (mList)
        mList->disconnect(this);

    mList = list;

    if (mList) {
        connect(mList, &Planets::prePlanetsItemAppended, this, [=] () {
            const int index = mList->items().size();
            beginInsertRows(QModelIndex(), index, index);
        });
        connect(mList, &Planets::postPlanetsItemAppended, this, [=] () {
            endInsertRows();
        });

        connect(mList, &Planets::prePlanetsItemRemoved, this, [=] (int index) {
            beginRemoveRows(QModelIndex(), index, index);
        });
        connect(mList, &Planets::postPlanetsItemRemoved, this, [=] () {
            endRemoveRows();
        });
    }
    endResetModel();
}

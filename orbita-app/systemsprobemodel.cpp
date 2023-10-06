#include "systemsprobemodel.h"

SystemsProbeModel::SystemsProbeModel(QObject *parent)
    : QAbstractListModel(parent)
    , mList (nullptr)
{
}

int SystemsProbeModel::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid() || !mList)
        return 0;

    return mList->items().size();
}

QVariant SystemsProbeModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || !mList)
        return QVariant();

    const SystemItem item = mList->items().at(index.row());

    switch (role) {
    case systemNameRole:
        return QVariant(item.systemName);
    case massRole:
        return QVariant(item.mass);
    case startModeRole:
        return QVariant(item.startMode);

    }


    return QVariant();
}

bool SystemsProbeModel::setData(const QModelIndex &index, const QVariant &value, int role)
{
    if (!mList)
        return false;

    SystemItem item = mList->items().at(index.row());
    switch (role) {
    case systemNameRole:
        item.systemName = value.toString();
        break;
    case massRole:
        item.mass = value.toDouble();
        break;
    case startModeRole:
        item.startMode = value.toBool();
        break;
    }

    if (mList->setEarthProbesSystems(index.row(), item)) {
        emit dataChanged(index, index, QVector<int>() << role);
        return true;
    }
    return false;
}

Qt::ItemFlags SystemsProbeModel::flags(const QModelIndex &index) const
{
    if (!index.isValid())
        return Qt::NoItemFlags;

    return Qt::ItemIsEditable;
}

QHash<int, QByteArray> SystemsProbeModel::roleNames() const
{
    QHash<int, QByteArray> names;
    names[systemNameRole] = "systemName";
    names[massRole] = "mass";
    names[startModeRole] = "startMode";
    return names;
}

SystemProbe *SystemsProbeModel::list() const
{
    return mList;
}

void SystemsProbeModel::setList(SystemProbe *list)
{
    beginResetModel();

    if (mList)
        mList->disconnect(this);

    mList = list;

    if (mList) {
        connect(mList, &SystemProbe::preEarthProbeSystemsAppended, this, [=] () {
            const int index = mList->items().size();
            beginInsertRows(QModelIndex(), index, index);
        });
        connect(mList, &SystemProbe::postEarthProbeSystemsAppended, this, [=] () {
            endInsertRows();
        });

        connect(mList, &SystemProbe::preEarthProbeSystemsRemoved, this, [=] (int index) {
            beginRemoveRows(QModelIndex(), index, index);
        });
        connect(mList, &SystemProbe::postEarthProbeSystemsRemoved, this, [=] () {
            endRemoveRows();
        });
    }
    endResetModel();
}

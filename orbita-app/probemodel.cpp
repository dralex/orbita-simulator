#include "probemodel.h"

#include "probe.h"

ProbeModel::ProbeModel(QObject *parent) : QAbstractListModel(parent)
{
}

int ProbeModel::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid() || !mList)
        return 0;

    return mList->items().size();
}

QVariant ProbeModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || !mList)
        return QVariant();
    const ProbeItem item = mList->items().at(index.row());
    switch (role) {
    case probeNumberRole:
        return QVariant(item.probeNumber);
    case probeNameRole:
        return QVariant(item.probeName);
    case missionRole:
        return QVariant(item.missionName);
    case outerRadiusRole:
        return QVariant(item.outerRadius);
    case innerRadiusRole:
        return QVariant(item.innerRadius);
    case pythonCodeRole:
        return QVariant(item.pythonCode);
    case filePathRole:
        return QVariant(item.filePath);
    }


    return QVariant();
}

bool ProbeModel::setData(const QModelIndex &index, const QVariant &value, int role)
{
    if (!mList)
        return false;

    ProbeItem item = mList->items().at(index.row());

    switch (role) {
    case probeNumberRole:
        item.probeNumber = value.toInt();
        break;
    case probeNameRole:
        item.probeName = value.toString();
        break;
    case missionRole:
        item.missionName = value.toString();
        break;
    case outerRadiusRole:
        item.outerRadius = value.toInt();
        break;
    case innerRadiusRole:
        item.innerRadius = value.toInt();
        break;
    case pythonCodeRole:
        item.pythonCode = value.toString();
        break;
    case filePathRole:
        item.filePath = value.toString();
        break;
    }
    if (mList->setProbe(index.row(), item)) {
        emit dataChanged(index, index, QVector<int>() << role);
        return true;
    }
    return false;
}

Qt::ItemFlags ProbeModel::flags(const QModelIndex &index) const
{
    if (!index.isValid())
        return Qt::NoItemFlags;

    return Qt::ItemIsEditable;
}

QHash<int, QByteArray> ProbeModel::roleNames() const
{
    QHash<int, QByteArray> names;
    names[probeNumberRole] = "probeNumber";
    names[probeNameRole] = "probeName";
    names[missionRole] = "missionName";
    names[outerRadiusRole] = "outerRadius";
    names[innerRadiusRole] = "innerRadius";
    names[pythonCodeRole] = "pythonCode";
    names[filePathRole] = "probeFilePath";
    return names;
}

Probe *ProbeModel::list() const
{
    return mList;
}

void ProbeModel::setList(Probe *list)
{
    beginResetModel();

    if (mList)
        mList->disconnect(this);

    mList = list;

    if (mList) {
        connect(mList, &Probe::preProbeAppended, this, [=] () {
            const int index = mList->items().size();
            beginInsertRows(QModelIndex(), index, index);
        });
        connect(mList, &Probe::postProbeAppended, this, [=] () {
            endInsertRows();
        });

        connect(mList, &Probe::preProbeRemoved, this, [=] (int index) {
            beginRemoveRows(QModelIndex(), index, index);
        });
        connect(mList, &Probe::postProbeRemoved, this, [=] () {
            endRemoveRows();
        });
    }
    endResetModel();
}


#include "systemsprobetablemodel.h"

SystemsProbeTableModel::SystemsProbeTableModel(QObject *parent)
    : QAbstractTableModel(parent)
    , mList(nullptr)
{
    table.append({"Название", "Масса", "Start State", "Файл"});
}

int SystemsProbeTableModel::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid() || !mList)
        return 0;

    return table.size() + mList->items().size();
}

int SystemsProbeTableModel::columnCount(const QModelIndex &parent) const
{
    if (parent.isValid() || !mList)
        return 0;

    return table.at(0).size();
}

QVariant SystemsProbeTableModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || !mList)
        return QVariant();

    if (role == tableDataRole) {
        if (index.row() == 0) {
            return table.at(index.row()).at(index.column());
        } else {
            int dataIndex = index.row() - 1;
            if (dataIndex < mList->items().size()) {
                const SystemItem item = mList->items().at(dataIndex);
                if (index.column() == 0) {
                    return item.systemName;
                } else if (index.column() == 1) {
                    return item.mass;
                } else if (index.column() == 2) {
                    return item.startMode;
                } else if (index.column() == 3) {
                    return item.diagramPath;
                }
            }
        }
    } else if (role == headingRole) {
        return index.row() == 0;
    }

    return QVariant();
}

bool SystemsProbeTableModel::setData(const QModelIndex &index, const QVariant &value, int role)
{
    if (!mList)
        return false;

    if (role == tableDataRole && index.row() > 0) {
        int dataIndex = index.row() - 1;
        if (dataIndex < mList->items().size()) {
            SystemItem item = mList->items()[dataIndex];
            if (index.column() == 0) {
                item.systemName = value.toString();
            } else if (index.column() == 1) {
                item.mass = value.toDouble();
            } else if (index.column() == 2) {
                item.startMode = value.toBool();
            } else if (index.column() == 3) {
                item.diagramPath = value.toString();
            }
            mList->setEarthProbesSystems(dataIndex, item);
            emit dataChanged(index, index, QVector<int>() << role);
            return true;
        }
    }

    return false;
}

Qt::ItemFlags SystemsProbeTableModel::flags(const QModelIndex &index) const
{
    if (!index.isValid())
        return Qt::NoItemFlags;

    return Qt::ItemIsEditable;
}

QHash<int, QByteArray> SystemsProbeTableModel::roleNames() const
{
    QHash<int, QByteArray> names;
    names[tableDataRole] = "tableData";
    names[headingRole] = "heading";
    return names;
}

SystemProbe *SystemsProbeTableModel::list() const
{
    return mList;
}

void SystemsProbeTableModel::setList(SystemProbe *list)
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

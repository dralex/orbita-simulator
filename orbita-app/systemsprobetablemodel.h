#ifndef SYSTEMSPROBETABLEMODEL_H
#define SYSTEMSPROBETABLEMODEL_H

#include <QAbstractTableModel>
#include "systemprobe.h"

class SystemProbe;

class SystemsProbeTableModel : public QAbstractTableModel
{
    Q_OBJECT
    Q_PROPERTY(SystemProbe *list READ list WRITE setList)

public:
    explicit SystemsProbeTableModel(QObject *parent = nullptr);

    enum {
        tableDataRole = Qt::UserRole + 1,
        headingRole
    };

    int rowCount(const QModelIndex &parent = QModelIndex()) const override;
    int columnCount(const QModelIndex &parent = QModelIndex()) const override;

    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;

    bool setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole) override;

    Qt::ItemFlags flags(const QModelIndex &index) const override;
    virtual QHash<int, QByteArray> roleNames() const override;

    SystemProbe *list() const;
    void setList(SystemProbe *list);

private:
    SystemProbe *mList;
    QVector<QVector<QString>> table;
};

#endif // SYSTEMSPROBETABLEMODEL_H

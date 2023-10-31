#ifndef STEPSLANDINGTABLEMODEL_H
#define STEPSLANDINGTABLEMODEL_H

#include <QAbstractTableModel>
#include "stepslanding.h"

class StepsLanding;

class StepsLandingTableModel : public QAbstractTableModel
{
    Q_OBJECT
    Q_PROPERTY(StepsLanding *list READ list WRITE setList)

public:
    explicit StepsLandingTableModel(QObject *parent = nullptr);

    enum {
        tableDataRole = Qt::UserRole + 1,
        headingRole
    };

    int rowCount(const QModelIndex &parent = QModelIndex()) const override;
    int columnCount(const QModelIndex &parent = QModelIndex()) const override;

    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;

    bool setData(const QModelIndex &index, const QVariant &value,
                 int role = Qt::EditRole) override;

    Qt::ItemFlags flags(const QModelIndex &index) const override;
    virtual QHash<int, QByteArray> roleNames() const override;

    StepsLanding *list() const;
    void setList(StepsLanding *list);

private:
    StepsLanding *mList;
    QVector<QVector<QString>> table;
};

#endif // STEPSLANDINGTABLEMODEL_H

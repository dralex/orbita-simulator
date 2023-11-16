#ifndef STEPSACTIVITYTABLEMODEL_H
#define STEPSACTIVITYTABLEMODEL_H

#include <QAbstractTableModel>
#include "stepsactivity.h"

class StepsActivity;

class StepsActivityTableModel : public QAbstractTableModel
{
    Q_OBJECT
    Q_PROPERTY(StepsActivity *list READ list WRITE setList)

public:
    explicit StepsActivityTableModel(QObject *parent = nullptr);

    enum {
        tableDataRole = Qt::UserRole + 1,
        headingRole
    };

    int rowCount(const QModelIndex &parent = QModelIndex()) const override;
    int columnCount(const QModelIndex &parent = QModelIndex()) const override;

    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;

    bool setData(const QModelIndex &index, const QVariant &value, int role = Qt::EditRole) override;

    Qt::ItemFlags flags(const QModelIndex& index) const override;
    virtual QHash<int, QByteArray> roleNames() const override;

    StepsActivity *list() const;
    void setList(StepsActivity *list);

private:
    StepsActivity *mList;
    QVector<QVector<QString>> table;
};

#endif // STEPSACTIVITYTABLEMODEL_H

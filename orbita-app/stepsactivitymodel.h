#ifndef STEPSACTIVITYMODEL_H
#define STEPSACTIVITYMODEL_H

#include <QAbstractListModel>
#include "stepsactivity.h"

class StepsActivity;

class StepsActivityModel : public QAbstractListModel
{
    Q_OBJECT
    Q_PROPERTY(StepsActivity *list READ list WRITE setList)

public:
    explicit StepsActivityModel(QObject *parent = nullptr);

    enum {
        idRole = Qt::UserRole,
        deviceNumberRole,
        timeRole,
        deviceRole,
        commandRole,
        argumentRole
    };

    // Basic functionality:
    int rowCount(const QModelIndex &parent = QModelIndex()) const override;

    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;

    // Editable:
    bool setData(const QModelIndex &index, const QVariant &value,
                 int role = Qt::EditRole) override;

    Qt::ItemFlags flags(const QModelIndex& index) const override;

    virtual QHash<int, QByteArray> roleNames() const override;

    StepsActivity *list() const;
    void setList(StepsActivity *list);

private:
    StepsActivity *mList;
};

#endif // STEPSACTIVITYMODEL_H

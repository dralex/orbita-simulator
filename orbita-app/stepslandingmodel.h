#ifndef STEPSLANDINGMODEL_H
#define STEPSLANDINGMODEL_H

#include <QAbstractListModel>
#include "stepslanding.h"

class StepsLanding;

class StepsLandingModel : public QAbstractListModel
{
    Q_OBJECT
    Q_PROPERTY(StepsLanding *list READ list WRITE setList)

public:
    explicit StepsLandingModel(QObject *parent = nullptr);

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

    StepsLanding *list() const;
    void setList(StepsLanding *list);

private:
    StepsLanding *mList;
};

#endif // STEPSLANDINGMODEL_H

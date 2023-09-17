#ifndef PLANETSDEVICESMODEL_H
#define PLANETSDEVICESMODEL_H

#include <QAbstractListModel>
#include "planetdevices.h"

class PlanetDevices;

class PlanetsDevicesModel : public QAbstractListModel
{
    Q_OBJECT
    Q_PROPERTY(PlanetDevices *list READ list WRITE setList)

public:
    explicit PlanetsDevicesModel(QObject *parent = nullptr);

    enum {
        textRole
    };

    // Basic functionality:
    int rowCount(const QModelIndex &parent = QModelIndex()) const override;

    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;

    // Editable:
    bool setData(const QModelIndex &index, const QVariant &value,
                 int role = Qt::EditRole) override;

    Qt::ItemFlags flags(const QModelIndex& index) const override;

    virtual QHash<int, QByteArray> roleNames() const override;
    PlanetDevices *list() const;
    void setList(PlanetDevices *list);


private:
    PlanetDevices *mList;
};

#endif // PLANETSDEVICESMODEL_H

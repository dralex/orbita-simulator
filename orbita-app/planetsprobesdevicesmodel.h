#ifndef PLANETSPROBESDEVICESMODEL_H
#define PLANETSPROBESDEVICESMODEL_H

#include <QAbstractTableModel>
#include "devices.h"

class Devices;

class PlanetsProbesDevicesModel : public QAbstractTableModel
{
    Q_OBJECT
    Q_PROPERTY(Devices *list READ list WRITE setList)

public:
    explicit PlanetsProbesDevicesModel(QObject *parent = nullptr);


    enum {
        deviceNumberRole = Qt::UserRole,
        deviceNameRole,
        startStateRole,
        inSafeModeRole
    };

    // Basic functionality:
    int rowCount(const QModelIndex &parent = QModelIndex()) const override;
    int columnCount(const QModelIndex &parent = QModelIndex()) const override;

    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;

    // Editable:
    bool setData(const QModelIndex &index, const QVariant &value,
                 int role = Qt::EditRole) override;

    Qt::ItemFlags flags(const QModelIndex& index) const override;

    virtual QHash<int, QByteArray> roleNames() const override;

    Devices *list() const;
    void setList(Devices *list);


private:
    Devices *mList;
};

#endif // PLANETSPROBESDEVICESMODEL_H

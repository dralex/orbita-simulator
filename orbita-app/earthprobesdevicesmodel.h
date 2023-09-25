#ifndef EARTHPROBESDEVICESMODEL_H
#define EARTHPROBESDEVICESMODEL_H

#include <QAbstractListModel>
#include "earthprobedevices.h"

class EarthProbeDevices;

class EarthProbesDevicesModel : public QAbstractListModel
{
    Q_OBJECT
    Q_PROPERTY(EarthProbeDevices *list READ list WRITE setList)

public:
    explicit EarthProbesDevicesModel(QObject *parent = nullptr);

    enum {
        deviceNameRole,
        massRole,
        startModeRole,
    };

    // Basic functionality:
    int rowCount(const QModelIndex &parent = QModelIndex()) const override;

    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;

    // Editable:
    bool setData(const QModelIndex &index, const QVariant &value,
                 int role = Qt::EditRole) override;

    Qt::ItemFlags flags(const QModelIndex& index) const override;


    virtual QHash<int, QByteArray> roleNames() const override;

    EarthProbeDevices *list() const;
    void setList(EarthProbeDevices *list);

private:
    EarthProbeDevices *mList;
};

#endif // EARTHPROBESDEVICESMODEL_H

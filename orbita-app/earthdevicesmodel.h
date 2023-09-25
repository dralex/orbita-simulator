#ifndef EARTHDEVICESMODEL_H
#define EARTHDEVICESMODEL_H

#include <QAbstractListModel>
#include "earthdevices.h"

class EarthDevices;

class EarthDevicesModel : public QAbstractListModel
{
    Q_OBJECT
    Q_PROPERTY(EarthDevices *list READ list WRITE setList)

public:
    explicit EarthDevicesModel(QObject *parent = nullptr);

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
    EarthDevices *list() const;
    void setList(EarthDevices *list);

private:
    EarthDevices *mList;
};

#endif // EARTHDEVICESMODEL_H

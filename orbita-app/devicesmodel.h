#ifndef DEVICESMODEL_H
#define DEVICESMODEL_H

#include <QAbstractListModel>

class Devices;

class DevicesModel : public QAbstractListModel
{
    Q_OBJECT
    Q_PROPERTY(Devices *list READ list WRITE setList)

public:
    explicit DevicesModel(QObject *parent = nullptr);

    enum {
        deviceNumberRole = Qt::UserRole,
        deviceNameRole,
        startStateRole,
        inSafeModeRole
    };

    // Basic functionality:
    int rowCount(const QModelIndex &parent = QModelIndex()) const override;

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

#endif // DEVICESMODEL_H

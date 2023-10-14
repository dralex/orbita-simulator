#ifndef COMBOBOXDEVICES_H
#define COMBOBOXDEVICES_H

#include <QAbstractListModel>
#include "devices.h"

class Devices;

class ComboBoxDevices : public QAbstractListModel
{
    Q_OBJECT

    Q_PROPERTY(Devices *list READ list WRITE setList)

public:
    explicit ComboBoxDevices(QObject *parent = nullptr);

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
    Devices *list() const;
    void setList(Devices *list);


private:
    Devices *mList;
};

#endif // COMBOBOXDEVICES_H

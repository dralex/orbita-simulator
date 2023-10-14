#ifndef EARTHSYSTEMSMODEL_H
#define EARTHSYSTEMSMODEL_H

#include <QAbstractListModel>
#include "systems.h"

class Systems;

class EarthSystemsModel : public QAbstractListModel
{
    Q_OBJECT
    Q_PROPERTY(Systems *list READ list WRITE setList)

public:
    explicit EarthSystemsModel(QObject *parent = nullptr);

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
    Systems *list() const;
    void setList(Systems *list);

private:
    Systems *mList;
};

#endif // EARTHSYSTEMSMODEL_H

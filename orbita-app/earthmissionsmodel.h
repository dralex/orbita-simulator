#ifndef EARTHMISSIONSMODEL_H
#define EARTHMISSIONSMODEL_H

#include <QAbstractListModel>

#include "earthmissions.h"

class EarthMissions;

class EarthMissionsModel : public QAbstractListModel
{
    Q_OBJECT
    Q_PROPERTY(EarthMissions *list READ list WRITE setList)

public:
    explicit EarthMissionsModel(QObject *parent = nullptr);

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

    EarthMissions *list() const;
    void setList(EarthMissions *list);

private:
    EarthMissions *mList;
};

#endif // EARTHMISSIONSMODEL_H

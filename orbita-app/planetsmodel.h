#ifndef PLANETSMODEL_H
#define PLANETSMODEL_H

#include <QAbstractListModel>
#include "planets.h"

class Planet;

class PlanetsModel : public QAbstractListModel
{
    Q_OBJECT
    Q_PROPERTY(Planets *list READ list WRITE setList)

public:
    explicit PlanetsModel(QObject *parent = nullptr);

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
    Planets *list() const;
    void setList(Planets *list);


private:
    Planets *mList;
};

#endif // PLANETSMODEL_H

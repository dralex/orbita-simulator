#ifndef IMAGESMODEL_H
#define IMAGESMODEL_H

#include <QAbstractListModel>
#include "simulationcontroller.h"

class SimulationController;

class ImagesModel : public QAbstractListModel
{
    Q_OBJECT
    Q_PROPERTY(SimulationController *list READ list WRITE setList)


public:
    explicit ImagesModel(QObject *parent = nullptr);

    enum {
        imageSourceRole
    };

    // Basic functionality:
    int rowCount(const QModelIndex &parent = QModelIndex()) const override;

    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;

    // Editable:
    bool setData(const QModelIndex &index, const QVariant &value,
                 int role = Qt::EditRole) override;

    Qt::ItemFlags flags(const QModelIndex& index) const override;
    virtual QHash<int, QByteArray> roleNames() const override;
    SimulationController *list() const;
    void setList(SimulationController *list);

private:
    SimulationController *mList;
};

#endif // IMAGESMODEL_H

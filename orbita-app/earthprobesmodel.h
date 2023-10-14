#ifndef EARTHPROBESMODEL_H
#define EARTHPROBESMODEL_H

#include <QAbstractListModel>

#include "earthprobe.h"

class EarthProbe;

class EarthProbesModel : public QAbstractListModel
{
    Q_OBJECT
    Q_PROPERTY(EarthProbe *list READ list WRITE setList)
public:
    explicit EarthProbesModel(QObject *parent = nullptr);

    enum {
        probeNumberRole = Qt::UserRole,
        probeNameRole,
        missionRole,
        fuelRole,
        voltageRole,
        xz_yz_solarRole,
        xz_yz_radiatorRole,
        xy_radiatorRole,
        pythonCodeRole,
        filePathRole
    };

    // Basic functionality:
    int rowCount(const QModelIndex &parent = QModelIndex()) const override;

    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;

    // Editable:
    bool setData(const QModelIndex &index, const QVariant &value,
                 int role = Qt::EditRole) override;

    Qt::ItemFlags flags(const QModelIndex& index) const override;

    virtual QHash<int, QByteArray> roleNames() const override;

    EarthProbe *list() const;
    void setList(EarthProbe *list);

private:
    EarthProbe *mList;
};

#endif // EARTHPROBESMODEL_H

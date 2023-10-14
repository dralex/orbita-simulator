#ifndef PROBEMODEL_H
#define PROBEMODEL_H

#include "devicesmodel.h"

class Probe;

class ProbeModel : public QAbstractListModel
{
    Q_OBJECT
    Q_PROPERTY(Probe *list READ list WRITE setList)


public:
    explicit ProbeModel(QObject *parent = nullptr);

    enum {
        probeNumberRole = Qt::UserRole,
        probeNameRole,
        missionRole,
        outerRadiusRole,
        innerRadiusRole,
        pythonCodeRole,
        filePathRole,
    };

    // Basic functionality:
    int rowCount(const QModelIndex &parent = QModelIndex()) const override;

    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;

    // Editable:
    bool setData(const QModelIndex &index, const QVariant &value,
                 int role = Qt::EditRole) override;

    Qt::ItemFlags flags(const QModelIndex& index) const override;

    virtual QHash<int, QByteArray> roleNames() const override;

    Probe *list() const;
    void setList(Probe *list);

private:
    Probe *mList;
};

#endif // PROBEMODEL_H

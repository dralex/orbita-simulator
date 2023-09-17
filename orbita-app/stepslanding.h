#ifndef STEPSLANDING_H
#define STEPSLANDING_H

#include <QObject>
#include <QVector>
#include "probe.h"

class Probe;

struct StepsLandingItem {
    int id;
    int deviceNumber;
    double time;
    QString device;
    QString command;
    int argument;
};

class StepsLanding : public QObject
{
    Q_OBJECT
public:
    explicit StepsLanding(QObject *parent = nullptr);
    const QVector<StepsLandingItem> items() const;

    bool setItem(int index, const StepsLandingItem &item);

signals:
    void preItemAppended();
    void postItemAppended();

    void preItemRemoved(int index);
    void postItemRemoved();

public slots:
    void appendItem(Probe* probe, bool typeCommand, int probeIndex, int deviceNumber,  double time, QString device, QString command, int argument);
    void removeItem(Probe* probe, bool typeCommand, int probeIndex, int index);
    void changeSteps(Probe* probe, int probeIndex);

    int size();

private:
    QVector<StepsLandingItem> mItems;
};

#endif // STEPSLANDING_H

#ifndef DEVICES_H
#define DEVICES_H

#include <QObject>
#include <QVector>
#include "probe.h"
#include "stepsactivity.h"
#include "stepslanding.h"

class Probe;
class StepsActivity;
class StepsLanding;

struct DevicesItem
{
    int id;
    int deviceNumber;
    QString deviceName;
    QString deviceCode;
    QString deviceEngName;
    QString startState;
    bool inSafeMode;
};

class Devices : public QObject
{
    Q_OBJECT
public:
    explicit Devices(QObject *parent = nullptr);

    QVector<DevicesItem> items() const;

    bool setDevicesItem(int index, const DevicesItem &item);

signals:
    void preDevicesItemAppended();
    void postDevicesItemAppended();

    void preDevicesItemRemoved(int index);
    void postDevicesItemRemoved();

    void preDevicesItemCleared();
    void postDevicesItemCleared();

public slots:
    void appendDevicesItem(Probe* probe, int probeIndex, QString deviceName, QString deviceCode, QString deviceEngName, QString startState, bool inSafeMode);
    void removeDevicesItem(Probe* probe, StepsActivity* stepsActivity, StepsLanding* stepsLanding, int probeIndex, int index);

    void changeDevices(Probe* probe, int probeIndex);

    int size();

private:
    QVector<DevicesItem> mItems;
};

#endif // DEVICES_H

#ifndef EARTHPROBEDEVICES_H
#define EARTHPROBEDEVICES_H

#include <QObject>
#include <QVector>
#include "earthprobe.h"

class EarthProbe;

struct EarthProbeDeviceItem {
    int id;
    QString deviceEngName;
    QString deviceName;
    double mass;
    bool startMode;
};

class EarthProbeDevices : public QObject
{
    Q_OBJECT
public:
    explicit EarthProbeDevices(QObject *parent = nullptr);

    QVector<EarthProbeDeviceItem> items() const;

    bool setEarthProbesDevices(int index, const EarthProbeDeviceItem &item);

signals:
    void preEarthProbeDeviceAppended();
    void postEarthProbeDeviceAppended();

    void preEarthProbeDeviceRemoved(int index);
    void postEarthProbeDeviceRemoved();

public slots:
    void appendEarthDevice(EarthProbe* earthProbe, int probeIndex, QString deviceEngName, QString deviceName, double mass, bool startMode);
    void removeEarthDevice(EarthProbe* earthProbe, int probeIndex, int index);

    void changeEarthDevices(EarthProbe* earthProbe, int probeIndex);

    int size();

private:
        QVector<EarthProbeDeviceItem> mItems;
};

#endif // EARTHPROBEDEVICES_H

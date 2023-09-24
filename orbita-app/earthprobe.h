#ifndef EARTHPROBE_H
#define EARTHPROBE_H

#include <QObject>
#include <QVector>
#include "earthprobedevices.h"

struct EarthProbeDeviceItem;

struct EarthProbeItem
{
    int probeNumber;
    QString probeName;
    QString missionName;
    QVector<EarthProbeDeviceItem> devices;
    QString pythonCode;
    QString diagrammPath;
    QString filePath;
};

class EarthProbe : public QObject
{
    Q_OBJECT
public:
    explicit EarthProbe(QObject *parent = nullptr);

    QVector<EarthProbeItem> items() const;

    bool setEarthProbe(int index, const EarthProbeItem &item);

signals:
    void preEarthProbeAppended();
    void postEarthProbeAppended();

    void preEarthProbeRemoved(int index);
    void postEarthProbeRemoved();

    void preEarthDeviceAppended();
    void postEarthDeviceAppended();

    void preEarthDeviceRemoved(int index);
    void postEarthDeviceRemoved();


public slots:
    void appendEarthProbe(QString probeName, QString missionName, QString filePath);
    void appendEarthDevice(int probeIndex, QString deviceEngName, QString deviceName, double mass);
    void removeEarthDevice(int probeIndex,int index);

    int size();
//    void saveEarthProbeToXml();
//    void loadEarthProbeFromXml(const QString &path);

private:
    QVector<EarthProbeItem> mItems;
};

#endif // EARTHPROBE_H

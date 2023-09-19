#ifndef EARTHPROBEDEVICES_H
#define EARTHPROBEDEVICES_H

#include <QObject>
#include <QVector>

struct EarthProbeDeviceItem {
    int id;
    QString deviceEngName;
    QString deviceName;
    double mass;
};

class EarthProbeDevices : public QObject
{
    Q_OBJECT
public:
    explicit EarthProbeDevices(QObject *parent = nullptr);

signals:
private:
        QVector<EarthProbeDeviceItem> mItems;
};

#endif // EARTHPROBEDEVICES_H

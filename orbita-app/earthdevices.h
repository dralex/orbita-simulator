#ifndef EARTHDEVICES_H
#define EARTHDEVICES_H

#include <QObject>
#include <QVector>
#include <QFile>
#include <QDebug>
#include <QXmlStreamReader>

struct EarthDevicesItem {
    int id;
    QString deviceEngName;
    QString deviceName;
    double mass;
};

class EarthDevices : public QObject
{
    Q_OBJECT
public:
    explicit EarthDevices(QObject *parent = nullptr);

public slots:
    void loadDevices(const QString &filePath);
    void showDevices();

signals:
    void preEarthDeviceAppended();
    void postEarthDeviceAppended();

    void postEarthDeviceRemoved(int index);
    void preEarthDeviceRemoved();

private:
    QVector<EarthDevicesItem> mItems;

};

#endif // EARTHDEVICES_H

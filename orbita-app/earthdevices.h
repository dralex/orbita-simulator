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

    QVector<EarthDevicesItem> items() const;

    bool setEarthDevices(int index, const EarthDevicesItem &item);

public slots:
    void loadDevices(const QString &filePath);
    void showDevices();

    QString getDeviceEngName(QString deviceName);
    double getMass(QString deviceName);

    int size();

signals:
    void preEarthDeviceAppended();
    void postEarthDeviceAppended();

    void preEarthDeviceRemoved(int index);
    void postEarthDeviceRemoved();

private:
    QVector<EarthDevicesItem> mItems;

};

#endif // EARTHDEVICES_H

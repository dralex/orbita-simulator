#ifndef PLANETSDEVICES_H
#define PLANETSDEVICES_H

#include <QObject>
#include <QVector>
#include <QFile>
#include <QXmlStreamReader>
#include <QXmlSchema>
#include <QXmlSchemaValidator>
#include <QDebug>

struct PlanetDeviceItems {
    int id;
    QString deviceEngName;
    QString deviceName;
    QString deviceCode;

};

class PlanetDevices : public QObject
{
    Q_OBJECT
public:
    explicit PlanetDevices(QObject *parent = nullptr);
    QVector<PlanetDeviceItems> items() const;

    bool setPlanetDevices(int index, const PlanetDeviceItems &item);

signals:
   void prePlanetDeviceAppended();
   void postPlanetDeviceAppended();

   void prePlanetDeviceRemoved(int index);
   void postPlanetDeviceRemoved();

public slots:
   QString getDeviceCode(QString deviceName);
   QString getDeviceEngName(QString deviceName);
   QString getDeviceName(QString deviceEngName);
   void loadDevices(const QString &filePath);
   int size();

private:
    QVector<PlanetDeviceItems> mItems;
};

#endif // PLANETSDEVICES_H

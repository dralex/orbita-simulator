#ifndef PROBE_H
#define PROBE_H

#include <QObject>
#include <QVector>
#include <QFile>
#include <QXmlStreamWriter>
#include "devices.h"
#include "stepsactivity.h"
#include "stepslanding.h"
#include "planets.h"
#include "planetdevices.h"
#include "settingsmanager.h"

struct DevicesItem;
struct StepsActivityItem;
struct StepsLandingItem;

struct ProbeItem
{
    int probeNumber;
    QString probeName;
    QString missionName;
    double outerRadius;
    double innerRadius;
    QVector<DevicesItem> devices;
    QVector<StepsActivityItem> stepsActivity;
    QVector<StepsLandingItem> stepsLanding;
    QString pythonCode;
    QString filePath;
};

class Planets;
class PlanetDevices;
class SettingsManager;

class Probe : public QObject
{
    Q_OBJECT

public:
    explicit Probe(QObject *parent = nullptr);

    QVector<ProbeItem> items() const;

    bool setProbe(int index, const ProbeItem &item);

signals:
   void preProbeAppended();
   void postProbeAppended();
   void preProbeRemoved(int index);
   void postProbeRemoved();

   void preDevicesItemAppended();
   void postDevicesItemAppended();
   void preDevicesItemRemoved(int index);
   void postDevicesItemRemoved();

   void preActivityAndLandingItemAppended();
   void postActivityAndLandingItemAppended();
   void preActivityAndLandingItemRemoved(int index);
   void postActivityAndLandingItemRemoved();

public slots:
    void appendProbe(QString probeName, QString missionName, double outerRadius, double innerRadius, QString pythonCode);
    void saveProbe(int probeIndex, QString probeName, double innerRadius, double outerRadius, QString pythonCode, const QString &filePath);

    void appendDevicesItem(int probeIndex, int deviceNumber, QString deviceName, QString deviceCode,  QString deviceEngName, QString startState, bool inSafeMode);
    void removeDevicesItem(int probeIndex,int index);

    void appendActivityAndLandingItem(int probeIndex, bool typCommand, int deviceNumber, double time, QString device, QString command, int argument);
    void removeActivityAndLandingItem(int probeIndex, bool typeCommand, int index);

    void saveToXml(int probeIndex, Planets *planetsData, int planetIndex, const QString &filename);
    void loadFromXml(QString filename, PlanetDevices *planetDevicesData, SettingsManager *settingsManager);

    int size();

private:
    QVector<ProbeItem> mItems;
};



#endif // PROBE_H

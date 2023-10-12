#ifndef EARTHPROBE_H
#define EARTHPROBE_H

#include <QObject>
#include <QVector>
#include <QDebug>
#include <QRandomGenerator>
#include "systemprobe.h"
#include "earthmissions.h"
#include "systems.h"
#include "systemprobe.h"

struct SystemItem;

struct EarthMessage {
    int msgfrom;
    int msgto;
};

struct DiagrammPathes {
    int id;
    QString systemEngName;
    QString path;
};

struct EarthProbeItem
{
    int probeNumber;
    QString probeName;
    QString missionName;
    double fuel;
    double voltage;
    double xz_yz_solar_panel_fraction;
    double xz_yz_radiator_fraction;
    double xy_radiator_fraction;
    QVector<SystemItem> systems;
    QString pythonCode;
    QVector<DiagrammPathes> diagrammPathes;
    QString filePath;
};

class EarthMissions;
class Systems;
class SystemProbe;

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

    void preEarthSystemAppended();
    void postEarthSystemAppended();

    void preEarthSystemRemoved(int index);
    void postEarthSystemRemoved();


public slots:
    void appendEarthProbe(QString probeName, QString missionName, QString pythonCode, QString filePath);
    void appendEarthDevice(int probeIndex, QString systemEngName, QString systemName,  QString type, double mass, bool startMode);
    void removeEarthDevice(int probeIndex,int index);

    void saveEarthProbe(int probeIndex, QString probeName, double fuel, double voltage,
                        double xz_yz_solar_panel_fraction, double xz_yz_radiator_fraction, double xy_radiator_fraction,
                        QString filePath);

    void appendDiagramm(int probeIndex, QString systemEngName, QString path);
    void removeDiagramm(int probeIndex, QString systemEngName);

    int size();
    void saveEarthProbeToXml(int probeIndex, EarthMissions *missions,  int missionIndex,
                             const QString &filename, const QString &oldFilename);
    void loadEarthProbeFromXml(const QString &path, Systems *systems, EarthMissions *missions);

private:
    QString generateIntData(QVector<int>);
    QString generateDoubleData(QVector<double>);
    QString generateRandomString();
    QList<EarthMessage> generateRandomMessages(int stationCount);
    QVector<EarthProbeItem> mItems;
};

#endif // EARTHPROBE_H

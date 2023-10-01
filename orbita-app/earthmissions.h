#ifndef EARTHMISSIONS_H
#define EARTHMISSIONS_H

#include <QObject>
#include <QVector>
#include <QFile>
#include <QXmlStreamReader>
#include <QDebug>

struct ControlStations {
    int id;
    QString name;
    QVector<double> fromToNumbers;
};

struct Messages {
   int id;
   QVector<double> data;
   QVector<double> timeout;
   int msgto;
   int msgfrom;
};

struct Missiles {
    int id;
    QVector<double> locatonAngle;
    QVector<double> launchTime;

};

struct EarthMissionsItem {
    int id;
    QString missionEngName;
    QString missionName;
    QString missionDescription;
    double duration;
    QVector<ControlStations> controlStations;
    QVector<double> orbitData;
    QVector<double> precision;
    QVector<double> lengthOfOnewayMessage;
    QVector<double> resolution;
    QVector<double> start_angular_velocity;
    QVector<double> target_angle;
    QVector<double> target_orbit;
    QVector<double> channel;
};

class EarthMissions : public QObject
{
    Q_OBJECT
public:
    explicit EarthMissions(QObject *parent = nullptr);

    QVector<EarthMissionsItem> items() const;

    bool setMissions(int index, const EarthMissionsItem &item);

public slots:
    void loadMissions(const QString &filePath);
    void showMissions();

    QString getMissionEngName(QString missionName);

    int size();


signals:
    void preEarthMissionsItemAppended();
    void postEarthMissionsItemAppended();

    void preEarthMissionsItemRemoved(int index);
    void postEarthMissionsItemRemoved();


private:
    QVector<EarthMissionsItem> mItems;

};

#endif // EARTHMISSIONS_H

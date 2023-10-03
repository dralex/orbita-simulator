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
   int number;
   QVector<double> data;
   QVector<double> timeout;
   int msgto;
   int msgfrom;
};

struct Missiles {
    int id;
    int number;
    QVector<double> locatonAngle;
    QVector<double> launchTime;
    int cooldown;

};

struct OnewayMessage {
    int id;
    QVector<double> length;
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
    QVector<OnewayMessage> onewayMessages;
    QVector<Missiles> missiles;
    QVector<Messages> messages;
    QVector<double> resolution;
    QVector<double> startAngularVelocity;
    QVector<double> targetAngle;
    QVector<double> targetOrbit;
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

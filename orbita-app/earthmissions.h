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

struct Message {
   int number;
   QVector<int> data;
   QVector<int> timeout;
};

struct Missiles {
    int id;
    int number;
    QVector<double> locatonAngle;
    QVector<int> launchTime;
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
    int duration;
    QVector<ControlStations> controlStations;
    QVector<int> orbitData;
    QVector<double> precision;
    QVector<OnewayMessage> onewayMessages;
    QVector<Missiles> missiles;
    Message message;
    QVector<double> resolution;
    QVector<double> targetAngle;
    QVector<int> targetOrbit;
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

#ifndef EARTHMISSIONS_H
#define EARTHMISSIONS_H

#include <QObject>
#include <QVector>
#include <QFile>
#include <QXmlStreamReader>
#include <QDebug>

struct EarthMissionsItem {
    int id;
    QString missionEngName;
    QString missionName;
    QString missionDescription;
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

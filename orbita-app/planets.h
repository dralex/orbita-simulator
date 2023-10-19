#ifndef PLANETS_H
#define PLANETS_H

#include <QObject>
#include <QVector>
#include <QFile>
#include <QDebug>
#include <QXmlStreamWriter>

struct PlanetsItem {
    int id;
    QString planetName;
    double height;
};

class Planets : public QObject
{
    Q_OBJECT
public:
    explicit Planets(QObject *parent = nullptr);

    QVector<PlanetsItem> items() const;

    bool setPlanets(int index, const PlanetsItem &item);

signals:
    void prePlanetsItemAppended();
    void postPlanetsItemAppended();

    void prePlanetsItemRemoved(int index);
    void postPlanetsItemRemoved();

public slots:
    void loadPlanets(const QString &filePath);
    int size();
private:
    bool checkUnique(QString planetName);
    QVector<PlanetsItem> mItems;
};

#endif // PLANETS_H

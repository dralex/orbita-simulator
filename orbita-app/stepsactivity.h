#ifndef STEPSACTIVITY_H
#define STEPSACTIVITY_H

#include <QObject>
#include <QVector>
#include "probe.h"

class Probe;

struct StepsActivityItem {
    int id;
    int deviceNumber;
    double time;
    QString device;
    QString command;
    int argument;
};

class StepsActivity : public QObject
{
    Q_OBJECT
public:
    explicit StepsActivity(QObject *parent = nullptr);
    const QVector<StepsActivityItem> items() const;

    bool setItem(int index, const StepsActivityItem &item);
signals:
    void preItemAppended();
    void postItemAppended();

    void preItemRemoved(int index);
    void postItemRemoved();

public slots:
    void appendItem(Probe* probe, bool typeCommand, int probeIndex, int deviceNumber, double time, QString device, QString command, int argument);
    void removeItem(Probe* probe, bool typeCommand, int probeIndex, int index);
    void changeSteps(Probe* probe, int probeIndex);

    int size();

private:
    QVector<StepsActivityItem> mItems;
};

#endif // STEPSACTIVITY_H

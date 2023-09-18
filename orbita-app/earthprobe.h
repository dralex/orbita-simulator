#ifndef EARTHPROBE_H
#define EARTHPROBE_H

#include <QObject>
#include <QVector>

struct EarthProbeItem
{
    int probeNumber;
    QString probeName;
    QString missionName;
    QString subsystem;
    QString devices;
    QString pythonCode;
    QString diagrammPath;
    QString filePath;
};

class EarthProbe : public QObject
{
    Q_OBJECT
public:
    explicit EarthProbe(QObject *parent = nullptr);

signals:
private:
    QVector<EarthProbeItem> mItems;
};

#endif // EARTHPROBE_H

#ifndef SYSTEMPROBE_H
#define SYSTEMPROBE_H

#include <QObject>
#include <QVector>
#include "earthprobe.h"

class EarthProbe;

struct SystemItem {
    int id;
    QString systemEngName;
    QString systemName;
    QString type;
    double mass;
    bool startMode;
    QString diagramPath;
};

class SystemProbe : public QObject
{
    Q_OBJECT
public:
    explicit SystemProbe(QObject *parent = nullptr);

    QVector<SystemItem> items() const;

    bool setEarthProbesSystems(int index, const SystemItem &item);

signals:
    void preEarthProbeSystemsAppended();
    void postEarthProbeSystemsAppended();

    void preEarthProbeSystemsRemoved(int index);
    void postEarthProbeSystemsRemoved();

public slots:
    void appendEarthSystem(EarthProbe* earthProbe, int probeIndex, QString systemEngName, QString systemName, QString type, double mass, bool startMode);
    void removeEarthSystem(EarthProbe* earthProbe, int probeIndex, int index);
    void appendDiagramPath(QString systemEngName, QString diagramPath);

    QString getText(int row, int column);

    bool checkUniqueType(QString type);

    void changeEarthSystems(EarthProbe* earthProbe, int probeIndex);


    int size();

private:
        QVector<SystemItem> mItems;
};

#endif // SYSTEMPROBE_H

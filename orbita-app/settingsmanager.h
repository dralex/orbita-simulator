#ifndef SETTINGSMANAGER_H
#define SETTINGSMANAGER_H

#include <QObject>
#include <QFile>
#include <QTextStream>

class SettingsManager : public QObject
{
    Q_OBJECT
public:
    explicit SettingsManager(QObject *parent = nullptr);

public slots:
    QString getProbesPath() const;
    QString getSimulationPath() const;
    QString getDevicesPath() const;
    QString getPlanetsPath() const;

    void setProbesPath(const QString &path);
    void setSimulationPath(const QString &path);
    void setDevicesPath(const QString &path);
    void setPlanetsPath(const QString &path);

    bool loadSettingsFromFile(const QString &filePath);
    bool saveSettingsToFile(const QString &filePath);

    bool checkSimulationFile(const QString &filePath);

private:
    QString probesPath = "/home/";
    QString simulationPath = "/home/";
    QString devicesPath = "/home/";
    QString planetsPath = "/home/";
};

#endif // SETTINGSMANAGER_H

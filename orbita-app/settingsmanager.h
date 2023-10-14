#ifndef SETTINGSMANAGER_H
#define SETTINGSMANAGER_H

#include <QObject>
#include <QFile>
#include <QTextStream>
#include <QDebug>

class SettingsManager : public QObject
{
    Q_OBJECT
public:
    explicit SettingsManager(QObject *parent = nullptr);


public slots:
    const QString getEarthSimulationPath() const;
    void setEarthSimulationPath(const QString &path);

    const QString getEarthSystemsPath() const;
    void setEarthSystemsPath(const QString &path);

    const QString getEarthProbesPath() const;
    void setEarthProbesPath(const QString &path);

    const QString getMissionsPath() const;
    void setMissionsPath(const QString &path);

    const QString getEarthCalculatorPath() const;
    void setEarthCalculatorPath(const QString &path);

    const QString getPlanetsProbesPath() const;
    void setProbesPath(const QString &path);

    const QString getSimulationPath() const;
    void setSimulationPath(const QString &path);

    const QString getDevicesPath() const;
    void setDevicesPath(const QString &path);

    const QString getPlanetsPath() const;
    void setPlanetsPath(const QString &path);

    const QString getPlanetsCalculatorPath() const;
    void setPlanetsCalculatorPath(const QString &path);

    bool loadSettingsFromFile(const QString &filePath, bool typeMission);
    bool saveSettingsToFile(const QString &filePath, bool typeMission);

    bool checkSimulationFile(const QString &filePath);

private:
    QString planetsProbesPath = "None";
    QString planetsSimulationPath = "None";
    QString planetsDevicesPath = "None";
    QString planetsPath = "None";
    QString planetCalculatorPath = "None";

    QString earthSimulationPath = "None";
    QString earthDevicesPath = "None";
    QString earthProbesPath = "None";
    QString missionPath = "None";
    QString earthCalculatorPath = "None";
};

#endif // SETTINGSMANAGER_H

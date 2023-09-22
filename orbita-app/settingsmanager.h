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
    QString getPlanetsProbesPath() const;
    QString getSimulationPath() const;
    QString getDevicesPath() const;
    QString getPlanetsPath() const;
    QString getPlanetsCalculatorPath() const;

    void setProbesPath(const QString &path);
    void setSimulationPath(const QString &path);
    void setDevicesPath(const QString &path);
    void setPlanetsPath(const QString &path);
    void setPlanetsCalculatorPath(const QString &path);

    bool loadSettingsFromFile(const QString &filePath);
    bool saveSettingsToFile(const QString &filePath);

    bool checkSimulationFile(const QString &filePath);

private:
    QString planetsProbesPath = "None";
    QString planetsSimulationPath = "None";
    QString devicesPath = "None";
    QString planetsPath = "None";
    QString planetCalculatorPath = "None";
};

#endif // SETTINGSMANAGER_H

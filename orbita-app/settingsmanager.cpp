#include "settingsmanager.h"

SettingsManager::SettingsManager(QObject *parent) : QObject(parent)
{
}

QString SettingsManager::getPlanetsProbesPath() const
{
    return planetsProbesPath;
}

QString SettingsManager::getSimulationPath() const
{
    return planetsSimulationPath;
}

QString SettingsManager::getDevicesPath() const
{
    return devicesPath;
}

QString SettingsManager::getPlanetsPath() const
{
    return planetsPath;
}

QString SettingsManager::getPlanetsCalculatorPath() const
{
    return planetCalculatorPath;
}

void SettingsManager::setProbesPath(const QString &path)
{
    planetsProbesPath = path;
}

void SettingsManager::setSimulationPath(const QString &path)
{
    planetsSimulationPath = path;
}

void SettingsManager::setDevicesPath(const QString &path)
{
    devicesPath = path;
}

void SettingsManager::setPlanetsPath(const QString &path)
{
    planetsPath = path;
}

void SettingsManager::setPlanetsCalculatorPath(const QString &path)
{
    planetCalculatorPath = path;
}

bool SettingsManager::loadSettingsFromFile(const QString &filePath)
{
    QFile file(filePath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        return false;
    }

    QTextStream in(&file);
    while (!in.atEnd()) {
        QString line = in.readLine();
        if (line.startsWith("simulation_path=")) {
            planetsSimulationPath = line.mid(16);
        } else if (line.startsWith("probes_path=")) {
            planetsProbesPath = line.mid(12);
        } else if (line.startsWith("devices_path=")) {
            devicesPath = line.mid(13);
        } else if (line.startsWith("planets_path=")) {
            planetsPath = line.mid(13);
        } else if (line.startsWith("planets_calculator_path="))
            planetCalculatorPath = line.mid(24);
    }

    file.close();
    return true;
}

bool SettingsManager::saveSettingsToFile(const QString &filePath)
{
    QFile file(filePath);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text)) {
        return false;
    }

    QTextStream out(&file);
    out << "simulation_path=" << planetsSimulationPath << "\n";
    out << "probes_path=" << planetsProbesPath << "\n";
    out << "devices_path=" << devicesPath << "\n";
    out << "planets_path=" << planetsPath << "\n";
    out << "planets_calculator_path=" << planetCalculatorPath << "\n";

    file.close();
    return true;
}

bool SettingsManager::checkSimulationFile(const QString &filePath)
{
    QFile file(filePath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        return false;
    }

    file.close();
    return true;
}

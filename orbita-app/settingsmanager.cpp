#include "settingsmanager.h"

SettingsManager::SettingsManager(QObject *parent) : QObject(parent)
{
}

const QString SettingsManager::getPlanetsProbesPath() const
{
    return planetsProbesPath;
}

const QString SettingsManager::getSimulationPath() const
{
    return planetsSimulationPath;
}

const QString SettingsManager::getDevicesPath() const
{
    return planetsDevicesPath;
}

const QString SettingsManager::getPlanetsPath() const
{
    return planetsPath;
}

const QString SettingsManager::getPlanetsCalculatorPath() const
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
    planetsDevicesPath = path;
}

void SettingsManager::setPlanetsPath(const QString &path)
{
    planetsPath = path;
}

void SettingsManager::setPlanetsCalculatorPath(const QString &path)
{
    planetCalculatorPath = path;
}

bool SettingsManager::loadSettingsFromFile(const QString &filePath, bool typeMission) {
    QFile file(filePath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        return false;
    }
    QTextStream in(&file);
    if (typeMission) {
        while (!in.atEnd()) {
            QString line = in.readLine();
            if (line.startsWith("simulation_path=")) {
                planetsSimulationPath = line.mid(16);
            } else if (line.startsWith("probes_path=")) {
                planetsProbesPath = line.mid(12);
            } else if (line.startsWith("devices_path=")) {
                planetsDevicesPath = line.mid(13);
            } else if (line.startsWith("planets_path=")) {
                planetsPath = line.mid(13);
            } else if (line.startsWith("planets_calculator_path=")) {
                planetCalculatorPath = line.mid(24);
            }
        }
        file.close();
        return true;
    } else {
        while (!in.atEnd()) {
            QString line = in.readLine();
            if (line.startsWith("earth_simulation_path=")) {
                earthSimulationPath = line.mid(22);
            } else if (line.startsWith("earth_devices_path=")) {
                earthDevicesPath = line.mid(19);
            } else if (line.startsWith("earth_probes_path=")) {
                earthProbesPath = line.mid(18);
            } else if (line.startsWith("earth_missions_path=")) {
                missionPath = line.mid(20);
            } else if (line.startsWith("earth_calculator_path=")) {
                earthCalculatorPath = line.mid(22);
            }
        }
        file.close();
        return true;
    }
}

bool SettingsManager::saveSettingsToFile(const QString &filePath, bool typeMission) {
    QFile file(filePath);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text)) {
        return false;
    }

    QTextStream out(&file);

    if (typeMission) {
        out << "simulation_path=" << planetsSimulationPath << "\n";
        out << "probes_path=" << planetsProbesPath << "\n";
        out << "devices_path=" << planetsDevicesPath << "\n";
        out << "planets_path=" << planetsPath << "\n";
        out << "planets_calculator_path=" << planetCalculatorPath << "\n";
    } else {
        out << "earth_simulation_path=" << earthSimulationPath << "\n";
        out << "earth_devices_path=" << earthDevicesPath << "\n";
        out << "earth_probes_path=" << earthProbesPath << "\n";
        out << "earth_missions_path=" << missionPath << "\n";
        out << "earth_calculator_path=" << earthCalculatorPath << "\n";
    }

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

const QString SettingsManager::getEarthCalculatorPath() const
{
    return earthCalculatorPath;
}

void SettingsManager::setEarthCalculatorPath(const QString &path)
{
    earthCalculatorPath = path;
}

const QString SettingsManager::getMissionsPath() const
{
    return missionPath;
}

void SettingsManager::setMissionsPath(const QString &path)
{
    missionPath = path;
}

const QString SettingsManager::getEarthProbesPath() const
{
    return earthProbesPath;
}

void SettingsManager::setEarthProbesPath(const QString &path)
{
    earthProbesPath = path;
}

const QString SettingsManager::getEarthSystemsPath() const
{
    return earthDevicesPath;
}

void SettingsManager::setEarthSystemsPath(const QString &path)
{
    earthDevicesPath = path;
}

const QString SettingsManager::getEarthSimulationPath() const
{
    return earthSimulationPath;
}

void SettingsManager::setEarthSimulationPath(const QString &path)
{
    earthSimulationPath = path;
}

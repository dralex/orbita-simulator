#include "simulationcontroller.h"

SimulationController::SimulationController(QObject *parent) : QObject(parent)
{
    simulationProcess = new QProcess(this);

    connect(simulationProcess, SIGNAL(finished(int, QProcess::ExitStatus)), this, SLOT(processFinished(int, QProcess::ExitStatus)));
}

QVector<ImageItem> SimulationController::imagesItems() const
{
    return images;
}

bool SimulationController::setImages(int index, const ImageItem &item)
{
    if (index < 0 || index >= images.size())
        return false;

    const ImageItem &olditem = images.at(index);
    if (item.imageSource == olditem.imageSource)
        return false;

    images[index] = item;
    return true;
}

QString SimulationController::getStandardOutput() const
{
    return mStandardOutput;
}

QString SimulationController::getStandardError() const
{
    return mStandardError;
}

QString SimulationController::missionStatus() const
{
    return mMissionStatus;
}



void SimulationController::startSimulation(QString probePath, SettingsManager *settingsManager, bool typeMission)
{
    QString process;
    QString infoFolderPath;
    QString simulationPath;
    if (simulationProcess->state() != QProcess::NotRunning) {
        qDebug() << "Симуляция уже запущена или завершается.";
        return;
    }

    if (typeMission) {
        simulationPath = settingsManager->getSimulationPath() + "/simulation.py";
        currentProbePath = probePath;
        infoFolderPath = currentProbePath.left(currentProbePath.length() - 4) + "_info";
        QDir infoFolder(infoFolderPath);
        if (!infoFolder.exists()) {
            if (!infoFolder.mkpath(infoFolderPath)) {
                qDebug() << "Ошибка при создании папки info";
                return;
            }
        }
    } else {
        simulationPath = settingsManager->getEarthSimulationPath() + "/simulation.py";
        currentProbePath = probePath;
        infoFolderPath = currentProbePath.left(currentProbePath.length() - 4) + "_info";
        QDir infoFolder(infoFolderPath);
        if (!infoFolder.exists()) {
            if (!infoFolder.mkpath(infoFolderPath)) {
                qDebug() << "Ошибка при создании папки info";
                return;
            }
        }
    }

    QStringList arguments;
    arguments << simulationPath << currentProbePath
              << "--mission-log=" + infoFolderPath + "/telemetry.log"
              << "--image=" + infoFolderPath + "/.";
    if (QSysInfo::productType() == "windows")
        process = "python";
    else
        process = "python3";

    whatIsSimulator = true;
    mMissionStatus = "Cимуляция в процессе.";
    emit updateMissionStatus(mMissionStatus);
    simulationProcess->start(process, arguments);
}

void SimulationController::startCalculatorSimulation(SettingsManager *settingsManager, bool typeMission)
{
    QString process;
    QString infoFolderPath = QDir::currentPath() + "/" + planetCalculatorData.planetName + "_info";
    QString simulationPath = settingsManager->getPlanetsCalculatorPath() + "/simulation.py";


    if (simulationProcess->state() != QProcess::NotRunning) {
        qDebug() << "Симуляция уже запущена или завершается.";
        return;
    }
    QDir infoFolder(infoFolderPath);
    if (!infoFolder.exists()) {
        if (!infoFolder.mkpath(infoFolderPath)) {
            qDebug() << "Ошибка при создании папки info";
            return;
        }
    }

    QStringList arguments;
    if (typeMission)
        arguments << simulationPath
                  << planetCalculatorData.planetName
                  << QString::number(planetCalculatorData.tick)
                  << QString::number(planetCalculatorData.square)
                  << QString::number(planetCalculatorData.mass)
                  << QString::number(planetCalculatorData.h)
                  << QString::number(planetCalculatorData.x)
                  << QString::number(planetCalculatorData.vy)
                  << QString::number(planetCalculatorData.vx)
                  << QString::number(planetCalculatorData.aeroCoeff)
                  << "--test-log=" + infoFolderPath + "/telemetry.log"
                  << "--img-templ=" + infoFolderPath + "/.";
    if (QSysInfo::productType() == "windows")
        process = "python";
    else
        process = "python3";

    whatIsSimulator = false;
    mMissionStatus = "Cимуляция в процессе.";
    emit updateMissionStatus(mMissionStatus);
    simulationProcess->start(process, arguments);
}

void SimulationController::stopSimulation()
{
    if (simulationProcess->state() == QProcess::Running) {
        simulationProcess->terminate();
        if (!simulationProcess->waitForFinished()) {
            qDebug() << "Ошибка при завершении симуляции: " << simulationProcess->errorString();
        }
    } else {
        qDebug() << "Симуляция не запущена.";
    }
}


void SimulationController::processFinished(int exitCode, QProcess::ExitStatus exitStatus)
{
    QByteArray standardOutput = simulationProcess->readAllStandardOutput();
    QByteArray standardError = simulationProcess->readAllStandardError();
    mStandardOutput.clear();
    mStandardError.clear();

    if (exitStatus == QProcess::NormalExit && exitCode == 0) {
        mStandardOutput = QString::fromUtf8("Симуляция завершилась успешно");
    } else {
        if (!standardOutput.isEmpty()) {
            mStandardOutput = QString::fromUtf8(standardOutput) + "\nКод завершения: " + QString::number(exitCode);

            mMissionStatus = "Симуляиця завершилась не успешно. Миссия провалена";
            emit updateMissionStatus(mMissionStatus);
            emit showErrorDialog(mStandardOutput);
        }

        if (!standardError.isEmpty()) {
            mStandardError = QString::fromUtf8(standardError) + "\nКод завершения: " + QString::number(exitCode);
            mMissionStatus = "Симуляция завершилась с ошибкой";
            emit updateMissionStatus(mMissionStatus);
            emit showErrorDialog(mStandardError);
        }
    }

    standardOutputUpdated(mStandardOutput);
    standardErrorUpdated(mStandardError);
    if (whatIsSimulator) {
        loadImagesFromFolder(currentProbePath.left(currentProbePath.length() - 4) + "_info/");
        telemetryLogContents = readTelemetryLog(currentProbePath.left(currentProbePath.length() - 4) + "_info/telemetry.log");
    } else {
        loadImagesFromFolder(QDir::currentPath() + "/" + planetCalculatorData.planetName + "_info/");
        telemetryLogContents = readTelemetryLog(QDir::currentPath() + "/" + planetCalculatorData.planetName + "_info/telemetry.log");
    }
    if (!exitCode)
        mMissionStatus = "Cимуляция завершилась успешно";
    emit updateMissionStatus(mMissionStatus);
    emit telemetryLogUpdated(telemetryLogContents);
}

QString SimulationController::readTelemetryLog(const QString &filePath)
{
    QString content;
    QFile file(filePath);

    if (file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        QTextStream in(&file);
        content = in.readAll();
        file.close();
    }
    return content;
}

QString SimulationController::getTelemetryLogContents() const
{
    return telemetryLogContents;
}

void SimulationController::loadImagesFromFolder(const QString &folderPath)
{
    QDir folderDir(folderPath);
    QFileInfoList fileInfoList = folderDir.entryInfoList(QDir::Files | QDir::Hidden);

    clearImages();

    for (const QFileInfo &fileInfo : fileInfoList) {
        if (fileInfo.suffix().toLower() == "png" || fileInfo.suffix().toLower() == "jpg" || fileInfo.suffix().toLower() == "jpeg") {
            QString imagePath = "file://" + fileInfo.filePath();
            emit preImageAppended();
            images.append({imagePath});
            emit postImageAppended();
        }
    }
}


void SimulationController::clearImages()
{
    for (int i = images.size() - 1; i >= 0; --i) {
        emit preImageRemoved(i);
        images.removeAt(i);
        emit postImageRemoved();
    }
}

void SimulationController::addPlanetCalculatorData(QString planetName, int tick, double square, double mass, int h, int x, int vx, int vy, double aeroCoeff)
{
    planetCalculatorData.planetName = planetName;
    planetCalculatorData.tick = tick;
    planetCalculatorData.square = square;
    planetCalculatorData.mass = mass;
    planetCalculatorData.h = h;
    planetCalculatorData.x = x;
    planetCalculatorData.vx = vx;
    planetCalculatorData.vy = vy;
    if (aeroCoeff)
        planetCalculatorData.aeroCoeff = aeroCoeff;
    else
        planetCalculatorData.aeroCoeff = 0.47;
}

void SimulationController::updateMissionStatus(const QString &status)
{
    emit missionStatusChanged(status);
}


void SimulationController::clearInfo()
{
    if (whatIsSimulator) {
        QString infoFolderPath = currentProbePath.left(currentProbePath.length() - 4) + "_info/";
        QDir infoDir(infoFolderPath);

        if (infoDir.exists())
            infoDir.removeRecursively();
    } else {
        QString infoFolderPath = QDir::currentPath() + "/" + planetCalculatorData.planetName + "_info/";
        QDir infoDir(infoFolderPath);
        if (infoDir.exists())
            infoDir.removeRecursively();
    }


    telemetryLogContents.clear();
    mStandardOutput.clear();
    mStandardError.clear();

    planetCalculatorData.planetName = "";
    planetCalculatorData.tick = 0;
    planetCalculatorData.square = 0;
    planetCalculatorData.mass = 0;
    planetCalculatorData.h = 0;
    planetCalculatorData.x = 0;
    planetCalculatorData.vx = 0;
    planetCalculatorData.vy = 0;
    planetCalculatorData.aeroCoeff = 0.47;

    emit telemetryLogUpdated(telemetryLogContents);
    emit standardOutputUpdated(mStandardOutput);
    emit standardErrorUpdated(mStandardError);
}





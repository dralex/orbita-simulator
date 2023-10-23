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
    qDebug()<<arguments;
    if (QSysInfo::productType() == "windows")
        process = "python";
    else
        process = "python3";

    simulationProcess->start(process, arguments);
}

void SimulationController::startCalculatorSimulation(SettingsManager *settingsManager, bool typeMission)
{
    QString process;
    QString infoFolderPath = QDir::currentPath() + "/" + planetCalculatorData.planetName + "_info";
    QString simulationPath = settingsManager->getPlanetsCalculatorPath() + "/simulation.py";

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
                  << "--test-log=" + infoFolderPath + "/test.log"
                  << "--img-templ=" + infoFolderPath + "/.";
    qDebug()<<arguments;
    if (QSysInfo::productType() == "windows")
        process = "python";
    else
        process = "python3";

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
        qDebug()<<standardOutput;
        qDebug()<<standardError;
        mStandardOutput = QString::fromUtf8("Симуляция завершилась успешно");
    } else {
        if (!standardOutput.isEmpty()) {
            mStandardOutput = QString::fromUtf8(standardOutput) + ". Код завершения: " + QString::number(exitCode);
        }

        if (!standardError.isEmpty()) {
            mStandardError = QString::fromUtf8(standardError) + ". Код завершения: " + QString::number(exitCode);
        }
    }

    standardOutputUpdated(mStandardOutput);
    standardErrorUpdated(mStandardError);
    loadImagesFromFolder(currentProbePath.left(currentProbePath.length() - 4) + "_info/");
    telemetryLogContents = readTelemetryLog();
    emit telemetryLogUpdated(telemetryLogContents);
}

QString SimulationController::readTelemetryLog()
{
    QString content;
    QFile file(currentProbePath.left(currentProbePath.length() - 4) + "_info/telemetry.log");

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
    QFileInfoList fileInfoList = folderDir.entryInfoList(QDir::Files);

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

void SimulationController::clearInfo()
{
    telemetryLogContents.clear();
    mStandardOutput.clear();
    mStandardError.clear();
    emit telemetryLogUpdated(telemetryLogContents);
    emit standardOutputUpdated(mStandardOutput);
    emit standardErrorUpdated(mStandardError);
}





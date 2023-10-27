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
    QString infoFolderPath;
    QString simulationPath;
    mTypeMission = typeMission;

    if (typeMission) {
        infoFolderPath = QDir::currentPath() + "/" + planetCalculatorData.planetName + "_info";
        simulationPath = settingsManager->getPlanetsCalculatorPath() + "/simulation.py";
    } else {
        infoFolderPath = QDir::currentPath() + "/testmodel_info";
        simulationPath = settingsManager->getEarthCalculatorPath() + "/simulation.py";
    }


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
                  << planetCalculatorData.square
                  << planetCalculatorData.mass
                  << QString::number(planetCalculatorData.h)
                  << QString::number(planetCalculatorData.x)
                  << QString::number(planetCalculatorData.vy)
                  << QString::number(planetCalculatorData.vx)
                  << QString::number(planetCalculatorData.aeroCoeff)
                  << "--test-log=" + infoFolderPath + "/telemetry.log"
                  << "--img-templ=" + infoFolderPath + "/.";
    else {
        QString filename = "testmodel.xml";
        QFile file(filename);
        if (file.open(QIODevice::WriteOnly | QIODevice::Text))
        {
            QXmlStreamWriter xmlWriter(&file);
            xmlWriter.setAutoFormatting(true);

            xmlWriter.writeStartDocument();
            xmlWriter.writeStartElement("v:testmodel");
            xmlWriter.writeAttribute("name", "testmodel");
            xmlWriter.writeAttribute("planet", "Earth");
            xmlWriter.writeNamespace("venus", "v");

            xmlWriter.writeTextElement("angular_velocity", QString::number(earthCalculatorData.angularVelocity));
            xmlWriter.writeTextElement("constr_edge", QString::number(earthCalculatorData.constrEdge));
            xmlWriter.writeTextElement("duration", QString::number(earthCalculatorData.duration));
            if (earthCalculatorData.impulseDuration && earthCalculatorData.impulseSpeed
                && earthCalculatorData.impulseTime && earthCalculatorData.impulseTraction) {
                xmlWriter.writeTextElement("impulse_duration", QString::number(earthCalculatorData.impulseDuration));
                xmlWriter.writeTextElement("impulse_speed", QString::number(earthCalculatorData.impulseSpeed));
                xmlWriter.writeTextElement("impulse_time", QString::number(earthCalculatorData.impulseTime));
                xmlWriter.writeTextElement("impulse_traction", QString::number(earthCalculatorData.impulseTraction));
            }
            xmlWriter.writeTextElement("mass", QString::number(earthCalculatorData.mass));
            xmlWriter.writeTextElement("moment", earthCalculatorData.moment);
            xmlWriter.writeTextElement("orient_angle", QString::number(earthCalculatorData.orientAngle));
            xmlWriter.writeTextElement("tick", QString::number(earthCalculatorData.tick));
            xmlWriter.writeTextElement("vx", QString::number(earthCalculatorData.vX));
            xmlWriter.writeTextElement("vy", QString::number(earthCalculatorData.vY));
            xmlWriter.writeTextElement("x", QString::number(earthCalculatorData.x));
            xmlWriter.writeTextElement("y", QString::number(earthCalculatorData.y));

            xmlWriter.writeEndElement();
            xmlWriter.writeEndDocument();
            file.close();
        }

        arguments << simulationPath
                  << QDir::currentPath() + "/testmodel.xml"
                  << "--test-log=" + infoFolderPath + "/telemetry.log"
                  << "--images=" + infoFolderPath + "/.";
    }
    qDebug()<<arguments;
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
        if (mTypeMission) {
            loadImagesFromFolder(QDir::currentPath() + "/" + planetCalculatorData.planetName + "_info/");
            telemetryLogContents = readTelemetryLog(QDir::currentPath() + "/" + planetCalculatorData.planetName + "_info/telemetry.log");
        } else {
            loadImagesFromFolder(QDir::currentPath() + "/testmodel_info/");
            telemetryLogContents = readTelemetryLog(QDir::currentPath() + "/testmodel_info/telemetry.log");
        }
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

void SimulationController::addPlanetCalculatorData(QString planetName, int tick, QString square, QString mass, int h, int x, int vx, int vy, double aeroCoeff)
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

void SimulationController::addEarthCalculatorData(int angularVelocity, int duration, int impulseDuration, int impulseSpeed,
                                                  int impulseTime, int impulseTraction, int mass,
                                                  QString moment, int orientAngle, int tick, int vX, int vY, int x, int y)
{
    earthCalculatorData.angularVelocity = angularVelocity;
    earthCalculatorData.constrEdge = 0.1;
    earthCalculatorData.duration = duration;
    earthCalculatorData.impulseDuration = impulseDuration;
    earthCalculatorData.impulseSpeed = impulseSpeed;
    earthCalculatorData.impulseTime = impulseTime;
    earthCalculatorData.impulseTraction = impulseTraction;
    earthCalculatorData.mass = mass;
    earthCalculatorData.moment = moment;
    earthCalculatorData.orientAngle = orientAngle;
    earthCalculatorData.tick = tick;
    earthCalculatorData.vX = vX;
    earthCalculatorData.vY = vY;
    earthCalculatorData.x = x;
    earthCalculatorData.y = y;
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

        QString infoFolderPathEarth = QDir::currentPath() + "/testmodel_info/";
        QDir infoEarthDir(infoFolderPathEarth);
        if (infoEarthDir.exists())
            infoEarthDir.removeRecursively();

        QString filename = "testmodel.xml";
        QFile fileToRemove(filename);
        if (fileToRemove.exists())
            fileToRemove.remove();
    }


    telemetryLogContents.clear();
    mStandardOutput.clear();
    mStandardError.clear();

    planetCalculatorData.planetName = "";
    planetCalculatorData.tick = 0;
    planetCalculatorData.square = "";
    planetCalculatorData.mass = "";
    planetCalculatorData.h = 0;
    planetCalculatorData.x = 0;
    planetCalculatorData.vx = 0;
    planetCalculatorData.vy = 0;
    planetCalculatorData.aeroCoeff = 0.47;

    earthCalculatorData.angularVelocity = 0;
    earthCalculatorData.constrEdge = 0;
    earthCalculatorData.duration = 0;
    earthCalculatorData.impulseDuration = 0;
    earthCalculatorData.impulseSpeed = 0;
    earthCalculatorData.impulseTime = 0;
    earthCalculatorData.impulseTraction = 0;
    earthCalculatorData.mass = 0;
    earthCalculatorData.moment = "";
    earthCalculatorData.orientAngle = 0;
    earthCalculatorData.tick = 0;
    earthCalculatorData.vX = 0;
    earthCalculatorData.vY = 0;
    earthCalculatorData.x = 0;
    earthCalculatorData.y = 0;

    emit telemetryLogUpdated(telemetryLogContents);
    emit standardOutputUpdated(mStandardOutput);
    emit standardErrorUpdated(mStandardError);
}





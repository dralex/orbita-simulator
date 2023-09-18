#include "simulationcontroller.h"

SimulationController::SimulationController(QObject *parent) : QObject(parent)
{
    simulationProcess = new QProcess(this);

    // Связываем сигнал finished() с обработчиком processFinished
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



void SimulationController::startSimulation(QString probePath, SettingsManager *settingsManager)
{
    QString process;
    if (simulationProcess->state() != QProcess::NotRunning) {
        qDebug() << "Симуляция уже запущена или завершается.";
        return;
    }

    QString simulationPath = settingsManager->getSimulationPath() + "/simulation.py";
    currentProbePath = probePath;

    // Создаем папку info в probesPath, если она не существует
    QString infoFolderPath = currentProbePath.left(currentProbePath.length() - 4) + " info";
    QDir infoFolder(infoFolderPath);
    if (!infoFolder.exists()) {
        if (!infoFolder.mkpath(infoFolderPath)) {
            qDebug() << "Ошибка при создании папки info";
            return;
        }
    }

    QStringList arguments;
    arguments << simulationPath << currentProbePath
              << "--mission-log=" + infoFolderPath + "/telemetry.log"
              << "--image=" + infoFolderPath + "/.";
    qDebug()<<QSysInfo::productType();
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
    loadImagesFromFolder(currentProbePath.left(currentProbePath.length() - 4) + " info/");
    telemetryLogContents = readTelemetryLog();
    emit telemetryLogUpdated(telemetryLogContents);
}

QString SimulationController::readTelemetryLog()
{
    QString content;
    QFile file(currentProbePath.left(currentProbePath.length() - 4) + " info/telemetry.log");

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

void SimulationController::clearInfo()
{
    telemetryLogContents.clear();
    mStandardOutput.clear();
    mStandardError.clear();
    emit telemetryLogUpdated(telemetryLogContents);
    emit standardOutputUpdated(mStandardOutput);
    emit standardErrorUpdated(mStandardError);
}





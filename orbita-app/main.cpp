#include <QGuiApplication>
#include <QQmlApplicationEngine>

#include <QLocale>
#include <QTranslator>
#include <QProcess>

#include <QQmlContext>

#include "probe.h"
#include "devices.h"
#include "stepslanding.h"
#include "stepsactivity.h"
#include "planets.h"
#include "planetdevices.h"

#include "probemodel.h"
#include "stepsactivitymodel.h"
#include "stepslandingmodel.h"
#include "comboboxdevices.h"
#include "planetsmodel.h"
#include "imagesmodel.h"
#include "planetsdevicesmodel.h"
#include "planetsprobesdevicesmodel.h"


#include "earthprobe.h"
#include "earthdevices.h"
#include "earthmissions.h"

#include "earthprobesmodel.h"
#include "earthmissionsmodel.h"

#include "simulationcontroller.h"
#include "settingsmanager.h"


int main(int argc, char *argv[])
{
#if QT_VERSION < QT_VERSION_CHECK(6, 0, 0)
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
#endif
    QGuiApplication app(argc, argv);
    app.setOrganizationName("Name");
    app.setOrganizationDomain("Name");

    QTranslator translator;
    const QStringList uiLanguages = QLocale::system().uiLanguages();
    for (const QString &locale : uiLanguages) {
        const QString baseName = "Orbita-app_" + QLocale(locale).name();
        if (translator.load(":/i18n/" + baseName)) {
            app.installTranslator(&translator);
            break;
        }
    }

    qmlRegisterType<ProbeModel>("ProbeModel", 1, 0, "ProbeModel");
    qmlRegisterType<DevicesModel>("DevicesModel", 1, 0, "DevicesModel");
    qmlRegisterType<StepsActivityModel>("StepsActivityModel", 1, 0, "StepsActivityModel");
    qmlRegisterType<StepsLandingModel>("StepsLandingModel", 1, 0, "StepsLandingModel");
    qmlRegisterType<PlanetsModel>("PlanetsModel", 1, 0, "PlanetsModel");
    qmlRegisterType<PlanetsDevicesModel>("PlanetsDevicesModel", 1, 0, "PlanetsDevicesModel");
    qmlRegisterType<PlanetsProbesDevicesModel>("PlanetsProbesDevicesModel", 1, 0, "PlanetsProbesDevicesModel");


    qmlRegisterType<EarthProbesModel>("EarthProbesModel", 1, 0, "EarthProbesModel");
    qmlRegisterType<EarthMissionsModel>("EarthMissionsModel", 1, 0, "EarthMissionsModel");


    qmlRegisterType<ComboBoxDevices>("ComboBoxDevicesModel", 1, 0, "ComboBoxDevicesModel");

    qmlRegisterType<QProcess>("SimulationProcess", 1, 0, "SimulationProcess");
    qmlRegisterType<ImagesModel>("ImagesModel", 1, 0, "ImagesModel");

    qmlRegisterUncreatableType<Probe>("Probe", 1, 0, "Probe",
                                        QStringLiteral("Probe should not be created in QML."));
    qmlRegisterUncreatableType<Devices>("Devices", 1, 0, "Devices",
                                        QStringLiteral("Devices should not be created in QML."));
    qmlRegisterUncreatableType<StepsActivity>("StepsActivity", 1, 0, "StepsActivity",
                                        QStringLiteral("StepsActivity should not be created in QML."));
    qmlRegisterUncreatableType<StepsActivity>("StepsLanding", 1, 0, "StepsLanding",
                                        QStringLiteral("StepsLanding should not be created in QML."));
    qmlRegisterUncreatableType<Planets>("Planets", 1, 0, "Planets",
                                        QStringLiteral("Planets should not be created in QML."));
    qmlRegisterUncreatableType<PlanetDevices>("PlanetDevices", 1, 0, "PlanetDevices",
                                              QStringLiteral("PlanetDevices should not be created in QML."));

    qmlRegisterUncreatableType<EarthProbe>("EarthProbe", 1, 0, "EarthProbe",
                                           QStringLiteral("EarthProbe should not be created in QML."));
    qmlRegisterUncreatableType<EarthMissions>("EarthMissions", 1, 0, "EarthMissions",
                                              QStringLiteral("EarthMissions should not be created in QML."));


    qmlRegisterUncreatableType<SimulationController>("SimulationController", 1, 0, "SimulationController",
                                                     QStringLiteral("SimulationController should not be created in QML."));

    Probe probes;
    Devices devicesItems;
    StepsActivity stepsActivityItems;
    StepsLanding stepsLandingItems;
    Planets planetsItems;
    PlanetDevices planetDevices;

    SimulationController simulationController;
    SettingsManager settingsManager;

    EarthDevices earthDevices;
    EarthMissions earthMissions;
    EarthProbe earthProbes;

    QQmlApplicationEngine engine;
    engine.rootContext()->setContextProperty(QStringLiteral("probes"), &probes);
    engine.rootContext()->setContextProperty(QStringLiteral("devicesItems"), &devicesItems);
    engine.rootContext()->setContextProperty(QStringLiteral("stepsActivityItems"), &stepsActivityItems);
    engine.rootContext()->setContextProperty(QStringLiteral("stepsLandingItems"), &stepsLandingItems);
    engine.rootContext()->setContextProperty(QStringLiteral("planetsItems"), &planetsItems);
    engine.rootContext()->setContextProperty(QStringLiteral("planetDevicesItems"), &planetDevices);

    engine.rootContext()->setContextProperty(QStringLiteral("earthProbes"), &earthProbes);
    engine.rootContext()->setContextProperty(QStringLiteral("earthMissions"), &earthMissions);

    engine.rootContext()->setContextProperty(QStringLiteral("simulationController"), &simulationController);
    engine.rootContext()->setContextProperty(QStringLiteral("settingsManager"), &settingsManager);



    const QUrl url(QStringLiteral("qrc:/main.qml"));
    QObject::connect(&engine, &QQmlApplicationEngine::objectCreated,
                     &app, [url](QObject *obj, const QUrl &objUrl) {
        if (!obj && url == objUrl)
            QCoreApplication::exit(-1);
    }, Qt::QueuedConnection);
    engine.load(url);

    return app.exec();
}

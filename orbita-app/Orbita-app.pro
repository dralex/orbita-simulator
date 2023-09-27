QT += quick \
    widgets

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
        comboboxdevices.cpp \
        comboboxearthdevices.cpp \
        devices.cpp \
        devicesmodel.cpp \
        devicestablemodel.cpp \
        earthdevices.cpp \
        earthdevicesmodel.cpp \
        earthmissions.cpp \
        earthmissionsmodel.cpp \
        earthprobe.cpp \
        earthprobedevices.cpp \
        earthprobesdevicesmodel.cpp \
        earthprobesmodel.cpp \
        imagesmodel.cpp \
        main.cpp \
        planetdevices.cpp \
        planets.cpp \
        planetsdevicesmodel.cpp \
        planetsmodel.cpp \
        planetsprobesdevicesmodel.cpp \
        probe.cpp \
        probemodel.cpp \
        settingsmanager.cpp \
        simulationcontroller.cpp \
        stepsactivity.cpp \
        stepsactivitymodel.cpp \
        stepslanding.cpp \
        stepslandingmodel.cpp

RESOURCES += qml.qrc

TRANSLATIONS += \
    Orbita-app_ru_RU.ts
CONFIG += lrelease
CONFIG += embed_translations

# Additional import path used to resolve QML modules in Qt Creator's code model
QML_IMPORT_PATH =

# Additional import path used to resolve QML modules just for Qt Quick Designer
QML_DESIGNER_IMPORT_PATH =

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

HEADERS += \
    comboboxdevices.h \
    comboboxearthdevices.h \
    devices.h \
    devicesmodel.h \
    devicestablemodel.h \
    earthdevices.h \
    earthdevicesmodel.h \
    earthmissions.h \
    earthmissionsmodel.h \
    earthprobe.h \
    earthprobedevices.h \
    earthprobesdevicesmodel.h \
    earthprobesmodel.h \
    imagesmodel.h \
    planetdevices.h \
    planets.h \
    planetsdevicesmodel.h \
    planetsmodel.h \
    planetsprobesdevicesmodel.h \
    probe.h \
    probemodel.h \
    settingsmanager.h \
    simulationcontroller.h \
    stepsactivity.h \
    stepsactivitymodel.h \
    stepslanding.h \
    stepslandingmodel.h

DISTFILES +=

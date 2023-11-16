QT += quick \
    widgets \
    xmlpatterns

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
        comboboxdevices.cpp \
        comboboxearthdevices.cpp \
        devices.cpp \
        devicestablemodel.cpp \
        earthmissions.cpp \
        earthmissionsmodel.cpp \
        earthprobe.cpp \
        earthprobesmodel.cpp \
        earthsystemsmodel.cpp \
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
        stepsactivitytablemodel.cpp \
        stepslanding.cpp \
        stepslandingtablemodel.cpp \
        systemprobe.cpp \
        systems.cpp \
        systemsprobetablemodel.cpp

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
    devicestablemodel.h \
    earthmissions.h \
    earthmissionsmodel.h \
    earthprobe.h \
    earthprobesmodel.h \
    earthsystemsmodel.h \
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
    stepsactivitytablemodel.h \
    stepslanding.h \
    stepslandingtablemodel.h \
    systemprobe.h \
    systems.h \
    systemsprobetablemodel.h

DISTFILES +=

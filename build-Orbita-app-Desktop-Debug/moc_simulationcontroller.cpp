/****************************************************************************
** Meta object code from reading C++ file 'simulationcontroller.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.15.3)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../orbita-app/simulationcontroller.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#include <QtCore/QVector>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'simulationcontroller.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.15.3. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_SimulationController_t {
    QByteArrayData data[33];
    char stringdata0[490];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_SimulationController_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_SimulationController_t qt_meta_stringdata_SimulationController = {
    {
QT_MOC_LITERAL(0, 0, 20), // "SimulationController"
QT_MOC_LITERAL(1, 21, 19), // "telemetryLogUpdated"
QT_MOC_LITERAL(2, 41, 0), // ""
QT_MOC_LITERAL(3, 42, 8), // "contents"
QT_MOC_LITERAL(4, 51, 13), // "imagesUpdated"
QT_MOC_LITERAL(5, 65, 18), // "QVector<ImageItem>"
QT_MOC_LITERAL(6, 84, 21), // "standardOutputUpdated"
QT_MOC_LITERAL(7, 106, 6), // "output"
QT_MOC_LITERAL(8, 113, 20), // "standardErrorUpdated"
QT_MOC_LITERAL(9, 134, 5), // "error"
QT_MOC_LITERAL(10, 140, 16), // "preImageAppended"
QT_MOC_LITERAL(11, 157, 17), // "postImageAppended"
QT_MOC_LITERAL(12, 175, 15), // "preImageRemoved"
QT_MOC_LITERAL(13, 191, 5), // "index"
QT_MOC_LITERAL(14, 197, 16), // "postImageRemoved"
QT_MOC_LITERAL(15, 214, 15), // "startSimulation"
QT_MOC_LITERAL(16, 230, 9), // "probePath"
QT_MOC_LITERAL(17, 240, 16), // "SettingsManager*"
QT_MOC_LITERAL(18, 257, 15), // "settingsManager"
QT_MOC_LITERAL(19, 273, 14), // "stopSimulation"
QT_MOC_LITERAL(20, 288, 15), // "processFinished"
QT_MOC_LITERAL(21, 304, 8), // "exitCode"
QT_MOC_LITERAL(22, 313, 20), // "QProcess::ExitStatus"
QT_MOC_LITERAL(23, 334, 10), // "exitStatus"
QT_MOC_LITERAL(24, 345, 16), // "readTelemetryLog"
QT_MOC_LITERAL(25, 362, 23), // "getTelemetryLogContents"
QT_MOC_LITERAL(26, 386, 9), // "clearInfo"
QT_MOC_LITERAL(27, 396, 20), // "loadImagesFromFolder"
QT_MOC_LITERAL(28, 417, 10), // "folderPath"
QT_MOC_LITERAL(29, 428, 11), // "clearImages"
QT_MOC_LITERAL(30, 440, 20), // "telemetryLogContents"
QT_MOC_LITERAL(31, 461, 14), // "standardOutput"
QT_MOC_LITERAL(32, 476, 13) // "standardError"

    },
    "SimulationController\0telemetryLogUpdated\0"
    "\0contents\0imagesUpdated\0QVector<ImageItem>\0"
    "standardOutputUpdated\0output\0"
    "standardErrorUpdated\0error\0preImageAppended\0"
    "postImageAppended\0preImageRemoved\0"
    "index\0postImageRemoved\0startSimulation\0"
    "probePath\0SettingsManager*\0settingsManager\0"
    "stopSimulation\0processFinished\0exitCode\0"
    "QProcess::ExitStatus\0exitStatus\0"
    "readTelemetryLog\0getTelemetryLogContents\0"
    "clearInfo\0loadImagesFromFolder\0"
    "folderPath\0clearImages\0telemetryLogContents\0"
    "standardOutput\0standardError"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_SimulationController[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
      16,   14, // methods
       3,  130, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       8,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    1,   94,    2, 0x06 /* Public */,
       4,    1,   97,    2, 0x06 /* Public */,
       6,    1,  100,    2, 0x06 /* Public */,
       8,    1,  103,    2, 0x06 /* Public */,
      10,    0,  106,    2, 0x06 /* Public */,
      11,    0,  107,    2, 0x06 /* Public */,
      12,    1,  108,    2, 0x06 /* Public */,
      14,    0,  111,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
      15,    2,  112,    2, 0x0a /* Public */,
      19,    0,  117,    2, 0x0a /* Public */,
      20,    2,  118,    2, 0x0a /* Public */,
      24,    0,  123,    2, 0x0a /* Public */,
      25,    0,  124,    2, 0x0a /* Public */,
      26,    0,  125,    2, 0x0a /* Public */,
      27,    1,  126,    2, 0x0a /* Public */,
      29,    0,  129,    2, 0x0a /* Public */,

 // signals: parameters
    QMetaType::Void, QMetaType::QString,    3,
    QMetaType::Void, 0x80000000 | 5,    3,
    QMetaType::Void, QMetaType::QString,    7,
    QMetaType::Void, QMetaType::QString,    9,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int,   13,
    QMetaType::Void,

 // slots: parameters
    QMetaType::Void, QMetaType::QString, 0x80000000 | 17,   16,   18,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int, 0x80000000 | 22,   21,   23,
    QMetaType::QString,
    QMetaType::QString,
    QMetaType::Void,
    QMetaType::Void, QMetaType::QString,   28,
    QMetaType::Void,

 // properties: name, type, flags
      30, QMetaType::QString, 0x00495001,
      31, QMetaType::QString, 0x00495001,
      32, QMetaType::QString, 0x00495001,

 // properties: notify_signal_id
       0,
       2,
       3,

       0        // eod
};

void SimulationController::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<SimulationController *>(_o);
        (void)_t;
        switch (_id) {
        case 0: _t->telemetryLogUpdated((*reinterpret_cast< const QString(*)>(_a[1]))); break;
        case 1: _t->imagesUpdated((*reinterpret_cast< const QVector<ImageItem>(*)>(_a[1]))); break;
        case 2: _t->standardOutputUpdated((*reinterpret_cast< const QString(*)>(_a[1]))); break;
        case 3: _t->standardErrorUpdated((*reinterpret_cast< const QString(*)>(_a[1]))); break;
        case 4: _t->preImageAppended(); break;
        case 5: _t->postImageAppended(); break;
        case 6: _t->preImageRemoved((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 7: _t->postImageRemoved(); break;
        case 8: _t->startSimulation((*reinterpret_cast< QString(*)>(_a[1])),(*reinterpret_cast< SettingsManager*(*)>(_a[2]))); break;
        case 9: _t->stopSimulation(); break;
        case 10: _t->processFinished((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< QProcess::ExitStatus(*)>(_a[2]))); break;
        case 11: { QString _r = _t->readTelemetryLog();
            if (_a[0]) *reinterpret_cast< QString*>(_a[0]) = std::move(_r); }  break;
        case 12: { QString _r = _t->getTelemetryLogContents();
            if (_a[0]) *reinterpret_cast< QString*>(_a[0]) = std::move(_r); }  break;
        case 13: _t->clearInfo(); break;
        case 14: _t->loadImagesFromFolder((*reinterpret_cast< const QString(*)>(_a[1]))); break;
        case 15: _t->clearImages(); break;
        default: ;
        }
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        switch (_id) {
        default: *reinterpret_cast<int*>(_a[0]) = -1; break;
        case 8:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 1:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< SettingsManager* >(); break;
            }
            break;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (SimulationController::*)(const QString & );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&SimulationController::telemetryLogUpdated)) {
                *result = 0;
                return;
            }
        }
        {
            using _t = void (SimulationController::*)(const QVector<ImageItem> & );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&SimulationController::imagesUpdated)) {
                *result = 1;
                return;
            }
        }
        {
            using _t = void (SimulationController::*)(const QString & );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&SimulationController::standardOutputUpdated)) {
                *result = 2;
                return;
            }
        }
        {
            using _t = void (SimulationController::*)(const QString & );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&SimulationController::standardErrorUpdated)) {
                *result = 3;
                return;
            }
        }
        {
            using _t = void (SimulationController::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&SimulationController::preImageAppended)) {
                *result = 4;
                return;
            }
        }
        {
            using _t = void (SimulationController::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&SimulationController::postImageAppended)) {
                *result = 5;
                return;
            }
        }
        {
            using _t = void (SimulationController::*)(int );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&SimulationController::preImageRemoved)) {
                *result = 6;
                return;
            }
        }
        {
            using _t = void (SimulationController::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&SimulationController::postImageRemoved)) {
                *result = 7;
                return;
            }
        }
    }
#ifndef QT_NO_PROPERTIES
    else if (_c == QMetaObject::ReadProperty) {
        auto *_t = static_cast<SimulationController *>(_o);
        (void)_t;
        void *_v = _a[0];
        switch (_id) {
        case 0: *reinterpret_cast< QString*>(_v) = _t->getTelemetryLogContents(); break;
        case 1: *reinterpret_cast< QString*>(_v) = _t->getStandardOutput(); break;
        case 2: *reinterpret_cast< QString*>(_v) = _t->getStandardError(); break;
        default: break;
        }
    } else if (_c == QMetaObject::WriteProperty) {
    } else if (_c == QMetaObject::ResetProperty) {
    }
#endif // QT_NO_PROPERTIES
}

QT_INIT_METAOBJECT const QMetaObject SimulationController::staticMetaObject = { {
    QMetaObject::SuperData::link<QObject::staticMetaObject>(),
    qt_meta_stringdata_SimulationController.data,
    qt_meta_data_SimulationController,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *SimulationController::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *SimulationController::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_SimulationController.stringdata0))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int SimulationController::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 16)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 16;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 16)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 16;
    }
#ifndef QT_NO_PROPERTIES
    else if (_c == QMetaObject::ReadProperty || _c == QMetaObject::WriteProperty
            || _c == QMetaObject::ResetProperty || _c == QMetaObject::RegisterPropertyMetaType) {
        qt_static_metacall(this, _c, _id, _a);
        _id -= 3;
    } else if (_c == QMetaObject::QueryPropertyDesignable) {
        _id -= 3;
    } else if (_c == QMetaObject::QueryPropertyScriptable) {
        _id -= 3;
    } else if (_c == QMetaObject::QueryPropertyStored) {
        _id -= 3;
    } else if (_c == QMetaObject::QueryPropertyEditable) {
        _id -= 3;
    } else if (_c == QMetaObject::QueryPropertyUser) {
        _id -= 3;
    }
#endif // QT_NO_PROPERTIES
    return _id;
}

// SIGNAL 0
void SimulationController::telemetryLogUpdated(const QString & _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 0, _a);
}

// SIGNAL 1
void SimulationController::imagesUpdated(const QVector<ImageItem> & _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 1, _a);
}

// SIGNAL 2
void SimulationController::standardOutputUpdated(const QString & _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 2, _a);
}

// SIGNAL 3
void SimulationController::standardErrorUpdated(const QString & _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 3, _a);
}

// SIGNAL 4
void SimulationController::preImageAppended()
{
    QMetaObject::activate(this, &staticMetaObject, 4, nullptr);
}

// SIGNAL 5
void SimulationController::postImageAppended()
{
    QMetaObject::activate(this, &staticMetaObject, 5, nullptr);
}

// SIGNAL 6
void SimulationController::preImageRemoved(int _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 6, _a);
}

// SIGNAL 7
void SimulationController::postImageRemoved()
{
    QMetaObject::activate(this, &staticMetaObject, 7, nullptr);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE

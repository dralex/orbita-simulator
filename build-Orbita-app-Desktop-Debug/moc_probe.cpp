/****************************************************************************
** Meta object code from reading C++ file 'probe.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.15.3)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../orbita-app/probe.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'probe.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.15.3. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_Probe_t {
    QByteArrayData data[52];
    char stringdata0[772];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_Probe_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_Probe_t qt_meta_stringdata_Probe = {
    {
QT_MOC_LITERAL(0, 0, 5), // "Probe"
QT_MOC_LITERAL(1, 6, 16), // "preProbeAppended"
QT_MOC_LITERAL(2, 23, 0), // ""
QT_MOC_LITERAL(3, 24, 17), // "postProbeAppended"
QT_MOC_LITERAL(4, 42, 15), // "preProbeRemoved"
QT_MOC_LITERAL(5, 58, 5), // "index"
QT_MOC_LITERAL(6, 64, 16), // "postProbeRemoved"
QT_MOC_LITERAL(7, 81, 22), // "preDevicesItemAppended"
QT_MOC_LITERAL(8, 104, 23), // "postDevicesItemAppended"
QT_MOC_LITERAL(9, 128, 21), // "preDevicesItemRemoved"
QT_MOC_LITERAL(10, 150, 22), // "postDevicesItemRemoved"
QT_MOC_LITERAL(11, 173, 33), // "preActivityAndLandingItemAppe..."
QT_MOC_LITERAL(12, 207, 34), // "postActivityAndLandingItemApp..."
QT_MOC_LITERAL(13, 242, 32), // "preActivityAndLandingItemRemoved"
QT_MOC_LITERAL(14, 275, 33), // "postActivityAndLandingItemRem..."
QT_MOC_LITERAL(15, 309, 11), // "appendProbe"
QT_MOC_LITERAL(16, 321, 9), // "probeName"
QT_MOC_LITERAL(17, 331, 11), // "missionName"
QT_MOC_LITERAL(18, 343, 11), // "outerRadius"
QT_MOC_LITERAL(19, 355, 11), // "innerRadius"
QT_MOC_LITERAL(20, 367, 10), // "pythonCode"
QT_MOC_LITERAL(21, 378, 11), // "removeProbe"
QT_MOC_LITERAL(22, 390, 9), // "saveProbe"
QT_MOC_LITERAL(23, 400, 10), // "probeIndex"
QT_MOC_LITERAL(24, 411, 8), // "filePath"
QT_MOC_LITERAL(25, 420, 17), // "appendDevicesItem"
QT_MOC_LITERAL(26, 438, 12), // "deviceNumber"
QT_MOC_LITERAL(27, 451, 10), // "deviceName"
QT_MOC_LITERAL(28, 462, 10), // "deviceCode"
QT_MOC_LITERAL(29, 473, 13), // "deviceEngName"
QT_MOC_LITERAL(30, 487, 10), // "startState"
QT_MOC_LITERAL(31, 498, 10), // "inSafeMode"
QT_MOC_LITERAL(32, 509, 17), // "removeDevicesItem"
QT_MOC_LITERAL(33, 527, 28), // "appendActivityAndLandingItem"
QT_MOC_LITERAL(34, 556, 10), // "typCommand"
QT_MOC_LITERAL(35, 567, 4), // "time"
QT_MOC_LITERAL(36, 572, 6), // "device"
QT_MOC_LITERAL(37, 579, 7), // "command"
QT_MOC_LITERAL(38, 587, 8), // "argument"
QT_MOC_LITERAL(39, 596, 28), // "removeActivityAndLandingItem"
QT_MOC_LITERAL(40, 625, 11), // "typeCommand"
QT_MOC_LITERAL(41, 637, 9), // "saveToXml"
QT_MOC_LITERAL(42, 647, 8), // "Planets*"
QT_MOC_LITERAL(43, 656, 11), // "planetsData"
QT_MOC_LITERAL(44, 668, 11), // "planetIndex"
QT_MOC_LITERAL(45, 680, 8), // "filename"
QT_MOC_LITERAL(46, 689, 11), // "loadFromXml"
QT_MOC_LITERAL(47, 701, 14), // "PlanetDevices*"
QT_MOC_LITERAL(48, 716, 17), // "planetDevicesData"
QT_MOC_LITERAL(49, 734, 16), // "SettingsManager*"
QT_MOC_LITERAL(50, 751, 15), // "settingsManager"
QT_MOC_LITERAL(51, 767, 4) // "size"

    },
    "Probe\0preProbeAppended\0\0postProbeAppended\0"
    "preProbeRemoved\0index\0postProbeRemoved\0"
    "preDevicesItemAppended\0postDevicesItemAppended\0"
    "preDevicesItemRemoved\0postDevicesItemRemoved\0"
    "preActivityAndLandingItemAppended\0"
    "postActivityAndLandingItemAppended\0"
    "preActivityAndLandingItemRemoved\0"
    "postActivityAndLandingItemRemoved\0"
    "appendProbe\0probeName\0missionName\0"
    "outerRadius\0innerRadius\0pythonCode\0"
    "removeProbe\0saveProbe\0probeIndex\0"
    "filePath\0appendDevicesItem\0deviceNumber\0"
    "deviceName\0deviceCode\0deviceEngName\0"
    "startState\0inSafeMode\0removeDevicesItem\0"
    "appendActivityAndLandingItem\0typCommand\0"
    "time\0device\0command\0argument\0"
    "removeActivityAndLandingItem\0typeCommand\0"
    "saveToXml\0Planets*\0planetsData\0"
    "planetIndex\0filename\0loadFromXml\0"
    "PlanetDevices*\0planetDevicesData\0"
    "SettingsManager*\0settingsManager\0size"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_Probe[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
      22,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
      12,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    0,  124,    2, 0x06 /* Public */,
       3,    0,  125,    2, 0x06 /* Public */,
       4,    1,  126,    2, 0x06 /* Public */,
       6,    0,  129,    2, 0x06 /* Public */,
       7,    0,  130,    2, 0x06 /* Public */,
       8,    0,  131,    2, 0x06 /* Public */,
       9,    1,  132,    2, 0x06 /* Public */,
      10,    0,  135,    2, 0x06 /* Public */,
      11,    0,  136,    2, 0x06 /* Public */,
      12,    0,  137,    2, 0x06 /* Public */,
      13,    1,  138,    2, 0x06 /* Public */,
      14,    0,  141,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
      15,    5,  142,    2, 0x0a /* Public */,
      21,    1,  153,    2, 0x0a /* Public */,
      22,    6,  156,    2, 0x0a /* Public */,
      25,    7,  169,    2, 0x0a /* Public */,
      32,    2,  184,    2, 0x0a /* Public */,
      33,    7,  189,    2, 0x0a /* Public */,
      39,    3,  204,    2, 0x0a /* Public */,
      41,    4,  211,    2, 0x0a /* Public */,
      46,    3,  220,    2, 0x0a /* Public */,
      51,    0,  227,    2, 0x0a /* Public */,

 // signals: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int,    5,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int,    5,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int,    5,
    QMetaType::Void,

 // slots: parameters
    QMetaType::Void, QMetaType::QString, QMetaType::QString, QMetaType::Double, QMetaType::Double, QMetaType::QString,   16,   17,   18,   19,   20,
    QMetaType::Void, QMetaType::Int,    5,
    QMetaType::Void, QMetaType::Int, QMetaType::QString, QMetaType::Double, QMetaType::Double, QMetaType::QString, QMetaType::QString,   23,   16,   19,   18,   20,   24,
    QMetaType::Void, QMetaType::Int, QMetaType::Int, QMetaType::QString, QMetaType::QString, QMetaType::QString, QMetaType::QString, QMetaType::Bool,   23,   26,   27,   28,   29,   30,   31,
    QMetaType::Void, QMetaType::Int, QMetaType::Int,   23,    5,
    QMetaType::Void, QMetaType::Int, QMetaType::Bool, QMetaType::Int, QMetaType::Double, QMetaType::QString, QMetaType::QString, QMetaType::Int,   23,   34,   26,   35,   36,   37,   38,
    QMetaType::Void, QMetaType::Int, QMetaType::Bool, QMetaType::Int,   23,   40,    5,
    QMetaType::Void, QMetaType::Int, 0x80000000 | 42, QMetaType::Int, QMetaType::QString,   23,   43,   44,   45,
    QMetaType::Void, QMetaType::QString, 0x80000000 | 47, 0x80000000 | 49,   45,   48,   50,
    QMetaType::Int,

       0        // eod
};

void Probe::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<Probe *>(_o);
        (void)_t;
        switch (_id) {
        case 0: _t->preProbeAppended(); break;
        case 1: _t->postProbeAppended(); break;
        case 2: _t->preProbeRemoved((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 3: _t->postProbeRemoved(); break;
        case 4: _t->preDevicesItemAppended(); break;
        case 5: _t->postDevicesItemAppended(); break;
        case 6: _t->preDevicesItemRemoved((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 7: _t->postDevicesItemRemoved(); break;
        case 8: _t->preActivityAndLandingItemAppended(); break;
        case 9: _t->postActivityAndLandingItemAppended(); break;
        case 10: _t->preActivityAndLandingItemRemoved((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 11: _t->postActivityAndLandingItemRemoved(); break;
        case 12: _t->appendProbe((*reinterpret_cast< QString(*)>(_a[1])),(*reinterpret_cast< QString(*)>(_a[2])),(*reinterpret_cast< double(*)>(_a[3])),(*reinterpret_cast< double(*)>(_a[4])),(*reinterpret_cast< QString(*)>(_a[5]))); break;
        case 13: _t->removeProbe((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 14: _t->saveProbe((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< QString(*)>(_a[2])),(*reinterpret_cast< double(*)>(_a[3])),(*reinterpret_cast< double(*)>(_a[4])),(*reinterpret_cast< QString(*)>(_a[5])),(*reinterpret_cast< const QString(*)>(_a[6]))); break;
        case 15: _t->appendDevicesItem((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2])),(*reinterpret_cast< QString(*)>(_a[3])),(*reinterpret_cast< QString(*)>(_a[4])),(*reinterpret_cast< QString(*)>(_a[5])),(*reinterpret_cast< QString(*)>(_a[6])),(*reinterpret_cast< bool(*)>(_a[7]))); break;
        case 16: _t->removeDevicesItem((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2]))); break;
        case 17: _t->appendActivityAndLandingItem((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< bool(*)>(_a[2])),(*reinterpret_cast< int(*)>(_a[3])),(*reinterpret_cast< double(*)>(_a[4])),(*reinterpret_cast< QString(*)>(_a[5])),(*reinterpret_cast< QString(*)>(_a[6])),(*reinterpret_cast< int(*)>(_a[7]))); break;
        case 18: _t->removeActivityAndLandingItem((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< bool(*)>(_a[2])),(*reinterpret_cast< int(*)>(_a[3]))); break;
        case 19: _t->saveToXml((*reinterpret_cast< int(*)>(_a[1])),(*reinterpret_cast< Planets*(*)>(_a[2])),(*reinterpret_cast< int(*)>(_a[3])),(*reinterpret_cast< const QString(*)>(_a[4]))); break;
        case 20: _t->loadFromXml((*reinterpret_cast< QString(*)>(_a[1])),(*reinterpret_cast< PlanetDevices*(*)>(_a[2])),(*reinterpret_cast< SettingsManager*(*)>(_a[3]))); break;
        case 21: { int _r = _t->size();
            if (_a[0]) *reinterpret_cast< int*>(_a[0]) = std::move(_r); }  break;
        default: ;
        }
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        switch (_id) {
        default: *reinterpret_cast<int*>(_a[0]) = -1; break;
        case 19:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 1:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< Planets* >(); break;
            }
            break;
        case 20:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 1:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< PlanetDevices* >(); break;
            case 2:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< SettingsManager* >(); break;
            }
            break;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (Probe::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&Probe::preProbeAppended)) {
                *result = 0;
                return;
            }
        }
        {
            using _t = void (Probe::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&Probe::postProbeAppended)) {
                *result = 1;
                return;
            }
        }
        {
            using _t = void (Probe::*)(int );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&Probe::preProbeRemoved)) {
                *result = 2;
                return;
            }
        }
        {
            using _t = void (Probe::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&Probe::postProbeRemoved)) {
                *result = 3;
                return;
            }
        }
        {
            using _t = void (Probe::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&Probe::preDevicesItemAppended)) {
                *result = 4;
                return;
            }
        }
        {
            using _t = void (Probe::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&Probe::postDevicesItemAppended)) {
                *result = 5;
                return;
            }
        }
        {
            using _t = void (Probe::*)(int );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&Probe::preDevicesItemRemoved)) {
                *result = 6;
                return;
            }
        }
        {
            using _t = void (Probe::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&Probe::postDevicesItemRemoved)) {
                *result = 7;
                return;
            }
        }
        {
            using _t = void (Probe::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&Probe::preActivityAndLandingItemAppended)) {
                *result = 8;
                return;
            }
        }
        {
            using _t = void (Probe::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&Probe::postActivityAndLandingItemAppended)) {
                *result = 9;
                return;
            }
        }
        {
            using _t = void (Probe::*)(int );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&Probe::preActivityAndLandingItemRemoved)) {
                *result = 10;
                return;
            }
        }
        {
            using _t = void (Probe::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&Probe::postActivityAndLandingItemRemoved)) {
                *result = 11;
                return;
            }
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject Probe::staticMetaObject = { {
    QMetaObject::SuperData::link<QObject::staticMetaObject>(),
    qt_meta_stringdata_Probe.data,
    qt_meta_data_Probe,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *Probe::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *Probe::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_Probe.stringdata0))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int Probe::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 22)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 22;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 22)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 22;
    }
    return _id;
}

// SIGNAL 0
void Probe::preProbeAppended()
{
    QMetaObject::activate(this, &staticMetaObject, 0, nullptr);
}

// SIGNAL 1
void Probe::postProbeAppended()
{
    QMetaObject::activate(this, &staticMetaObject, 1, nullptr);
}

// SIGNAL 2
void Probe::preProbeRemoved(int _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 2, _a);
}

// SIGNAL 3
void Probe::postProbeRemoved()
{
    QMetaObject::activate(this, &staticMetaObject, 3, nullptr);
}

// SIGNAL 4
void Probe::preDevicesItemAppended()
{
    QMetaObject::activate(this, &staticMetaObject, 4, nullptr);
}

// SIGNAL 5
void Probe::postDevicesItemAppended()
{
    QMetaObject::activate(this, &staticMetaObject, 5, nullptr);
}

// SIGNAL 6
void Probe::preDevicesItemRemoved(int _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 6, _a);
}

// SIGNAL 7
void Probe::postDevicesItemRemoved()
{
    QMetaObject::activate(this, &staticMetaObject, 7, nullptr);
}

// SIGNAL 8
void Probe::preActivityAndLandingItemAppended()
{
    QMetaObject::activate(this, &staticMetaObject, 8, nullptr);
}

// SIGNAL 9
void Probe::postActivityAndLandingItemAppended()
{
    QMetaObject::activate(this, &staticMetaObject, 9, nullptr);
}

// SIGNAL 10
void Probe::preActivityAndLandingItemRemoved(int _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 10, _a);
}

// SIGNAL 11
void Probe::postActivityAndLandingItemRemoved()
{
    QMetaObject::activate(this, &staticMetaObject, 11, nullptr);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE

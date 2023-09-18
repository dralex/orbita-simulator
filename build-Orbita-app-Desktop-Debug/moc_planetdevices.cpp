/****************************************************************************
** Meta object code from reading C++ file 'planetdevices.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.15.3)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../orbita-app/planetdevices.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'planetdevices.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.15.3. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_PlanetDevices_t {
    QByteArrayData data[15];
    char stringdata0[213];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_PlanetDevices_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_PlanetDevices_t qt_meta_stringdata_PlanetDevices = {
    {
QT_MOC_LITERAL(0, 0, 13), // "PlanetDevices"
QT_MOC_LITERAL(1, 14, 23), // "prePlanetDeviceAppended"
QT_MOC_LITERAL(2, 38, 0), // ""
QT_MOC_LITERAL(3, 39, 24), // "postPlanetDeviceAppended"
QT_MOC_LITERAL(4, 64, 22), // "prePlanetDeviceRemoved"
QT_MOC_LITERAL(5, 87, 5), // "index"
QT_MOC_LITERAL(6, 93, 23), // "postPlanetDeviceRemoved"
QT_MOC_LITERAL(7, 117, 13), // "getDeviceCode"
QT_MOC_LITERAL(8, 131, 10), // "deviceName"
QT_MOC_LITERAL(9, 142, 16), // "getDeviceEngName"
QT_MOC_LITERAL(10, 159, 13), // "getDeviceName"
QT_MOC_LITERAL(11, 173, 13), // "deviceEngName"
QT_MOC_LITERAL(12, 187, 11), // "loadDevices"
QT_MOC_LITERAL(13, 199, 8), // "filePath"
QT_MOC_LITERAL(14, 208, 4) // "size"

    },
    "PlanetDevices\0prePlanetDeviceAppended\0"
    "\0postPlanetDeviceAppended\0"
    "prePlanetDeviceRemoved\0index\0"
    "postPlanetDeviceRemoved\0getDeviceCode\0"
    "deviceName\0getDeviceEngName\0getDeviceName\0"
    "deviceEngName\0loadDevices\0filePath\0"
    "size"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_PlanetDevices[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       9,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       4,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    0,   59,    2, 0x06 /* Public */,
       3,    0,   60,    2, 0x06 /* Public */,
       4,    1,   61,    2, 0x06 /* Public */,
       6,    0,   64,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
       7,    1,   65,    2, 0x0a /* Public */,
       9,    1,   68,    2, 0x0a /* Public */,
      10,    1,   71,    2, 0x0a /* Public */,
      12,    1,   74,    2, 0x0a /* Public */,
      14,    0,   77,    2, 0x0a /* Public */,

 // signals: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int,    5,
    QMetaType::Void,

 // slots: parameters
    QMetaType::QString, QMetaType::QString,    8,
    QMetaType::QString, QMetaType::QString,    8,
    QMetaType::QString, QMetaType::QString,   11,
    QMetaType::Void, QMetaType::QString,   13,
    QMetaType::Int,

       0        // eod
};

void PlanetDevices::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<PlanetDevices *>(_o);
        (void)_t;
        switch (_id) {
        case 0: _t->prePlanetDeviceAppended(); break;
        case 1: _t->postPlanetDeviceAppended(); break;
        case 2: _t->prePlanetDeviceRemoved((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 3: _t->postPlanetDeviceRemoved(); break;
        case 4: { QString _r = _t->getDeviceCode((*reinterpret_cast< QString(*)>(_a[1])));
            if (_a[0]) *reinterpret_cast< QString*>(_a[0]) = std::move(_r); }  break;
        case 5: { QString _r = _t->getDeviceEngName((*reinterpret_cast< QString(*)>(_a[1])));
            if (_a[0]) *reinterpret_cast< QString*>(_a[0]) = std::move(_r); }  break;
        case 6: { QString _r = _t->getDeviceName((*reinterpret_cast< QString(*)>(_a[1])));
            if (_a[0]) *reinterpret_cast< QString*>(_a[0]) = std::move(_r); }  break;
        case 7: _t->loadDevices((*reinterpret_cast< const QString(*)>(_a[1]))); break;
        case 8: { int _r = _t->size();
            if (_a[0]) *reinterpret_cast< int*>(_a[0]) = std::move(_r); }  break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (PlanetDevices::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&PlanetDevices::prePlanetDeviceAppended)) {
                *result = 0;
                return;
            }
        }
        {
            using _t = void (PlanetDevices::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&PlanetDevices::postPlanetDeviceAppended)) {
                *result = 1;
                return;
            }
        }
        {
            using _t = void (PlanetDevices::*)(int );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&PlanetDevices::prePlanetDeviceRemoved)) {
                *result = 2;
                return;
            }
        }
        {
            using _t = void (PlanetDevices::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&PlanetDevices::postPlanetDeviceRemoved)) {
                *result = 3;
                return;
            }
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject PlanetDevices::staticMetaObject = { {
    QMetaObject::SuperData::link<QObject::staticMetaObject>(),
    qt_meta_stringdata_PlanetDevices.data,
    qt_meta_data_PlanetDevices,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *PlanetDevices::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *PlanetDevices::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_PlanetDevices.stringdata0))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int PlanetDevices::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 9)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 9;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 9)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 9;
    }
    return _id;
}

// SIGNAL 0
void PlanetDevices::prePlanetDeviceAppended()
{
    QMetaObject::activate(this, &staticMetaObject, 0, nullptr);
}

// SIGNAL 1
void PlanetDevices::postPlanetDeviceAppended()
{
    QMetaObject::activate(this, &staticMetaObject, 1, nullptr);
}

// SIGNAL 2
void PlanetDevices::prePlanetDeviceRemoved(int _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 2, _a);
}

// SIGNAL 3
void PlanetDevices::postPlanetDeviceRemoved()
{
    QMetaObject::activate(this, &staticMetaObject, 3, nullptr);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE

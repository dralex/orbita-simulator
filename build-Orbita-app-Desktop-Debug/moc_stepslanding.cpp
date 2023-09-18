/****************************************************************************
** Meta object code from reading C++ file 'stepslanding.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.15.3)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../orbita-app/stepslanding.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'stepslanding.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.15.3. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_StepsLanding_t {
    QByteArrayData data[20];
    char stringdata0[201];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_StepsLanding_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_StepsLanding_t qt_meta_stringdata_StepsLanding = {
    {
QT_MOC_LITERAL(0, 0, 12), // "StepsLanding"
QT_MOC_LITERAL(1, 13, 15), // "preItemAppended"
QT_MOC_LITERAL(2, 29, 0), // ""
QT_MOC_LITERAL(3, 30, 16), // "postItemAppended"
QT_MOC_LITERAL(4, 47, 14), // "preItemRemoved"
QT_MOC_LITERAL(5, 62, 5), // "index"
QT_MOC_LITERAL(6, 68, 15), // "postItemRemoved"
QT_MOC_LITERAL(7, 84, 10), // "appendItem"
QT_MOC_LITERAL(8, 95, 6), // "Probe*"
QT_MOC_LITERAL(9, 102, 5), // "probe"
QT_MOC_LITERAL(10, 108, 11), // "typeCommand"
QT_MOC_LITERAL(11, 120, 10), // "probeIndex"
QT_MOC_LITERAL(12, 131, 12), // "deviceNumber"
QT_MOC_LITERAL(13, 144, 4), // "time"
QT_MOC_LITERAL(14, 149, 6), // "device"
QT_MOC_LITERAL(15, 156, 7), // "command"
QT_MOC_LITERAL(16, 164, 8), // "argument"
QT_MOC_LITERAL(17, 173, 10), // "removeItem"
QT_MOC_LITERAL(18, 184, 11), // "changeSteps"
QT_MOC_LITERAL(19, 196, 4) // "size"

    },
    "StepsLanding\0preItemAppended\0\0"
    "postItemAppended\0preItemRemoved\0index\0"
    "postItemRemoved\0appendItem\0Probe*\0"
    "probe\0typeCommand\0probeIndex\0deviceNumber\0"
    "time\0device\0command\0argument\0removeItem\0"
    "changeSteps\0size"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_StepsLanding[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       8,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       4,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    0,   54,    2, 0x06 /* Public */,
       3,    0,   55,    2, 0x06 /* Public */,
       4,    1,   56,    2, 0x06 /* Public */,
       6,    0,   59,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
       7,    8,   60,    2, 0x0a /* Public */,
      17,    4,   77,    2, 0x0a /* Public */,
      18,    2,   86,    2, 0x0a /* Public */,
      19,    0,   91,    2, 0x0a /* Public */,

 // signals: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int,    5,
    QMetaType::Void,

 // slots: parameters
    QMetaType::Void, 0x80000000 | 8, QMetaType::Bool, QMetaType::Int, QMetaType::Int, QMetaType::Double, QMetaType::QString, QMetaType::QString, QMetaType::Int,    9,   10,   11,   12,   13,   14,   15,   16,
    QMetaType::Void, 0x80000000 | 8, QMetaType::Bool, QMetaType::Int, QMetaType::Int,    9,   10,   11,    5,
    QMetaType::Void, 0x80000000 | 8, QMetaType::Int,    9,   11,
    QMetaType::Int,

       0        // eod
};

void StepsLanding::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<StepsLanding *>(_o);
        (void)_t;
        switch (_id) {
        case 0: _t->preItemAppended(); break;
        case 1: _t->postItemAppended(); break;
        case 2: _t->preItemRemoved((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 3: _t->postItemRemoved(); break;
        case 4: _t->appendItem((*reinterpret_cast< Probe*(*)>(_a[1])),(*reinterpret_cast< bool(*)>(_a[2])),(*reinterpret_cast< int(*)>(_a[3])),(*reinterpret_cast< int(*)>(_a[4])),(*reinterpret_cast< double(*)>(_a[5])),(*reinterpret_cast< QString(*)>(_a[6])),(*reinterpret_cast< QString(*)>(_a[7])),(*reinterpret_cast< int(*)>(_a[8]))); break;
        case 5: _t->removeItem((*reinterpret_cast< Probe*(*)>(_a[1])),(*reinterpret_cast< bool(*)>(_a[2])),(*reinterpret_cast< int(*)>(_a[3])),(*reinterpret_cast< int(*)>(_a[4]))); break;
        case 6: _t->changeSteps((*reinterpret_cast< Probe*(*)>(_a[1])),(*reinterpret_cast< int(*)>(_a[2]))); break;
        case 7: { int _r = _t->size();
            if (_a[0]) *reinterpret_cast< int*>(_a[0]) = std::move(_r); }  break;
        default: ;
        }
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        switch (_id) {
        default: *reinterpret_cast<int*>(_a[0]) = -1; break;
        case 4:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< Probe* >(); break;
            }
            break;
        case 5:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< Probe* >(); break;
            }
            break;
        case 6:
            switch (*reinterpret_cast<int*>(_a[1])) {
            default: *reinterpret_cast<int*>(_a[0]) = -1; break;
            case 0:
                *reinterpret_cast<int*>(_a[0]) = qRegisterMetaType< Probe* >(); break;
            }
            break;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (StepsLanding::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&StepsLanding::preItemAppended)) {
                *result = 0;
                return;
            }
        }
        {
            using _t = void (StepsLanding::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&StepsLanding::postItemAppended)) {
                *result = 1;
                return;
            }
        }
        {
            using _t = void (StepsLanding::*)(int );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&StepsLanding::preItemRemoved)) {
                *result = 2;
                return;
            }
        }
        {
            using _t = void (StepsLanding::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&StepsLanding::postItemRemoved)) {
                *result = 3;
                return;
            }
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject StepsLanding::staticMetaObject = { {
    QMetaObject::SuperData::link<QObject::staticMetaObject>(),
    qt_meta_stringdata_StepsLanding.data,
    qt_meta_data_StepsLanding,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *StepsLanding::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *StepsLanding::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_StepsLanding.stringdata0))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int StepsLanding::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 8)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 8;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 8)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 8;
    }
    return _id;
}

// SIGNAL 0
void StepsLanding::preItemAppended()
{
    QMetaObject::activate(this, &staticMetaObject, 0, nullptr);
}

// SIGNAL 1
void StepsLanding::postItemAppended()
{
    QMetaObject::activate(this, &staticMetaObject, 1, nullptr);
}

// SIGNAL 2
void StepsLanding::preItemRemoved(int _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 2, _a);
}

// SIGNAL 3
void StepsLanding::postItemRemoved()
{
    QMetaObject::activate(this, &staticMetaObject, 3, nullptr);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE

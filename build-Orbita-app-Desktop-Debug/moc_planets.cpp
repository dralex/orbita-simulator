/****************************************************************************
** Meta object code from reading C++ file 'planets.h'
**
** Created by: The Qt Meta Object Compiler version 67 (Qt 5.15.3)
**
** WARNING! All changes made in this file will be lost!
*****************************************************************************/

#include <memory>
#include "../orbita-app/planets.h"
#include <QtCore/qbytearray.h>
#include <QtCore/qmetatype.h>
#if !defined(Q_MOC_OUTPUT_REVISION)
#error "The header file 'planets.h' doesn't include <QObject>."
#elif Q_MOC_OUTPUT_REVISION != 67
#error "This file was generated using the moc from 5.15.3. It"
#error "cannot be used with the include files from this version of Qt."
#error "(The moc has changed too much.)"
#endif

QT_BEGIN_MOC_NAMESPACE
QT_WARNING_PUSH
QT_WARNING_DISABLE_DEPRECATED
struct qt_meta_stringdata_Planets_t {
    QByteArrayData data[10];
    char stringdata0[133];
};
#define QT_MOC_LITERAL(idx, ofs, len) \
    Q_STATIC_BYTE_ARRAY_DATA_HEADER_INITIALIZER_WITH_OFFSET(len, \
    qptrdiff(offsetof(qt_meta_stringdata_Planets_t, stringdata0) + ofs \
        - idx * sizeof(QByteArrayData)) \
    )
static const qt_meta_stringdata_Planets_t qt_meta_stringdata_Planets = {
    {
QT_MOC_LITERAL(0, 0, 7), // "Planets"
QT_MOC_LITERAL(1, 8, 22), // "prePlanetsItemAppended"
QT_MOC_LITERAL(2, 31, 0), // ""
QT_MOC_LITERAL(3, 32, 23), // "postPlanetsItemAppended"
QT_MOC_LITERAL(4, 56, 21), // "prePlanetsItemRemoved"
QT_MOC_LITERAL(5, 78, 5), // "index"
QT_MOC_LITERAL(6, 84, 22), // "postPlanetsItemRemoved"
QT_MOC_LITERAL(7, 107, 11), // "loadPlanets"
QT_MOC_LITERAL(8, 119, 8), // "filePath"
QT_MOC_LITERAL(9, 128, 4) // "size"

    },
    "Planets\0prePlanetsItemAppended\0\0"
    "postPlanetsItemAppended\0prePlanetsItemRemoved\0"
    "index\0postPlanetsItemRemoved\0loadPlanets\0"
    "filePath\0size"
};
#undef QT_MOC_LITERAL

static const uint qt_meta_data_Planets[] = {

 // content:
       8,       // revision
       0,       // classname
       0,    0, // classinfo
       6,   14, // methods
       0,    0, // properties
       0,    0, // enums/sets
       0,    0, // constructors
       0,       // flags
       4,       // signalCount

 // signals: name, argc, parameters, tag, flags
       1,    0,   44,    2, 0x06 /* Public */,
       3,    0,   45,    2, 0x06 /* Public */,
       4,    1,   46,    2, 0x06 /* Public */,
       6,    0,   49,    2, 0x06 /* Public */,

 // slots: name, argc, parameters, tag, flags
       7,    1,   50,    2, 0x0a /* Public */,
       9,    0,   53,    2, 0x0a /* Public */,

 // signals: parameters
    QMetaType::Void,
    QMetaType::Void,
    QMetaType::Void, QMetaType::Int,    5,
    QMetaType::Void,

 // slots: parameters
    QMetaType::Void, QMetaType::QString,    8,
    QMetaType::Int,

       0        // eod
};

void Planets::qt_static_metacall(QObject *_o, QMetaObject::Call _c, int _id, void **_a)
{
    if (_c == QMetaObject::InvokeMetaMethod) {
        auto *_t = static_cast<Planets *>(_o);
        (void)_t;
        switch (_id) {
        case 0: _t->prePlanetsItemAppended(); break;
        case 1: _t->postPlanetsItemAppended(); break;
        case 2: _t->prePlanetsItemRemoved((*reinterpret_cast< int(*)>(_a[1]))); break;
        case 3: _t->postPlanetsItemRemoved(); break;
        case 4: _t->loadPlanets((*reinterpret_cast< const QString(*)>(_a[1]))); break;
        case 5: { int _r = _t->size();
            if (_a[0]) *reinterpret_cast< int*>(_a[0]) = std::move(_r); }  break;
        default: ;
        }
    } else if (_c == QMetaObject::IndexOfMethod) {
        int *result = reinterpret_cast<int *>(_a[0]);
        {
            using _t = void (Planets::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&Planets::prePlanetsItemAppended)) {
                *result = 0;
                return;
            }
        }
        {
            using _t = void (Planets::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&Planets::postPlanetsItemAppended)) {
                *result = 1;
                return;
            }
        }
        {
            using _t = void (Planets::*)(int );
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&Planets::prePlanetsItemRemoved)) {
                *result = 2;
                return;
            }
        }
        {
            using _t = void (Planets::*)();
            if (*reinterpret_cast<_t *>(_a[1]) == static_cast<_t>(&Planets::postPlanetsItemRemoved)) {
                *result = 3;
                return;
            }
        }
    }
}

QT_INIT_METAOBJECT const QMetaObject Planets::staticMetaObject = { {
    QMetaObject::SuperData::link<QObject::staticMetaObject>(),
    qt_meta_stringdata_Planets.data,
    qt_meta_data_Planets,
    qt_static_metacall,
    nullptr,
    nullptr
} };


const QMetaObject *Planets::metaObject() const
{
    return QObject::d_ptr->metaObject ? QObject::d_ptr->dynamicMetaObject() : &staticMetaObject;
}

void *Planets::qt_metacast(const char *_clname)
{
    if (!_clname) return nullptr;
    if (!strcmp(_clname, qt_meta_stringdata_Planets.stringdata0))
        return static_cast<void*>(this);
    return QObject::qt_metacast(_clname);
}

int Planets::qt_metacall(QMetaObject::Call _c, int _id, void **_a)
{
    _id = QObject::qt_metacall(_c, _id, _a);
    if (_id < 0)
        return _id;
    if (_c == QMetaObject::InvokeMetaMethod) {
        if (_id < 6)
            qt_static_metacall(this, _c, _id, _a);
        _id -= 6;
    } else if (_c == QMetaObject::RegisterMethodArgumentMetaType) {
        if (_id < 6)
            *reinterpret_cast<int*>(_a[0]) = -1;
        _id -= 6;
    }
    return _id;
}

// SIGNAL 0
void Planets::prePlanetsItemAppended()
{
    QMetaObject::activate(this, &staticMetaObject, 0, nullptr);
}

// SIGNAL 1
void Planets::postPlanetsItemAppended()
{
    QMetaObject::activate(this, &staticMetaObject, 1, nullptr);
}

// SIGNAL 2
void Planets::prePlanetsItemRemoved(int _t1)
{
    void *_a[] = { nullptr, const_cast<void*>(reinterpret_cast<const void*>(std::addressof(_t1))) };
    QMetaObject::activate(this, &staticMetaObject, 2, _a);
}

// SIGNAL 3
void Planets::postPlanetsItemRemoved()
{
    QMetaObject::activate(this, &staticMetaObject, 3, nullptr);
}
QT_WARNING_POP
QT_END_MOC_NAMESPACE

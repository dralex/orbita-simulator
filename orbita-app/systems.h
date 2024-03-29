#ifndef SYSTEMS_H
#define SYSTEMS_H

#include <QObject>
#include <QVector>
#include <QFile>
#include <QDebug>
#include <QXmlStreamReader>
#include <QXmlSchema>
#include <QXmlSchemaValidator>

struct EarthSystemItem {
    int id;
    QString systemEngName;
    QString systemName;
    QString type;
    double mass;
    bool allowState;
    bool allowProgram;
};

class Systems : public QObject
{
    Q_OBJECT
public:
    explicit Systems(QObject *parent = nullptr);

    QVector<EarthSystemItem> items() const;

    bool setEarthSystems(int index, const EarthSystemItem &item);

public slots:
    void loadSystems(const QString &filePath);
    void showSystems();

    QString getSystemsEngName(QString systemName);
    QString getSystemNameByEng(QString systemEngName);
    QString getType(QString systemName);
    double getMass(QString systemName);
    bool getAllowState(QString systemName);
    bool getAllowProgram(QString systemName);

    int size();

signals:
    void preEarthSystemAppended();
    void postEarthSystemAppended();

    void preEarthSystemsRemoved(int index);
    void postEarthSystemsRemoved();

private:
    QVector<EarthSystemItem> mItems;

};

#endif // SYSTEMS_H

#include "earthmissions.h"

EarthMissions::EarthMissions(QObject *parent)
    : QObject{parent}
{

}

QVector<EarthMissionsItem> EarthMissions::items() const
{
    return mItems;
}

bool EarthMissions::setMissions(int index, const EarthMissionsItem &item)
{
    if (index < 0 || index >= mItems.size())
        return false;

    const EarthMissionsItem &olditem = mItems.at(index);
    if (item.id == olditem.id)
        return false;

    mItems[index] = item;
    return true;
}

void EarthMissions::loadMissions(const QString &filePath) {
    QFile file(filePath);

    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        qDebug() << "Не удалось открыть XML файл.";
        return;
    }

    QXmlStreamReader xmlReader(&file);

    while (!xmlReader.atEnd() && !xmlReader.hasError()) {
        xmlReader.readNext();

        if (xmlReader.isStartElement() && xmlReader.name() == "mission") {
            EarthMissionsItem missionItem;
            QXmlStreamAttributes attributes = xmlReader.attributes();
            missionItem.id = mItems.size();
            missionItem.missionEngName = attributes.value("name").toString();
            missionItem.missionName = attributes.value("full_name").toString();

            while (!(xmlReader.isEndElement() && xmlReader.name() == "description")) {
                xmlReader.readNext();
                if (xmlReader.isCharacters()) {
                    missionItem.missionDescription = xmlReader.text().toString();
                }
            }

            // TODO: Read other mission properties as needed, e.g., duration, image, achievements, generator, etc.

            // Emit signals or append to mItems as required
            emit preEarthMissionsItemAppended();

            mItems.append(missionItem);

            emit postEarthMissionsItemAppended();
        }
    }

    if (xmlReader.hasError()) {
        qDebug() << "Ошибка чтения XML файла: " << xmlReader.errorString();
    }

    file.close();
}

void EarthMissions::showMissions()
{
    for (int i = 0; i < mItems.size(); ++i) {
        qDebug()<<"Миссия:"<<mItems[i].missionName;
        qDebug()<<"Описание:"<<mItems[i].missionDescription;

    }
}

int EarthMissions::size()
{
    return mItems.size();
}

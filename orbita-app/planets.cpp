#include "planets.h"

Planets::Planets(QObject *parent)
    : QObject{parent}
{
}

QVector<PlanetsItem> Planets::items() const
{
    return mItems;
}

bool Planets::setPlanets(int index, const PlanetsItem &item)
{
    if (index < 0 || index >= mItems.size())
        return false;

    const PlanetsItem &olditem = mItems.at(index);
    if (item.id == olditem.id)
        return false;

    mItems[index] = item;
    return true;
}

void Planets::loadPlanets(const QString &filePath)
{
    QFile file(filePath);
    if (!file.open(QFile::ReadOnly | QFile::Text)) {
        qDebug() << "Не удалось открыть файл планет";
        return;
    }

    QXmlStreamReader xmlReader(&file);

    while (!xmlReader.atEnd() && !xmlReader.hasError()) {
        QXmlStreamReader::TokenType token = xmlReader.readNext();
        if (token == QXmlStreamReader::StartElement) {
            if (xmlReader.name() == "planet") {
                PlanetsItem planet;
                planet.id = mItems.size();
                planet.planetName = xmlReader.attributes().value("name").toString();
                while (!(xmlReader.tokenType() == QXmlStreamReader::EndElement && xmlReader.name() == "planet")) {
                    xmlReader.readNext();
                    if (xmlReader.name() == "height") {
                        planet.height = xmlReader.readElementText().toDouble();
                    }
                }
                if (planet.planetName != "Earth") {
                    emit prePlanetsItemAppended();

                    mItems.append(planet);

                    emit postPlanetsItemAppended();
                }

            }
        }
    }


    file.close();
}

int Planets::size()
{
    return mItems.size();
}


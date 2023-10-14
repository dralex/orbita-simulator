#include "imagesmodel.h"

ImagesModel::ImagesModel(QObject *parent)
    : QAbstractListModel(parent)
    , mList(nullptr)
{
}

int ImagesModel::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid() || !mList)
        return 0;

    return mList->imagesItems().size();
}

QVariant ImagesModel::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || !mList)
        return QVariant();

    const ImageItem item = mList->imagesItems().at(index.row());

    switch (role) {
    case imageSourceRole:
        return QVariant(item.imageSource);
    }


    return QVariant();
}

bool ImagesModel::setData(const QModelIndex &index, const QVariant &value, int role)
{
    if (!mList)
        return false;

    ImageItem item = mList->imagesItems().at(index.row());

    switch (role) {
    case imageSourceRole:
        item.imageSource = value.toString();
        break;
    }

    if (mList->setImages(index.row(), item)) {
        emit dataChanged(index, index, QVector<int>() << role);
        return true;
    }
    return false;
}

Qt::ItemFlags ImagesModel::flags(const QModelIndex &index) const
{
    if (!index.isValid())
        return Qt::NoItemFlags;

    return Qt::ItemIsEditable;
}

QHash<int, QByteArray> ImagesModel::roleNames() const
{
    QHash<int, QByteArray> names;
    names[imageSourceRole] = "imageSource";
    return names;
}

SimulationController *ImagesModel::list() const
{
    return mList;
}

void ImagesModel::setList(SimulationController *list)
{    beginResetModel();

     if (mList)
         mList->disconnect(this);

     mList = list;

     if (mList) {
         connect(mList, &SimulationController::preImageAppended, this, [=] () {
             const int index = mList->imagesItems().size();
             beginInsertRows(QModelIndex(), index, index);
         });
         connect(mList, &SimulationController::postImageAppended, this, [=] () {
             endInsertRows();
         });

         connect(mList, &SimulationController::preImageRemoved, this, [=] (int index) {
             beginRemoveRows(QModelIndex(), index, index);
         });
         connect(mList, &SimulationController::postImageRemoved, this, [=] () {
             endRemoveRows();
         });
     }
     endResetModel();

}

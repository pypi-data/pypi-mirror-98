from PyQt5.QtCore import QUrl
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQuickWidgets import QQuickWidget


def quickWidget(url, parent=None):
    if isinstance(url, QUrl):
        return QQuickWidget(url, parent)
    elif isinstance(url, str):
        return QQuickWidget(QUrl(url), parent)


def quickWidgetFromFile(fp: str, parent=None):
    qWidget = QQuickWidget()
    qWidget.setSource(QUrl.fromLocalFile(fp))
    qWidget.show()
    return qWidget


def quickView(url: str):
    view = QQuickView()
    view.setResizeMode(QQuickView.SizeRootObjectToView)

    view.setSource(QUrl(url))
    view.show()
    return view

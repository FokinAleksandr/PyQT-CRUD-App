#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
функции
"""
def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if not instance:
        instance = model(**kwargs)
        session.add(instance)
    return instance

def clear_layout(layout):
    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            else:
                clear_layout(item.layout())
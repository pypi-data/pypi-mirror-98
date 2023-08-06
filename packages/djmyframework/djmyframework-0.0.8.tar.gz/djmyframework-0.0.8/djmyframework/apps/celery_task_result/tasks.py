# -*- coding: utf-8 -*-


from celery_app import app, Task


@app.task(bind=True, ignore_result=True)
def test_live(self: Task):
    return True

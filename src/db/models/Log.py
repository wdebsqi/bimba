from datetime import datetime

from ...db import sql_db


class Log(sql_db.Model):
    __tablename__ = "logs"

    id = sql_db.Column(sql_db.Integer, primary_key=True)
    created_at = sql_db.Column(sql_db.DateTime, default=datetime.now(), nullable=False)
    type = sql_db.Column(sql_db.String, nullable=False)
    file = sql_db.Column(sql_db.String, nullable=False)
    message = sql_db.Column(sql_db.String, nullable=False)

from datetime import datetime, time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import PickleType

db = SQLAlchemy()

# ---------- Persons ----------------------------------------------------------
class Person(db.Model):
    __tablename__ = "people"
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(80), unique=True, nullable=False)
    encodings = db.Column(PickleType, nullable=False)   # list[np.ndarray]
    images    = db.Column(PickleType, nullable=False)   # list[jpeg-bytes]

    @classmethod
    def all_encodings(cls):
        encs, names = [], []
        for p in cls.query.all():
            encs.extend(p.encodings)
            names.extend([p.name] * len(p.encodings))
        return encs, names

# ---------- Attendance -------------------------------------------------------
class Attendance(db.Model):
    __tablename__ = "attendance"
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(80), nullable=False)
    date       = db.Column(db.Date,   nullable=False)
    entry_time = db.Column(db.Time,   nullable=False)
    exit_time  = db.Column(db.Time,   nullable=True)

    @classmethod
    def mark(cls, name, mark_type):
        now = datetime.now()
        today = now.date()
        current_time = now.time()

        with db.session.no_autoflush:
            record = cls.query.filter_by(name=name, date=today).first()

            if mark_type == "Entry":
                if record:
                    return False
                else:
                    record = cls(name=name, date=today, entry_time=current_time)
                    db.session.add(record)
                    db.session.commit()
                    return True

            elif mark_type == "Exit":
                if record and not record.exit_time:
                    record.exit_time = current_time
                    db.session.commit()
                    return True
                else:
                    return False
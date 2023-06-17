from .. import db_connector


class CRUD:
    def save(self):
        """Saves the object to the database"""
        Session = db_connector.sessionmaker

        with Session() as session:
            session.add(self)
            session.commit()

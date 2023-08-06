"""
Checks that the database schema doesn't throw any obvious errors
"""
import unittest
from curriculum_model.db import schema
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy.exc import IntegrityError


class TestSchema(unittest.TestCase):

    def test_schema(self):
        """Checks the schema is valid"""
        self.engine = create_engine("sqlite:///:memory:", echo=False)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        schema.Base.metadata.create_all(self.engine)
        from curriculum_model.db.schema import views


class TestTables(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # In memory database for testing
        cls.engine = create_engine("sqlite:///:memory:", echo=False)
        Session = sessionmaker(bind=cls.engine)
        cls.session = Session()
        schema.Base.metadata.create_all(cls.engine)
        cls.session.execute('pragma foreign_keys=on')

    def test_1curriculum(self):
        test_curriculum = schema.Curriculum(curriculum_id=1,
                                            description="Test curriculum",
                                            created_date=datetime.now(),
                                            acad_year=2020)
        inserted_curriculum = insert_query(self.session,
                                           test_curriculum, schema.Curriculum)
        self.assertEqual(test_curriculum, inserted_curriculum)

    def test_2course(self):
        test_course = schema.Course(course_id=1,
                                    pathway="Jazz",
                                    curriculum_id=1)
        inserted_course = insert_query(self.session, test_course, schema.Course)
        self.assertEqual(inserted_course, test_course)
        setattr(test_course, "curriculum_id", 2)
        print(test_course)
        self.session.add(test_course)


def insert_query(session, test_obj, base_obj):
    session.add(test_obj)
    session.flush()
    return session.query(base_obj).one()


if __name__ == '__main__':
    unittest.main()

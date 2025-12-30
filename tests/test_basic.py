import unittest
from app import create_app, db

class BasicTests(unittest.TestCase):

    def setUp(self):
        """Set up test variables."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        # Create all tables in the in-memory database
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_app_exists(self):
        """Test if the application instance is created."""
        self.assertIsNotNone(self.app)

    def test_health_endpoint(self):
        """Test the /health endpoint."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'OK')

if __name__ == '__main__':
    unittest.main()

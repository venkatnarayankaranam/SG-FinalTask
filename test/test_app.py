import unittest
from app import create_app

class TaskManagerTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

import tempfile
import unittest
from pathlib import Path
from fastapi.testclient import TestClient
from app.db import repository
from app.main import app


class HistoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.previous_path = repository.DB_PATH
        repository.DB_PATH = Path(self.tmp.name) / 'test.db'
        repository.init_db()
        self.client = TestClient(app)
        self.payload = {'question_id': 'ds-array-vs-linkedlist-easy', 'answer': 'An array supports O(1) indexing. A linked list has nodes and pointers.', 'candidate_name': 'Alice'}

    def tearDown(self):
        self.client.close()
        repository.DB_PATH = self.previous_path
        self.tmp.cleanup()

    def test_preview_does_not_persist_and_normal_evaluation_does(self):
        self.assertEqual(self.client.post('/api/evaluate-preview', json=self.payload).status_code, 200)
        self.assertEqual(repository.analytics('Alice')['total_attempts'], 0)
        self.assertEqual(self.client.post('/api/evaluate', json=self.payload).status_code, 200)
        self.assertEqual(repository.analytics('Alice')['total_attempts'], 1)

    def test_removal_reset_and_undo_preserve_other_candidate(self):
        ids = [self.client.post('/api/evaluate', json=self.payload).json()['id'] for _ in range(2)]
        self.client.post('/api/evaluate', json={**self.payload, 'candidate_name': 'Bob'})
        self.assertEqual(len(self.client.get('/api/history?candidate_name=Alice').json()), 2)
        self.assertEqual(self.client.delete(f'/api/history/{ids[0]}?candidate_name=Bob').status_code, 404)
        removed = self.client.delete(f'/api/history/{ids[0]}?candidate_name=Alice').json()
        self.assertEqual(removed['count'], 1)
        self.assertEqual(len(repository.study_attempts('Alice')), 1)
        reset = self.client.delete('/api/history?candidate_name=Alice').json()
        self.assertEqual(reset['count'], 1)
        self.assertEqual(repository.analytics('Alice')['total_attempts'], 0)
        self.assertEqual(repository.analytics('Bob')['total_attempts'], 1)
        self.assertEqual(self.client.post(f"/api/history/restore/{reset['batch']}?candidate_name=Bob").json()['count'], 0)
        self.client.post(f"/api/history/restore/{reset['batch']}?candidate_name=Alice")
        self.assertEqual(repository.analytics('Alice')['total_attempts'], 1)
        self.client.post(f"/api/history/restore/{removed['batch']}?candidate_name=Alice")
        self.assertEqual(repository.analytics('Alice')['total_attempts'], 2)
        with repository.connect() as conn:
            self.assertEqual(conn.execute('SELECT count(*) FROM attempts').fetchone()[0], 3)

    def test_existing_database_migration_is_repeatable(self):
        with repository.connect() as conn:
            conn.execute('ALTER TABLE attempts DROP COLUMN deleted_batch')
        repository.init_db()
        repository.init_db()
        self.assertEqual(repository.analytics('Alice')['total_attempts'], 0)

if __name__ == '__main__':
    unittest.main()

import unittest
import core

class IncidentIntervals(unittest.TestCase):
    def test_exact_event_endpoints(self):
        for i in range(6):
            rows=[dict(id=str(j),source='ledger',incident='test',event=name,time=f'2025-05-01T09:{j*(i+2):02}:00Z') for j,name in enumerate(['detected','restarted','resolved'])]
            ans=core.answer(rows,'Elapsed time from restarted to resolved for test')
            self.assertEqual(ans['answer'],f'{(i+2)*60} seconds')
            self.assertEqual([c['id'] for c in ans['citations']],['1','2'])

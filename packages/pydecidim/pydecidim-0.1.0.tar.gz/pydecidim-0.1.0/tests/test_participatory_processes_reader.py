import unittest
from typing import List

from api.decidim_connector import DecidimConnector
from api.participatory_processes_reader import ParticipatoryProcessesReader

API_URL = "https://meta.decidim.org/api"


class ParticipatoryProcessesReaderTest(unittest.TestCase):
    def test_execute(self):
        decidim_connector: DecidimConnector = DecidimConnector(API_URL)
        reader: ParticipatoryProcessesReader = ParticipatoryProcessesReader(decidim_connector,  base_path="..")
        participatory_processes: List[str] = reader.execute()
        self.assertIsInstance(participatory_processes, List)
        if len(participatory_processes) > 0:
            self.assertIsInstance(participatory_processes[0], str)


if __name__ == '__main__':
    unittest.main()

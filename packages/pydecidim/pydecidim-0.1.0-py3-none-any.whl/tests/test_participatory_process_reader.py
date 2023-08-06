import unittest

from api.decidim_connector import DecidimConnector
from api.participatory_process_reader import ParticipatoryProcessReader
from model.participatory_process import ParticipatoryProcess

API_URL = "https://meta.decidim.org/api"


class ParticipatoryProcessesReaderTest(unittest.TestCase):
    def test_execute_not_exists(self):
        decidim_connector: DecidimConnector = DecidimConnector(API_URL)
        reader: ParticipatoryProcessReader = ParticipatoryProcessReader(decidim_connector, base_path="..")
        participatory_process = reader.execute("-4")  # We use the participatory process #40 on Decidim.org api.
        self.assertIsNone(participatory_process)

    def test_execute(self):
        decidim_connector: DecidimConnector = DecidimConnector(API_URL)
        reader: ParticipatoryProcessReader = ParticipatoryProcessReader(decidim_connector, base_path="..")
        participatory_process = reader.execute("40")  # We use the participatory process #40 on Decidim.org api.
        self.assertIsInstance(participatory_process, ParticipatoryProcess)


if __name__ == '__main__':
    unittest.main()

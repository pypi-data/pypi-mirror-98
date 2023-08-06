"""
This Reader retrives the current version of Decidim.
"""

from api.abstract_decidim_reader import AbstractDecidimReader
from api.decidim_connector import DecidimConnector

# Path to the query schema
API_URL = 'queries/version.graphql'


class VersionReader(AbstractDecidimReader):
    """
    This reader retrieves the current version of Decidim.
    """

    def __init__(self, decidim_connector: DecidimConnector, base_path="."):
        """

        :param decidim_connector: An instance of a DecidimConnector class.
        :param base_path: The base path to the schema directory.
        """
        super().__init__(decidim_connector, base_path + "/" + API_URL)

    def execute(self) -> str:
        """
        Send the query to the API and parse the dictionary to extract the version.
        :return: The version of the Decidim Platform.
        """
        response: dict = super().process_query_from_file()
        return response['decidim']['version']

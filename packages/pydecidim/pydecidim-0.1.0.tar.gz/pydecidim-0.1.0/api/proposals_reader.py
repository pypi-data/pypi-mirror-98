"""
This Reader retrives a list of Proposals from Decidim.
"""
from typing import List

from api.abstract_decidim_reader import AbstractDecidimReader
from api.decidim_connector import DecidimConnector
from model.elemental_type_element import ElementalTypeElement

# Path to the query schema
from model.proposal import Proposal

API_URL = 'queries/proposals.graphql'


class ProposalsReader(AbstractDecidimReader):
    """
    This reader retrieves list of Proposals from Decidim.
    """

    def __init__(self, decidim_connector: DecidimConnector, base_path="."):
        """

        :param decidim_connector: An instance of a DecidimConnector class.
        :param base_path: The base path to the schema directory.
        """
        super().__init__(decidim_connector, base_path + "/" + API_URL)

    def execute(self, participatory_process_id: str) -> List[str]:
        """
        Send the query to the API and extract a list of proposals ids from a participatory space.
        :param participatory_process_id: The participatory process id.
        :return: A list of proposals ids.
        """

        response: dict = super().process_query_from_file({'id': ElementalTypeElement(participatory_process_id)})

        proposals_id: List[Proposal] = []
        for proposal_dict in response['participatoryProcess']['components'][0]['proposals']['nodes']:
            proposal_id: str = proposal_dict['id']
            proposals_id.append(proposal_id)
        return proposals_id

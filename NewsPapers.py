import logging
import newspaper
from pydantic import BaseModel, Field

__name__ = "NewsPaper"

import Logger

from Outlets import OutletsSource

logger = logging.getLogger(__name__)

import logging
import newspaper

logger = Logger.get_logger(__name__)


class NewsPaper:

    def __init__(self, agent='', headers='') -> None:
        super().__init__()
        self.agent = agent
        self.headers = headers
        self.paper = None
        self.newspaper = newspaper
        self.config = {}

    def __iter__(self):
        super().__iter__()

    def generate_paper(self, paper) -> object:
        """
        Generates the newspaper object
        :return: paper object
        """
        try:
            paper.download()
            paper.parse()
            paper.set_categories()
            paper.download_categories()  # mthread
            paper.parse_categories()
            paper.generate_articles()
            self.paper = paper
            return self.paper
        except ValueError as e:
            logger.error(f"Could not build Paper , reason: Error: {e}")

    def build(self, outlet: OutletsSource) -> object:
        """
        Builds the newspaper object
        :param outlet:
        :return: generated object
        """
        self.config = {
            'memoize_articles': False,
            'concurrent': True,
            'follow_meta_refresh': True,
            'http_success_only': False,
            'headers': self.headers,
            'agent': self.agent
        }
        try:

            paper = self.newspaper.build(outlet.url, **self.config)
            return self.generate_paper(paper)
        except ValueError as e:
            print(e)
            return None


class NewsPaperBuilder:
    pass

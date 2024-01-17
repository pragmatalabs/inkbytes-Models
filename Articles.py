# --------------------------------
# Article Class
# --------------------------------
import json
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
import langdetect
import newspaper

import uuid

from datetime import datetime

__name__ = "Articles Classes"

from Entities import Entity
from EntityCollection import EntityCollection
import Logger

logger = Logger.get_logger(__name__)


class Article(BaseModel):
    id: Optional[str] = Field(default=None, primary_key=True)
    uid: Optional[str] = None
    doc_id: Optional[int] = None
    publish_date: Optional[str] = None
    category: Optional[str] = None
    fetched_on: Optional[str] = None
    last_updated: Optional[str] = None
    cluster: Optional[str | int] = None
    factual: Optional[str] = None
    sentiment: Optional[str] = None
    entities: Optional[EntityCollection | list | dict | Dict] = []
    article_url: Optional[str] = None
    article_source: Optional[str] = None
    title: Optional[str] = None
    text: Optional[str] = None
    authors: Optional[List[str]] = None
    summary: Optional[str] = None
    similars: Optional[List[str]] = []
    related: Optional[List[str]] = []
    topics: Optional[List[str]] = []
    source_url: Optional[str] = None
    language: Optional[str] = "en"
    keywords: Optional[List[str]] = []
    metadata: Optional[Dict[str, Any]] = Field(default=None, alias="metadata")
    combined: Optional[str] = None
    cluster_centroid: Optional[int] = None

    class Config:
        arbitrary_types_allowed = True
        orm: True

    def __getitem__(self, key):
        return self.__dict__

    def from_dict(self, data: Dict):
        return self(**data)

    def to_dict(self):
        article_dict = self.__dict__.copy()
        article_dict['entities'] = [entity.to_dict() for entity in
                                    self.entities]  # Convert EntitiesCollection to list of dictionaries
        return article_dict

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def to_json(self) -> str:
        return json.dumps(self, cls=ArticleEncoder)

    def set_topics(self, topics):
        self.topics = topics

    def update(self, article):
        _article = article.to_dict()
        for key, value in _article.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise KeyError(f"Invalid field '{key}' for Article")

    def encode(self):
        return json.dumps(self.__dict__)

    # def __str__(self):
    #    return f"{self.title} {self.id}"

    def get_entities(self):
        return self.entities

    def set_entities(self, entitiesCollection: EntityCollection):
        self.entities = [entity for entity in entitiesCollection]
        return self.entities

    def get_entity_links(self, entity_type):
        links = []
        for entity in self.entities:
            if entity["type"] == entity_type:
                links.extend(entity["links"])
        return links

    def get_all_entity_types(self):
        entity_types = set()
        for entity in self.entities:
            entity_types.add(entity["type"])
        return list(entity_types)

    def get_links(self):
        return self.links

    def set_links(self, links):
        self.links = links

    def get_entities_by_type(self, entity_type):
        entities = []
        for entity in self.entities:
            if entity["type"] == entity_type:
                entities.append(entity)
        return entities

    def add_related_article(self, article):
        self.related.append(article)

    def get_related_articles(self):
        return self.related

    def add_similars_article(self, article):
        self.similars.append(article)

    def get_similars_articles(self):
        return self.similars

    def add_topic(self, topic):
        self.topics.append(topic)

    def get_category(self):
        return self.category

    def get_word_count(self):
        return len(self.text.split())

    def get_top_keywords(self, num_keywords=3):
        return sorted(self.keywords, key=lambda x: x[1], reverse=True)[:num_keywords]

    def set_sentiment(self, sentiment):
        self.sentiment = sentiment

    def set_factual(self, factual):
        self.factual = factual

    def set_summary(self, summary):
        self.summary = summary

    def extract_category(self):
        # Extracting category from the URL
        self.category = self.article_url.split("/")[-2]
        return self.category


class ArticleBuilder(BaseModel):
    id: str = None
    uid: str = None
    publish_date: str = None
    fetched_on: str = None
    last_updated: str = None
    last_update: str = None
    cluster: str = None
    factual: str = None
    sentiment: str = None
    entities: EntityCollection = EntityCollection()
    article_url: str = None
    article_source: str = None
    title: str = None
    text: str = None
    authors: str = None
    summary: str = None
    similars: List[Dict] = []
    related: List[Dict] = []
    topics: List[str] = []
    source_url: str = None
    language: str = "en"
    keywords: List[str] = []
    metadata: List[str] = []
    version: str = None
    social_media: List[str] = []
    pure_text: str = None
    signature: str = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

    def buildFromNewspaper3K(self, article: newspaper.Article, newsPaperBrand: str) -> Article:
        articleData = {}
        try:
            articleData = {
                'fetched_on': str(datetime.now()),
                'id': str(uuid.uuid3(uuid.NAMESPACE_URL, article.url)),
                'uid': str(uuid.uuid3(uuid.NAMESPACE_URL, article.url)),
                'title': article.title or "untitled",
                'text': article.text,
                'authors': article.authors or [],
                'publish_date': str(article.publish_date),
                'source_url': newsPaperBrand,
                'article_url': article.url,
                'keywords': article.keywords,
                'summary': article.summary,
                'similars': [],
                'related': [],
                'topics': [],
                'sentiment': '',
                'factual': '',
                'language': langdetect.detect(article.text) or "en",
                'last_updated': str(datetime.now()),
                'metadata': article.meta_data or None,
                'category': article.meta_data.get('category') or None,
            }
        except ValueError as e:
            logger.error(f"Error fetching article: {e}")
        return Article(**articleData)


class ArticleEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Article):
            return obj.to_dict()
        if isinstance(obj, Entity):
            return obj.to_dict()
        if isinstance(obj, EntityCollection):
            return obj.to_list()  # Serialize EntitiesCollection as a list of dictionaries
        return super().default(obj)


class ArticleCollection(BaseModel):
    articles: List[Article] = []

    def __iter__(self):
        return iter(self.articles)

    def __len__(self):
        return len(self.articles)

    def count(self):
        return len(self.articles)

    def append(self, article):
        self.add_article(article)

    def add_article(self, article):
        self.articles.append(article)

    def size(self):
        return len(self.articles)

    def remove_article(self, article):
        self.articles.remove(article)

    def filter_articles(self, filter_func):
        filtered_articles = [article for article in self.articles if filter_func(article)]
        filtered_collection = ArticleCollection()
        filtered_collection.articles = filtered_articles
        return filtered_collection

    def find_article(self, article_id):
        for article in self.articles:
            if article.id == article_id:
                return article
        return None

    def save_to_json(self, file_path):
        data = [article.to_dict() for article in self.articles]
        with open(file_path, "w") as file:
            json.dump(data, file)

    def load_from_json(self, file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            for article_data in data:
                article = Article.from_dict(article_data)
                self.add_article(article)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.articles[key.start:key.stop:key.step]
        else:
            return self.articles[key]

    def __setitem__(self, key, value):
        self.articles[key] = value

    def add_article(self, article):
        # Add an article to the collection
        self.articles.append(article)

    def get_article(self, id):
        # get the article in the collection that has the given id
        for article in self.articles:
            if article.id == id:
                return article

    def remove_article(self, article):
        # Remove an article from the collection
        self.articles.remove(article)

    def save_to_json(self, file_path):
        # Save the collection to a JSON file
        data = [article.to_json() for article in self.articles]
        with open(file_path, "w") as file:
            json.dump(data, file)

    def load_articles_from_json(self, data):
        builder = ArticleBuilder()
        self.articles = [builder.from_json(article_data).build() for article_data in data]

    def load_from_json(self, file_path):
        # Load the collection from a JSON file
        with open(file_path, "r") as file:
            data = json.load(file)
            for article_data in data:
                article = Article(article_data)
                self.add_article(article)

    def to_dict(self):
        # Convert the collection to a Python dictionary
        return {
            "articles": [article.to_dict() for article in self.articles]
        }

    def from_dict(self, data):
        # Create an ArticleCollection object from a Python dictionary
        collection = self()
        if "articles" in data:
            for article_data in data["articles"]:
                article = Article(article_data)
                self.add_article(article)
        return collection

    def filter_articles(self, filter_func):

        # Filter the articles in the collection using a filter function
        filtered_articles = [article for article in self.articles if filter_func(article)]
        # Create a new ArticleCollection object with the filtered articles
        filtered_collection = ArticleCollection()
        filtered_collection.articles = filtered_articles
        return filtered_collection


def build_article_collection(documents) -> ArticleCollection:
    _articles: ArticleCollection = ArticleCollection()
    for article_data in documents:
        article = Article(vars(article_data))
        article.doc_id = article_data.doc_id
        _articles.append(article)
    return _articles


def group_articles_by_cluster(articles) -> dict:
    clusters = {}
    for article in articles:
        cluster_id = article.cluster
        if cluster_id not in clusters:
            clusters[cluster_id] = []
        clusters[cluster_id].append(article)
    return clusters


def extract_unique_clusters(articles: ArticleCollection) -> List[int]:
    cluster_numbers = set()
    for article in articles:
        cluster_numbers.add(article.cluster)
    unique_clusters = list(cluster_numbers)
    return unique_clusters


class ArticleProcessor:
    pass

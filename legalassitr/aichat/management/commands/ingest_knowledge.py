
from django.core.management.base import BaseCommand, CommandParser

from legalassitr.aichat.knowledge_base.news_networks import load_news

class IngestKnowledgeCommand(BaseCommand):
    help = 'Run Ingestion on the Knowledge sources in the knowledge repository'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('--news', action='store_true', help='Ingest News')
        parser.add_argument('--law_books', type=str, default="./", help='Ingest Books related to Law and Psychology.')

    def handle(self, *args, **options):
        is_news = options.get('news', False)
        law_books = options.get('law_books', None)

        if is_news:
            load_news()

    
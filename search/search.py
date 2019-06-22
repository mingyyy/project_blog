# from elasticsearch_dsl.connections import connections
# from .utils import PostIndex
# from elasticsearch.helpers import bulk
# from elasticsearch import Elasticsearch
# from blog.models import Post
# from elasticsearch_dsl import *
#
# connections.create_connection()
#
#
# def bulk_indexing():
#     PostIndex.init()
#     es = Elasticsearch()
#     bulk(client=es, actions=(b.indexing() for b in Post.objects.all().iterator()))
#
#
# def search(author):
#     s = Search().filter('match', author=author)
#     response = s.execute()
#     return response
# from django_elasticsearch_dsl import Document
# from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl import DocType, Index
from blog.models import Post


# @registry.register_document
# class PostDucment(Document):
#     class Index:
#         name = 'cars'
#         settings = {
#             'number_of_shards':1,
#             'number_of_replicas':0
#         }
#
#     class Django:
#         model = Post
#         fields = [
#             'title',
#             'content',
#             'author',
#             'id',
#         ]


# posts = Index('posts')
#
# @posts.doc_type
# class PostDocument(DocType):
#     class Meta:
#         model = Post
#         fields = [
#             'title',
#             'content',
#             'author',
#             'id',
#         ]

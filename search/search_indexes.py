# from blog.models import Post
# from haystack import indexes
#
#
# class PostIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.EdgeNgramField(document=True, use_template=True, template_name='search/post_text.txt')
#     title = indexes.CharField(model_attr='title')
#     content = indexes.CharField(model_attr='content')
#
#     def get_model(self):
#         return Post
#
#     def index_queryset(self, using=None):
#         return self.get_model().objects.all()

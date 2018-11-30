from app import ma


class PageWordCountSerializer(ma.Schema):
    class Meta:
        fields = ('id', 'url', 'word_count')


page_word_count_serializer = PageWordCountSerializer()
page_word_counts_serializer = PageWordCountSerializer(many=True)

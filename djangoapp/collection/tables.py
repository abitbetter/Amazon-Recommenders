# tutorial/tables.py
import django_tables2 as tables


class ResultsTable(tables.Table):
    RecommendationNumber1 = tables.Column()
    RecommendationNumber2 = tables.Column()
    RecommendationNumber3 = tables.Column()
    RecommendationNumber4 = tables.Column()
#    class Meta:
#         attrs = {'class': 'table table-condensed table-vertical-center', 'id': 'dashboard_table'}
#         fields = ('name', 'surname', 'address')
#         sequence = fields
#         order_by = ('-name', )
#         #template_name = 'django_tables2/bootstrap.html'

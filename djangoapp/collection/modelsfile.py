# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Books(models.Model):
    index = models.IntegerField(primary_key=True, blank=False, null=False)
    marketplace = models.TextField(blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    review_id = models.TextField(blank=True, null=True)
    product_id = models.TextField(blank=True, null=True)
    product_parent = models.IntegerField(blank=True, null=True)
    product_title = models.TextField(blank=True, null=True)
    product_category = models.TextField(blank=True, null=True)
    star_rating = models.TextField(blank=True, null=True)
    helpful_votes = models.FloatField(blank=True, null=True)
    total_votes = models.FloatField(blank=True, null=True)
    vine = models.TextField(blank=True, null=True)
    verified_purchase = models.TextField(blank=True, null=True)
    review_headline = models.TextField(blank=True, null=True)
    review_body = models.TextField(blank=True, null=True)
    review_date = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'books'


class Movies(models.Model):
    index = models.IntegerField(primary_key=True, blank=False, null=False)
    marketplace = models.TextField(blank=True, null=True)
    customer_id = models.IntegerField(blank=True, null=True)
    review_id = models.TextField(blank=True, null=True)
    product_id = models.TextField(blank=True, null=True)
    product_parent = models.IntegerField(blank=True, null=True)
    product_title = models.TextField(blank=True, null=True)
    product_category = models.TextField(blank=True, null=True)
    star_rating = models.TextField(blank=True, null=True)
    helpful_votes = models.FloatField(blank=True, null=True)
    total_votes = models.FloatField(blank=True, null=True)
    vine = models.TextField(blank=True, null=True)
    verified_purchase = models.TextField(blank=True, null=True)
    review_headline = models.TextField(blank=True, null=True)
    review_body = models.TextField(blank=True, null=True)
    review_date = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movies'

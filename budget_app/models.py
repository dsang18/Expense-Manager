from django.db import models


class Credentials(models.Model):
    UID = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=50)
    email_id = models.CharField(max_length=50)
    phone_no = models.BigIntegerField()
    username = models.CharField(max_length=50, unique=True)
    password = models.BinaryField()

class expense_categories(models.Model):
    user = models.ForeignKey(Credentials, db_column='user', on_delete=models.CASCADE)
    cat_type = models.CharField(max_length=40)

class expense(models.Model):
    user = models.ForeignKey(Credentials, db_column='user', on_delete=models.CASCADE)
    expense_type = models.CharField(max_length=50)
    expense_amnt = models.IntegerField()
    expense_day = models.CharField(max_length=15)
    expense_date = models.CharField(max_length=20)
    expense_time = models.CharField(max_length=20)
    
class budget(models.Model):
    user_exp = models.ForeignKey(Credentials, db_column='user_exp', on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    total_budget = models.IntegerField()
    left_budget = models.IntegerField()

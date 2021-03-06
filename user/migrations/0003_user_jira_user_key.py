# Generated by Django 2.1.2 on 2019-09-02 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20190327_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='jira_user_key',
            field=models.CharField(blank=True, choices=[('admin', 'Abdullah Yousuf'), ('apon', 'Apon Shahriar'), ('emran', 'Emran Hossain'), ('zilani', 'Golam Zilani'), ('hakan', 'Håkan Jonsson'), ('iftakharul', 'Iftakharul Islam'), ('jenat', 'Jenat Ara'), ('sayem', 'Km Sayem'), ('melon', 'Mahabubur Rahaman Melon'), ('ikhtiar', 'Md. Mahmudul hasan'), ('rubayet', 'Md. Rubayet Hossain'), ('oliver', 'Oliver Hertzman Kraft'), ('reaz', 'Reaz Abedin'), ('sazedul', 'Sazedul Haque'), ('shawon', 'Shafiqul Islam'), ('shuvankar', 'Shuvankar Paul')], max_length=100, null=True, verbose_name='jira user'),
        ),
    ]

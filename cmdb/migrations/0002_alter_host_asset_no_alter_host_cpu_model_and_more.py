# Generated by Django 5.1.2 on 2024-10-17 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='asset_no',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='资产编号'),
        ),
        migrations.AlterField(
            model_name='host',
            name='cpu_model',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='CPU型号'),
        ),
        migrations.AlterField(
            model_name='host',
            name='cpu_num',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='CPU数量'),
        ),
        migrations.AlterField(
            model_name='host',
            name='disk',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='硬盘信息'),
        ),
        migrations.AlterField(
            model_name='host',
            name='ip',
            field=models.GenericIPAddressField(blank=True, null=True, verbose_name='业务IP'),
        ),
        migrations.AlterField(
            model_name='host',
            name='memo',
            field=models.TextField(blank=True, max_length=200, null=True, verbose_name='备注信息'),
        ),
        migrations.AlterField(
            model_name='host',
            name='memory',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='内存大小'),
        ),
        migrations.AlterField(
            model_name='host',
            name='os',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='操作系统'),
        ),
        migrations.AlterField(
            model_name='host',
            name='other_ip',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='BMC以及其它IP'),
        ),
        migrations.AlterField(
            model_name='host',
            name='position',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='所在位置'),
        ),
        migrations.AlterField(
            model_name='host',
            name='sn',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='SN号 码'),
        ),
        migrations.AlterField(
            model_name='host',
            name='up_time',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='上架时间'),
        ),
        migrations.AlterField(
            model_name='host',
            name='vendor',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='设备厂商'),
        ),
    ]
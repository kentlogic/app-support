# Generated by Django 3.0.5 on 2020-05-12 14:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickets', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketattachment',
            name='uploaded_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='uploader', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ticket',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tickets.Category'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tickets.Client'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='closed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='resolved_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ticket',
            name='hot_issue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='tickets.HotIssue', verbose_name='Issue'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='last_update_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='last_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ticket',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tickets.Module'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tickets.Product'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tickets.Project'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='solution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='comment_solution', to='tickets.Comment'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tickets.Status'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='sub_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tickets.SubCategory'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ticket_owner', to='users.Team', verbose_name='Assigned to'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tickets.Category', verbose_name='Category'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='scat_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='scat_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tickets.Status', verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='status',
            name='stat_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='proj_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='proj_client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='project_client', to='tickets.Client', verbose_name='Client'),
        ),
        migrations.AddField(
            model_name='project',
            name='proj_last_update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='project_last_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='proj_manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='project_manager', to=settings.AUTH_USER_MODEL, verbose_name='Project Manager'),
        ),
        migrations.AddField(
            model_name='project',
            name='proj_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tickets.Status', verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='producttype',
            name='prod_type_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='producttype',
            name='prod_type_last_update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='prod_type_last_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='client',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, related_name='product_client', to='tickets.Client', verbose_name='Client'),
        ),
        migrations.AddField(
            model_name='product',
            name='prod_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='prod_last_update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='product_last_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='product',
            name='prod_manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_manager', to=settings.AUTH_USER_MODEL, verbose_name='Product Manger'),
        ),
        migrations.AddField(
            model_name='product',
            name='prod_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tickets.Status'),
        ),
        migrations.AddField(
            model_name='product',
            name='prod_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='tickets.ProductType', verbose_name='Product Type'),
        ),
        migrations.AddField(
            model_name='module',
            name='mod_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='module',
            name='mod_last_update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='mod_last_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='module',
            name='mod_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tickets.Status', verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='module',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tickets.Product', verbose_name='Product'),
        ),
        migrations.AddField(
            model_name='hotissue',
            name='hi_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hotissue',
            name='hi_last_update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='hi_last_update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='hotissue',
            name='hi_module',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='tickets.Module', verbose_name='Module'),
        ),
        migrations.AddField(
            model_name='hotissue',
            name='hi_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tickets.Product', verbose_name='Product'),
        ),
        migrations.AddField(
            model_name='hotissue',
            name='hi_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tickets.Status', verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tickets.Ticket'),
        ),
        migrations.AddField(
            model_name='client',
            name='account_manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='account_manager', to=settings.AUTH_USER_MODEL, verbose_name='Account manager'),
        ),
        migrations.AddField(
            model_name='client',
            name='client_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='client',
            name='client_last_update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='client_last_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='client',
            name='client_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tickets.Status', verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='category',
            name='cat_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='category_manager', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='category',
            name='cat_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tickets.Status', verbose_name='Status'),
        ),
    ]
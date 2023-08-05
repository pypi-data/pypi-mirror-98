# Generated by Django 2.2.17 on 2021-01-29 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djangoldp_energiepartagee', '0024_auto_20210125_2207'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actor',
            options={'default_permissions': ['add', 'change', 'delete', 'view', 'control']},
        ),
        migrations.AlterModelOptions(
            name='college',
            options={'default_permissions': ['add', 'change', 'delete', 'view', 'control']},
        ),
        migrations.AlterModelOptions(
            name='collegeepa',
            options={'default_permissions': ['add', 'change', 'delete', 'view', 'control']},
        ),
        migrations.AlterModelOptions(
            name='contribution',
            options={'default_permissions': ['add', 'change', 'delete', 'view', 'control']},
        ),
        migrations.AlterModelOptions(
            name='integrationstep',
            options={'default_permissions': ['add', 'change', 'delete', 'view', 'control']},
        ),
        migrations.AlterModelOptions(
            name='interventionzone',
            options={'default_permissions': ['add', 'change', 'delete', 'view', 'control']},
        ),
        migrations.AlterModelOptions(
            name='legalstructure',
            options={'default_permissions': ['add', 'change', 'delete', 'view', 'control']},
        ),
        migrations.AlterModelOptions(
            name='paymentmethod',
            options={'default_permissions': ['add', 'change', 'delete', 'view', 'control']},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'default_permissions': ['add', 'change', 'delete', 'view', 'control']},
        ),
        migrations.AlterModelOptions(
            name='region',
            options={'default_permissions': ['add', 'change', 'delete', 'view', 'control']},
        ),
        migrations.AlterModelOptions(
            name='regionalnetwork',
            options={'default_permissions': ['add', 'change', 'delete', 'view', 'control']},
        ),
        migrations.AlterModelOptions(
            name='relatedactor',
            options={'default_permissions': ['add', 'change', 'delete', 'view', 'control']},
        ),
        migrations.AlterField(
            model_name='actor',
            name='college',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actors', to='djangoldp_energiepartagee.College', verbose_name='Collège'),
        ),
        migrations.AlterField(
            model_name='actor',
            name='collegeepa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actors', to='djangoldp_energiepartagee.Collegeepa', verbose_name='Collège EPA'),
        ),
        migrations.AlterField(
            model_name='actor',
            name='interventionzone',
            field=models.ManyToManyField(blank=True, max_length=50, null=True, related_name='actors', to='djangoldp_energiepartagee.Interventionzone', verbose_name="Zone d'intervention"),
        ),
        migrations.AlterField(
            model_name='actor',
            name='legalstructure',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actors', to='djangoldp_energiepartagee.Legalstructure', verbose_name='Structure Juridique'),
        ),
        migrations.AlterField(
            model_name='actor',
            name='presentation',
            field=models.TextField(blank=True, null=True, verbose_name='Présentation/objet de la structure'),
        ),
        migrations.AlterField(
            model_name='actor',
            name='region',
            field=models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actors', to='djangoldp_energiepartagee.Region', verbose_name='Région'),
        ),
    ]

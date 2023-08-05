# Generated by Django 2.2.17 on 2021-01-25 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoldp_energiepartagee', '0022_auto_20210125_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='actortype',
            field=models.CharField(blank=True, choices=[('soc_citoy', 'Sociétés Citoyennes'), ('collectivite', 'Collectivités'), ('structure', 'Structures d’Accompagnement'), ('partenaire', 'Partenaires')], max_length=50, null=True, verbose_name="Type d'acteur"),
        ),
        migrations.AlterField(
            model_name='actor',
            name='category',
            field=models.CharField(blank=True, choices=[('collectivite', 'Collectivités'), ('porteur_dev', 'Porteurs de projet en développement'), ('porteur_exploit', 'Porteurs de projet en exploitation'), ('partenaire', 'Partenaires')], max_length=50, null=True, verbose_name='Catégorie de cotisant'),
        ),
        migrations.AlterField(
            model_name='relatedactor',
            name='role',
            field=models.CharField(blank=True, choices=[('admin', 'Administrateur'), ('membre', 'Membre')], max_length=50, null=True, verbose_name="Rôle de l'utilisateur"),
        ),
    ]

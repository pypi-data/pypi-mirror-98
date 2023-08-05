# Generated by Django 2.2.17 on 2021-01-18 13:07

from django.db import migrations, models
import django.db.models.deletion
import djangoldp.fields


class Migration(migrations.Migration):

    dependencies = [
        ('djangoldp_energiepartagee', '0004_auto_20210114_1652'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('urlid', djangoldp.fields.LDPUrlField(blank=True, null=True, unique=True)),
                ('is_backlink', models.BooleanField(default=False, help_text='set automatically to indicate the Model is a backlink')),
                ('allow_create_backlink', models.BooleanField(default=True, help_text='set to False to disable backlink creation after Model save')),
                ('year', models.IntegerField(verbose_name='Année de cotisation')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Montant à payer')),
                ('iban', models.CharField(blank=True, max_length=35, null=True, verbose_name='IBAN du destinataire')),
                ('address', models.CharField(blank=True, max_length=250, null=True, verbose_name='Adresse postale du destinataire')),
                ('calldate', models.DateField(blank=True, null=True, verbose_name='Date du dernier appel')),
                ('paymentdate', models.DateField(blank=True, null=True, verbose_name='Date de paiement')),
                ('receptdate', models.DateField(blank=True, null=True, verbose_name="Date de l'envoi du reçu")),
                ('receptnumber', models.CharField(blank=True, max_length=250, null=True, verbose_name='Numéro de reçu')),
                ('receptfile', models.URLField(blank=True, null=True, verbose_name='Reçu')),
                ('callfile', models.URLField(blank=True, null=True, verbose_name='Appel à cotisations')),
                ('nonrenewed', models.BooleanField(default=False, verbose_name='Cotisation non renouvelée')),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoldp_energiepartagee.Actor', verbose_name='Acteur')),
                ('contributionstatus', models.ForeignKey(max_length=50, on_delete=django.db.models.deletion.CASCADE, to='djangoldp_energiepartagee.Contributionstatus', verbose_name='Etat de la cotisation')),
                ('paymentmethod', models.ForeignKey(blank=True, max_length=50, null=True, on_delete=django.db.models.deletion.CASCADE, to='djangoldp_energiepartagee.Paymentmethod', verbose_name='Moyen de paiement')),
                ('paymentto', models.ForeignKey(max_length=250, on_delete=django.db.models.deletion.CASCADE, to='djangoldp_energiepartagee.Regionalnetwork', verbose_name='Paiement à effectuer à')),
                ('receivedby', models.ForeignKey(blank=True, max_length=250, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contribution_requests_created', to='djangoldp_energiepartagee.Regionalnetwork', verbose_name='Paiement reçu par')),
            ],
            options={
                'anonymous_perms': ['view', 'add', 'change'],
            },
        ),
        migrations.DeleteModel(
            name='Invoicing',
        ),
    ]

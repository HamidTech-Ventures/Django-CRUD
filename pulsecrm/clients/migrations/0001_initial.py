from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        (settings.AUTH_USER_MODEL.split('.')[0], '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_name', models.CharField(max_length=150)),
                ('company', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(blank=True, max_length=50)),
                ('industry', models.CharField(blank=True, max_length=150)),
                ('website', models.URLField(blank=True)),
                ('address', models.CharField(blank=True, max_length=300)),
                ('description', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Complete', 'Complete'), ('Prospects', 'Prospects')], default='Prospects', max_length=20)),
                ('joining_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='client_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
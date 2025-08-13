from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('budget', models.DecimalField(decimal_places=2, max_digits=14, validators=[django.core.validators.MinValueValidator(0)])),
                ('priority', models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Medium', max_length=10)),
                ('deadline', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='clients.client')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.AddIndex(
            model_name='project',
            index=models.Index(fields=['priority'], name='projects_pr_priority_3a0cc5_idx'),
        ),
        migrations.AddIndex(
            model_name='project',
            index=models.Index(fields=['deadline'], name='projects_pr_deadlin_8a53cc_idx'),
        ),
        migrations.AddField(
            model_name='project',
            name='team',
            field=models.ManyToManyField(blank=True, related_name='projects', to='employees.employee'),
        ),
    ]
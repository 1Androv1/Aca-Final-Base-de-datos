from django.db import migrations, models


def set_first_user_as_admin(apps, schema_editor):
    MyUser = apps.get_model('myuser', 'MyUser')
    first_user = MyUser.objects.order_by('id').first()
    if first_user is not None:
        first_user.is_admin = True
        first_user.save(update_fields=['is_admin'])


class Migration(migrations.Migration):

    dependencies = [
        ('myuser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(set_first_user_as_admin, migrations.RunPython.noop),
    ]

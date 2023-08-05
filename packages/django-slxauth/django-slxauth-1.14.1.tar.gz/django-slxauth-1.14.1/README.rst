django-slxauth
==============

Consult the django-project-template on how to use it.

Upgrade from 1.7 to 1.8
-----------------------

In 1.8 there is a new username column introduced which removes unique identification responsibility from the email
column. To migrate existing users and populate the DB sucessfully add the following script to your migrations.
Fix the model name as needed and update the dependency to the last previous migration.

Afterwards run makemigrations as usual to update other fields.

populate username migration::

	import django.contrib.auth.validators
	from django.db import migrations, models
	from django.db.models import Count


	def populate_usernames(apps, schema_editor):
		User = apps.get_model('app', 'User')

		for grp in User.objects.exclude(um_id__isnull=True).values('um_id').annotate(ct=Count('um_id')):
			if grp['ct'] > 1:
				User.objects.filter(um_id=grp['um_id']).update(um_id=None)

		for u in User.objects.all():
			if u.um_id:
				u.username = 'um_%s' % u.um_id
			else:
				u.username = 'user_%s' % u.id
			u.save()


	class Migration(migrations.Migration):

		dependencies = [
			('app', '0009_auto_20180208_1339'),
		]

		operations = [
			migrations.AddField(
				model_name='user',
				name='username',
				field=models.CharField(null=True,
									   help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
									   max_length=150, unique=False,
									   validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
									   verbose_name='username'),
			),
			migrations.RunPython(populate_usernames),
			migrations.AlterField(
				model_name='user',
				name='username',
				field=models.CharField(error_messages={'unique': 'A user with that username already exists.'},
									   help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
									   max_length=150, unique=True,
									   validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
									   verbose_name='username'),
			)
		]
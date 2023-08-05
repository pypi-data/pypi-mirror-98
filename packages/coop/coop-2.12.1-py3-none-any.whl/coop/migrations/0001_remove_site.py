"""
Remove the automatically generated site and home page
NOTE: This migration should be faked when converting a site to coop.
"""

from django.db import migrations


def remove_site(apps, schema):
    Site = apps.get_model('wagtailcore', 'site')
    Page = apps.get_model('wagtailcore', 'page')

    # Check if the site is premade
    site = Site.objects.first()
    if site.hostname == 'localhost':
        # Remove all the pre-defined sites
        Site.objects.all().delete()

        # Delete the home page
        Page.objects.get(pk=2).delete()
        # Fix the root page to show it has no children
        Page.objects.filter(pk=1).update(numchild=0)


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '__latest__'),
    ]

    operations = [
        migrations.RunPython(remove_site, migrations.RunPython.noop)
    ]

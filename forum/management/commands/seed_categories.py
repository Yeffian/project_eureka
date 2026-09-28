from django.core.management.base import BaseCommand
from forum.models import Category


class Command(BaseCommand):
    help = "Create the default forum categories"

    CATEGORIES = [
        ("English", "english", "Practice, share tips, and help each other with reading and writing.", 0),
        ("Maths", "maths", "Get help with problems, share resources, celebrate small wins.", 1),
        ("Ask a Teacher", "ask-a-teacher", "Any question about class, homework, or how something works.", 3),
    ]

    def handle(self, *args, **options):
        for name, slug, description, order in self.CATEGORIES:
            obj, created = Category.objects.get_or_create(
                slug=slug,
                defaults={"name": name, "description": description, "order": order},
            )
            verb = "Created" if created else "Already exists"
            self.stdout.write(f"{verb}: {name}")
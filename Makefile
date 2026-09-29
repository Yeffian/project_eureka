run:
	python manage.py runserver

cleandb:
	export DATABASE_URL="postgresql://neondb_owner:npg_xBiVYLcK28Ro@ep-bold-queen-b36yfi8z.c-4.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
	python manage.py flush
	python manage.py createsuperuser
	python manage.py seed_categories

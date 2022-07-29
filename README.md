# Pokemon Crawler

Project started from https://docs.docker.com/compose/django/

A directory should exist for postgres to save the data to.
`mkdir -p volumes/database`

Also, images should build when launched with:
`docker-compose up -d`

The 'startup' service runs the `manage.py startup` command (defined in `pokecrawler/management/commands/startup.py`), which is an infinite loop with a timer as a rate limiter.
I didn't want to use Celery for this and django-background-tasks was buggier than expected with Postgres.

If I were to write tests for this, I would test the important functions in `tasks.py`: `findNewPokemon` and `refreshStalePokemon`.

* `findNewPokemon` should fail gracefully when there is a network error and the timeout is reached and also when the last Pokemon has id -1 (which shouldn't happen anyway).
* `refreshStalePokemon` should fail gracefully as well when the timeout is reached and for any other exception.

Note: I know the description for the Pokemon isn't very well generated.

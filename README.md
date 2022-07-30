I wasn't happy with what I did yesterday, so I decided to try again and learn Celery while at it.

So I did it and it actually took less than 2h, hah!

I'm using Redis as both a broker and backend for Celery and saving the data, but it would work ok without persistence.

I'm still saving the database to `./volumes/database`.
Redis saves to `./volumes/redis`.

```shell
mkdir -p ./volumes/database
mkdir -p ./volumes/redis
```

To build the image and run the application:

```shell
docker-compose up -d
```

I defined a few settings:
* CRAWL_INTERVAL_SECONDS: 
  The interval for crawling the API for new Pokemons, in seconds. `findNewPokemons` will run every CRAWL_INTERVAL_SECONDS seconds.
* REFRESH_INTERVAL_SECONDS: 
  Same as CRAWL_INTERVAL_SECONDS, but for refreshing the stale Pokemons.
* STALENESS_THRESHOLD_SECONDS: 
  The interval, in seconds, after which a Pokemon is considered stale.
* POKEMON_BATCH_SIZE:
  How many Pokemons to look for in one crawl.

I didn't write any tests for this one either. Other than `findNewPokemons` and `refreshStalePokemons`, the model should be tested too. When updating a Pokemon, the associated Sprite instance is kept even after creating a new, updated, one.
So I would test to make sure the old instance exists after the update.
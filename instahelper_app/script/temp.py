import redis

r = redis.Redis()
pipe = r.pipeline()
pipe.rpush("tocopylist", "bilginhale007")
pipe.set("bilginhale007", "hale758599")
pipe.rpush("tocopylist", "kaanxhakan")
pipe.set("kaanhakanx", "KHa758599")
pipe.execute()
import redis
from django.conf import settings

# redis_instance = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT , charset="utf-8", decode_responses=True, db=0)
redis_pool_db_0_consumer = redis.ConnectionPool(host=settings.REDIS_HOST,port=settings.REDIS_PORT,decode_responses=True, db=0)
class RedisUtils:

    def redis_connection(self, mode='r', connection_type='local'):
        # if mode=='w':
            # return redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT , charset="utf-8", decode_responses=True, db=0)
        return redis.StrictRedis(connection_pool=redis_pool_db_0_consumer)

    def add_to_sorted_set(self, key, score, member):
        r = self.redis_connection()
        data = {member: score}  
        res = r.zadd(key, data)
        return res

    def remove_from_sorted_set(self, key, member):
        r = self.redis_connection()
        # r = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT , charset="utf-8", decode_responses=True, db=0)
        res = r.zrem(key, member)
        return res

    def get_all_memeber_from_sorted_set(self, key,start=None, end=None):
        # r = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT , charset="utf-8", decode_responses=True, db=0)
        # r  = redis.StrictRedis(connection_pool=redis_pool_db_0_consumer)
        r = self.redis_connection()
        if start is None:
            start = 0
        if end is None:
            end = -1
        res = r.zrange(key, start, end)
        return res


    def get_key_ttl(self, key):
        r = self.redis_connection()
        ttl = r.ttl(key)
        return ttl

    def add_to_front_redis_list(self, key, value, expiry=None):
        r = self.redis_connection()
        r.lpush(key, value)
        if expiry:
            r.expire(key, expiry)

    def get_value_from_key(self, key):
        r = self.redis_connection(mode='w')
        value = r.get(key)
        if value:
            value = value.decode("utf-8")
        return value

    def set_value_for_key(self, key, value, expiry=3600 * 24 * 7):
        r = self.redis_connection()
        r.set(key, value)
        if expiry:
            r.expire(key, expiry)

    def get_rev_sorted_set_members(self, key, start=0, end=-1, redis_con=None):
        if not redis_con:
            redis_con = self.redis_connection()
        value = redis_con.zrevrange(key, start, end)
        return value

    def key_exists(self, key):
        r = self.redis_connection()
        return r.exists(key)

    def set_redis_key_ttl(self, key, ttl):
        r = self.redis_connection()
        r.expire(key, ttl)

    def set_list_value_at_index_from_left(self, key, index, updated_value):
        r = self.redis_connection()
        res = r.lset(key, index, updated_value)
        return res

    def get_selected_members_from_sorted_set(self, key, start, end):
        r = self.redis_connection()
        res = r.zrange(key, start, end)
        return res

    def get_set_members(self, key):
        r = self.redis_connection()
        return list(r.smembers(key))

    def get_reverse_members_from_sorted_set(self, key, start, end):
        r = self.redis_connection()
        res = r.zrevrange(key, start, end)
        return res

    def get_first_member_from_set(self, key):
        r = self.redis_connection()
        res = r.zrange(key, 0, 0, withscores=True)
        return res

    def check_if_member_exists_in_sorted_set(self, key, member):
        r = self.redis_connection()
        res = r.zscore(key, member)
        exists = False
        if res:
            exists = True

        return exists

    def check_redis_key_exist(self, key):
        r = self.redis_connection()
        res = r.exists(key)
        return res

    def set_redis_key(self, key, TTL):
        r = self.redis_connection(MODE_WRITE)
        r.expire(key, TTL)

    def get_members_from_set(self, key, count):
        r = self.redis_connection()
        print("key is " + key)
        res = r.srandmember(key, count)
        print(res)
        if res:
            print(res)
        else:
            print("nothing found")
        return res

    def remove_member_from_set(self, key, members):
        r = self.redis_connection()
        res = r.srem(key, members)
        return res

    def add_to_hash_map_set(self, key, dictionary):
        r = self.redis_connection()
        r.hmset(key, dictionary)

    def get_all_fields_value_from_map(self, key,format_data=True):
        r = self.redis_connection()
        res = r.hgetall(key)
        if format_data is False:
            return res
        if res:
            d = {}
            for k, v in res.items():
                k = k.decode("utf-8")
                v = v.decode('utf-8')
                d[k] = v
            res = d
        return res

    def get_field_value_from_map(self, key, field,decode=True):
        r = self.redis_connection()
        res = r.hget(key, field)
        if decode and isinstance(res, bytes):
            res = res.decode("utf-8")
        return res

    def set_field_value_to_map(self, key, field, value, ttl=-1,mapping=None):
        r = self.redis_connection()
        if mapping:
            res = r.hset(key, mapping=mapping)
        else:
            res = r.hset(key, field, value)
        if ttl != -1:
            r.expire(key, ttl)
        return res

    def del_field_from_map(self, key, field):
        r = self.redis_connection()
        r.hdel(key, field)

    def increment_field_value_of_hash_map(self, key, field, incrby):
        r = self.redis_connection()
        res = r.hincrby(key, field, incrby)
        return res

    def delete_key(self, key):
        r = self.redis_connection()
        res = r.delete(key)
        return res

    def delete_in_batch(self, keys):
        r = self.redis_connection()
        res = r.delete(*keys)
        return res

    def get_sorted_set_cardinality(self,key):
        r = self.redis_connection()
        res = r.zcard(key)
        return res

    def add_member_to_set(self, key, member):
        r = self.redis_connection()
        r.sadd(key, member)

    def get_number_of_elements_in_sorted_set(self,key,min,max):
        r = self.redis_connection()
        res = r.zcount(key,min,max)
        return res

    def remove_elements_from_sorted_set(self,key,start,stop):
        r = self.redis_connection()
        res = r.zremrangebyrank(key,start,stop)
        return res

    def get_list_content(self, key, start, end, db=0):
        return self.redis_connection().lrange(key, start, end)

    def cache_id(self, cache_key, cache_id, create_time=None, add=True):
        r = self.redis_connection()
        cache_exists = r.exists(cache_key)
        if cache_exists:
            if add:
                self.add_to_sorted_set(cache_key, create_time, cache_id)
            else:
                r.zrem(cache_key, cache_id)

    def increment_sorted_set_member(self, key, member, score):
        r = self.redis_connection()
        r.zincrby(key, score, member)

    def get_sorted_set_member_score(self, key, member):
        r = self.redis_connection()
        return r.zscore(key, member)

    def get_sorted_set_rev_range(self, key, start, end):
        r = self.redis_connection()
        return r.zrevrange(key, start, end)
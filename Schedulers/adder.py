import redis

redis_host = '127.0.0.1'
redis_port = 6379
redis_password = ''
r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)


def add_value_to_list(key, value):
    r.rpush(key, value)


def main():
    key = "userERSReport"
    add_value_to_list(key, 17)


if __name__ == "__main__":
    main()

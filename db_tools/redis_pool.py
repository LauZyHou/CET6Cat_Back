import redis


class RedisPool:
    """Redis连接池"""
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379)

    @staticmethod
    def get_connection():
        """从连接池中获取一个连接对象"""
        return redis.Redis(connection_pool=RedisPool.pool)


if __name__ == '__main__':
    # 测试一下
    r = RedisPool.get_connection()
    # print(r.get('myKey').decode('utf8'))
    print(int(r.get('aaa')))

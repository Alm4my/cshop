import redis

from cshop import settings

# connect to redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


class Recommender(object):

    def get_product_key(self, id_):
        """Build Redis key."""
        return f'product:{id_}:purchased_with'

    def products_bought(self, products):
        products_ids = [p.id for p in products]
        for product_id in products_ids:
            for with_id in products_ids:
                # get the other products bought with each product
                if product_id != with_id:
                    # increment score for product purchased together
                    r.zincrby(self.get_product_key(product_id), 1, with_id)


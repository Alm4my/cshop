import redis

from cshop import settings

# connect to redis
from shop.models import Product

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

    def suggest_products_for(self, products, max_results=6):
        """

        :param products:  list of Product objects to get recommendations for (one or more product)
        :param max_results: int maximum number of recommendations to return
        :return:
        """
        product_ids = [p.id for p in products]
        if len(products) == 1:
            # only 1 product
            suggestions = r.zrange(self.get_product_key(product_ids[0]),
                                   0,
                                   -1,
                                   desc=True)[:max_results]
        else:
            # generate a temporary key
            flat_ids = ''.join([str(id_) for id_ in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            # multiple products, combine scores of all products
            # store the resulting sorted set in a temporary key
            keys = [self.get_product_key(id_) for id_ in product_ids]
            r.zunionstore(tmp_key, keys)
            # remove ids for the products the recommendation is for
            r.zrem(tmp_key, *product_ids)
            # get the product ids by their score, descendant sort
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            # remove temporary key
            r.delete(tmp_key)
        suggested_products_ids = [int(id_) for id_ in suggestions]
        # get suggested products and sort by order of appearance
        suggested_products = list(Product.objects.filter(id__in=suggested_products_ids))
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        for id_ in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id_))

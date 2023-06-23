from models import List, Card
from flask_cache import cache


@cache.memoize(timeout=7)
def get_list_by_userId(user_id):
    return List.query.filter_by(user_id=user_id).all()


@cache.memoize(timeout=5)
def get_card_by_id(card_id):
    return Card.query.filter_by(cid=card_id).first()

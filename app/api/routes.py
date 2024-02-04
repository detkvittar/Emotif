from flask import Blueprint

api = Blueprint('api', __name__)

@api.route('/posts', methods=['GET'])
def get_posts():
    # Logic to fetch posts
    pass

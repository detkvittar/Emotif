from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.post_service import get_unseen_posts_for_user, discover_posts
from app.services.user_service import (
    set_user_mood, send_follow_request,
    accept_follow_request, decline_follow_request, block_user, get_user_followers, unfollow_user,
    toggle_user_privacy
)

api = Blueprint('api', __name__)

@api.route('/posts/main', methods=['GET'])
@jwt_required()
def get_main_page_posts():
    current_user_id = get_jwt_identity()
    posts = get_unseen_posts_for_user(current_user_id)

    posts_data = [{'id': post.id, 'title': post.title, 'content': post.content} for post in posts]
    return jsonify(posts_data)

@api.route('/posts/discover', methods=['GET'])
@jwt_required()
def get_discover_page_posts():
    current_user_id = get_jwt_identity()
    hashtags = request.args.get('hashtags')
    location = request.args.get('location')
    posts = discover_posts(current_user_id, hashtags, location)

    # Convert posts to JSON
    posts_data = [{'id': post.id, 'title': post.title, 'content': post.content} for post in posts]
    return jsonify(posts_data)

@api.route('/user/mood', methods=['POST'])
@jwt_required()
def user_set_mood():
    user_id = get_jwt_identity()
    data = request.get_json()
    user, message = set_user_mood(user_id, data)
    if user is None:
        return jsonify({'message': message}), 404
    return jsonify({'message': message}), 200

@api.route('/user/update_profile', methods=['POST'])
@jwt_required()
def user_update_profile():
    user_id = get_jwt_identity()
    data = request.get_json()
    user, message = update_user_profile(user_id, data)
    if user is None:
        return jsonify({'message': message}), 404
    return jsonify({'message': message}), 200

@api.route('/follow_request/send', methods=['POST'])
@jwt_required()
def user_follow_or_send_follow_request():
    user_id = get_jwt_identity()
    data = request.get_json()
    request_result, message = send_follow_request(user_id, data)
    if request_result is None:
        return jsonify({'message': message}), 409
    return jsonify({'message': message}), 201

@api.route('/friend_follow/accept', methods=['POST'])
@jwt_required()
def user_accept_follow_request():
    user_id = get_jwt_identity()
    data = request.get_json()
    request_result, message = accept_follow_request(user_id, data)
    if request_result is None:
        return jsonify({'message': message}), 404
    return jsonify({'message': message}), 200

@api.route('/follow_request/decline', methods=['POST'])
@jwt_required()
def user_decline_follow_request():
    user_id = get_jwt_identity()
    data = request.get_json()
    request_result, message = decline_follow_request(user_id, data)
    if request_result is None:
        return jsonify({'message': message}), 404
    return jsonify({'message': message}), 200
    # MUST CHECK IF THIS ROUTE WORKS

@api.route('/user/block', methods=['POST'])
@jwt_required()
def user_block():
    user_id = get_jwt_identity()
    data = request.get_json()
    block_result, message = block_user(user_id, data)
    if block_result is None:
        return jsonify({'message': message}), 409
    return jsonify({'message': message}), 200

@api.route('/user/followers', methods=['GET'])
@jwt_required()
def user_followers():
    user_id = get_jwt_identity()
    followers = get_user_followers(user_id)
    return jsonify(followers)

@api.route('/user/unfollow', methods=['POST'])
@jwt_required()
def user_unfollow():
    user_id = get_jwt_identity()
    data = request.get_json()
    unfollow_result, message = unfollow_user(user_id, data)
    if unfollow_result is None:
        return jsonify({'message': message}), 200
    return jsonify({'message': message}), 409

@api.route('/user/toggle_privacy', methods=['POST'])
@jwt_required()
def user_toggle_privacy():
    user_id = get_jwt_identity()
    user, message = toggle_user_privacy(user_id)
    if user is None:
        return jsonify({'message': message}), 404
    return jsonify({'message': message}), 200

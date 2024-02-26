from datetime import datetime
from app.data.models import User, Friendship, Block
from app.data.database import db

def set_user_mood(user_id, data):
    user = User.query.get(user_id)
    if not user:
        return None, 'User not found'

    user.mood = data.get('mood')
    user.mood_timestamp = datetime.utcnow()
    user.mood_public = data.get('mood_public', True)
    db.session.commit()
    return user, 'Mood updated successfully'

def send_follow_request(user_id, data):
    requested_id = data.get('requested_id')
    requested_user = User.query.get(requested_id)

    if not requested_user:
        return None, 'User not found'

    # Check if already following or request already sent
    if Friendship.query.filter_by(follower_id=user_id, followed_id=requested_id).first():
        return None, 'Already following or request already sent'

    if requested_user.is_private:
        # If user is private, send follow request
        new_request = Friendship(follower_id=user_id, followed_id=requested_id, status='requested')
        db.session.add(new_request)
        db.session.commit()
        return new_request, 'Follow request sent'
    else:
        # If user is public, automatically follow
        new_friendship = Friendship(follower_id=user_id, followed_id=requested_id, status='accepted')
        db.session.add(new_friendship)
        db.session.commit()
        return new_friendship, 'Now following'

def accept_follow_request(user_id, data):
    requester_id = data.get('requester_id')
    follow_request = Friendship.query.filter_by(follower_id=requester_id, followed_id=user_id, status='requested').first()
    if not follow_request:
        return None, 'Follow request not found'

    follow_request.status = 'accepted'
    db.session.commit()
    return follow_request, 'Follow request accepted'

def decline_follow_request(user_id, data):
    requester_id = data.get('requester_id')
    follow_request = Friendship.query.filter_by(follower_id=requester_id, followed_id=user_id, status='requested').first()
    if not follow_request:
        return None, 'Follow request not found'

    db.session.delete(follow_request)
    db.session.commit()
    return None, 'Follow request declined'

def block_user(user_id, data):
    blocked_id = data.get('blocked_id')
    if Block.query.filter_by(blocker_id=user_id, blocked_id=blocked_id).first():
        return None, 'User already blocked'

    new_block = Block(blocker_id=user_id, blocked_id=blocked_id)
    db.session.add(new_block)
    db.session.commit()
    return new_block, 'User blocked successfully'

def get_user_followers(user_id):
    followers = Friendship.query.filter_by(followed_id=user_id).all()
    followers_list = [{'follower_id': f.follower_id, 'username': f.follower.username} for f in followers]
    return followers_list

def unfollow_user(user_id, data):
    followed_id = data.get('followed_id')
    friendship = Friendship.query.filter_by(follower_id=user_id, followed_id=followed_id).first()
    if not friendship:
        return None, 'You are not following this user'

    db.session.delete(friendship)
    db.session.commit()
    return None, 'Successfully unfollowed the user'

def toggle_user_privacy(user_id):
    user = User.query.get(user_id)
    if not user:
        return None, 'User not found'

    user.is_private = not user.is_private
    db.session.commit()
    return user, 'Privacy setting updated'



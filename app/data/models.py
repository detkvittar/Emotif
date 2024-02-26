from datetime import datetime
from app.data.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(121), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    profile_picture = db.Column(db.String(255))  # URL to the user's profile picture
    bio = db.Column(db.Text)  # Short bio or description about the user
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    mood = db.Column(db.String(15))  # Store mood as a string (e.g., 'happy', 'sad', etc.)
    mood_timestamp = db.Column(db.DateTime)
    mood_public = db.Column(db.Boolean, default=True)
    is_private = db.Column(db.Boolean, default=False)
    comments = db.relationship('Comment', backref='commenter', lazy='dynamic')
    reactions = db.relationship('Reaction', backref='reactor', lazy='dynamic')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'


class Friendship(db.Model):
    # Consider changing 'Friendship' to 'Followship' or smth
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(10), default='requested') # 'requested', 'accepted'

    follower = db.relationship('User', foreign_keys=[follower_id], backref=db.backref('followed', lazy='dynamic'), lazy='joined')
    followed = db.relationship('User', foreign_keys=[followed_id], backref=db.backref('followers', lazy='dynamic'), lazy='joined')

    def __repr__(self):
        return f'<Friendship {self.follower.username} -> {self.followed.username}>'


class FollowRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    requested_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    requester = db.relationship('User', foreign_keys=[requester_id], backref='sent_requests', lazy='joined')
    requested = db.relationship('User', foreign_keys=[requested_id], backref='received_requests', lazy='joined')

    def __repr__(self):
        return f'<FollowRequest from {self.requester.username} to {self.requested.username}>'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))
    hashtags = db.Column(db.String(255))
    location = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    reactions = db.relationship('Reaction', backref='post', lazy='dynamic')

    def __repr__(self):
        return f'<Post {self.title}>'


class ViewedPost(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('viewed_posts', lazy='dynamic'))
    post = db.relationship('Post', backref=db.backref('viewed_by', lazy='dynamic'))

    def __repr__(self):
        return f'<ViewedPost User {self.user_id} Post {self.post_id}>'


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f'<Comment {self.content}>'


class Reaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f'<Reaction {self.type}>'


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)  # e.g, 'New Comment'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # User who receives the notification
    data = db.Column(db.Text)  # Additional data or context for the notification (JSON format or similar)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)  # Time when the notification was generated
    read = db.Column(db.Boolean, default=False)  # Whether the notification has been read

    def __repr__(self):
        return f'<Notification {self.name} for User {self.user_id}>'


class Block(db.Model):
    blocker_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    blocked_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    blocker = db.relationship('User', foreign_keys=[blocker_id], backref='blocking', lazy='joined')
    blocked = db.relationship('User', foreign_keys=[blocked_id], backref='blocked_by', lazy='joined')

    def __repr__(self):
        return f'<Block Blocker {self.blocker.username} Blocked {self.blocked.username}>'

from app.data.models import Post, User, Friendship, ViewedPost

def get_unseen_posts_for_user(current_user_id):
    # Fetch unseen posts from followed users
    followed_users = Friendship.query.filter_by(follower_id=current_user_id, status='accepted').all()
    followed_ids = [user.followed_id for user in followed_users]

    seen_posts = ViewedPost.query.filter_by(user_id=current_user_id).all()
    seen_post_ids = [post.post_id for post in seen_posts]

    unseen_posts = Post.query.filter(
        Post.user_id.in_(followed_ids),
        Post.id.notin_(seen_post_ids)
    ).order_by(Post.date_posted.desc()).all()

    return unseen_posts

def discover_posts(current_user_id, hashtags=None, location=None):
    # Fetch posts based on hashtags or location from users not followed by the current user
    query = Post.query.filter(Post.user_id != current_user_id)
    if hashtags:
        query = query.filter(Post.hashtags.contains(hashtags))  # Adjust based on your actual implementation
    if location:
        query = query.filter(Post.location == location)  # Adjust based on your actual implementation

    return query.order_by(Post.date_posted.desc()).all()

import pytest
from post.models import Comment

@pytest.mark.django_db
def test_create_star(auth_client, user, active_post):

    payload = dict(
        post_slug=active_post.slug,
        user_id=user.id,
        comment='Do u love me ?',
    )

    response = auth_client.post('/post/comment_create/', payload)

    comment = Comment.objects.get(user=user, post=active_post)

    # 201: created success
    assert response.status_code == 201
    assert comment.comment == payload['comment']
    assert comment.user.id == payload['user_id']
    assert comment.post.slug == payload['post_slug']
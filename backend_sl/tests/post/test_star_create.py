import pytest
from post.models import Star

@pytest.mark.django_db
def test_create_star(auth_client, user, active_post):

    payload = dict(
        post_slug=active_post.slug,
        user_id=user.id,
    )

    response = auth_client.post('/post/star_create/', payload)

    star = Star.objects.get(user=user, post=active_post)

    # 201: created success
    assert response.status_code == 201
    assert star.post.slug == payload['post_slug']
    assert star.user.id == payload['user_id']


@pytest.mark.django_db
def test_create_duplicated_star_fail(auth_client, user, active_post):

    payload = dict(
        post_slug=active_post.slug,
        user_id=user.id,
    )

    response1 = auth_client.post('/post/star_create/', payload)
    response2 = auth_client.post('/post/star_create/', payload)

    # 201: created success
    assert response1.status_code == 201
    assert response2.status_code == 400
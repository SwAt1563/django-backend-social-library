import pytest
from post.models import Star


@pytest.mark.django_db
def test_star_remove(auth_client, user, active_post):
    star = Star.objects.create(user=user, post=active_post)

    payload = dict(
        post_slug=active_post.slug,
        user_id=user.id,
    )

    response = auth_client.delete('/post/star_remove/', payload)

    with pytest.raises(Star.DoesNotExist):
        star.refresh_from_db()
    assert response.status_code == 204

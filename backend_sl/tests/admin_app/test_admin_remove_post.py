import pytest
from post.models import Post



@pytest.mark.django_db
def test_admin_remove_post(un_active_post, auth_admin_client, admin):
    # order or parameters is important in the test function

    payload = dict(
        post_slug=un_active_post.slug,
        user_id=admin.id,
    )

    response = auth_admin_client.delete('/admin_app/remove_post/', payload)


    with pytest.raises(Post.DoesNotExist):
        un_active_post.refresh_from_db()

    assert response.status_code == 204



@pytest.mark.django_db
def test_admin_remove_post(active_post, auth_admin_client, admin):
    # order or parameters is important in the test function


    payload = dict(
        post_slug=active_post.slug,
        user_id=admin.id,
    )

    response = auth_admin_client.delete('/admin_app/remove_post/', payload)

    with pytest.raises(Post.DoesNotExist):
        active_post.refresh_from_db()

    assert response.status_code == 204

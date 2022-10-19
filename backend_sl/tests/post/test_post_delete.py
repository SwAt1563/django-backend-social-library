import pytest
from post.models import Post


@pytest.mark.django_db
def test_post_delete(auth_client, user, active_post):
    post_slug = active_post.slug

    payload = dict(
        user_id=user.id,
    )

    response = auth_client.delete(f'/post/post_delete/{post_slug}/', payload)

    # that mean when refresh the post to get the final result we will see that it not exist
    with pytest.raises(Post.DoesNotExist):
        active_post.refresh_from_db()

    assert response.status_code == 204


@pytest.mark.django_db
def test_post_delete_not_owner(auth_admin_client, admin, active_post):
    '''
    active_post: the user posted it not the admin
    so just the user can delete it no anyone can delete it
    admins has different links to delete posts
    '''
    post_slug = active_post.slug

    payload = dict(
        user_id=admin.id,
    )

    response = auth_admin_client.delete(f'/post/post_delete/{post_slug}/', payload)

    assert response.status_code == 403


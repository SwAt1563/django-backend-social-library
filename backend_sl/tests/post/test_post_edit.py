import pytest





@pytest.mark.django_db
def test_post_edit(auth_client, user, active_post):
    payload = dict(
        user_id=user.id,
        title='new_title',
    )
    old_post_title = active_post.title
    old_post_slug = active_post.slug

    # change title will affect on the slug
    response = auth_client.put(f'/post/post_edit/{old_post_slug}/', payload)

    active_post.refresh_from_db()

    assert active_post.title != old_post_title
    assert active_post.slug != old_post_slug
    assert response.status_code == 200

@pytest.mark.django_db
def test_post_edit_not_owner(auth_admin_client, admin, active_post):
    payload = dict(
        user_id=admin.id,
        title='new_title',
    )

    post_slug = active_post.slug

    # change title will affect on the slug
    response = auth_admin_client.put(f'/post/post_edit/{post_slug}/', payload)

    active_post.refresh_from_db()

    assert response.status_code == 403

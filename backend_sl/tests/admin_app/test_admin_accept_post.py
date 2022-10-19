import pytest


@pytest.mark.django_db
def test_admin_accept_post(un_active_post, auth_admin_client, admin):
    # order or parameters is important in the test function
    old_post_status = un_active_post.status
    payload = dict(
        post_slug=un_active_post.slug,
        user_id=admin.id,
    )

    response = auth_admin_client.post('/admin_app/accept_post/', payload)
    un_active_post.refresh_from_db()

    assert response.status_code == 200
    assert un_active_post.status == 'COMPLETED'
    assert un_active_post.status != old_post_status
import pytest
from notification.models import Notification
from friend.models import UserFollowing

@pytest.mark.django_db
def test_user_accept_post_notification(un_active_post, auth_admin_client, admin, user):
    # order or parameters is important in the test function

    payload = dict(
        post_slug=un_active_post.slug,
        user_id=admin.id,
    )

    response = auth_admin_client.post('/admin_app/accept_post/', payload)

    notification = Notification.objects.get(from_user=admin, to_user=user)

    assert response.status_code == 200
    assert notification is not None



@pytest.mark.django_db
def test_user_remove_post_notification(active_post, auth_admin_client, admin, user):
    # order or parameters is important in the test function


    payload = dict(
        post_slug=active_post.slug,
        user_id=admin.id,
    )

    response = auth_admin_client.delete('/admin_app/remove_post/', payload)

    notification = Notification.objects.get(from_user=admin, to_user=user)
    assert response.status_code == 204
    assert notification is not None





@pytest.mark.django_db
def test_follow_user_notification(auth_client, user, admin):
    payload = dict(
        user_id=user.id,
        following_user_slug=admin.profile.slug,
    )

    response = auth_client.post('/friend/follow/', payload)

    notification = Notification.objects.filter(from_user=user, to_user=admin).get()
    assert response.status_code == 201
    assert notification


@pytest.mark.django_db
def test_unfollow_user_notification(auth_client, user, admin):
    UserFollowing.objects.create(user_id=user, following_user_id=admin)

    payload = dict(
        user_id=user.id,
        following_user_slug=admin.profile.slug,
    )

    response = auth_client.delete('/friend/unfollow/', payload)

    notification = Notification.objects.filter(from_user=user, to_user=admin).get()
    assert response.status_code == 204
    assert notification
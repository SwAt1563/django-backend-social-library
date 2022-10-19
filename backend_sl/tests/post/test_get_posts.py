import pytest



@pytest.mark.django_db
def test_get_all_posts(auth_client, active_posts):

    response = auth_client.get('/post/all_posts/')
    data = response.data

    assert response.status_code == 200
    assert active_posts.count() == 3
    assert active_posts.count() == data['count']
    assert active_posts.get(title='test_post_1').title == data['results'][0]['title']


@pytest.mark.django_db
def test_get_all_posts_filter(auth_client, active_posts):

    payload = dict(
        filter='test_post_3'
    )
    response = auth_client.get('/post/all_posts/', payload)
    data = response.data

    assert response.status_code == 200
    assert data['count'] == 1
    assert 'test_post_3' == data['results'][0]['title']


@pytest.mark.django_db
def test_get_all_posts_by_owner(auth_client, active_posts, user):

    payload = dict(
        posts_owner_slug=user.profile.slug
    )
    response = auth_client.get('/post/all_posts/', payload)
    data = response.data

    assert response.status_code == 200
    assert data['count'] == 3

@pytest.mark.django_db
def test_get_all_posts_by_empty_owner(auth_admin_client, active_posts, admin):

    payload = dict(
        posts_owner_slug=admin.profile.slug
    )
    response = auth_admin_client.get('/post/all_posts/', payload)
    data = response.data

    assert response.status_code == 200
    assert data['count'] == 0


@pytest.mark.django_db
def test_get_all_posts_by_owner_and_filter(auth_client, active_posts, user):

    payload = dict(
        posts_owner_slug=user.profile.slug,
        filter='Just for testing_2',
    )
    response = auth_client.get('/post/all_posts/', payload)
    data = response.data

    assert response.status_code == 200
    assert data['count'] == 1
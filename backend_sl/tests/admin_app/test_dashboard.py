import pytest


@pytest.mark.django_db
def test_dashboard_get_all_posts(active_posts, auth_admin_client):
    '''
    Be careful -important-
    the order is sensitive here (active_posts, auth_admin_client) when use this
    the APIClient will be on admin
    but if we used (auth_admin_client, active_posts)
    the APIClient will be on user
    '''

    response = auth_admin_client.get('/admin_app/dashboard/')
    data = response.data

    assert response.status_code == 200
    assert active_posts.count() == 3
    assert active_posts.count() == data['count']
    assert active_posts.get(title='test_post_1').title == data['results'][0]['title']

@pytest.mark.django_db
def test_dashboard_filter(active_posts, auth_admin_client):

    payload = dict(
        filter='test_post_2'
    )
    response = auth_admin_client.get('/admin_app/dashboard/', payload)
    data = response.data

    assert response.status_code == 200
    assert data['count'] == 1
    assert 'test_post_2' == data['results'][0]['title']
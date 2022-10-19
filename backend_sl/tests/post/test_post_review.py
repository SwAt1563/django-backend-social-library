import pytest


@pytest.mark.django_db
def test_post_review(auth_client, user, active_post):
    post_slug = active_post.slug

    response = auth_client.get(f'/post/post_review/{post_slug}/')
    data = response.data

    assert response.status_code == 200
    assert data['title'] == active_post.title
    assert data['description'] == active_post.description
    assert data['slug'] == active_post.slug
    assert 'file' in data
    assert data['profile_slug'] == active_post.user.profile.slug
    assert data['username'] == active_post.user.username
    assert data['user_email'] == active_post.user.email



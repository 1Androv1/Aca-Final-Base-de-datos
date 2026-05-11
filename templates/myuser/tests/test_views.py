from django import urls
from django.contrib.auth import get_user_model
import pytest


@pytest.mark.parametrize('param', [
	('home'),
	('user_signup'),
	('user_login')
])
@pytest.mark.django_db
def test_render_views(client, param):
	temp_url = urls.reverse(param)
	resp = client.get(temp_url)
	assert resp.status_code == 200


@pytest.mark.django_db
def test_user_signup(client, user_data):
	user_model = get_user_model()
	assert user_model.objects.count() == 0
	signup_url = urls.reverse('user_signup')
	resp = client.post(signup_url, user_data)
	assert user_model.objects.count() == 1
	assert resp.status_code == 302


@pytest.mark.django_db
def test_user_login(client, create_test_user, user_data):
	user_model = get_user_model()
	assert user_model.objects.count() == 1
	login_url = urls.reverse('user_login')
	resp = client.post(login_url, data=user_data)
	assert resp.status_code == 302
	assert resp.url == urls.reverse('home')


@pytest.mark.django_db
def test_user_login_invalid_password(client, create_test_user, user_data):
	login_url = urls.reverse('user_login')
	invalid_data = dict(user_data)
	invalid_data['password'] = 'wrong-password'
	resp = client.post(login_url, data=invalid_data)
	assert resp.status_code == 200


@pytest.mark.django_db
def test_user_logout(client, authenticated_user):
	logout_url = urls.reverse('user_logout')
	resp = client.get(logout_url)
	assert resp.status_code == 302
	assert resp.url == urls.reverse('home')


@pytest.mark.django_db
def test_first_user_is_admin(user_data):
	user_model = get_user_model()
	first_user = user_model.objects.create_user(**user_data)
	assert first_user.is_admin is True


@pytest.mark.django_db
def test_second_user_is_not_admin(user_data):
	user_model = get_user_model()
	user_model.objects.create_user(**user_data)
	second_user_data = {
		'email': 'second_user@email.com',
		'name': 'second_user',
		'password': 'second_pass543',
	}
	second_user = user_model.objects.create_user(**second_user_data)
	assert second_user.is_admin is False


@pytest.mark.django_db
def test_user_update(client, authenticated_user):
	update_url = urls.reverse('user_update')
	update_data = {
		'email': 'updated_user@email.com',
		'name': 'updated_name',
		'password': '',
	}
	resp = client.post(update_url, data=update_data)
	assert resp.status_code == 302

	authenticated_user.refresh_from_db()
	assert authenticated_user.email == 'updated_user@email.com'
	assert authenticated_user.name == 'updated_name'


@pytest.mark.django_db
def test_admin_can_delete_user(client, user_data):
	user_model = get_user_model()
	admin_user = user_model.objects.create_user(**user_data)
	admin_user.set_password(user_data['password'])
	admin_user.save()

	other_user_data = {
		'email': 'delete_user@email.com',
		'name': 'delete_user',
		'password': 'delete_pass543',
	}
	other_user = user_model.objects.create_user(**other_user_data)
	assert user_model.objects.count() == 2

	client.login(**user_data)
	delete_url = urls.reverse('user_delete', kwargs={'user_id': other_user.id})
	resp = client.post(delete_url)
	assert resp.status_code == 302
	assert user_model.objects.filter(id=other_user.id).count() == 0


@pytest.mark.django_db
def test_non_admin_cannot_delete_user(client, user_data):
	user_model = get_user_model()
	admin_user = user_model.objects.create_user(**user_data)
	admin_user.set_password(user_data['password'])
	admin_user.save()

	non_admin_data = {
		'email': 'non_admin@email.com',
		'name': 'non_admin',
		'password': 'non_admin_pass543',
	}
	non_admin_user = user_model.objects.create_user(**non_admin_data)
	non_admin_user.set_password(non_admin_data['password'])
	non_admin_user.save()

	client.login(**non_admin_data)
	delete_url = urls.reverse('user_delete', kwargs={'user_id': admin_user.id})
	resp = client.post(delete_url)
	assert resp.status_code == 403
	assert user_model.objects.filter(id=admin_user.id).exists()

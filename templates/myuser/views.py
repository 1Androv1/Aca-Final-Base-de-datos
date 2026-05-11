from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def home(request):
	user_model = get_user_model()
	all_users = user_model.objects.all().order_by('id')
	return render(request, 'myuser/home.html', {'all_users': all_users})


def user_signup(request):
	if request.method == 'POST':
		email = request.POST['email']
		name = request.POST['name']
		password = request.POST['password']
		user_model = get_user_model()
		user_obj = user_model.objects.create_user(email=email, name=name)
		user_obj.set_password(password)
		user_obj.save()
		user_auth = authenticate(username=email, password=password)
		login(request, user_auth)
		return redirect('home')
	else:
		return render(request, 'myuser/signup.html')


def user_login(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		user_auth = authenticate(username=email, password=password)
		if user_auth is None:
			context = {'error': 'Correo o contrasena incorrectos.'}
			return render(request, 'myuser/login.html', context)
		login(request, user_auth)
		return redirect('home')
	else:
		return render(request, 'myuser/login.html')


def user_logout(request):
	logout(request)
	return redirect('home')


@login_required
def user_update(request):
	if request.method == 'POST':
		email = request.POST['email']
		name = request.POST['name']
		password = request.POST.get('password')
		user_model = get_user_model()
		email_exists = user_model.objects.exclude(id=request.user.id).filter(email=email).exists()
		if email_exists:
			context = {
				'error': 'El correo ya esta en uso por otro usuario.',
				'form_user': request.user,
			}
			return render(request, 'myuser/user_update.html', context)

		request.user.email = email
		request.user.name = name
		if password:
			request.user.set_password(password)
		request.user.save()

		if password:
			user_auth = authenticate(username=email, password=password)
			if user_auth is not None:
				login(request, user_auth)
		return redirect('home')

	return render(request, 'myuser/user_update.html', {'form_user': request.user})


@login_required
def user_delete(request, user_id):
	if not request.user.is_admin:
		return HttpResponseForbidden('Solo el administrador puede eliminar usuarios.')

	if request.method != 'POST':
		return redirect('home')

	user_model = get_user_model()
	user_to_delete = get_object_or_404(user_model, id=user_id)
	is_self_delete = user_to_delete.id == request.user.id
	user_to_delete.delete()

	if is_self_delete:
		logout(request)

	return redirect('home')


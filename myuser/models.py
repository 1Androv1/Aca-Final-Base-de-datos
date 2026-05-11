from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone


class MyUserManager(BaseUserManager):
	def create_user(self, email, name, password=None):
		if not email:
			raise ValueError('El usuario debe tener un correo electronico.')

		is_first_user = self.model.objects.count() == 0
		my_user = self.model(
			email=self.normalize_email(email),
			name=name,
			is_admin=is_first_user,
		)
		my_user.set_password(password)
		my_user.save(using=self._db)
		return my_user

	def create_superuser(self, email, name, password=None):
		my_user = self.create_user(email=email, name=name, password=password)
		my_user.is_admin = True
		my_user.save(using=self._db)
		return my_user


class MyUser(AbstractBaseUser):
	email = models.EmailField(max_length=150, unique=True)
	name = models.CharField(max_length=100, blank=True)
	is_admin = models.BooleanField(default=False)
	objects = MyUserManager()
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name']

	@property
	def is_staff(self):
		return self.is_admin

	@property
	def is_superuser(self):
		return self.is_admin

	@property
	def is_active(self):
		return True

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return self.is_admin

	def __str__(self):
		return self.email

	class Meta:
		verbose_name = 'Usuario'
		verbose_name_plural = 'Usuarios'


class Estudiante(models.Model):
	documento = models.CharField(max_length=20, unique=True)
	nombres = models.CharField(max_length=100)
	apellidos = models.CharField(max_length=100)
	correo = models.EmailField(max_length=150, unique=True)
	telefono = models.CharField(max_length=20, blank=True, null=True)
	fecha_nacimiento = models.DateField()
	fecha_registro = models.DateTimeField(default=timezone.now)
	estado = models.CharField(max_length=20, default='ACTIVO')

	def __str__(self):
		return f'{self.nombres} {self.apellidos}'

	class Meta:
		managed = False
		db_table = 'ESTUDIANTES'
		ordering = ['apellidos', 'nombres']
		verbose_name = 'Estudiante'
		verbose_name_plural = 'Estudiantes'


class Docente(models.Model):
	documento = models.CharField(max_length=20, unique=True)
	nombres = models.CharField(max_length=100)
	apellidos = models.CharField(max_length=100)
	correo = models.EmailField(max_length=150, unique=True)
	especialidad = models.CharField(max_length=120)
	estado = models.CharField(max_length=20, default='ACTIVO')

	def __str__(self):
		return f'{self.nombres} {self.apellidos}'

	class Meta:
		managed = False
		db_table = 'DOCENTES'
		ordering = ['apellidos', 'nombres']
		verbose_name = 'Docente'
		verbose_name_plural = 'Docentes'


class Curso(models.Model):
	codigo = models.CharField(max_length=20, unique=True)
	nombre = models.CharField(max_length=120)
	creditos = models.IntegerField()
	cupo_maximo = models.IntegerField()
	docente = models.ForeignKey(Docente, on_delete=models.PROTECT, related_name='cursos')
	estado = models.CharField(max_length=20, default='ACTIVO')

	def __str__(self):
		return f'{self.codigo} - {self.nombre}'

	class Meta:
		managed = False
		db_table = 'CURSOS'
		ordering = ['codigo']
		verbose_name = 'Curso'
		verbose_name_plural = 'Cursos'


class Matricula(models.Model):
	estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name='matriculas')
	curso = models.ForeignKey(Curso, on_delete=models.PROTECT, related_name='matriculas')
	fecha_matricula = models.DateTimeField(default=timezone.now)
	nota_final = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
	estado = models.CharField(max_length=20, default='MATRICULADO')

	def __str__(self):
		return f'{self.estudiante} - {self.curso}'

	class Meta:
		managed = False
		db_table = 'MATRICULAS'
		ordering = ['-fecha_matricula']
		unique_together = ('estudiante', 'curso')
		verbose_name = 'Matricula'
		verbose_name_plural = 'Matriculas'


class AuditoriaMatricula(models.Model):
	matricula_id = models.IntegerField()
	accion = models.CharField(max_length=20)
	usuario_bd = models.CharField(max_length=80)
	fecha_evento = models.DateTimeField(default=timezone.now)
	detalle = models.CharField(max_length=500, blank=True, null=True)

	def __str__(self):
		return f'{self.accion} - {self.matricula_id}'

	class Meta:
		managed = False
		db_table = 'AUDITORIA_MATRICULAS'
		ordering = ['-fecha_evento']
		verbose_name = 'Auditoria de matricula'
		verbose_name_plural = 'Auditoria de matriculas'

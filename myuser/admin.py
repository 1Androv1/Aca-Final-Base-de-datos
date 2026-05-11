from django.contrib import admin
from .models import MyUser, Estudiante, Docente, Curso, Matricula, AuditoriaMatricula


@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
	list_display = ('id', 'email', 'name', 'is_admin')
	search_fields = ('email', 'name')
	list_filter = ('is_admin',)


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
	list_display = ('id', 'documento', 'nombres', 'apellidos', 'correo', 'estado')
	search_fields = ('documento', 'nombres', 'apellidos', 'correo')
	list_filter = ('estado',)


@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
	list_display = ('id', 'documento', 'nombres', 'apellidos', 'especialidad', 'estado')
	search_fields = ('documento', 'nombres', 'apellidos', 'especialidad')
	list_filter = ('estado', 'especialidad')


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
	list_display = ('id', 'codigo', 'nombre', 'creditos', 'cupo_maximo', 'docente', 'estado')
	search_fields = ('codigo', 'nombre')
	list_filter = ('estado', 'creditos')


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
	list_display = ('id', 'estudiante', 'curso', 'fecha_matricula', 'nota_final', 'estado')
	search_fields = ('estudiante__documento', 'estudiante__nombres', 'estudiante__apellidos', 'curso__codigo', 'curso__nombre')
	list_filter = ('estado', 'curso')


@admin.register(AuditoriaMatricula)
class AuditoriaMatriculaAdmin(admin.ModelAdmin):
	list_display = ('id', 'matricula_id', 'accion', 'usuario_bd', 'fecha_evento')
	search_fields = ('accion', 'usuario_bd', 'detalle')
	list_filter = ('accion',)
	readonly_fields = ('matricula_id', 'accion', 'usuario_bd', 'fecha_evento', 'detalle')

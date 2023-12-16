from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    SuperUserAccount,
	AdminAccount,
	InstructorAccount,
	ParentAccount,
	StudentAccount,
	CompanyRequest,
	Company,
	ExtraPermissions
 
  )


class SuperUserAccountAdmin(UserAdmin):
	list_display 	  = (
        'email', 'username', 'first_name',
        'last_name', 'is_active', 'is_superuser',
        'is_staff'
    )
 
	search_fields 	  = ('email', 'username')
	readonly_fields	  = ('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter 	  = ()
	fieldsets = (
		(None, {
			"fields": (
				'email', 'username', 'password', 'first_name', 'last_name')}),
		('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
		('Personal', {'fields': ('date_joined', 'last_login')})
	)
	add_fieldsets = (
		(None, {
				'classes': ('wide',),
				'fields': ('email', 'username', 'password1', 'password2', 'first_name', 'last_name',
               	'is_staff', 'is_active', 'is_superuser')
			 }
		),
	)

admin.site.register(SuperUserAccount, SuperUserAccountAdmin)

class AdminAccountAdmin(UserAdmin):
	list_display 	  = (
        'email', 'username', 'first_name',
        'last_name', 'company_name',
        'is_active', 'admin_type'
    )
 
	search_fields 	  = ('email', 'username', 'company_name', 'admin_type')
	readonly_fields	  = ('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter 	  = ()
	fieldsets = (
		(None, {
			"fields": (
				'email', 'username', 'password', 'first_name', 'last_name', 'company_name', 'admin_type')}),
		('Permissions', {'fields': ('is_active',)}),
		('Personal', {'fields': ('date_joined', 'last_login')})
	)
	add_fieldsets = (
		(None, {
				'classes': ('wide',),
				'fields': ('email', 'username', 'password1', 'password2', 'first_name', 'last_name', 'company_name', 'admin_type', 'is_active')
			 }
		),
	)
admin.site.register(AdminAccount, AdminAccountAdmin)


class InstructorAccountAdmin(UserAdmin):
	list_display 	  = (
        'email', 'username', 'first_name', 'last_name', 'department',
        'instructor_type', 'company_name', 'is_active'
    )
 
	search_fields 	  = ('email', 'username', 'company_name', 'instructor_type', 'department')
	readonly_fields	  = ('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter 	  = ()
	fieldsets = (
		(None, {
			"fields": (
				'email', 'username', 'password', 'first_name', 'last_name', 'company_name', 'department', 'instructor_type')}),
		('Permissions', {'fields': ('is_active',)}),
		('Personal', {'fields': ('date_joined', 'last_login')})
	)
	add_fieldsets = (
		(None, {
				'classes': ('wide',),
				'fields': ('email', 'username', 'password1', 'password2', 'first_name', 'last_name', 'company_name', 'department', 'instructor_type', 'is_active')
			 }
		),
	)
admin.site.register(InstructorAccount, InstructorAccountAdmin)


class ParentAccountAdmin(UserAdmin):
	list_display 	  = (
        'email', 'username', 'first_name', 'national_id',
        'last_name', 'is_active',
    )
 
	search_fields 	  = ('email', 'username', 'national_id')
	readonly_fields	  = ('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter 	  = ()
	fieldsets = (
		(None, {
			"fields": (
				'email', 'username', 'password', 'first_name', 'last_name', 'national_id')}),
		('Permissions', {'fields': ('is_active',)}),
		('Personal', {'fields': ('date_joined', 'last_login')})
	)
	add_fieldsets = (
		(None, {
				'classes': ('wide',),
				'fields': ('email', 'username', 'password1', 'password2', 'first_name', 'last_name', 'national_id', 'is_active')
			 }
		),
	)
admin.site.register(ParentAccount, ParentAccountAdmin)


class StudentAccountAdmin(UserAdmin):
	list_display 	  = (
        'email', 'username', 'first_name',
        'last_name', 'company_name', 'department',
        'national_id', 'parent_national_id', 'is_active'
    )
 
	search_fields 	  = ('email', 'username', 'company_name', 'national_id', 'parent_national_id', 'department')
	readonly_fields	  = ('date_joined', 'last_login')

	filter_horizontal = ()
	list_filter 	  = ()
	fieldsets = (
		(None, {
			"fields": (
				'email', 'username', 'password', 'first_name', 'last_name', 'company_name', 'department', 'gender', 'age', 'national_id', 'parent_national_id')}),
		('Permissions', {'fields': ('is_active',)}),
		('Personal', {'fields': ('date_joined', 'last_login')})
	)
	add_fieldsets = (
		(None, {
				'classes': ('wide',),
				'fields': ('email', 'username', 'password1', 'password2', 'first_name', 'last_name', 'company_name', 'department', 'gender', 'age', 'national_id', 'parent_national_id', 'is_active')
			 }
		),
	)
admin.site.register(StudentAccount, StudentAccountAdmin)

admin.site.register(CompanyRequest)
admin.site.register(Company)
admin.site.register(ExtraPermissions)

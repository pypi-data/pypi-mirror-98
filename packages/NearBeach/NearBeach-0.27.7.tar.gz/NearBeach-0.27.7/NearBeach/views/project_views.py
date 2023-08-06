import urllib

from django.contrib.auth.decorators import login_required
from NearBeach.models import *
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.template import loader
from django.db.models import Sum, Q, Min
from NearBeach.forms import *
from NearBeach.views.tools.internal_functions import *
from NearBeach.user_permissions import return_user_permission_level

import json, urllib3


@login_required(login_url='login',redirect_field_name="")
def new_project(request):
    """

    :param request:
    :return:
    """
    # ADD IN PERMISSIONS CHECKER

    # Template
    t = loader.get_template('NearBeach/projects/new_project.html')

    # Get data we require
    group_results = group.objects.filter(
        is_deleted=False,
    )

    # Context
    c = {
        'group_results': serializers.serialize('json',group_results),
    }

    return HttpResponse(t.render(c,request))


@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name='')
def new_project_save(request):
    """

    :param request:
    :return:
    """

    # CHECK USERS PERMISSION HERE

    # Get the form data
    form = NewProjectForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Create the project
    project_submit = project(
        change_user=request.user,
        creation_user=request.user,
        project_name=form.cleaned_data['project_name'],
        project_description=form.cleaned_data['project_description'],
        project_start_date=form.cleaned_data['project_start_date'],
        project_end_date=form.cleaned_data['project_end_date'],
        organisation=form.cleaned_data['organisation'],
    )
    project_submit.save()

    # Get the group list and apply the permissions
    group_list = request.POST.getlist("group_list")

    for single_group in group_list:
        # Get the group instance
        group_instance = group.objects.get(group_id=single_group)

        # Save the group instance against object assignment
        submit_object_assignment = object_assignment(
            group_id=group_instance,
            project=project_submit,
            change_user=request.user,
        )

        # Save
        submit_object_assignment.save()

    # Send back requirement_information URL
    return HttpResponse(reverse('project_information', args={project_submit.project_id}))


@login_required(login_url='login',redirect_field_name="")
def project_information(request,project_id):
    """

    :param request:
    :param project_id:
    :return:
    """
    # ADD IN PERMISSIONS CHECKER

    # Template
    t = loader.get_template('NearBeach/projects/project_information.html')

    # Get data
    project_results = project.objects.get(project_id=project_id)

    organisation_results = organisation.objects.filter(
        is_deleted=False,
        organisation_id=project_results.organisation_id,
    )

    # Context
    c = {
        'organisation_results': serializers.serialize('json',organisation_results),
        'project_id': project_id,
        'project_results': serializers.serialize('json',[project_results]),
    }

    return HttpResponse(t.render(c,request))


@require_http_methods(['POST'])
@login_required(login_url='login',redirect_field_name='')
def project_information_save(request,project_id):
    """

    :param request:
    :param project_id:
    :return:
    """

    # ADD IN PERMISSION CHECKER

    # Get the form data
    form = ProjectForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the project data
    project_update = project.objects.get(project_id=project_id)
    project_update.project_name = form.cleaned_data['project_name']
    project_update.project_description = form.cleaned_data['project_description']
    project_update.project_start_date = form.cleaned_data['project_start_date']
    project_update.project_end_date = form.cleaned_data['project_end_date']

    # Save
    project_update.save()

    return HttpResponse("Good")

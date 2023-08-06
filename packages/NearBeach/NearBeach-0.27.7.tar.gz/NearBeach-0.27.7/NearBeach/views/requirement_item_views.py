from django.contrib.auth.decorators import login_required
from NearBeach.models import *
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.template import loader
from django.db.models import Sum, Q, Min
from NearBeach.forms import *
from NearBeach.user_permissions import return_user_permission_level
from NearBeach.views.requirement_views import get_requirement_items
from django.views.decorators.http import require_http_methods

import json


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def add_requirement_item_link(request, requirement_item_id):
    # ADD IN PERMISSION
    permission_results = return_user_permission_level(request, None, ['requirement', 'requirement_link','requirement_item'])
    # What about requirement items? Will need to fix this elegantly.

    if permission_results['requirement'] < 2 & permission_results['requirement_item'] < 2:
        return HttpResponseRedirect(reverse('permission_denied'))

    form = AddRequirementLinkForm(request.POST)

    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Get the requirement instnace
    requirement_item_instance = requirement_item.objects.get(requirement_item_id=requirement_item_id)

    # Get the project list from the form
    for row in request.POST.getlist("project"):
        submit_object_assignment = object_assignment(
            requirement_item=requirement_item_instance,
            project=project.objects.get(project_id=row),
            change_user=request.user,
        )
        submit_object_assignment.save()

    for row in request.POST.getlist("task"):
        submit_object_assignment = object_assignment(
            requirement_item=requirement_item_instance,
            task=task.objects.get(task_id=row),
            change_user=request.user,
        )
        submit_object_assignment.save()

    for row in request.POST.getlist("opportunity"):
        submit_object_assignment = object_assignment(
            requirement_item=requirement_item_instance,
            opportunity=opportunity.objects.get(opportunity_id=row),
            change_user=request.user,
        )
        submit_object_assignment.save()

    return HttpResponse("Success")


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def get_requirement_item_links_list(request,requirement_item_id):
    """

    :param request:
    :param requirement_item_id:
    :return:
    """

    # Use object_assignment to get the requirme
    link_results = object_assignment.objects.filter(
        Q(
            is_deleted=False,
            requirement_item_id=requirement_item_id
        ) & Q(
            Q(opportunity_id__isnull=False) |
            Q(quote_id__isnull=False) |
            Q(project_id__isnull=False) |
            Q(task_id__isnull=False)
        )
    ).values(
        'opportunity_id',
        'opportunity_id__opportunity_name',
        'opportunity_id__opportunity_stage_id__opportunity_stage_description',
        'quote_id',
        'quote_id__quote_title',
        'quote_id__quote_stage_id__quote_stage',
        'project_id',
        'project_id__project_name',
        'project_id__project_status',
        'task_id',
        'task_id__task_short_description',
        'task_id__task_status',
        'requirement_item_id',
        'requirement_item_id__requirement_item_title',
    )

    """
    As explained on stack overflow here - https://stackoverflow.com/questions/7650448/django-serialize-queryset-values-into-json#31994176
    We need to Django's serializers can't handle a ValuesQuerySet. However, you can serialize by using a standard 
    json.dumps() and transforming your ValuesQuerySet to a list by using list().[sic]
    """

    # Send back json data
    json_results = json.dumps(list(link_results), cls=DjangoJSONEncoder)

    return HttpResponse(json_results, content_type='application/json')


@login_required(login_url='login', redirect_field_name="")
def get_user_requirement_item_permissions(request, requirement_id):
    """
    Use the requirement_id and find out if the user has access to this requirement
    :param requirement_id:
    :return:
    """
    requirement_groups = object_assignment.objects.filter(
        is_deleted=False,
        # requirement_id=requirement_id
    ).values('group_id')

    if requirement_id > 0:
        # Make sure to filter by requirement groups
        requirement_groups = requirement_groups.filter(
            requirement_id=requirement_id
        )

    return return_user_permission_level(request, requirement_groups, ['requirement', 'requirement_link'])


@login_required(login_url='login', redirect_field_name="")
def new_requirement_item(request, requirement_id):
    # Check to see if POST
    if not request.method == "POST":
        return HttpResponseBadRequest("Sorry - needs to be in POST")

    # Check user permissions
    permission_results = get_user_requirement_item_permissions(request, requirement_id)

    # If user has no permissions to create requirements or requirement items, then send them to the appropriate location
    if permission_results['requirement'] <= 2 and permission_results['requirement_item'] <= 2:
        # Users can not create requirement.
        return HttpResponseRedirect(reverse('permission_denied'))

    # Get the data into the form for cleaning
    form = NewRequirementItemForm(request.POST)

    # Check to make sure there are no errors in the form
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Save the data
    submit_requirement_item = requirement_item(
        requirement=requirement.objects.get(requirement_id=requirement_id),
        requirement_item_title=form.cleaned_data['requirement_item_title'],
        requirement_item_scope=form.cleaned_data['requirement_item_scope'],
        requirement_item_status=form.cleaned_data['requirement_item_status'],
        requirement_item_type=form.cleaned_data['requirement_item_type'],
        change_user=request.user,
    )
    submit_requirement_item.save()

    # Actuall return all the new requirement_item results to feed upstream
    return get_requirement_items(request, requirement_id)


@login_required(login_url='login', redirect_field_name="")
def requirement_item_information(request, requirement_item_id):
    """
        Loads the requirement item information.
        :param request:
        :param requirement_item_id:
        :return:
        """
    # Get the requirement information
    requirement_item_results = requirement_item.objects.get(requirement_item_id=requirement_item_id)

    # Check the permissions
    permission_results = get_user_requirement_item_permissions(request, requirement_item_id)

    # If user has no permissions to this requirement send them to the appropriate location
    if permission_results['requirement'] == 0:
        # Users who create the requirement get at least read only
        if requirement_item_results.creation_user == request.user:
            return HttpResponseRedirect(reverse('requirement_readonly', args={requirement_item_id}))

        # Users who did not create the requirement get sent to permission denied.
        return HttpResponseRedirect(reverse('permission_denied'))

    # If the requirement has been closed - send user to the read only section
    if requirement_item_results.requirement_item_status.status_is_closed:
        return HttpResponseRedirect(reverse('requirement_readonly', args={requirement_item_id}))

    # Load template
    t = loader.get_template('NearBeach/requirement_items/requirement_item_information.html')

    # Get any extra data required
    organisation_results = organisation.objects.get(
        organisation_id=requirement_item_results.requirement.organisation_id,
    )

    status_list = list_of_requirement_item_status.objects.filter(
        is_deleted=False,
        status_is_closed=False,
    )

    type_list = list_of_requirement_item_type.objects.filter(
        is_deleted=False,
    )

    group_results = group.objects.filter(
        is_deleted=False,
    )

    # context
    c = {
        'group_results': serializers.serialize("json", group_results),
        'organisation_results': serializers.serialize("json", [organisation_results]),
        'permission_results': permission_results,
        'requirement_item_id': requirement_item_id,
        'requirement_item_results': serializers.serialize("json", [requirement_item_results]),
        'status_list': serializers.serialize("json", status_list),
        'type_list': serializers.serialize("json", type_list),
    }

    return HttpResponse(t.render(c, request))


@require_http_methods(['POST'])
@login_required(login_url='login', redirect_field_name="")
def requirement_information_save(request, requirement_item_id):
    """
    The following will save data
    :param request:
    :param requirement_id:
    :return:
    """
    # Check the permissions
    permission_results = get_user_requirement_item_permissions(request, requirement_item_id)

    # If user has no permissions to this requirement send them to the appropriate location
    if permission_results['requirement'] <= 1:
        return HttpResponseRedirect(reverse('permission_denied'))

    # Get form data
    form = UpdateRequirementItemForm(request.POST)
    if not form.is_valid():
        return HttpResponseBadRequest(form.errors)

    # Save the data
    requirement_item_submit = requirement_item.objects.get(requirement_item_id=requirement_item_id)
    requirement_item_submit.change_user = request.user
    requirement_item_submit.requirement_item_title = form.cleaned_data['requirement_item_title']
    requirement_item_submit.requirement_item_scope = form.cleaned_data['requirement_item_scope']
    requirement_item_submit.requirement_item_status = form.cleaned_data['requirement_item_status']
    requirement_item_submit.requirement_item_type = form.cleaned_data['requirement_item_type']
    requirement_item_submit.save()

    # Send back an empty response
    return HttpResponse("")

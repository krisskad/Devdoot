from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from devdoot.models import ExtendedUser, ProblemReport, PublicProblem, Cities, SolvedProblem, ProblemType
from django.contrib import messages
from django.db import close_old_connections
import json


# Create your views here.
@login_required(login_url='login')
def dashboard_page(request):

    username = request.user
    anymnos = 1

    try:
        detail = ExtendedUser.objects.get(user=username)
        city_id = detail.city_id
        jsonDec = json.decoder.JSONDecoder()
        problems_temp = jsonDec.decode(detail.problem_types)
        problems_pk = []

        for i in problems_temp:
            problems_pk.append(int(i))
        total_problem_count = PublicProblem.objects.filter(city=city_id, problem_type__in=problems_pk).count()
    except ExtendedUser.DoesNotExist:
        anymnos = 0

    if anymnos:

        pending_problems = SolvedProblem.objects.filter(is_solved=0, solved_problem__in=problems_pk).count()
        total_solved = SolvedProblem.objects.filter(is_solved=1, solved_problem__in=problems_pk).count()

        context = {
                   'username': username, 'pending_problems': pending_problems,
                   'total_problem_count': total_problem_count,
                   'total_solved': total_solved, 'pending_problems': pending_problems}
        return render(request, 'dashboard/dashboard.html', context)
    else:
        msg = "No Data Available"
        context = {'first_name': msg, 'last_name': msg, 'email': msg, 'username': username,
                   'public': msg}
        close_old_connections()

        return render(request, 'dashboard/dashboard.html', context)


@login_required(login_url='login')
def profilePage(request):

    username = request.user

    try:
        detail = ExtendedUser.objects.get(user=username)
    except ExtendedUser.DoesNotExist:
        detail = "User Does not exist"

    if detail != "User Does not exist":
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        state = detail.state
        city = detail.city
        address = detail.address
        groupname = detail.group_name
        jsonDec = json.decoder.JSONDecoder()
        problems_temp = jsonDec.decode(detail.problem_types)
        problems_pk = []

        for i in problems_temp:
            problems_pk.append(int(i))

        problems = ProblemType.objects.filter(pk__in=problems_pk)
        # print(problems)

        all_problems = ProblemType.objects.all()

        if request.method == 'POST':

            s_fn = request.POST.get('first_name')
            s_ln = request.POST.get('last_name')
            s_m = request.POST.get('mobile')
            s_email = request.POST.get('email')
            s_problems = request.POST.getlist('problemtypes[]')
            s_gender = request.POST.get('gender')
            user_instance = User.objects.get(id=request.user.id)
            check = User.objects.all().exclude(id=request.user.id)
            if len(s_m) != 10:
                messages.info(request, 'Mobile number must be 10 digits long')
            else:
                try:
                    check.get(username=s_m)
                    messages.info(request, 'Mobile number is already exist')

                except User.DoesNotExist:
                    user_instance.username = s_m

                try:
                    check.get(email=s_email)
                    messages.info(request, 'Email is already exist')

                except User.DoesNotExist:
                    user_instance.email = s_email

                finally:
                    if s_fn and s_ln and s_problems and s_gender:
                        user_instance.first_name = s_fn
                        user_instance.last_name = s_ln
                        user_instance.save()

                        detail.gender = s_gender
                        if len(s_problems) > 0:
                            s_problems = json.dumps(s_problems)
                        else:
                            s_problems = None
                        detail.problem_types = s_problems
                        detail.save()
        context = {'first_name': first_name, 'last_name': last_name,
                   'email': email, 'username': username, 'detail': detail,
                   'state': state, 'city': city, 'address': address, 'problems': problems, 'all_problems':all_problems,
                   'groupname': groupname}
        close_old_connections()

        return render(request, 'dashboard/profile.html', context)
    else:
        msg = "No Data Available"
        context = {'first_name': msg, 'last_name': msg,
                   'email': msg, 'username': username, 'detail': msg,
                   'state': msg, 'city': msg, 'address': msg, 'problems': msg, 'all_problems':msg,
                   'groupname': msg}
        close_old_connections()

        return render(request, 'dashboard/profile.html', context)


@login_required(login_url='login')
def requested_problems(request):

    username = request.user
    first_name = request.user.first_name
    last_name = request.user.last_name
    all_problems = ProblemType.objects.all()

    try:
        detail = ExtendedUser.objects.get(user=username)
    except ExtendedUser.DoesNotExist:
        detail = "Data Not Available"

    cityid = detail.city_id

    city = Cities.objects.get(id=cityid)

    problem_id = request.GET.get('solved')
    if problem_id:
        try:
            problem_instance = PublicProblem.objects.get(id=problem_id)
            solve_save = SolvedProblem.objects.get(solved_problem=problem_instance)
            # solve_save.is_solved = 1
            # solve_save.save()
            # print("update")
        except SolvedProblem.DoesNotExist:
            solve_save = SolvedProblem(solved_problem=problem_instance, is_solved=0, solved_by=detail)
            solve_save.save()
            # print('save')

    # all_problems = PublicProblem.objects.all()
    # cityid_p = PublicProblem.objects.filter(city=453).values_list('city', flat=True)
    a = SolvedProblem.objects.filter(solved_by=detail.id).values('solved_problem')

    jsonDec = json.decoder.JSONDecoder()
    problems_temp = jsonDec.decode(detail.problem_types)
    problems_pk = []

    for i in problems_temp:
        problems_pk.append(int(i))

    related_data = list(PublicProblem.objects.filter(city=city, problem_type__in=problems_pk).exclude(id__in=a).select_related().order_by('-timestamp'))

    if request.method == 'POST':
        title = request.POST.get('report_options')
        description = request.POST.get('report_description')
        reported_to = PublicProblem.objects.get(id=request.POST.get('reported_to'))

        if title and description and reported_to:
            report = ProblemReport(submitted_by=detail,
                                   title=title, description=description,
                                   reported_to=reported_to)
            report.save()

    context = {'first_name': first_name, 'last_name': last_name, 'problems': related_data, 'all_problems':all_problems}
    close_old_connections()

    return render(request, 'dashboard/requestedproblem.html', context)


@login_required(login_url='login')
def solved_problems(request):

    related_data = SolvedProblem.objects.filter(solved_by=request.user.id).prefetch_related('solved_by', 'solved_problem')
    # all_problems = ProblemType.objects.all()

    # related_data[0].solved_by.user.get_full_name()
    # related_data = related_data.filter(is_solved=1)

    problem_id = request.GET.get('not_solved')
    if problem_id:
        problem_instance = SolvedProblem.objects.get(id=problem_id)
        problem_instance.delete()

    context = {'problems': related_data}
    close_old_connections()

    return render(request, 'dashboard/solvedproblems.html', context)

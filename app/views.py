from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.db.models import *
from datetime import datetime,date
from .models import *

# Create your views here.
def home(request):
    return render(request,"home.html")
def student_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        obj = authenticate(username = username,password = password)
        if obj is not None:
            if obj.role == "student":
                login(request,obj)
                return redirect("/student-dashboard/")
        return render(request,"student_login.html",context={'error':"error"})
    return render(request,"student_login.html")
def staff_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        obj = authenticate(username = username,password = password)
        if obj is not None:
            if obj.role == "staff":
                login(request,obj)
                return redirect("/staff-dashboard/")
        return render(request,"staff_login.html",context={'error':"error"})
    return render(request,"staff_login.html")
def admin_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        obj = authenticate(username = username,password = password)
        if obj is not None:
            if obj.role == "admin":
                login(request,obj)
                return redirect("/admin-dashboard/")
        return render(request,"admin_login.html",context={'error':"error"})
    return render(request,"admin_login.html")

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url="/admin-login/")
def admin_dashboard(request):
    total_student = student.objects.count()
    total_male = student.objects.filter(gender = 'Male').count()
    total_female = student.objects.filter(gender = 'Female').count()
    total_staff = staff.objects.count()
    return render(request,"admin.html",context={'user':request.user,'tot_stu':total_student,'tot_staff':total_staff,'tot_male':total_male,'tot_female':total_female})
@login_required(login_url="/admin-login/")
def student_page(request):
    students = student.objects.select_related('dept').all().order_by('rollno')
    if request.method == "POST":
        search = request.POST.get('q')
        students = students.filter(Q(rollno__icontains = search) | Q(name__icontains = search) | Q(regno__icontains = search) | Q(course__name__icontains = search) | Q(email__icontains = search) | Q(gender__contains = search) | Q(phone__icontains = search) | Q(dob__icontains = search))

    return render(request,"admin_student_page.html",context={'user':request.user,'students':students})
@login_required(login_url="/admin-login/")
def add_student_page(request):
    dept = department.objects.all()
    degre = degree.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        rollno = request.POST.get("rollno")
        regno = request.POST.get("regno")
        dob = request.POST.get("dob")
        depart = request.POST.get("dept")
        course = request.POST.get("course")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        admission = request.POST.get("admission")
        obj = student.objects.create(name = name, rollno = rollno, regno = regno, dob = dob, dept_id = depart, course_id = course, gender = gender, email = email, phone = phone, admission = admission )
        sub = subject.objects.filter(course_id = course)
        for i in sub:
            add_sems = semester.objects.create(stu = obj, sub = i, sem = i.semester, internal = 0, external = 0)
            add_sems.save()
        obj.save()
        dob_obj = datetime.strptime(dob,"%Y-%m-%d")
        dob_formatted = dob_obj.strftime("%d-%m-%Y")
        CustomUser.objects.create_user(username=email, password=dob_formatted, first_name = name, role = "student")
        return redirect("/admin-dashboard/student/")
    return render(request,"add_student.html",context={'title':"Add Student",'user':request.user,'dept':dept,'degree':degre})
def delete_student(request,rollno):
    obj = student.objects.get(rollno = rollno)
    user = CustomUser.objects.get(username = obj.email)
    user.delete()
    user = semester.objects.filter(stu__name = obj.name)
    user.delete()
    obj.delete()
    return redirect("/admin-dashboard/student/")
def update_student(request,rollno):
    obj = student.objects.get(rollno = rollno)
    user = CustomUser.objects.get(username = obj.email)
    dept = department.objects.all()
    degre = degree.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        rollno = request.POST.get("rollno")
        regno = request.POST.get("regno")
        dob = request.POST.get("dob")
        depart = request.POST.get("dept")
        course = request.POST.get("course")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        admission = request.POST.get("admission")
        obj.name = name
        obj.rollno = rollno
        obj.regno = regno
        obj.dob = dob
        obj.dept_id = depart
        obj.course_id = course
        obj.gender = gender
        obj.email = email
        obj.phone = phone
        obj.admission = admission
        obj.save()
        dob_obj = datetime.strptime(dob,"%Y-%m-%d")
        dob_formatted = dob_obj.strftime("%d-%m-%Y")
        user.password = make_password(dob_formatted)
        user.username = email
        user.save()
        return redirect("/admin-dashboard/student/")
    return render(request,"update_student.html",context={'student':obj,'dept':dept,'degree':degre})

@login_required(login_url="/admin-login/")
def admin_staff_page(request):
    obj = staff.objects.select_related('dept').all().order_by('name')
    if request.method == "POST":
        search = request.POST.get('q')
        obj = obj.filter(Q(name__icontains = search) | Q(email__icontains = search) | Q(dept__name__icontains = search) | Q(designation__icontains = search))
    return render(request,"admin_staff_page.html",context={'user':request.user,'staffs':obj})

@login_required(login_url="/admin-login/")
def add_staff(request):
    dept = department.objects.all()
    degre = degree.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        designation = request.POST.get("designation")
        dob = request.POST.get("dob")
        depart = request.POST.get("dept")
        course = request.POST.get("course")
        dob_obj = datetime.strptime(dob,"%Y-%m-%d")
        dob_formatted = dob_obj.strftime("%d-%m-%Y")
        CustomUser.objects.create_user(username = email, password = dob_formatted, role = "staff", first_name = name)
        obj = staff.objects.create(name=name,email=email,designation=designation,dob=dob,dept_id = depart,course_id = course)
        obj.save()
        return redirect("/admin-dashboard/staff/")
    return render(request,"add_staff.html",context={'user':request.user,'dept':dept,'degree':degre})
def update_staff(request,id):
    dept = department.objects.all()
    degre = degree.objects.all()
    obj = staff.objects.get(id = id)
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        designation = request.POST.get("designation")
        dob = request.POST.get("dob")
        depart = request.POST.get("dept")
        course = request.POST.get("course")
        obj.name = name
        obj.email = email
        obj.designation = designation
        obj.dob = dob
        obj.dept_id = depart
        obj.course_id = course
        obj.save()
        return redirect("/admin-dashboard/staff/")
    return render(request,"update_staff.html",context={'user':request.user,'staff':obj,'dept':dept,'degree':degre})
@login_required(login_url="/admin-login/")
def delete_staff(request,id):
    obj = staff.objects.filter(id = id)
    user = CustomUser.objects.get(username = obj.email)
    user.delete()
    obj.delete()
    return redirect("/admin-dashboard/staff/")

@login_required(login_url="/admin-login/")
def subject_page(request):
    obj = subject.objects.all().order_by('semester')
    if request.method == "POST":
        search = request.POST.get("q")
        obj = subject.objects.filter(Q(staff__name__icontains = search) | Q(name__icontains = search) | Q(semester__icontains = search)).order_by('semester')
    return render(request,"subject_page.html",context={'user':request.user,'subjects':obj})

@login_required(login_url="/admin-login/")
def add_subject(request):
    course = degree.objects.all()
    teacher = staff.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        credit = request.POST.get("credit")
        crs = request.POST.get("course")
        professor = request.POST.get("staff")
        code = request.POST.get("code")
        sem_no = request.POST.get("semester")
        part = request.POST.get("part")
        obj = subject.objects.create(name=name,semester=sem_no,staff_id=professor,code = code,credit=credit,course_id=crs, part = part)
        students = student.objects.filter(course_id = crs)
        for stu in students:
            sems = semester.objects.create(stu = stu, sub = obj, sem = int(sem_no), internal = 0, external = 0)
            sems.save()
        obj.save()
        return redirect("/admin-dashboard/subject/")
    return render(request,"add_subject.html",context={'user':request.user,'staffs':teacher,'degree':course})
def delete_subject(request,id):
    obj = subject.objects.filter(id = id)
    obj.delete()
    return redirect("/admin-dashboard/subject/")
def update_subject(request,id):
    obj = subject.objects.get(id = id)
    course = degree.objects.all()
    teacher = staff.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        credit = request.POST.get("credit")
        crs = request.POST.get("course")
        professor = request.POST.get("staff")
        code = request.POST.get("code")
        semester = request.POST.get("semester")
        part = request.POST.get("part")
        obj.name = name
        obj.semester = semester
        obj.staff_id = professor
        obj.course_id = crs
        obj.code = code
        obj.part = part
        obj.credit = credit
        obj.save()
        return redirect("/admin-dashboard/subject/")
    return render(request,"update_subject.html",context={'user':request.user,'subject':obj,'staffs':teacher,'degree':course})
@login_required(login_url="/staff-login/")
def staff_dashboard(request):
    subjects = subject.objects.filter(staff__name = request.user.first_name).order_by("semester")
    return render(request,"staff.html",context={'user':request.user.first_name,'subjects':subjects})
@login_required(login_url="/staff-login/")
def mark_entry(request):
    section = staff.objects.get(name = request.user.first_name)
    section = section.course.name
    sub = subject.objects.filter(staff__name = request.user.first_name)
    if request.method == "POST":
        post_type = request.POST.get('form_type')
        if post_type == "search":
            sub_id = request.POST.get('subject')
            class_room = request.POST.get('class')
            admission_year = date.today().year - (int(class_room) - 1)
            students = semester.objects.filter(sub_id = sub_id, stu__admission__year = admission_year).order_by("stu__rollno")
            disp = {'sub':int(sub_id),'year':int(class_room),'class': ("I" * int(class_room))}
            return render(request,"mark_entry_page.html",context={'user':request.user.first_name,'students':students,'subject':sub,'class':section,'disp':disp})
        else:
            stu_ids = request.POST.getlist("stu_ids")
            sub_id = request.POST.get("sub_id")
            students = semester.objects.filter(stu_id__in = stu_ids, sub_id = sub_id)
            for stu in students:
                stu_id = stu.stu.id
                sub_obj = subject.objects.get(id = sub_id)
                sem = sub_obj.semester
                internal = request.POST.get(f"inter_{stu.stu.id}")
                external = request.POST.get(f"exter_{stu.stu.id}")
                if internal == "" and external == "":
                    internal = 0
                    external = 0
                obj = semester.objects.get(stu_id = stu_id, sub = sub_obj)
                obj.stu.id = stu_id
                obj.sub = sub_obj
                obj.sem = sem
                obj.internal = internal
                obj.external = external
                obj.save()
            return redirect("/staff-dashboard/")

    context = {
        'user':request.user.first_name,
        'subject':sub,
        'class':section,
        }
    return render(request,"mark_entry_page.html",context=context)
    
@login_required(login_url="/student-login/")    
def student_dashboard(request):
    stu = student.objects.get(name = request.user.first_name)
    today = date.today()
    months = (today.year - stu.admission.year) * 12 + (today.month - stu.admission.month)
    sems = (months // 6) + 1
    sub = semester.objects.filter(sem__lte = (sems - 1), stu = stu)
    user = sub.annotate(total_marks = ExpressionWrapper(F('internal')+F('external'),output_field=IntegerField()))
    fail_subjects = user.filter(total_marks__lt = 40)
    result = user.aggregate( total_pass=Count('id',filter=Q(total_marks__gte = 40)),total_fail = Count('id',filter=Q(total_marks__lt = 40)))
    aggre = user.aggregate(mark_obtained = Sum('total_marks'),max_marks = Count('id') * 100)
    percentage = (aggre['mark_obtained'] / aggre['max_marks']) * 100 if aggre['mark_obtained'] else 0
    percentage = round(percentage,2)
    semester_wise = list()
    semester_parts = []
    for i in range(1,sems):
        temp = sub.filter(sem = i)
        temp = temp.annotate(total_marks = ExpressionWrapper(F('internal')+F('external'),output_field=IntegerField()),grade_point=ExpressionWrapper((F('internal') + F('external')) / 10.0, output_field=FloatField())).order_by("-total_marks","sub__name")
        part_wise = temp.values('sub__part').annotate(
        total_gp=Sum('grade_point'),         # sum of GP in this part
        total_credits=Sum('sub__credit'),    # sum of credits in this part
        subject_count=Count('id')            # number of subjects in this part
        ).annotate(
        average_gp=ExpressionWrapper(F('total_gp') / F('subject_count'), output_field=FloatField()),  # divide by subject count
        weighted_gp=ExpressionWrapper(F('total_credits') * F('average_gp'), output_field=FloatField())
        ).order_by('sub__part')

        semester_parts.append({
        'semester': i,
        'parts': list(part_wise)  # each part has total_gp, average_gp, total_credits, weighted_gp
        })
        semester_wise.append(temp)

    semester_gpas = []  # list to store GPA per semester

    for sem in semester_parts:
        total_weighted_gp = sum([p['weighted_gp'] for p in sem['parts']])
        total_credits = sum([p['total_credits'] for p in sem['parts']])

        sem_gpa = round(total_weighted_gp / total_credits, 2) if total_credits else 0

        semester_gpas.append(sem_gpa)

    total_semesters = len(semester_gpas)
    cgpa = round(sum(semester_gpas) / total_semesters, 2) if total_semesters else 0    

    return render(request,"stu_dashboard.html",context={'title':"Let's Progress | Dashboard",'user':request.user.first_name,'result':result,'percentage':percentage,'semester':('a'*(sems - 1)),'marks':semester_wise,'cgpa':cgpa,'fail_subjects':fail_subjects,'gpa':semester_gpas})

@login_required(login_url="/student-login/")
def leaderboard(request):
    user = student.objects.get(email = request.user.username)
    curr_sem = (date.today().year - user.admission.year) * 12 + (date.today().month - user.admission.month)
    curr_sem = (curr_sem // 6)
    students = (
    semester.objects.filter(
        sem__lte=curr_sem,
        stu__course__name=user.course.name,
        stu__admission__year=user.admission.year
    )
    .values('stu__id', 'stu__rollno', 'stu__name')  # only student fields
    .order_by('stu__rollno')
    .distinct()
    )
    results = []
    # loop through all students
    for stu in students:
        # get all semesters for this student up to current semester
        subs = semester.objects.filter(stu_id=stu["stu__id"], sem__lte=curr_sem).annotate(
            total_marks=ExpressionWrapper(F('internal') + F('external'), output_field=IntegerField()),
            grade_point=ExpressionWrapper((F('internal') + F('external')) / 10.0, output_field=FloatField())
        )

        # -------- Percentage --------
        aggre = subs.aggregate(
            mark_obtained=Sum('total_marks'),
            max_marks=Count('id') * 100
        )
        percentage = (aggre['mark_obtained'] / aggre['max_marks'] * 100) if aggre['mark_obtained'] else 0
        percentage = round(percentage, 2)

        # -------- Semester GPA + CGPA --------
        semester_gpas = []
        for i in range(1, curr_sem + 1):
            sem_subs = subs.filter(sem=i)

            part_wise = sem_subs.values('sub__part').annotate(
                total_gp=Sum('grade_point'),
                total_credits=Sum('sub__credit'),
                subject_count=Count('id')
            ).annotate(
                average_gp=ExpressionWrapper(F('total_gp') / F('subject_count'), output_field=FloatField()),
                weighted_gp=ExpressionWrapper(F('total_credits') * F('average_gp'), output_field=FloatField())
            )

            total_weighted_gp = sum([p['weighted_gp'] for p in part_wise])
            total_credits = sum([p['total_credits'] for p in part_wise])
            sem_gpa = round(total_weighted_gp / total_credits, 2) if total_credits else 0
            semester_gpas.append(sem_gpa)

        cgpa = round(sum(semester_gpas) / len(semester_gpas), 2) if semester_gpas else 0

        results.append({
            'student': stu["stu__name"],
            'percentage': percentage,
            'cgpa': cgpa,
            'semester_gpas': semester_gpas
        })
    results.sort(key=lambda x: (x['cgpa'], x['percentage']), reverse=True)

    context = {
        'user':request.user.first_name,
        'title':"Students | Leaderboard",
        'students':results
        }
    return render(request,"leaderboard.html",context=context)

@login_required(login_url="/admin-login/")
def admin_mark_entry(request):
    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == "search":
            if request.method == "POST":
                rollno = request.POST.get("rollno")
                stu = student.objects.get(rollno = rollno)
                sem = ((date.today().year - stu.admission.year) * 12 +(date.today().month - stu.admission.month))//6
                sub = semester.objects.filter(sem__lte = sem, stu = stu)
                semester_wise = list()
                for i in range(1,(int(sem)+1)):
                    temp = sub.filter(sem = i).order_by("sub__name")
                    semester_wise.append(temp)
                return render(request,"admin_mark_entry.html",context={'user':request.user,'semester':semester_wise,'disp':rollno})
        else:
            rollno = request.POST.get("rollno")
            subjects = request.POST.getlist("subjects")
            subs = semester.objects.filter(stu__rollno = rollno, sub_id__in = subjects)
            for i in subs:
                internal = request.POST.get(f"inter_{i.sub.id}")
                external = request.POST.get(f"exter_{i.sub.id}")
                internal = int(internal) if internal else 0
                external = int(external) if external else 0
                i.internal = internal
                i.external = external
                i.save()
            return redirect("/admin-dashboard/mark-entry/")
    context = {
        'user':request.user
    }
    return render(request,"admin_mark_entry.html",context=context)
def demo(request):
    return render(request,"demo.html")
import html

from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required

from dacParser.tools.dacParser import generateAllSubjectsFrom, getAllInstitutes
from dacParser.tools.dacParserHelper import *
from dacParser.models import Student, Offering, Subject, Teacher, Institute

@login_required
def updatePage(request):
    try:
        allInstitutes = Institute.objects.all().order_by('code')
    except:
        raise Http404("Erro ao parsear institutos")

    results = {
        'institutes': allInstitutes
    }

    return render(request, 'dacParser/update.html', results)


@login_required
def updateInstitutes(request):
    try:
        institutes = getAllInstitutes()
    except:
        raise Http404("Erro ao parsear institutos")

    allInstitutes = []
    for institute in institutes:
        try:
            inst, created = Institute.objects.all().get_or_create(
                code = institute[0],
                name = institute[1],
            )
            allInstitutes.append(inst)
        except:
            raise Http404("Erro ao criar institutos")

    results = {
        'institutes': allInstitutes
    }
    return render(request, 'dacParser/update.html', results)


@login_required
def updateDisciplines(request, institute):
    # First parses all the subjects in this semester
    try:
        print("Parseando disciplinas de "+institute.upper())
        subjects = generateAllSubjectsFrom(institute.upper(), 2016, 2)
        print("Terminou de Parsear disciplinas")
    except:
        print("Erro ao parsear disciplinas")

    # If everything is alright, we hava an array of Subjects
    for subject in subjects:
        # Creats Subject Model
        SubjectModel, created = Subject.objects.all().get_or_create(
            code = subject.code,
            name = subject.name,
            type = subject.type,
            descryption = subject.emment
        )
        print(subject)

        # Runs the array of offerings in subject
        for off in subject.offerings:
            # Creates Teacher Model
            if off.teacher:
                TeacherModel, created = Teacher.objects.get_or_create(
                    name = off.teacher
                )
            else:
                TeacherModel, created = Teacher.objects.get_or_create(
                    name = 'Sem Professor'
                )

            # Creates discipline Model
            OfferingModel, created = Offering.objects.get_or_create(
                subject = SubjectModel,
                offering_id = off.offering_id,
                year = off.year,
                semester = off.semester,
            )

            # Add this fields to offering.
            # Dont do this when creating because they are changeable.
            OfferingModel.teacher = TeacherModel
            OfferingModel.vacancies = int(off.vacancies)
            OfferingModel.registered = int(off.registered)

            # First we check if the offering had studnts:
            try:
                oldStudents = Student.objects.all().filter(
                    stu_offerings = OfferingModel
                )
            except:
                oldStudents = []


            newStudents = []
            # Now were going to create a Student model and add it to discipline
            # as we add the discipline to the student
            studentsInOffering = off.students
            for student in studentsInOffering:
                try:
                    StudentModel, created = Student.objects.get_or_create(
                        ra = student.ra.strip(),
                        name = html.unescape(student.name.strip()),
                        course = student.course,
                        course_type = student.course_modality,
                    )
                except Exception as inst:
                    print(type(inst))
                    print(inst.args)
                    print(str(inst))


                newStudents.append(StudentModel)
                print(StudentModel)
                # Insert the offering in the student
                StudentModel.stu_offerings.add(OfferingModel)
                # Insert the student in the offering
                OfferingModel.students.add(StudentModel)

            for oldStudent in oldStudents:
                print(oldStudent)
                if oldStudent not in newStudents:
                    OfferingModel.students.remove(oldStudent)
                    OfferingModel.giveups.add(oldStudent)
                    oldStudent.stu_offerings.remove(OfferingModel)

            OfferingModel.save()

    print("Terminamos de gerar informações")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

from app.models import Course, Grade, Student


class EnrollmentService(object):
    def get_courses(self, student):
        return student.courses.all()

    def get_students(self, course):
        return course.students.all()

    def enroll(self, student, course):
        if course.students.all().count() >= 20:
            raise Exception
        if student in course.students.all():
            raise Exception
        if course in student.courses.all():
            raise Exception
        course.students.add(student)
        student.courses.add(course)

    def disenroll(self, student, course):
        course.students.remove(student)
        student.courses.remove(course)


class GradeService(object):
    def __grade_validator(course, student, grade=100):
        if grade < 0 or grade > 100:
            raise Exception
        if student not in course.students.all():
            raise Exception
        if course not in student.courses.all():
            raise Exception

    def __grade_average_validator(course, student):
        if student is None and course is None:
            raise Exception
        if student is not None and course is not None:
            raise Exception
        if student is not None and student.courses.all().count() < 1:
            raise Exception
        if course is not None and course.students.all().count() < 1:
            raise Exception

    def __get_letter_grade(grade):
        letters = {6: 'D', 7: 'C', 8: 'B', 9: 'A'}
        if grade < 0 or grade > 100:
            raise Exception
        elif grade < 59:
            return 'F'
        elif grade == 100:
            return 'A+'
        else:
            tens = int(grade / 10)
            units = grade % 10
            letter = letters[tens]
            if units < 3:
                return letter + '-'
            elif units < 7:
                return letter
            else:
                return letter + '+'

    def __get_average(grades):
        grade_amount = grades.count()

        if grade_amount == 0:
            raise Exception

        acc = 0
        for grade in grades:
            acc += grade.value
        average_grade = acc / grades.count()

        return round(average_grade)

    def __get_course_grade_average(course):
        grades = Grade.objects.filter(course=course)
        return GradeService.__get_average(grades)

    def __get_student_grade_average(student):
        grades = Grade.objects.filter(student=student)
        return GradeService.__get_average(grades)

    def assign_grade(self, course, student, grade):
        GradeService.__grade_validator(course, student, grade)
        search_grade = Grade.objects.filter(
            student=student, course=course).first()
        if search_grade is not None:
            raise Exception
        grade = Grade(student=student, course=course, value=grade)
        grade.save()

    def adjust_grade(self, course, student, grade):
        GradeService.__grade_validator(course, student, grade)
        search_grade = Grade.objects.filter(
            student=student, course=course).first()
        if search_grade is None:
            raise Exception
        search_grade.value = grade
        search_grade.save()

    def get_grade(self, course, student):
        GradeService.__grade_validator(course, student)
        search_grade = Grade.objects.filter(
            course=course, student=student).first()
        if search_grade is None:
            raise Exception
        return search_grade.value

    def get_average_grade(self, course=None, student=None, is_letter_grade=False):
        GradeService.__grade_average_validator(course, student)

        average_grade = 0

        if student is not None:
            average_grade = GradeService.__get_student_grade_average(student)

        if course is not None:
            average_grade = GradeService.__get_course_grade_average(course)

        if is_letter_grade:
            return GradeService.__get_letter_grade(average_grade)
        else:
            return average_grade

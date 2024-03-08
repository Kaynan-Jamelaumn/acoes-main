from django.contrib.auth.models import AbstractUser
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=150, blank=False,
                            null=False,  primary_key=True, unique=True)
    region = models.CharField(max_length=150, blank=False, null=False)


class Address(models.Model):
    address = models.CharField(max_length=250, blank=False, null=False)
    complement = models.CharField(max_length=250, blank=True, null=True)
    neighborhood = models.CharField(max_length=50, blank=True, null=True)

    city = models.ForeignKey(City, on_delete=models.CASCADE)


class Institute(models.Model):
    name = models.CharField(max_length=250, blank=False,
                            null=False, primary_key=True, unique=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


class PreviousSchool(models.Model):
    name = models.CharField(max_length=250, blank=False,
                            null=False, primary_key=True)
    completion_date = models.DateField()
    TYPE_cHOICES = [
        ('Private', 'Private'),
        ('Public', 'Public'),
    ]
    type = models.CharField(
        max_length=10, choices=TYPE_cHOICES, null=False, blank=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


class Course(models.Model):
    name = models.CharField(max_length=250, blank=False,
                            null=False)

    SHIFT_cHOICES = [
        ('Morning', 'Morning'),
        ('Afternoon', 'Afternoon'),
        ('Night', 'Night'),
        ('Full-time', 'Full-time'),
    ]
    TYPE_cHOICES = [
        ('Integrated Technical', 'Integrated Technical'),
        ('Subsequent Technical', 'Subsequent Technical'),
        ('Degree ', 'Degree '),
        ('Postgraduate ', 'Postgraduate'),
        ('Extension  ', 'Extension'),
        ('Youth and Adult Education (EJA) ', 'EJA'),
    ]
    shift = models.CharField(
        max_length=10, choices=SHIFT_cHOICES, null=False, blank=False)
    type = models.CharField(
        max_length=32, choices=TYPE_cHOICES, null=False, blank=False)
    time_required = models.IntegerField()
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)


class CustomUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        error_messages={
            "unique": "user with the same username already exists",
        },
    )

    last_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    groups = models.ManyToManyField(
        'auth.Group', related_name='custom_users', blank=True)
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='custom_users')

    def __str__(self):
        return self.username


class Student(models.Model):
    name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    social_name = models.CharField(max_length=150, null=True, blank=True)
    mother_name = models.CharField(max_length=150, null=False, blank=False)
    father_name = models.CharField(max_length=150, null=True, blank=True)
    birth_date = models.DateField(null=False, blank=False)
    registration = models.IntegerField(null=True, blank=True, unique=True)
    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    DISABILITY_CHOICES = [
        ('None', 'None'),
        ('Deafness', 'Deafness'),
        ('Visual Impairment', 'Visual Impairment'),
        ('Physical Disability', 'Physical Disability'),
        ('Autism/Spectrum Disorder', 'Autism/Spectrum Disorder'),
        ('Down Syndrome', 'Down Syndrome'),
        ('Dyslexia', 'Dyslexia'),
        ('Attention Deficit Hyperactivity Disorder (ADHD)', 'ADHD'),
        ('Deafness', 'Deafness'),
        ('Low Vision', 'Low Vision'),
        ('Deafblindness', 'Deafblindness'),
        ('Multiple Disabilities', 'Multiple Disabilities'),
        ('Other', 'Other'),
    ]

    GENDER_CHOICES = [
        ('Woman', 'Woman'),
        ('Man', 'Man'),
        ('Non-binary', 'Non-binary'),
        ('Genderfluid', 'Genderfluid'),
        ('Other', 'Other'),
    ]
    sex = models.CharField(
        max_length=6, choices=SEX_CHOICES, null=True, blank=True)
    gender = models.CharField(
        max_length=30, choices=GENDER_CHOICES, null=True, blank=True)
    disability = models.CharField(
        max_length=50, choices=DISABILITY_CHOICES, null=True, blank=True)

    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    previous_school = models.ForeignKey(
        PreviousSchool, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class StudentCourse(models.Model):
    name = models.CharField(max_length=250, blank=False,
                            null=False)

    ADMISSION_PROCESS_CHOICES = [
        (' Self-declared Black, Brown, and Indigenous (BBI)',
         ' Self-declared Black, Brown, and Indigenous (BBI)'),
        ('Income up to 1.5 times the minimum wage per capita',
         'Income up to 1.5 times the minimum wage per capita'),
        ('Income greater than 1.5 up to 3 times the minimum wage per capita',
         'Income greater than 1.5 up to 3 times the minimum wage per capita'),
        ('for People with Disabilities (PWD):',
         'for People with Disabilities (PWD):'),
        ('Public School', 'Public School'),
        ('Public School + Income up to 1.5 times the minimum wage per capita',
         'Public School + Income up to 1.5 times the minimum wage per capita'),
        ('Public School + PWD + Income up to 1.5 times the minimum wage per capita',
         'Public School + PWD + Income up to 1.5 times the minimum wage per capita'),
        ('Public School + PWD + BBI +  Income up to 1.5 times the minimum wage per capita',
         'Public School + PWD + BBI + Income up to 1.5 times the minimum wage per capita'),
        ('Public School + BBI +  Income up to 1.5 times the minimum wage per capita',
         'Public School + BBI + Income up to 1.5 times the minimum wage per capita'),
        ('Public School + PWD', 'Public School + PWD'),
        ('Public School + BBI', 'Public School + BBI'),
        ('Public School + PWD+ BBI', 'Public School + PWD + BBI'),
        ('BBI + PWD', 'BBI + PWD'),
        ('BBI + PWD  + Income up to 1.5 times the minimum wage per capita',
         'BBI + PWD + Income up to 1.5 times the minimum wage per capita'),
        ('BBI + Income up to 1.5 times the minimum wage per capita',
         'BBI + Income up to 1.5 times the minimum wage per capita'),
        ('PWD + Income up to 1.5 times the minimum wage per capita',
         'PWD + Income up to 1.5 times the minimum wage per capita'),
        ('General competition', 'General competition'),
    ]
    admission_process = models.CharField(
        max_length=79, choices=ADMISSION_PROCESS_CHOICES, null=True, blank=True)
    ingressed_semester = models.CharField(max_length=10)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Status(models.Model):
    STATUS_cHOICES = [
        ('Canceld', 'Canceld'),
        ('In Progress', 'In Progress'),
        ('Concluded', 'Concluded')
    ]
    status = models.CharField(
        max_length=11, choices=STATUS_cHOICES, null=False, blank=False)
    current_semester = models.CharField(max_length=10, null=False, blank=False)
    student_course = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

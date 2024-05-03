from django.contrib.auth.models import AbstractUser
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=150, blank=False,
                            null=False,  primary_key=True, unique=True)

class Address(models.Model):
    address = models.CharField(max_length=250, blank=False, null=False)
    complement = models.CharField(max_length=250, blank=True, null=True)
    neighborhood = models.CharField(max_length=50, blank=True, null=True)

    city = models.ForeignKey(City, on_delete=models.CASCADE)


class Institute(models.Model):
    name = models.CharField(max_length=250, blank=False,
                            null=False, primary_key=True, unique=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    region = models.CharField(max_length=150, blank=False, null=False)


class PreviousSchool(models.Model):
    name = models.CharField(max_length=250, blank=True,null=True)
    completion_date = models.DateField(blank=True, null=True)
    TYPE_CHOICES = [
        ('Comunitária', 'Comunitária'),
        ('Municipal', 'Municipal'),
        ('Estadual', 'Estadual'),
        ('Federal', 'Federal'),
        ('Privada', 'Privada'),
        ('Outra', 'Outra'),
    ]
    type = models.CharField(
        max_length=11, choices=TYPE_CHOICES, null=False, blank=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)


class Course(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False)

    SHIFT_CHOICES = [
        ('Matutino', 'Matutino'),
        ('Vespertino', 'Vespertino'),
        ('Noturno', 'Noturno'),
        ('Integral', 'Integral'),
    ]
    MODALITY_CHOICES = [
        ('Presencial', 'Presencial'),
        ('Híbrido', 'Híbrido'),
        ('A Distância', 'A Distância'),
    ]
    TYPE_CHOICES = [
        ('Educação de Jovens e Adultos (EJA)', 'EJA'),
        ('Técnico Integrado', 'Técnico Integrado'),
        ('Técnico Subsequente', 'Técnico Subsequente'),
        ('Tecnólogo', 'Tecnólogo'),
        ('Bacharelado', 'Bacharelado'),
        ('Licenciatura', 'Licenciatura'),
    ]
    shift = models.CharField(
        max_length=12, choices=SHIFT_CHOICES, null=False, blank=False)
    modality = models.CharField(
        max_length=16, choices=MODALITY_CHOICES, null=False, blank=False)
    type = models.CharField(
        max_length=34, choices=TYPE_CHOICES, null=False, blank=False)
    time_required = models.IntegerField()
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    year_created = models.IntegerField(blank=False, null=False)



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
    name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    social_name = models.CharField(max_length=150, null=True, blank=True)
    #mother_name = models.CharField(max_length=150, null=True, blank=True)
    father_name = models.CharField(max_length=150, null=True, blank=True)
    birth_date = models.DateField(null=False, blank=False)
    registration = models.IntegerField(null=True, blank=True, unique=True)
    SEX_CHOICES = [
    ('Masculino', 'Masculino'),
    ('Feminino', 'Feminino'),

    ]
    DISABILITY_CHOICES = [
    ('Nenhum', 'Nenhum'),
    ('Surdez', 'Surdez'),
    ('Deficiência Visual', 'Deficiência Visual'),
    ('Deficiência Física', 'Deficiência Física'),
    ('Transtorno do Espectro Autista (TEA)', 'Transtorno do Espectro Autista (TEA)'),
    ('Síndrome de Down', 'Síndrome de Down'),
    ('Dislexia', 'Dislexia'),
    ('Transtorno de Déficit de Atenção e Hiperatividade (TDAH)', 'Transtorno de Déficit de Atenção e Hiperatividade (TDAH)'),
    ('Baixa Visão', 'Baixa Visão'),
    ('Surdocegueira', 'Surdocegueira'),
    ('Múltiplas Deficiências', 'Múltiplas Deficiências'),
    ('Outro', 'Outro'),
    ]

    GENDER_CHOICES = [
        ('Mulher', 'Mulher'),
        ('Homem', 'Homem'),
        ('Não-binário', 'Não-binário'),
        ('Gênero Fluído', 'Gênero Fluído'),
        ('Outro', 'Outro'),
    ]
    COLOR_RACE_CHOISES = [
        ('Branco', 'Branco'),
        ('Pardo', 'Pardo'),
        ('Preto', 'Preto'),
        ('Amarelo', 'Amarelo'),
        ('Não Declarada', 'Não Declarada'),
        ('Outro', 'Outro'),
    ]
    sex = models.CharField(
        max_length=10, choices=SEX_CHOICES, null=True, blank=True)
    gender = models.CharField(
        max_length=30, choices=GENDER_CHOICES, null=True, blank=True)
    color_race = models.CharField(
        max_length=30, choices=GENDER_CHOICES, null=True, blank=True)
    disability = models.CharField(
        max_length=56, choices=DISABILITY_CHOICES, null=True, blank=True)

    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
    # previous_school = models.ForeignKey(
    #     PreviousSchool, on_delete=models.CASCADE)

    SCHOOL_TYPE_CHOICES = [
        ('Comunitária', 'Comunitária'),
        ('Municipal', 'Municipal'),
        ('Estadual', 'Estadual'),
        ('Federal', 'Federal'),
        ('Privada', 'Privada'),
        ('Outra', 'Outra'),
    ]
    school_type = models.CharField(
        max_length=30, choices=SCHOOL_TYPE_CHOICES, null=False, blank=False)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class StudentCourse(models.Model):

    ADMISSION_PROCESS_CHOICES = [
    ('Competição geral', 'Competição geral'),
    ('Auto-declarado Preto, Pardo e Indígena (PPI)',
    'Auto-declarado Preto, Pardo e Indígena (PPI)'),
    ('Renda até 1,5 vezes o salário mínimo per capita',
    'Renda até 1,5 vezes o salário mínimo per capita'),
    ('Renda maior que 1,5 até 3 vezes o salário mínimo per capita',
    'Renda maior que 1,5 até 3 vezes o salário mínimo per capita'),
    ('para Pessoas com Deficiência (PCD):',
    'para Pessoas com Deficiência (PCD):'),
    ('Escola Pública', 'Escola Pública'),
    ('Escola Pública + Renda até 1,5 vezes o salário mínimo per capita',
    'Escola Pública + Renda até 1,5 vezes o salário mínimo per capita'),
    ('Escola Pública + PCD + Renda até 1,5 vezes o salário mínimo per capita',
    'Escola Pública + PCD + Renda até 1,5 vezes o salário mínimo per capita'),
    ('Escola Pública + PCD + PPI + Renda até 1,5 vezes o salário mínimo per capita',
    'Escola Pública + PCD + PPI + Renda até 1,5 vezes o salário mínimo per capita'),
    ('Escola Pública + PPI + Renda até 1,5 vezes o salário mínimo per capita',
    'Escola Pública + PPI + Renda até 1,5 vezes o salário mínimo per capita'),
    ('Escola Pública + PCD', 'Escola Pública + PCD'),
    ('Escola Pública + PPI', 'Escola Pública + PPI'),
    ('Escola Pública + PCD + PPI', 'Escola Pública + PCD + PPI'),
    ('PPI + PCD', 'PPI + PCD'),
    ('PPI + PCD + Renda até 1,5 vezes o salário mínimo per capita',
    'PPI + PCD + Renda até 1,5 vezes o salário mínimo per capita'),
    ('PPI + Renda até 1,5 vezes o salário mínimo per capita',
    'PPI + Renda até 1,5 vezes o salário mínimo per capita'),
    ('PCD + Renda até 1,5 vezes o salário mínimo per capita',
    'PCD + Renda até 1,5 vezes o salário mínimo per capita'),

    ]
    admission_process = models.CharField(
        max_length=79, choices=ADMISSION_PROCESS_CHOICES, null=True, blank=True)
    ingressed_semester = models.CharField(max_length=10)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        # Define a combinação única de course e student
        unique_together = ['course', 'student']


class Status(models.Model):
    STATUS_CHOICES = [
    ('Cancelado', 'Cancelado'),
    ('Cancelado', 'Cancelado'),
    ('Cursando', 'Cursando'),
    ('Trancado', 'Trancado'),
    ('Concluído', 'Concluído'),
    ('Desconhecido', 'Desconhecido')

    ]
    status = models.CharField(  
        max_length=12, choices=STATUS_CHOICES, default='Desconhecido', null=False, blank=False)
    current_semester = models.CharField(max_length=10, null=True, blank=True)
    student_course = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

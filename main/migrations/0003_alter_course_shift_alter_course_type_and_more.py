# Generated by Django 5.0.2 on 2024-03-08 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_complemento_address_complement_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='shift',
            field=models.CharField(choices=[('Manhã', 'Manhã'), ('Tarde', 'Tarde'), ('Noite', 'Noite'), ('Período integral', 'Período integral')], max_length=16),
        ),
        migrations.AlterField(
            model_name='course',
            name='type',
            field=models.CharField(choices=[('Educação de Jovens e Adultos (EJA)', 'EJA'), ('Técnico Integrado', 'Técnico Integrado'), ('Técnico Subsequente', 'Técnico Subsequente'), ('Tecnólogo', 'Tecnólogo'), ('Bacharelado', 'Bacharelado'), ('Licenciatura', 'Licenciatura')], max_length=34),
        ),
        migrations.AlterField(
            model_name='status',
            name='status',
            field=models.CharField(choices=[('Cancelado', 'Cancelado'), ('Em Progresso', 'Em Progresso'), ('Concluído', 'Concluído')], max_length=12),
        ),
        migrations.AlterField(
            model_name='student',
            name='disability',
            field=models.CharField(blank=True, choices=[('Nenhum', 'Nenhum'), ('Surdez', 'Surdez'), ('Deficiência Visual', 'Deficiência Visual'), ('Deficiência Física', 'Deficiência Física'), ('Transtorno do Espectro Autista (TEA)', 'Transtorno do Espectro Autista (TEA)'), ('Síndrome de Down', 'Síndrome de Down'), ('Dislexia', 'Dislexia'), ('Transtorno de Déficit de Atenção e Hiperatividade (TDAH)', 'Transtorno de Déficit de Atenção e Hiperatividade (TDAH)'), ('Surdez', 'Surdez'), ('Baixa Visão', 'Baixa Visão'), ('Surdocegueira', 'Surdocegueira'), ('Múltiplas Deficiências', 'Múltiplas Deficiências'), ('Outro', 'Outro')], max_length=56, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(blank=True, choices=[('Mulher', 'Mulher'), ('Homem', 'Homem'), ('Não-binário', 'Não-binário'), ('Gênero Fluído', 'Gênero Fluído'), ('Outro', 'Outro')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='sex',
            field=models.CharField(blank=True, choices=[('Masculino', 'Masculino'), ('Feminino', 'Feminino')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='studentcourse',
            name='admission_process',
            field=models.CharField(blank=True, choices=[('Competição geral', 'Competição geral'), ('Auto-declarado Preto, Pardo e Indígena (PPI)', 'Auto-declarado Preto, Pardo e Indígena (PPI)'), ('Renda até 1,5 vezes o salário mínimo per capita', 'Renda até 1,5 vezes o salário mínimo per capita'), ('Renda maior que 1,5 até 3 vezes o salário mínimo per capita', 'Renda maior que 1,5 até 3 vezes o salário mínimo per capita'), ('para Pessoas com Deficiência (PCD):', 'para Pessoas com Deficiência (PCD):'), ('Escola Pública', 'Escola Pública'), ('Escola Pública + Renda até 1,5 vezes o salário mínimo per capita', 'Escola Pública + Renda até 1,5 vezes o salário mínimo per capita'), ('Escola Pública + PCD + Renda até 1,5 vezes o salário mínimo per capita', 'Escola Pública + PCD + Renda até 1,5 vezes o salário mínimo per capita'), ('Escola Pública + PCD + PPI + Renda até 1,5 vezes o salário mínimo per capita', 'Escola Pública + PCD + PPI + Renda até 1,5 vezes o salário mínimo per capita'), ('Escola Pública + PPI + Renda até 1,5 vezes o salário mínimo per capita', 'Escola Pública + PPI + Renda até 1,5 vezes o salário mínimo per capita'), ('Escola Pública + PCD', 'Escola Pública + PCD'), ('Escola Pública + PPI', 'Escola Pública + PPI'), ('Escola Pública + PCD + PPI', 'Escola Pública + PCD + PPI'), ('PPI + PCD', 'PPI + PCD'), ('PPI + PCD + Renda até 1,5 vezes o salário mínimo per capita', 'PPI + PCD + Renda até 1,5 vezes o salário mínimo per capita'), ('PPI + Renda até 1,5 vezes o salário mínimo per capita', 'PPI + Renda até 1,5 vezes o salário mínimo per capita'), ('PCD + Renda até 1,5 vezes o salário mínimo per capita', 'PCD + Renda até 1,5 vezes o salário mínimo per capita')], max_length=79, null=True),
        ),
    ]

from django.db import models

# Create your models here.
class TestingFormModel(models.Model):
    github_username = models.CharField(max_length=50, verbose_name='GitHub username')
    gh_first_repo = models.URLField(null=True, verbose_name='GitHub First contributed repository')
    gh_git_training_exercise = models.URLField(null=True, verbose_name='GitHub Training repository')
    gh_most_contributed_repo = models.URLField(null=True, verbose_name='GitHub Most contributed repository')

    gitlab_user_id = models.CharField(max_length=50, verbose_name='GitLab user id')
    gl_first_repo_id = models.SmallIntegerField(null=True, verbose_name='GitLab first contributed repository id')
    gl_git_training_exercise = models.SmallIntegerField(null=True, verbose_name='Gitlab training repository id')
    gl_most_contributed_repo_id = models.SmallIntegerField(null=True, verbose_name='Gitlab Most contributed repository id')

    submitted_on = models.TextField(null=True)
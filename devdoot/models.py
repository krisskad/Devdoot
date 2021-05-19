from django.db import models
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True


# Create your models here.
class Countries(models.Model):
    id = models.AutoField(primary_key=True)
    sortname = models.CharField(max_length=3)
    name = models.CharField(max_length=150)
    phonecode = models.IntegerField()

    class Meta:
        # managed = False
        verbose_name_plural = 'countries'
        db_table = 'countries'

    def __str__(self):
        return self.name


class States(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    # country_id = models.IntegerField()
    country = models.ForeignKey(Countries, related_name='unser_country', on_delete=models.CASCADE, default=None)

    class Meta:
        # managed = False
        verbose_name_plural = 'states'
        db_table = 'states'

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_states():
        return States.objects.all()


class Cities(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    # state_id = models.IntegerField()
    state = models.ForeignKey(States, related_name='under_state', on_delete=models.CASCADE, default=None)

    class Meta:
        # managed = False
        verbose_name_plural = 'cities'
        db_table = 'cities'

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_cities():
        return Cities.objects.all()


class ProblemType(models.Model):
    id = models.AutoField(primary_key=True)
    problem_title = models.CharField(max_length=120)
    problem_title_m = models.CharField(max_length=120, default=None, null=True)
    problem_title_h = models.CharField(max_length=120, default=None, null=True)

    def __str__(self):
        return self.problem_title


class PublicProblem(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=260, null=False, blank=False)
    # first_name = models.CharField(max_length=260, null=False, blank=False)
    # last_name = models.CharField(max_length=260, null=False, blank=False)
    mobile = models.CharField(max_length=20, null=False, blank=False)
    state = models.ForeignKey(States, related_name='from_state', on_delete=models.DO_NOTHING)
    city = models.ForeignKey(Cities, related_name='from_city', on_delete=models.DO_NOTHING)
    problem_type = models.ForeignKey(ProblemType, related_name='has_problem', on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=500, null=True, blank=True)

    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.mobile

    @staticmethod
    def get_all_problems():
        return PublicProblem.objects.all()


class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    state = models.ForeignKey(States, related_name='belong_to_state', on_delete=models.DO_NOTHING)
    city = models.ForeignKey(Cities, related_name='belong_to_city', on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=160, null=True, blank=True, default="None")
    profession = models.CharField(max_length=60, null=True, blank=True, default="None")
    group_name = models.CharField(max_length=160, null=True, blank=True, default="None")
    problem_types = models.TextField(max_length=1000, null=True, blank=True, default="None")

    ACCOUNT_CHOICES = (
        ('individual', 'Individual'),
        ('group', 'Group'),
    )
    account_type = models.CharField(max_length=10, choices=ACCOUNT_CHOICES)
    # timestamp = models.DateTimeField(auto_now=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.user.username

    @property
    def full_name(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)


class SolvedProblem(models.Model):
    id = models.AutoField(primary_key=True)
    solved_problem = models.ForeignKey(PublicProblem, related_name='Solved_Public_Problem', on_delete=models.CASCADE)
    is_solved = models.BooleanField(default=0)
    solved_by = models.ForeignKey(ExtendedUser, related_name='problem_solved_by', on_delete=models.DO_NOTHING,
                                  null=True, blank=True)

    when = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.solved_by.user.username

    @staticmethod
    def get_all_solved_problems():
        return PublicProblem.objects.all()


class ProblemReport(models.Model):
    submitted_by = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=60, null=False, blank=False)
    description = models.CharField(max_length=260, null=False, blank=False)
    reported_to = models.ForeignKey(PublicProblem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)



from django.db import models

# DB 테이블의 구조를 파이썬 클래스로 보여주고, 수정가능

class AllLecture(models.Model):
    subject_num = models.IntegerField(primary_key=True)
    subject_name = models.CharField(max_length=70)
    classification = models.CharField(max_length=45)
    selection = models.CharField(max_length=45, blank=True, null=True)
    grade = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'all_lecture'


class NewLecture(models.Model):
    subject_num = models.OneToOneField(AllLecture, models.DO_NOTHING, db_column='subject_num', primary_key=True)

    class Meta:
        managed = False
        db_table = 'new_lecture'


class Standard(models.Model):
    user_year = models.IntegerField(primary_key=True)
    user_dep = models.CharField(max_length=50)
    sum_score = models.IntegerField()
    major_essential = models.IntegerField()
    major_selection = models.IntegerField()
    core_essential = models.IntegerField()
    core_selection = models.IntegerField()
    basic = models.IntegerField()
    ce_list = models.CharField(max_length=100)
    cs_list = models.CharField(max_length=100)
    b_list = models.CharField(max_length=100)
    sum_eng = models.IntegerField()
    pro = models.IntegerField()
    bsm = models.IntegerField()
    build = models.IntegerField()
    pro_acc_list = models.CharField(max_length=100)
    bsm_ess_list = models.CharField(max_length=100)
    bsm_sel_list = models.CharField(max_length=100, blank=True, null=True)
    build_ess_list = models.CharField(max_length=100)
    build_sel_list = models.CharField(max_length=100)
    engine_major_list = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'standard'
        unique_together = (('user_year', 'user_dep'),)


class SubjectGroup(models.Model):
    subject_num = models.OneToOneField(AllLecture, models.DO_NOTHING, db_column='subject_num', primary_key=True)
    group_num = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'subject_group'


class TestTable(models.Model):
    num = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'test_table'
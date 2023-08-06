from django.db import models

class ModelTestGenerateSchemaA(models.Model):
    
    binary_field = models.BinaryField()
    boolean_field = models.BooleanField()
    boolean_field_nullable = models.BooleanField(null=True, blank=True)
    null_boolean_field = models.NullBooleanField()
    char_field = models.CharField(max_length=100)
    char_field_unique = models.CharField(max_length=100, unique=True)
    char_field_nullable = models.CharField(max_length=100, null=True, blank=True)
    date_field = models.DateField()
    datetime_field = models.DateTimeField()
    time_field = models.TimeField()
    decimal_field = models.DecimalField(max_digits=10, decimal_places=2)
    duration_field = models.DurationField()
    email_field = models.EmailField()
    float_field = models.FloatField()
    integer_field = models.IntegerField()
    integer_field_unique = models.IntegerField(unique=True)
    small_integer_field = models.SmallIntegerField()
    small_integer_field_unique = models.SmallIntegerField(unique=True)
    positive_integer_field = models.PositiveIntegerField()
    positive_integer_field_unique = models.PositiveIntegerField(unique=True)
    # positive_big_integer_field = models.PositiveBigIntegerField()
    # positive_big_integer_field_unique = models.PositiveBigIntegerField(unique=True)
    # positive_small_integer_field = models.PositiveSmallIntegerField()
    # positive_small_integer_field_unique = models.PositiveSmallIntegerField(unique=True)
    slug_field = models.SlugField()
    slug_field_unique = models.SlugField(unique=True)
    text_field = models.TextField()
    text_field_nullable = models.TextField(null=True, blank=True)
    url_field = models.URLField()
    url_field_unique = models.URLField(unique=True)
    uuid_field = models.UUIDField()
    uuid_field_unique = models.UUIDField(unique=True)
    foreign_key_field = models.ForeignKey('ModelTestGenerateSchemaA', on_delete=models.CASCADE, related_name='foreign_key_related')
    one_to_one_field = models.OneToOneField('ModelTestGenerateSchemaA', on_delete=models.CASCADE, related_name='one_to_one_related')
    manytomany_field = models.ManyToManyField('ModelTestGenerateSchemaA', related_name='many_to_many_related')

class ModelTestGenerateSchemaB(models.Model):
    foreign_key_field = models.ForeignKey('ModelTestGenerateSchemaA', on_delete=models.CASCADE, related_name='foreign_key_B_related')
    one_to_one_field = models.OneToOneField('ModelTestGenerateSchemaA', on_delete=models.CASCADE, related_name='one_to_one_B_related')
    manytomany_field = models.ManyToManyField('ModelTestGenerateSchemaA', related_name='many_to_many_B_related')


class Person(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    father = models.ForeignKey('self', on_delete=models.CASCADE, related_name="childs", null=True, blank=True)
    friends = models.ManyToManyField('self')



class TestFkA(models.Model):
    text = models.CharField(max_length=100, null=True, blank=True)
    testFkB = models.ForeignKey('TestFkB', on_delete=models.CASCADE, related_name='testFkAs')


class TestFkB(models.Model):
    text = models.CharField(max_length=100, null=True, blank=True)
    testFkC = models.ForeignKey('TestFkC', on_delete=models.CASCADE)

class TestFkC(models.Model):
    text = models.CharField(max_length=100, null=True, blank=True)

class TestO2oA(models.Model):
    text = models.CharField(max_length=100, null=True, blank=True)
    TestO2oB = models.OneToOneField('TestO2oB', on_delete=models.CASCADE, related_name='testO2oA')

class TestO2oB(models.Model):
    text = models.CharField(max_length=100, null=True, blank=True)
    TestO2oC = models.OneToOneField('TestO2oC', on_delete=models.CASCADE)

class TestO2oC(models.Model):
    text = models.CharField(max_length=100, null=True, blank=True)

class TestM2mA(models.Model):
    text = models.CharField(max_length=100, null=True, blank=True)
    testM2mBs = models.ManyToManyField('TestM2mB', related_name='testM2mAs')

class TestM2mB(models.Model):
    text = models.CharField(max_length=100, null=True, blank=True)
    testM2mCs = models.ManyToManyField('TestM2mC')

class TestM2mC(models.Model):
    text = models.CharField(max_length=100, null=True, blank=True)
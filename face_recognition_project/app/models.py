from django.db import models

# Create your models here.
    
class MarkAttendance(models.Model):
    # employee_id = models.CharField()
    employee_name = models.CharField(max_length=100)
    # mark_date = models.DateField()
    mark_time = models.TimeField()
    shift = models.CharField(choices=(
        ("Morning_In", "Morning_In"),
        ("Morning_Out", "Morning_Out"),
        ("Evening_In", "Evening_In"),
        ("Evening_Out", "Evening_Out")
    ), max_length=100)
    
    def __str__(self):
        return str(self.employee_name)

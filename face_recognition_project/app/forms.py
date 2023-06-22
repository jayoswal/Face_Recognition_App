from django import forms
from app.models import MarkAttendance
        
class MarkAttendanceForm(forms.ModelForm):
    
    class Meta:
        model = MarkAttendance
        fields = ['employee_name', 'mark_time', 'shift']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['employee_id'].widget.attrs.update({'class' : 'form-control', 'readonly':"True"})
        self.fields['employee_name'].widget.attrs.update({'class' : 'form-control', 'readonly':"True"})
        # self.fields['mark_date'].widget.attrs.update({'class' : 'form-control', 'readonly':"True"})
        self.fields['mark_time'].widget.attrs.update({'class' : 'form-control', 'readonly':"True"})
        self.fields['shift'].widget.attrs.update({'class' : 'form-control', 'readonly':"True"})
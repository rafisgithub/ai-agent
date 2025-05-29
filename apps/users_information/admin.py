from django.contrib import admin


from unfold.admin import ModelAdmin
from . models import UserInformation
from django.utils.html import format_html

@admin.register(UserInformation)
class CustomAdminClass(ModelAdmin):
    model = UserInformation
    list_display = (
        "custom_user",
        "full_name",
        "phone_number",
        "cv_file_link",
        "country",
        "preferred_study_country",
        "current_degree",
        "field_of_study",
        "gpa",
        "gre_score",
        "ielts_score",
        "toefl_score",
        "cgpa_scale",
        "has_research_experience",
        "research_area",
        "number_of_publications",
        "work_experience_years",
        "cv_file",
        "interested_degree",
        "preferred_university_type",
    )

    list_filter = (
        "custom_user",
        "country",
        "current_degree",
        "field_of_study",
        "has_research_experience",
        "interested_degree",
        "preferred_university_type",
    )

    search_fields = (
        "custom_user__email",
        "full_name",
        "phone_number",
        "country",
        "preferred_study_country",
        "current_degree",
        "field_of_study",
        "gpa",
        "gre_score",
        "ielts_score",
        "toefl_score",
        "cgpa_scale",
        "research_area",
        "interested_degree",
        "preferred_university_type",
    )



    def cv_file_link(self, obj):
        if obj.cv_file:
            return format_html('<a href="{}" target="_blank">View CV</a>', obj.cv_file.url)
        return "No CV uploaded"

    cv_file_link.short_description = "cv_file"  # This keeps the column name as 'cv_file'
from rest_framework import serializers

from patients.models import Patient


GENDER_CHOICES = ['Male', 'Female', 'Other']


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

    def validate_age(self, value):
        if value < 0 or value > 150:
            raise serializers.ValidationError('Age must be between 0 and 150.')
        return value

    def validate_gender(self, value):
        if value not in GENDER_CHOICES:
            raise serializers.ValidationError(f'Gender must be one of: {", ".join(GENDER_CHOICES)}.')
        return value

    def validate_contact_number(self, value):
        cleaned = value.replace(' ', '').replace('-', '').replace('+', '')
        if not cleaned.isdigit():
            raise serializers.ValidationError('Contact number must contain only digits, spaces, hyphens, or a leading +.')
        return value

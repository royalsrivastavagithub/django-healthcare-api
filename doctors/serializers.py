from rest_framework import serializers

from doctors.models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')

    def validate_years_of_experience(self, value):
        if value < 0 or value > 70:
            raise serializers.ValidationError('Years of experience must be between 0 and 70.')
        return value

    def validate_contact_number(self, value):
        cleaned = value.replace(' ', '').replace('-', '').replace('+', '')
        if not cleaned.isdigit():
            raise serializers.ValidationError('Contact number must contain only digits, spaces, hyphens, or a leading +.')
        return value

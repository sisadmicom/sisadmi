from rest_framework import serializers
from companies.models import Company, Branch

class SelectCompanySerializer(serializers.Serializer):
    company_id = serializers.IntegerField()
    branch_id = serializers.IntegerField(required=False, allow_null=True)

    def validate(self, attrs):
        company_id = attrs.get("company_id")
        branch_id = attrs.get("branch_id", None)

        try:
            company = Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            raise serializers.ValidationError({"company_id": "Empresa no encontrada."})

        if branch_id:
            try:
                branch = Branch.objects.get(pk=branch_id)
            except Branch.DoesNotExist:
                raise serializers.ValidationError({"branch_id": "Sucursal no encontrada."})
            if branch.company_id != company.id:
                raise serializers.ValidationError({"branch_id": "La sucursal no pertenece a la empresa seleccionada."})
            attrs["branch"] = branch
        else:
            attrs["branch"] = None

        attrs["company"] = company
        return attrs



from rest_framework import serializers
from users.models import UserCompanyMembership
from companies.models import Company

class UserCompanyMembershipSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    company_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = UserCompanyMembership
        fields = ['id', 'company_id', 'company_name', 'role', 'is_active']

    def create(self, validated_data):
        user = self.context['request'].user
        company_id = validated_data.pop('company_id')
        try:
            company = Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            raise serializers.ValidationError({'company_id': 'Empresa no encontrada.'})
        membership, created = UserCompanyMembership.objects.get_or_create(
            user=user,
            company=company,
            defaults={'role': validated_data.get('role', 'VIEWER'), 'is_active': validated_data.get('is_active', True)}
        )
        if not created:
            # update role/is_active
            membership.role = validated_data.get('role', membership.role)
            membership.is_active = validated_data.get('is_active', membership.is_active)
            membership.save()
        return membership

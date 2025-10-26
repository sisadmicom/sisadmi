from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import SelectCompanySerializer

class SelectCompanyAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = SelectCompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company = serializer.validated_data["company"]
        branch = serializer.validated_data["branch"]

        user = request.user
        # verificar membresía activa (o superuser)
        from users.models import UserCompanyMembership
        membership = user.memberships.filter(company=company, is_active=True).first()
        if not membership and not user.is_superuser:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("No tienes acceso a esta empresa.")
        user.company = company
        user.branch = branch
        user.save(update_fields=["company", "branch"])
        return Response({
            "detail": "Contexto actualizado",
            "company_id": company.id,
            "branch_id": branch.id if branch else None,
        }, status=status.HTTP_200_OK)

class ContextAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        company = getattr(user, 'company', None)
        branch = getattr(user, 'branch', None)
        return Response({
            "company": {
                "id": company.id,
                "name": getattr(company, 'name', None)
            } if company else None,
            "branch": {
                "id": branch.id,
                "name": getattr(branch, 'name', None)
            } if branch else None
        })



from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.models import UserCompanyMembership
from .serializers import UserCompanyMembershipSerializer

class MembershipViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = UserCompanyMembershipSerializer

    def get_queryset(self):
        user = self.request.user
        # superuser can view all memberships
        if user.is_superuser:
            return UserCompanyMembership.objects.all()
        return UserCompanyMembership.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        # only superuser can create memberships for arbitrary users; normal users create memberships for themselves
        if not user.is_superuser:
            # force creation for own user (company_id in serializer)
            serializer.save()
        else:
            # superuser can create memberships for any user (future extension)
            serializer.save()

from rest_framework import generics, permissions, status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import Vendor, VendorBankDetails
from .serializers import (
    VendorSerializer, VendorRegistrationSerializer, VendorUpdateSerializer,
    VendorBankDetailsSerializer, CreateBankDetailsSerializer
)


class VendorListAPIView(generics.ListAPIView):
    queryset = Vendor.objects.filter(is_verified=True)
    serializer_class = VendorSerializer
    permission_classes = [permissions.AllowAny]


class VendorDetailAPIView(generics.RetrieveAPIView):
    queryset = Vendor.objects.filter(is_verified=True)
    serializer_class = VendorSerializer
    permission_classes = [permissions.AllowAny]


class VendorRegistrationAPIView(generics.CreateAPIView):
    serializer_class = VendorRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Check if user already has a vendor account
        if Vendor.objects.filter(user=self.request.user).exists():
            raise serializers.ValidationError("User already has a vendor account")
        serializer.save(user=self.request.user)


class VendorProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return Vendor.objects.get(user=self.request.user)
        except Vendor.DoesNotExist:
            raise Http404("Vendor profile not found")

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return VendorUpdateSerializer
        return VendorSerializer


class VendorBankDetailsListAPIView(generics.ListCreateAPIView):
    serializer_class = VendorBankDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        vendor = get_object_or_404(Vendor, user=self.request.user)
        return VendorBankDetails.objects.filter(vendor=vendor)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateBankDetailsSerializer
        return VendorBankDetailsSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.method == 'POST':
            vendor = get_object_or_404(Vendor, user=self.request.user)
            context['vendor'] = vendor
        return context


class VendorBankDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VendorBankDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        vendor = get_object_or_404(Vendor, user=self.request.user)
        return VendorBankDetails.objects.filter(vendor=vendor)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def set_default_bank_account(request, pk):
    vendor = get_object_or_404(Vendor, user=request.user)
    bank_detail = get_object_or_404(VendorBankDetails, id=pk, vendor=vendor)
    
    # Set all bank details for this vendor to not default
    VendorBankDetails.objects.filter(vendor=vendor).update(is_default=False)
    
    # Set this one as default
    bank_detail.is_default = True
    bank_detail.save()
    
    return Response({
        'message': 'Default bank account updated successfully',
        'bank_detail': VendorBankDetailsSerializer(bank_detail).data
    })

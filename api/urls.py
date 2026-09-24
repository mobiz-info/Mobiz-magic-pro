from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import LoginAPIView, MeAPIView, UserViewSet, BusinessTypeViewSet, ClientViewSet, CountryViewSet, StateViewSet, DistrictViewSet, AreaViewSet, BranchViewSet, CustomerViewSet, EventNameViewSet, CustomerEventViewSet

router = DefaultRouter()

router.register("users", UserViewSet, basename="users")
router.register("business-types", BusinessTypeViewSet, basename="business-types")
router.register("clients", ClientViewSet, basename="clients")
router.register("countries", CountryViewSet, basename="countries")
router.register("states", StateViewSet, basename="states")
router.register("districts", DistrictViewSet, basename="districts")
router.register("areas", AreaViewSet, basename="areas")
router.register("branches", BranchViewSet, basename="branches")
router.register("customers", CustomerViewSet, basename="customers")
router.register("event-names", EventNameViewSet, basename="event-names")
router.register("customer-events", CustomerEventViewSet, basename="customer-events")

urlpatterns = [
    path("auth/login/", LoginAPIView.as_view(), name="api_login"),
    path("auth/me/", MeAPIView.as_view(), name="api_me"),
    path("", include(router.urls)),
]
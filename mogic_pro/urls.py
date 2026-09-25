from django.urls import include, path

from core import views as core_views
from masters import views as master_views
from operations import views as operation_views


urlpatterns = [

    # =====================================================
    # LOGIN
    # =====================================================

    path("", core_views.owner_login, name="home"),
    path("owner/login/", core_views.owner_login, name="owner_login"),
    path("owner/logout/", core_views.user_logout, name="user_logout"),
    path("owner/dashboard/", core_views.owner_dashboard, name="owner_dashboard"),


    # =====================================================
    # CLIENT MANAGEMENT
    # =====================================================

    path("owner/clients/", operation_views.client_list, name="client_list"),
    path("owner/clients/add/", operation_views.client_create, name="client_create"),
    path("owner/clients/<int:pk>/edit/", operation_views.client_edit, name="client_edit"),
    path("owner/clients/<int:pk>/delete/", operation_views.client_delete, name="client_delete"),
    path("owner/clients/<int:pk>/owner-details/", operation_views.owner_details, name="owner_details"),


    # =====================================================
    # BRANCH MANAGEMENT
    # =====================================================

    path("owner/branches/", operation_views.branch_list, name="branch_list"),
    path("owner/branches/add/", operation_views.branch_create, name="branch_create"),
    path("owner/branches/<int:pk>/edit/", operation_views.branch_edit, name="branch_edit"),
    path("owner/branches/<int:pk>/delete/", operation_views.branch_delete, name="branch_delete"),


    # =====================================================
    # CUSTOMER MANAGEMENT
    # =====================================================

    path("owner/customers/", operation_views.customer_list, name="customer_list"),
    path("owner/customers/add/", operation_views.customer_create, name="customer_create"),
    path("owner/customers/<int:pk>/edit/", operation_views.customer_edit, name="customer_edit"),
    path("owner/customers/<int:pk>/delete/", operation_views.customer_delete, name="customer_delete"),


    # =====================================================
    # BUSINESS TYPE
    # =====================================================

    path("owner/business-types/", master_views.business_type_list, name="business_type_list"),
    path("owner/business-types/add/", master_views.business_type_create, name="business_type_create"),
    path("owner/business-types/<int:pk>/edit/", master_views.business_type_edit, name="business_type_edit"),
    path("owner/business-types/<int:pk>/delete/", master_views.business_type_delete, name="business_type_delete"),


    # =====================================================
    # COUNTRY
    # =====================================================

    path("owner/countries/", master_views.country_list, name="country_list"),
    path("owner/countries/add/", master_views.country_create, name="country_create"),
    path("owner/countries/<int:pk>/edit/", master_views.country_edit, name="country_edit"),
    path("owner/countries/<int:pk>/delete/", master_views.country_delete, name="country_delete"),


    # =====================================================
    # STATE / PROVINCE
    # =====================================================

    path("owner/states/", master_views.state_list, name="state_list"),
    path("owner/states/add/", master_views.state_create, name="state_create"),
    path("owner/states/<int:pk>/edit/", master_views.state_edit, name="state_edit"),
    path("owner/states/<int:pk>/delete/", master_views.state_delete, name="state_delete"),


    # =====================================================
    # DISTRICT
    # =====================================================

    path("owner/districts/", master_views.district_list, name="district_list"),
    path("owner/districts/add/", master_views.district_create, name="district_create"),
    path("owner/districts/<int:pk>/edit/", master_views.district_edit, name="district_edit"),
    path("owner/districts/<int:pk>/delete/", master_views.district_delete, name="district_delete"),


    # =====================================================
    # AREA
    # =====================================================

    path("owner/areas/", master_views.area_list, name="area_list"),
    path("owner/areas/add/", master_views.area_create, name="area_create"),
    path("owner/areas/<int:pk>/edit/", master_views.area_edit, name="area_edit"),
    path("owner/areas/<int:pk>/delete/", master_views.area_delete, name="area_delete"),


    # =====================================================
    # CUSTOMER EVENTS
    # =====================================================

    path("owner/customer-events/", operation_views.customer_event_list, name="customer_event_list"),
    path("customer-events/add/",operation_views.customer_event_create,name="customer_event_create",),  
    path("owner/customer-events/<int:pk>/edit/", operation_views.customer_event_edit, name="customer_event_edit"),
    path("owner/customer-events/<int:pk>/delete/", operation_views.customer_event_delete, name="customer_event_delete"),


    # =====================================================
    # EVENT NAMES
    # =====================================================

    path("owner/event-names/", master_views.event_name_list, name="event_name_list"),
    path("owner/event-names/add/", master_views.event_name_create, name="event_name_create"),
    path("owner/event-names/<int:pk>/edit/", master_views.event_name_edit, name="event_name_edit"),
    path("owner/event-names/<int:pk>/delete/", master_views.event_name_delete, name="event_name_delete"),


    # =====================================================
    # API
    # =====================================================

    path("api/", include("api.urls")),
]

from django.contrib import admin
from django.urls import path
from PCPLapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('index/',views.index, name="index"),
    path("signup-record/", views.signuprec,name="signuprec"),
    path("sign_up_rec_delete/<iid>/", views.sign_up_rec_delete,name="sign_up_rec_delete"),
    path("Order_Deatils/", views.Order_Deatils,name="Order_Deatils"),
    path("preserve/", views.preserve,name="preserve"),
    path("Order_Service", views.Order_Service,name="Order_Service"),
    path('order_update/<iid>/',views.order_update,name='order_update'),
    path('order_delete/<iid>/',views.order_delete,name='order_delete'),
    path('invoice/<iid>/',views.invoice,name='invoice'),
    path('vehicle_expense/',views.vehicle_expense,name='vehicle_expense'),
    path('vehicle_reparing/',views.vehicle_reparing,name='vehicle_reparing'),
    path('expense_report/',views.expense_report,name='expense_report'),

    path('Mark-attendence/',views.markAttendence,name='markAttendence'),
    
     
    path('users_profile/',views.users_profile,name='users_profile'),
    path('search/',views.search,name='search'),
    path('sign_up_record/',views.sign_up_record,name='sign_up_record'),

    # --------------------------- AJAX ----------------------------
    path('fghevbn/ajaxcall/',views.ajaxCall,name="ajax_call"),



    # transporter
    path('transpoter_details/',views.transpoter_details,name='transpoter_details'),
    path('transpoter_entry/',views.transpoter_entry,name='transpoter_entry'),
    path('transpoter_details_update/<iid>/',views.transpoter_details_update,name='transpoter_details_update'),
    path('transpoter_details_delete/<iid>/',views.transpoter_details_delete,name='transpoter_details_delete'),
    # vehicle
    path('vehicle_service/',views.vehicle_entry,name='vehicle_service'),
    path('vehicle_details/',views.vehicle_details,name='vehicle_details'),
    path('vehicle_details_delete/<iid>/',views.vehicle_details_delete,name='vehicle_details_delete'),
    path('vehicle_details_update/<iid>/',views.vehicle_details_update,name='vehicle_details_update'),
    # driver details
    path('driver_details/',views.driver_details,name="driver_details"),
    path('driver_entry/',views.driver_entry,name="driver_entry"),
    path('driver_details_update/<iid>/',views.driver_details_update,name='driver_details_update'),
    path('driver_details_delete/<iid>/',views.driver_details_delete,name='driver_details_delete'),
    # driver payment
    path('driver_payment_entry/',views.driver_payment_entry,name='driver_payment_entry'),
    path('driver_payment/',views.driver_payment,name='driver_payment'),
    path('driver_payment/<iid>/',views.driver_payment_update,name='driver_payment_update'),
    path('driver_payment_delete/<iid>/',views.driver_payment_delete,name='driver_payment_delete'),

    # ====================================== Aman Kumar ================================================
    #  Deport
    path('Depot/',views.deport,name='Depot'),
    # path('Depot_Servie/',views.search_deport,name='search_deport'),
    path('Depot_Service/',views.search_deport,name='Depot_Service'),
    path('Depot_update/<iid>/',views.Depot_update,name='Depot_update'),
    path('deport_delete/<iid>/',views.deport_delete,name='deport_delete'),
    #  Disturubtor
    path('Distributor_details/',views.Distributor_details,name='Distributor_details'),
    path('Distributor/',views.dis,name='Distributor'),
    path('distributor_update/<iid>/',views.distributor_update,name='distributor_update'),
    
    path('distributor_delete/<iid>/',views.distributor_delete,name='distributor_delete'),


path('attendence/',views.attendence,name='attendence'),


    #vehicle expense
    path('vehicle_expense/',views.vehicle_expense,name='vehicle_expense'),
    path('expense_update/<iid>/',views.expense_update,name='expense_update'),
    path('expense_delete/<iid>/',views.expense_delete,name='expense_delete'),
    #vehicle rep    
    path('vehicle_reparing/',views.vehicle_reparing,name='vehicle_reparing'),
    path('rep_update/<iid>/',views.rep_update,name='rep_update'),
    path('rep_delete/<iid>/',views.rep_delete,name='rep_delete'),
    #expense report
    path('expense_report/',views.expense_report,name='expense_report'),
    # -----------------------------------------------------------------------------------------------
      
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


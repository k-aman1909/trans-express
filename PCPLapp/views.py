from django.http import JsonResponse
from django.shortcuts import HttpResponse,render,redirect
from django.conf import settings
from django.urls import reverse
from PCPLapp import models
from loginapp.models import User
from django.utils import timezone
from django.contrib import messages
from django import http
import datetime
def index(request):
    aman = {
        'title': 'PCPL',
        's_user' : request.s_user,
        'username' : request.user,
        # 'profile' : models.profile_update.objects.get(userid=request.user),
        
    }
    number=models.automatic1.objects.all()
    vehicle= models.plvehicle.objects.all()
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'GET':
            depot_name = request.GET.get('depot_name')
            request.session['depot_name'] = depot_name
            return JsonResponse({'depot_name':depot_name})

    s_user = request.s_user
    if s_user == 'User':
        aman['page_name'] = 'base_user.html'
        diponame = User.objects.filter(username=request.user)
        for x in diponame:
            aman['diponame'] = x.diponame
    elif s_user == 'Admin':
        aman['page_name'] = 'base.html'
        diponame = User.objects.filter(username=request.user)
        for x in diponame:
            aman['diponame'] = x.diponame
    else:
        aman['page_name'] = 'base.html'
    if s_user ==True :
        value = models.profile_update.objects.filter(userid=request.user)
        if value.exists():
            pass
        else:
            super_user=User.objects.filter(username=request.user)
            
            for x in super_user:
                models.profile_update(userid=x.username, first_name= x.first_name, cont_no=x.phone_number, email=x.email).save()
    if not request.session.get('once in time'):
        user = User.objects.filter(is_active=False)
        request.session['once in time'] = 'my_value'
    else:
        user=None
    dname = models.dipo.objects.values('pri_name').distinct()
    if not models.automatic1.objects.all().exists():
        models.automatic1.objects.get_or_create(trans_id=0,drv_id=0,dist_id=0,dipo_id=0)

    return render(request, 'index.html' ,{'dname':dname,'sign_r':user, 'aman':aman,'number':number ,'vehicle':vehicle})

def signuprec(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == "GET":
            diponame =request.GET.get('depo_name')
            role =request.GET.get('role')
            username =request.GET.get('username')
            user = User.objects.filter(username=username)
            for x in user:
                x.is_active = True
                x.diponame = diponame
                x.role = role
                x.save()
                models.profile_update(userid=username, first_name= x.first_name, cont_no=x.phone_number, email=x.email).save()
            
        return JsonResponse({'status':True})

def users_profile(request):
    aman={
        'title' : 'PCPL | Order Page',
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    uu = models.profile_update.objects.get(userid=request.user)
    s_user = request.s_user
    if s_user == 'User':
        aman['page_name'] = 'base_user.html'
    else:
        aman['page_name'] = 'base.html'
    update=models.profile_update.objects.get(userid=request.user)
    if request.method =='POST':
        
        if request.FILES.get('profile_pic'):
            update.profile_pic=request.FILES.get('profile_pic')
        update.first_name=request.POST.get('first_name')
        update.cont_no=request.POST.get('cont_no')
        update.email=request.POST.get('email')
        update.gender=request.POST.get('gender')
        update.dob=request.POST.get('dob')
        update.state=request.POST.get('state') 
        update.distr=request.POST.get('district')
        update.pincode=request.POST.get('pincode')
        update.adrs=request.POST.get('adrs')
        update.save()
        user = User.objects.get(username=update.userid)
        user.email=update.email
        user.phone_number=update.cont_no
        
        user.save()
            
        messages.success(request, 'Successfully updated')
        return redirect(reverse('users_profile'))
        
    else:
        
        if update.distr:
            data = models.state1.objects.get(stat=update.state)
            data= data.distr.split(',')     
            return render(request,'users-profile.html',{'aman':aman,'data':data})
        else:
            return render(request,'users-profile.html',{'aman':aman })


def sign_up_rec_delete(request,iid):
    User.objects.filter(username=iid).delete()
    messages.success(request,'Record Deleted')
    return redirect("index")


def markAttendence(request):
    data = {
        'title' : 'Mark Attendence',
        'page_name' : 'base.html',
        'dist_id' : models.distri_details.objects.values('dist_id'),
    }
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'GET':
            iid = request.GET.get('iid')
            if iid is not None:
                try :
                    dist_details = models.distri_details.objects.get(dist_id=iid)
                    response_data = {
                        'status' : True,
                        'name' : dist_details.dist_name,
                        'post' : 'Distributor',
                        'contact' : dist_details.cont_no
                    }
                    return http.JsonResponse(response_data, safe=False)
                except models.distri_details.DoesNotExist:
                    response_data = {
                        'status' : False,
                        'message' : 'Details Not Found'
                    }
                    return http.JsonResponse(response_data, safe=False)
        if request.method == "POST":
            mark = models.markAttendence()
            mark.emp_id = request.POST.get('distributor_id')
            mark.status = True
            mark.time = datetime.datetime.now().time()
            mark.date = datetime.datetime.now().date()
            mark.save()
            if mark.pk is not None:
                response_data = {
                    'status' : True,
                    'title' : 'Success...!',
                    'message' : 'Attendence Marked Successfully.'
                }
                return http.JsonResponse(response_data, safe=False)
            else:
                response_data = {
                    'status' : False,
                    'title' : 'Oops....!',
                    'message' : 'Something Went Wrong !'
                }
                return http.JsonResponse(response_data, safe=False)
    return render(request, 'markattendence.html',{'data':data})

def Order_Deatils(request):
    dname = models.dipo.objects.all()
    depot_name = request.session.get('depot_name')
    
    aman={
        'title' : 'PCPL | Order Page',
        'username' : request.user,
        's_user' : request.s_user,
        'diponame' : models.dipo.objects.get(pri_name=depot_name).pri_name,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    data= {
        'depotname' : models.dipo.objects.get(pri_name=depot_name),
        'distri_name' : models.distri_details.objects.filter(dipo_name=depot_name),
        'transp_name' : models.transporter_details.objects.filter(dipo_id=depot_name),
        'v_type' : models.plvehicle.objects.filter(dipo_id=depot_name),
        'preservelr':models.preserve.objects.filter(diponame=depot_name),
        }
    s_user = request.s_user
    if s_user == 'User':
        aman['page_name'] = 'base_user.html'
    elif s_user == 'Admin':
        aman['page_name'] = 'base.html'
        diponame = User.objects.filter(username=request.user)
        for x in diponame:
            aman['diponame'] = x.diponame
    else:
        aman['page_name'] = 'base.html'
        
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == "GET":
            dist_name = request.GET.get('dist_name')
            trans_name = request.GET.get('trans_name')
            dist_town=request.GET.get('dist_town')
            v_type=request.GET.get('v_type')
            l_type=request.GET.get('l_type')
            preserveid=request.GET.get('preserveid')
           
        
            if dist_town is not None and v_type is not None and l_type is not None:
                try:
                    order = models.plvehicle.objects.get(cname=dist_town, lt=l_type, vtype=v_type)
                    response_data = {
                        'success': True,
                        'data': order.vprise,
                    }
                    return JsonResponse(response_data)
                except models.plvehicle.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Order not found.'})
            
            
            if dist_name is not None:
                order = models.distri_details.objects.get(dist_name=dist_name)
                response_data = {
                    'success': True,
                    'data': order.city,   
                }            
                return http.JsonResponse(response_data,safe=False)
            
            
            if preserveid is not None:
                order = models.transporter_details.objects.filter(trans_name=trans_name)
                preserve = models.preserve.objects.get(order_id=preserveid)
                veh_ty_options = []
                veh_tys = preserve.v_type.split(',')
                for veh_ty in veh_tys:
                    veh_ty = veh_ty.strip()
                    veh_ty_options.append(f'<option value="{veh_ty}">{veh_ty}</option>')
                response_data = {
                    'success': True,
                    'data': preserve.order_id,   
                    'lr_date': preserve.lr_date,   
                    'dist_name': preserve.dist_name,   
                    'dist_town': preserve.dist_town,   
                    'trnas_name': preserve.trnas_name,  
                    'v_type': veh_ty_options,   
                    'v_no': preserve.v_no,   
                    'l_type': preserve.l_type,   
                    'invoice_no': preserve.invoice_no,   
                    'invoice_val': preserve.invoice_val,   
                    'quantity': preserve.quantity,   
                    'quan': preserve.quan,   
                    'invoice_date': preserve.invoice_date,   
                    'weight': preserve.weight,   
                    'weig': preserve.weig,   
                    'labour_exp': preserve.labour_exp,   
                    'freight': preserve.freight,   
                    'misc_charge': preserve.misc_charge,   
                    'total_amt': preserve.total_amt,   
                    'advance_amnt': preserve.advance_amnt,   
                    'advance_per': preserve.advance_per,   
                    'due_amnt': preserve.due_amnt,   
                    'product': preserve.product,  
                }            
                return http.JsonResponse(response_data,safe=False)
            
            if trans_name is not None:
                order = models.transporter_details.objects.filter(trans_name=trans_name)
                veh_ty_options = []
                for x in order:
                    veh_tys = x.veh_ty.split(',')
                    for veh_ty in veh_tys:
                        veh_ty_options.append(
                            f'<option value="{veh_ty.strip()}">{veh_ty.strip()}</option>',
                        )
        
                    response_data = {
                        'success': True,
                        'data': veh_ty_options,
                    }          
                
                return http.JsonResponse(response_data,safe=False)
    if request.method == 'POST':
        order_id=request.POST['order_id']
        lr_date=request.POST['lr_date']
        dist_name=request.POST['dist_name']
        dist_town=request.POST['dist_town']
        trans_name=request.POST['trans_name']
        v_type=request.POST['v_type']
        v_no=request.POST['v_no']
        l_type=request.POST['l_type']
        invoice_no=request.POST['invoice_no']
        invoice_val=request.POST['invoice_val']
        quantity=request.POST['quantity']
        quan=request.POST['quan']
        invoice_date=request.POST['invoice_date']
        weight=request.POST['weight']
        weig=request.POST['weig']
        labour_exp=request.POST['labour_exp']
        freight=request.POST['freight']
        misc_charge=request.POST['misc_charge']
        total_amt=request.POST['total_amt']
        advance_amnt=request.POST['advance_amnt']
        advance_per=request.POST['advance_per']
        due_amnt=request.POST['due_amnt']
        product=request.POST['product']
        diponame=request.POST['diponame']
        update = models.automatic1.objects.get(id=1)
        rs = update.order_id 
        rs = int(rs)
        rs = rs + 1
        order_id2 = str(rs)
        update.order_id = order_id2
        update.save()
        try:
           preserve_data = models.preserve.objects.get(order_id=order_id) 
           preserve_data.delete()
        except models.preserve.DoesNotExist:
            pass
        obj = models.order_details(order_id=order_id,lr_date=lr_date,dist_name=dist_name,dist_town=dist_town,trnas_name=trans_name,v_type=v_type,v_no=v_no,l_type=l_type,invoice_no=invoice_no,invoice_val=invoice_val,quantity=quantity,quan=quan,invoice_date=invoice_date,weight=weight,weig=weig,labour_exp=labour_exp,freight=freight,misc_charge=misc_charge,total_amt=total_amt,advance_amnt=advance_amnt,advance_per=advance_per,due_amnt=due_amnt,product=product,diponame=diponame)
        obj.save()
        messages.success(request, 'Successfully inserted')
        return redirect('Order_Deatils')
    else:
        yr = datetime.date.today().year%100
        rs = models.automatic1.objects.get(id=1).order_id
        rs = int(rs) + 1
        if rs < 10:
            order_id = str(data['depotname'].diop_id)+'/'+str(yr)+'/'+'000' + str(rs)
        elif rs < 100:
            order_id = str(data['depotname'].diop_id)+'/'+str(yr)+'/'+'00' + str(rs)
        else:
            order_id = str(data['depotname'].diop_id)+'/'+str(yr)+'/'+'0' + str(rs)
    return render(request,'Order_Deatils.html',{'aman':aman,'data':data ,'order_id':order_id,'dname':dname})

def preserve(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'POST':
            order_id=request.POST.get('order_id')
            lr_date=request.POST.get('lr_date')
            dist_name=request.POST.get('dist_name')
            dist_town=request.POST.get('dist_town')
            trans_name=request.POST.get('trans_name')
            v_type=request.POST.get('v_type')
            v_no=request.POST.get('v_no')
            l_type=request.POST.get('l_type')
            invoice_no=request.POST.get('invoice_no')
            invoice_val=request.POST.get('invoice_val')
            quantity=request.POST.get('quantity')
            quan=request.POST.get('quan')
            invoice_date=request.POST.get('invoice_date')
            weight=request.POST.get('weight')
            weig=request.POST.get('weig')
            labour_exp=request.POST.get('labour_exp')
            freight=request.POST.get('freight')
            misc_charge=request.POST.get('misc_charge')
            total_amt=request.POST.get('total_amt')
            advance_amnt=request.POST.get('advance_amnt')
            advance_per=request.POST.get('advance_per')
            due_amnt=request.POST.get('due_amnt')
            product=request.POST.get('product')
            diponame=request.POST.get('diponame')
            update = models.automatic1.objects.get(id=1)
            rs = update.order_id 
            rs = int(rs)
            rs = rs + 1
            order_id2 = str(rs)
            update.order_id = order_id2
            update.save()
            obj = models.preserve.objects.update_or_create(order_id=order_id, defaults = {'lr_date':lr_date,'dist_name':dist_name,'dist_town':dist_town,'trnas_name':trans_name,'v_type':v_type,'v_no':v_no,'l_type':l_type,'invoice_no':invoice_no,'invoice_val':invoice_val,'quantity':quantity,'quan':quan,'invoice_date':invoice_date,'weight':weight,'weig':weig,'labour_exp':labour_exp,'freight':freight,'misc_charge':misc_charge,'total_amt':total_amt,'advance_amnt':advance_amnt,'advance_per':advance_per,'due_amnt':due_amnt,'product':product,'diponame':diponame})
            response_data = {
                'success' : True,
            }
            return http.JsonResponse(response_data,safe=False)




def Order_Service(request):
    dname = models.dipo.objects.all()
    depot_name = request.session.get('depot_name')
    aman={
        'title' : 'PCPL | Order Page',
        'username' : request.user,
        's_user' : request.s_user,
        'diponame' : models.dipo.objects.get(pri_name=depot_name).pri_name,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
  
    data ={
        
        'diponame' : models.order_details.objects.filter(diponame=depot_name).values('order_id').distinct(),
        'distname' : models.order_details.objects.filter(diponame=depot_name).values('dist_name').distinct(),
        'tranname' : models.order_details.objects.filter(diponame=depot_name).values('trnas_name').distinct(),
        'disttown' : models.order_details.objects.filter(diponame=depot_name).values('dist_town').distinct(),
        
    }
    s_user = request.s_user
    if s_user == 'User':
        aman['page_name'] = 'base_user.html'
    elif s_user == 'Admin':
        aman['page_name'] = 'base.html'
        diponame = User.objects.filter(username=request.user)
        for x in diponame:
            aman['diponame'] = x.diponame
    else:
        aman['page_name'] = 'base.html'
        
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'POST':
            order_id= request.POST.get('order_id')
            deponame = request.POST.get('deponame')
            dist_name = request.POST.get('dist_name')
            trnas_name = request.POST.get('trnas_name')
            dist_town = request.POST.get('dist_town')
            f_date = request.POST['f_date']
            t_date = request.POST['t_date']
            url={}
            if deponame != None:
                url['diponame'] = deponame
            if order_id!=None:
                url['order_id']=order_id
            if dist_name!=None:
                url['dist_name']=dist_name
            if trnas_name!=None:
                url['trnas_name']=trnas_name
            if dist_town!=None:
                url['dist_town']=dist_town
            if f_date and  t_date:
                url['lr_date__range']=[f_date , t_date]
            # data = models.distri_details.objects.all() 
            obj = models.order_details.objects.filter(**url)
            if obj.exists():   
                value=f' <table class="dis_table"><thead><th>ID</th><th>Order ID</th><th>Lr date</th><th>Distributor name</th><th>Distributor town</th><th>Transporter name</th><th>vehicle type</th><th>vehicle no</th><th>load type</th><th>invoice no</th><th>invoice value</th><th>quantity</th> <th>invoice date</th><th>weight</th><th>Labour Expense</th><th>Freight</th><th>Miscallaneous charge</th><th>Total amount</th> <th>Advance amount</th><th>Dues Amount</th><th>Product</th><th colspan="3" align="centre">Action&nbsp;Here</th></thead><tbody>'
                for x in obj:
                    value+=f'<tr>'
                    value+=f'<td>{x.id}</td>'
                    value+=f'<td>{x.order_id}</td>'
                    value+=f'<td>{x.lr_date}</td>'
                    value+=f'<td>{x.dist_name}</td>'
                    value+=f'<td>{x.dist_town}</td>'
                    value+=f'<td>{x.trnas_name}</td>'
                    value+=f'<td>{x.v_type}</td>'
                    value+=f'<td>{x.v_no}</td>'
                    value+=f'<td>{x.l_type}</td>'
                    value+=f'<td>{x.invoice_no}</td>'
                    value+=f'<td>{x.invoice_val}</td>'
                    value+=f'<td>{x.quantity} {x.quan}</td>'
                    value+=f'<td>{x.invoice_date}</td>'
                    value+=f'<td>{x.weight} {x.weig}</td>'
                    value+=f'<td>{x.labour_exp}</td>'
                    value+=f'<td>{x.freight}</td>'
                    value+=f'<td>{x.misc_charge}</td>'
                    value+=f'<td>{x.total_amt}</td>'
                    value+=f'<td>{x.advance_amnt}</td>'
                    value+=f'<td>{x.due_amnt}</td>'
                    value+=f'<td>{x.product}</td>'
                    value += f'<td  class="leave"><a href="/invoice/{x.id}/" ><i class="fa-solid fa-print"></i></a></td>'
                    value += f'<td  class="leave"><a href="/order_update/{x.id}/" ><i class="fa-solid fa-file-pen"></i></a></td>'
                    value += f'<td  class="leave"><a onclick="del(\'/order_delete/{x.id}/\')" ><i class="fa-solid fa-trash" style="color:red;cursor:pointer;"></i></a></td>'
                    
                    value+=f'</tr>'
                value+= '</tbody></table>'
                response ={
                    'success':True,
                    'value' :value
                }
                return http.JsonResponse(response, safe=False)
            else:
                response ={
                    'success' :False,
                    'message':'NO records Found'
                }
                return http.JsonResponse(response, safe=False)
    else:
    
        return render(request,'order_Service.html',{'aman':aman,'dname':dname ,'data':data})

def order_delete(request, iid):
    models.order_details.objects.get(id=iid).delete()
    
    messages.success(request, 'Record Deleted Enjoy !')
    return redirect('Order_Service')

def order_update(request,iid):
    dname = models.dipo.objects.all()
    depot_name = request.session.get('depot_name')
    
    aman={
        'title' : 'PCPL | Order Page',
        'username' : request.user,
        's_user' : request.s_user,
        'diponame' : models.dipo.objects.get(pri_name=depot_name).pri_name,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    data= {
        'depotname' : models.dipo.objects.get(pri_name=depot_name),
        'distri_name' : models.distri_details.objects.filter(dipo_name=depot_name),
        'transp_name' : models.transporter_details.objects.filter(dipo_id=depot_name),
        'v_type' : models.plvehicle.objects.filter(dipo_id=depot_name),
        }
    s_user = request.s_user
    if s_user == 'User':
        aman['page_name'] = 'base_user.html'
    elif s_user == 'Admin':
        aman['page_name'] = 'base.html'
        diponame = User.objects.filter(username=request.user)
        for x in diponame:
            aman['diponame'] = x.diponame
    else:
        aman['page_name'] = 'base.html'
        
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == "GET":
            dist_name = request.GET.get('dist_name')
            trans_name = request.GET.get('trans_name')
            dist_town=request.GET.get('dist_town')
            v_type=request.GET.get('v_type')
            l_type=request.GET.get('l_type')
            if dist_town is not None and v_type is not None and l_type is not None:
                order = models.plvehicle.objects.get(cname=dist_town,lt=l_type,vtype=v_type)
                response_data = {
                    'success': True,
                    'data': order.vprise,   
                }         
                return http.JsonResponse(response_data,safe=False)
            
            if dist_name is not None:
                order = models.distri_details.objects.get(dist_name=dist_name)
                response_data = {
                    'success': True,
                    'data': order.city,   
                }            
                return http.JsonResponse(response_data,safe=False)
            
            if trans_name is not None:
                order = models.transporter_details.objects.filter(trans_name=trans_name)
                veh_ty_options = []
                for x in order:
                    veh_tys = x.veh_ty.split(',')
                    for veh_ty in veh_tys:
                        veh_ty_options.append(
                            f'<option value="{veh_ty.strip()}">{veh_ty.strip()}</option>',
                        
                                              )
        
                    response_data = {
                        'success': True,
                        'data': veh_ty_options,
                    }          
                
                return http.JsonResponse(response_data,safe=False)
    update= models.order_details.objects.get(id=iid)
    if request.method=='POST':
        update.order_id=request.POST['order_id']
        update.lr_date=request.POST['lr_date']
        update.dist_name=request.POST['dist_name']
        update.dist_town=request.POST['dist_town']
        update.trnas_name=request.POST['trans_name']
        update.v_type=request.POST['v_type']
        update.v_no=request.POST['v_no']
        update.l_type=request.POST['l_type']
        update.invoice_no=request.POST['invoice_no']
        update.invoice_val=request.POST['invoice_val']
        update.quantity=request.POST['quantity']
        update.quan=request.POST['quan']
        update.invoice_date=request.POST['invoice_date']
        update.weight=request.POST['weight']
        update.weig=request.POST['weig']
        update.labour_exp=request.POST['labour_exp']
        update.freight=request.POST['freight']
        update.misc_charge=request.POST['misc_charge']
        update.total_amt=request.POST['total_amt']
        update.advance_amnt=request.POST['advance_amnt']
        update.due_amnt=request.POST['due_amnt']
        update.product=request.POST['product']
        update.save()
        messages.success(request,'Record Sucessfully updated')
        # return render(request,'Order_Deatils.html')
        return redirect('Order_Deatils')
    else:
        # data = models.state1.objects.get(stat=update.state)
        # data= data.distr.split(',')        
        return render(request,'Order_Deatils_update.html',{"u":update, 'aman':aman,'data':data ,'dname':dname})
    
def invoice(request,iid):
    invoice=models.order_details.objects.get(id=iid)
    invoice.order_id.split('/')
    distri = models.distri_details.objects.get(dist_name=invoice.dist_name)
    patliputra = models.dipo.objects.get(diop_id=invoice.order_id.split('/')[0].strip())
    if patliputra.ope_name == 'TransExpress':
        gst = '10EOSPS5914H1ZM'
        pan = 'EOSPS5914H'
    else:
        gst = '10AAFHS9900L1Z2'
        pan = 'AAFHS9900L'
    data = {
        'invoice' : invoice,
        'gst' : gst,
        'pan' : pan,
        'adrs':patliputra.addr,
        'distadrs':distri.addrs
    }
    return render(request,'updatedinvoice.html',{"data":data})

def sign_up_record(request):
    
    data ={
        'dipo':models.dipo.objects.values('pri_name').distinct(),
        'user' : User.objects.filter(is_active=False),
         
    }
    aman={
        'title' : 'PCPL | Order Page',
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    s_user = request.s_user
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    elif s_user == 'Admin':
        aman['page_name'] = 'base.html'
        diponame = User.objects.filter(username=request.user)
        for x in diponame:
            aman['diponame'] = x.diponame
    else:
        aman['page_name'] = 'base.html'
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == "GET":
            diponame =request.GET.get('depo_name')
            role =request.GET.get('role')
            username =request.GET.get('username')
            user = User.objects.filter(username=username)
            for x in user:
                x.is_active = True
                x.diponame = diponame
                x.role = role
                x.save()
        return JsonResponse({'status':True})
    return render(request,'sign_up_record.html',{'data':data,'aman':aman})

# Deport

def deport(request):
    aman={
        'title' : 'PCPL | Deport Page',
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    dname = models.dipo.objects.all()
    s_user = request.s_user
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    else:
        aman['page_name'] = 'base.html'
    if request.method == 'POST':
        # Extract data from the form
        did = request.POST['did']
        pri_name = request.POST['pre-com-name']
        ope_name = request.POST['ope-com-name']
        man_name = request.POST['dmanager-name']
        man_cont = request.POST['dmanager-no']
        depo_cont = request.POST['depot-no']
        depo_tel = request.POST['depot-tno']
        state = request.POST['state']
        distr = request.POST['district']
        addr = request.POST['address']
        gst = request.POST['gst-no']

        # Check if dipo_id was manually edited
        existing_dipo_id = request.POST.get('dipo_id')
        
        if existing_dipo_id:
            dipo_id = existing_dipo_id
        else:
            # Auto-generate dipo_id
            rs = models.automatic1.objects.get(id=1).dipo_id
            rs = int(rs) + 1
            if rs < 10:
                dipo_id = 'D00' + str(rs)
            elif rs < 100:
                dipo_id = 'D0' + str(rs)
            else:
                dipo_id = 'D' + str(rs)
            if dipo_id == did:
            # Save to the automatic1 table
                models.automatic1.objects.filter(id=1).update(dipo_id=rs)

        # Save to the dipo table
        obj = models.dipo(diop_id=did, pri_name=pri_name, ope_name=ope_name, man_name=man_name,
                          man_cont=man_cont, depo_cont=depo_cont, depo_tel=depo_tel, state=state,
                          distr=distr, addr=addr, gst=gst)
        obj.save()

        messages.success(request, 'Successfully inserted')
        return redirect(reverse('Depot'))
    
    else:
        # Auto-generate dipo_id for new entry
        rs = models.automatic1.objects.get(id=1).dipo_id
        rs = int(rs) + 1
        if rs < 10:
            dipo_id = 'D00' + str(rs)
        elif rs < 100:
            dipo_id = 'D0' + str(rs)
        else:
            dipo_id = 'D' + str(rs)

        return render(request, 'Depot.html', {'dipo_id': dipo_id, 'dname': dname,'aman':aman})
        
def search(request):
    dname = models.dipo.objects.all()
    data={
        'user':User.objects.values('diponame').distinct(),
        
    }
    aman={
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    dname = models.dipo.objects.all()
    s_user = request.s_user
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    else:
        aman['page_name'] = 'base.html'
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':  
        if request.method == "POST":
            user =request.POST.get('depo_name')
            url={}
            if user != "" and user is not None:
                url['diponame']=user
            if url:
                url['is_active'] = True
                obj = User.objects.filter(**url)
                if obj.exists():
                    value = f'<table><thead><th>sl no.</th><th>User Name</th><th>Depo name</th><th>Role</th><th>Status</th><th>Inactivate</th></thead></tbody>'
                    for x in obj:
                        value += f'<tr>'
                        value += f'<td>{x.id}</td>'
                        value += f'<td>{x.username}</td>'
                        value += f'<td>{x.diponame}</td>'
                        value += f'<td>{x.role}</td>'
                        if x.is_active == True:
                            value += f"<td>Active</td>"
                        else:
                            value += f"<td>Inactive</td>"
                        
                        value += f'<td><div style="color:red; cursor:Pointer;" onclick="inactive_user(\'{x.username}\')" id="inactive" ><i class="fa-solid fa-user-xmark"></i></div></td>'
                        value += f'</tr>'
                    value += '</tbody></table>'
                    response ={
                        'success' : True,
                        'value' : value
                    }
                    return http.JsonResponse(response, safe=False)
                else:
                    response ={
                        'success' : False,
                        'message' : 'No Deatils For this Depot'
                    }
                    return http.JsonResponse(response, safe=False)
            else:
                response ={
                        'success' : False,
                        'message' : 'Select Any depot Depot'
                    }
                return http.JsonResponse(response, safe=False)
        if request.method == "GET":
            username =request.GET.get('username')
            user = User.objects.filter(username=username)
            for x in user:
                x.is_active = False
                x.save()
        return JsonResponse({'status':True})
    else: 
        return render(request, 'search.html', {'data':data,'dname':dname,'aman':aman})
    


def search_deport(request):
    dname = models.dipo.objects.all()
    data ={
        'name' :models.dipo.objects.values('pri_name').distinct(),
        'distr' : models.dipo.objects.values('distr').distinct(),
        
    }
    aman={
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    dname = models.dipo.objects.all()
    s_user = request.s_user
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    else:
        aman['page_name'] = 'base.html'
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == "POST":
            name = request.POST.get('s1')
            dist = request.POST.get('s2')
            url={}
            if name != None:
                url['pri_name']=name
            if dist != None:
                url['distr']=dist
            obj = models.dipo.objects.filter(**url)
            if obj.exists():
                value = f'<table><thead> <th ">Dipo Id</th><th>Pri-Com-Name</th><th>Ope-Com_Name</th><th>Depot Man Name</th><th>Depot Man-no</th><th>Depot-mob-no</th><th>Depo-Tel-no</th><th>state</th><th>district</th><th>Address</th><th>gst-no</th><th colspan="3" align="centre">Action&nbsp;Here</th></thead><tbody>'
                for x in obj:
                    value += f'<tr>'
                    value += f'<td>{x.diop_id}</td>'
                    value += f'<td>{x.pri_name}</td>'
                    value += f'<td>{x.ope_name}</td>'
                    value += f'<td>{x.man_name}</td>'
                    value += f'<td>{x.man_cont}</td>'
                    value += f'<td>{x.depo_cont}</td>'
                    value += f'<td>{x.depo_tel}</td>'
                    value += f'<td>{x.state}</td>'
                    value += f'<td>{x.distr}</td>'
                    value += f'<td>{x.addr}</td>'
                    value += f'<td>{x.gst}</td>'
                    value += f'<td><a href="/Depot_update/{x.id}/" ><i class="fa-solid fa-file-pen"></i></a></td>'
                    value += f'<td><a onclick="del(\'/deport_delete/{x.id}/\')" ><i class="fa-solid fa-trash"></i></a></td>'
                    value += f'</tr>'
                value += '</tbody></table>'
                response ={
                    'success' : True,
                    'value' : value
                }
                return http.JsonResponse(response, safe=False)
            else:
                response ={
                    'success' : False,
                    'message' : 'No Record Available'
                }
                return http.JsonResponse(response, safe=False)
    else: 
        return render(request, 'Depot_Service.html', {'data':data,'dname':dname,'aman':aman})
def Depot_update(request,iid):
    aman={
        'title' : 'PCPL | Deport Page',
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    dname = models.dipo.objects.all()
    s_user = request.s_user
    print(s_user)
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    elif s_user == 'Admin':
        aman['page_name'] = 'base.html'
        diponame = User.objects.filter(username=request.user)
        for x in diponame:
            aman['diponame'] = x.diponame
    elif s_user == True:
        aman['page_name'] = 'base.html'
    else:
        aman['page_name'] = 'base.html'
    dname = models.dipo.objects.all()
    update= models.dipo.objects.get(id=iid)
    if request.method=='POST':
        update.diop_id=request.POST['did']
        update.pri_name=request.POST['pre-com-name']
        update.ope_name=request.POST['ope-com-name']
        update.man_name=request.POST['dmanager-name']
        update.man_cont=request.POST['dmanager-no']
        update.depo_cont=request.POST['depot-no']
        update.depo_tel=request.POST['depot-tno']
        update.state=request.POST['state']
        update.distr=request.POST['district']
        update.addr=request.POST['address']
        update.gst=request.POST['gst-no']
        update.save()
        messages.success(request,'Record Sucessfully updated')
        return redirect('Depot')
    else:
        data = models.state1.objects.get(stat=update.state)
        data= data.distr.split(',')        
        return render(request,'Depot_update.html',{"u":update,'data':data,'dname':dname,'aman':aman})
def deport_delete(request,iid):
    models.dipo.objects.filter(id=iid).delete()
    messages.success(request,'Record Deleted ')
    return redirect("Depot_Service")




# Disturubtor 

# def Distributor_details(request):
    # data={
    #     'title' : 'PCPL | Deport Page'
    # }
    # dname = models.dipo.objects.all()
    # s_user = request.s_user
    # if s_user == 'User':
    #     messages.info(request,'You have not permission for this page')
    #     return redirect('index')
    # else:
    #     data['page_name'] = 'base.html'
    # dname = models.dipo.objects.all()
    # # print(request.method)
    # if request.method=='POST':
    #     dis_id=request.POST['dis_id']
    #     dist_name=request.POST['dist_name']
    #     depot_name=request.POST['depot_name']
    #     cont_no=request.POST['cont_no']
    #     landline_no=request.POST['landline_no']
    #     lab_expense=request.POST['lab_expense']
    #     state=request.POST['state']
    #     district=request.POST['district']
    #     address=request.POST['address']
    #     pin_code=request.POST['pin_code']
    #     gst_no=request.POST['gst_no']
    #     # Check if dipo_id was manually edited
    #     existing_dist_id = request.POST.get('dist_id')
        
    #     if existing_dist_id:
    #         dist_id = existing_dist_id
    #     else:
    #         # Auto-generate dipo_id
    #         rs = models.automatic1.objects.get(id=1).dist_id
    #         rs = int(rs) + 1
    #         if rs < 10:
    #             dist_id = 'DS00' + str(rs)
    #         elif rs < 100:
    #             dist_id = 'DS0' + str(rs)
    #         else:
    #             dist_id = 'DS' + str(rs)
    #         if dist_id == dist_id:
    #         # Save to the automatic1 table
    #             models.automatic1.objects.filter(id=1).update(dist_id=rs)
        
    #     obj=models.distri_details(dist_id=dis_id,dist_name=dist_name,dipo_name=depot_name,cont_no=cont_no,landline_no=landline_no,le_ex=lab_expense,state=state,district=district,addrs=address,pin=pin_code,gst_no=gst_no)
    #     obj.save()
        
    #     messages.success(request,'sucessfully inserted')
    #     return redirect(reverse('Distributor_details'))
    #     # return render(request,'Distributor_details.html')
    # else:
    #     rs=models.automatic1.objects.get(id=1).dist_id
    #     rs=int(rs)+1
    #     if rs<10:
    #         dist_id='DS00'+str(rs)
    #     elif rs<100:
    #         dist_id='DS0'+str(rs)
    #     else:
    #         dist_id='DS'+str(rs)
    #     return render(request,'Distributor_details.html',{'dist_id':dist_id ,'dname':dname,'data':data})


import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.conf import settings

def generate_qr_code(data):
    """
    Generate a QR code and return it as an in-memory file.
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")

    # Save the image to an in-memory file
    img_io = BytesIO()
    img.save(img_io, format="PNG")  # Save as PNG
    return ContentFile(img_io.getvalue(), name=f"qr_{data}.png")  # Return as Django file object


def send_email_with_qr(distributor, emailID):
    """
    Sends an email with the distributor's details and attached QR code.
    """
    subject = f"Distributor Details - {distributor.dist_name}"
    body = f"""
    Distributor Details:
    --------------------
    Distributor ID: {distributor.dist_id}
    Name: {distributor.dist_name}
    Depot Name: {distributor.dipo_name}
    Contact Number: {distributor.cont_no}
    Landline: {distributor.landline_no}
    Lab Expense: {distributor.le_ex}
    State: {distributor.state}
    City: {distributor.city}
    Address: {distributor.addrs}
    PIN Code: {distributor.pin}
    GST Number: {distributor.gst_no}

    QR Code is attached to this email.
    """

    # Generate QR Code for distributor ID
    qr_code_file = generate_qr_code(distributor.dist_id)

    # Prepare email
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,  # Configure in settings.py
        to=[emailID],  # Change this to the recipient's email
    )

    # Attach QR Code
    email.attach(qr_code_file.name, qr_code_file.read(), "image/png")

    # Send email
    email.send()
    print("✅ Email with QR code sent successfully!")


def Distributor_details(request):
    dname = models.dipo.objects.all()
    aman={
        'title' : 'PCPL | Deport Page',
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    dname = models.dipo.objects.all()
    s_user = request.s_user
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    elif s_user == 'Admin':
        aman['page_name'] = 'base.html'
        diponame = User.objects.filter(username=request.user)
        for x in diponame:
            aman['diponame'] = x.diponame
    else:
        aman['page_name'] = 'base.html'
    if request.method=='POST':
        dis_id=request.POST['dis_id']
        dist_name=request.POST['dist_name']
        depot_name=request.POST['depot_name']
        cont_no=request.POST['cont_no']
        landline_no=request.POST['landline_no']
        emailid=request.POST['emailID']
        lab_expense=request.POST['lab_expense']
        state=request.POST['state']
        city=request.POST['city']
        address=request.POST['address']
        pin_code=request.POST['pin_code']
        gst_no=request.POST['gst_no']
        existing_dist_id = request.POST.get('dist_id')
        
        if existing_dist_id:
            dist_id = existing_dist_id
        else:
            rs = models.automatic1.objects.get(id=1).dist_id
            rs = int(rs) + 1
            if rs < 10:
                dist_id = 'DS00' + str(rs)
            elif rs < 100:
                dist_id = 'DS0' + str(rs)
            else:
                dist_id = 'DS' + str(rs)
            if dist_id == dis_id:
                models.automatic1.objects.filter(id=1).update(dist_id=rs)
        obj=models.distri_details(dist_id=dis_id,dist_name=dist_name,dipo_name=depot_name,cont_no=cont_no,landline_no=landline_no,le_ex=lab_expense,state=state,city=city,addrs=address,pin=pin_code,gst_no=gst_no,qrCode=generate_qr_code(dis_id))
        send_email_with_qr(obj, emailid)
        obj.save()
        messages.success(request, 'Successfully inserted')
        return redirect(reverse('Distributor_details'))
    
    
    else:
        rs = models.automatic1.objects.get(id=1).dist_id
        rs = int(rs) + 1
        if rs < 10:
            dist_id = 'DS00' + str(rs)
        elif rs < 100:
            dist_id = 'DS0' + str(rs)
        else:
            dist_id = 'DS' + str(rs)

        return render(request,'Distributor_details.html',{'dist_id':dist_id ,'dname':dname,'aman':aman})

def dis(request):
    depot_name = request.session.get('depot_name')
    data= {
        'depotname' : models.distri_details.objects.filter(dipo_name=depot_name)
        }
    dname = models.dipo.objects.all()
    
    aman={
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    dname = models.dipo.objects.all()
    s_user = request.s_user
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    elif s_user == 'Admin':
        aman['page_name'] = 'base.html'
        diponame = User.objects.filter(username=request.user)
        for x in diponame:
            aman['diponame'] = x.diponame
    else:
        aman['page_name'] = 'base.html'
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'POST':
            srcid= request.POST.get('srcid')
            deponame = request.POST.get('deponame')
            srcdisname = request.POST.get('srcdisname')
            srcdis = request.POST.get('srcdis')
            url={}
            if deponame != None:
                url['dipo_name'] = deponame
            if srcid!=None:
                url['dist_id']=srcid
            if srcdisname!=None:
                url['dist_name']=srcdisname
            if srcdis!=None:
                url['city']=srcdis
            # data = models.distri_details.objects.all() 
            obj = models.distri_details.objects.filter(**url)
            if obj.exists():   
                value=f' <table class="dis_table"><thead><th>ID</th><th>Dist-ID</th><th>Distributor Name</th><th>Depot Name</th><th>contact no</th><th>Landline-No</th><th>Labour Exp</th><th>State</th><th>city</th><th>Address</th><th>Pin Code</th><th>gst-no</th><th colspan="3" align="centre">Action&nbsp;Here</th></thead><tbody>'
                for x in obj:
                    value+=f'<tr>'
                    value+=f'<td>{x.id}</td>'
                    value+=f'<td>{x.dist_id}</td>'
                    value+=f'<td>{x.dist_name}</td>'
                    value+=f'<td>{x.dipo_name}</td>'
                    value+=f'<td>{x.cont_no}</td>'
                    value+=f'<td>{x.landline_no}</td>'
                    value+=f'<td>{x.le_ex}</td>'
                    value+=f'<td>{x.state}</td>'
                    value+=f'<td>{x.city}</td>'
                    value+=f'<td>{x.addrs}</td>'
                    value+=f'<td>{x.pin}</td>'
                    value+=f'<td>{x.gst_no}</td>'
                    value += f'<td  class="leave"><a href="/distributor_update/{x.id}/" ><i class="fa-solid fa-file-pen"></i></a></td>'
                    value += f'<td  class="leave"><a onclick="del(\'/distributor_delete/{x.id}/\')" ><i class="fa-solid fa-trash" style="color:red;cursor:pointer;"></i></a></td>'
                    
                    value+=f'</tr>'
                value+= '</tbody></table>'
                response ={
                    'success':True,
                    'value' :value
                }
                return http.JsonResponse(response, safe=False)
            else:
                response ={
                    'success' :False,
                    'message':'NO records Found'
                }
                return http.JsonResponse(response, safe=False)
    else:
        return render(request, 'Distributor.html', {'data':data,'dname':dname,'aman':aman})

def distributor_update(request,iid):
    dname = models.dipo.objects.all()
    aman={
        'title' : 'PCPL | Deport Page',
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    dname = models.dipo.objects.all()
    s_user = request.s_user
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    else:
        aman['page_name'] = 'base.html'
    update= models.distri_details.objects.get(id=iid)
    if request.method=='POST':
        update.dist_id=request.POST['dis_id']
        update.dist_name=request.POST['dist_name']
        update.dipo_name=request.POST['depot_name']
        update.cont_no=request.POST['cont_no']
        update.landline_no=request.POST['landline_no']
        update.le_ex=request.POST['lab_expense']
        update.state=request.POST['state']
        update.city=request.POST['district']
        update.addrs=request.POST['address']
        update.pin=request.POST['pin_code']
        update.gst_no=request.POST['gst_no']
        update.save()
        messages.success(request,'Record Sucessfully updated')
        return redirect('Distributor_details')
    else:
        # data = models.state1.objects.get(stat=update.state)
        # data= data.distr.split(',')        
        return render(request,'distributor_update.html',{"u":update, 'dname':dname,'aman':aman})
def distributor_delete(request,iid):
    messages.success(request,'Record Deleted ')
    models.distri_details.objects.filter(id=iid).delete()
    return redirect('Distributor')


# transporter

def transpoter_entry(request):
    dname = models.dipo.objects.all()
    depot_name = request.session.get('depot_name')
    
    state = models.state1.objects.values('stat').order_by('stat')
    aman={
        'title' : 'PCPL | Deport Page',
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user),
        'vehicle' : models.plvehicle.objects.filter(dipo_id=depot_name)
    }
    dname = models.dipo.objects.all()
    s_user = request.s_user
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    elif s_user == 'Admin':
        aman['page_name'] = 'base.html'
        diponame = User.objects.filter(username=request.user)
        for x in diponame:
            aman['diponame'] = x.diponame
    else:
        aman['page_name'] = 'base.html'
    if request.method=='POST':
        trans_id=request.POST['trans_id']
        trans_name=request.POST['trans_name']
        cont_no=request.POST['mob_no']
        land_no=request.POST['landline_no']
        prop_name=request.POST['pro_name']
        addrs=request.POST['add']
        state=request.POST['state']
        distr=request.POST['district']
        bnk_name=request.POST['bank_name']
        acchold_name=request.POST['ac_holder_name']
        acc_no=request.POST['conf_acc_no']
        ifsc=request.POST['ifsc']
        veh_ty=request.POST['vehicle_type']
        depo_id=request.POST['depo_id']
        traport_details=models.transporter_details(trans_id=trans_id,trans_name=trans_name,cont_no=cont_no,land_no=land_no,prop_name=prop_name,addrs=addrs,state=state,distr=distr,bnk_name=bnk_name,acchold_name=acchold_name,acc_no=acc_no,ifsc=ifsc,veh_ty=veh_ty,dipo_id=depo_id)
        traport_details.save()
        if traport_details.pk is not None:
            if '0' in request.POST['trans_id']:
                trans_id=trans_id[trans_id.rfind('0')+1:]
            else:
                trans_id=trans_id[2:]
            models.automatic1.objects.all().update(trans_id=trans_id)
            messages.success(request,"Transporter Details Added Successfully!")
        else:
            messages.error(request,"Please try again later!")
        return redirect('transpoter_details')
    else:
        rs=int(models.automatic1.objects.all().get().trans_id)+1
        trans_id=''
        if(rs<10):
            trans_id='TR00'+str(rs)
        elif(rs<100):
            trans_id='TR0'+str(rs)
        elif(rs<1000):
            trans_id='TR'+str(rs)
        else:
            trans_id="End Auto"
            messages.error(request,"Auto Increment is End")
    return render(request,'transpoter_entry.html', {'trans_id':trans_id,  'state':state, 'dname':dname,'aman':aman})

def transpoter_details(request):
    depot_name = request.session.get('depot_name')
    dname = models.dipo.objects.all()
    data = {
        'distr':models.transporter_details.objects.values('distr').distinct(),
        'state':models.transporter_details.objects.values('state').distinct(),
        'trans_name':models.transporter_details.objects.values('trans_name').distinct(),
        'veh_ty':models.transporter_details.objects.values('veh_ty').distinct(),
        'depotname' : models.transporter_details.objects.filter(dipo_id=depot_name),
        'username' : request.user,
        's_user' : request.s_user
    }
    
    aman={
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    dname = models.dipo.objects.all()
    s_user = request.s_user
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    elif s_user == 'Admin':
        aman['page_name'] = 'base.html'
        diponame = User.objects.filter(username=request.user)
        for x in diponame:
            aman['diponame'] = x.diponame
    else:
        aman['page_name'] = 'base.html'
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method=="POST":
            trans_name = request.POST['trans_name']
            distr = request.POST['distr']
            state = request.POST['state']
            deponame = request.POST.get('deponame')
            veh_ty = request.POST['veh_ty']
            conditions = {}
            if deponame != None :
                conditions['dipo_id'] = deponame
            if trans_name != "":
                conditions['trans_name']=trans_name
            if distr != "":
                conditions['distr']=distr
            if state != "":
                conditions['state']=state
            if veh_ty != "":
                conditions['veh_ty']=veh_ty
            if conditions:
                obj = models.transporter_details.objects.filter(**conditions)
                if obj.exists():
                    value = f'<table><thead><tr><th>SL</th><th>Transported ID</th><th>Transported Name</th><th>Mobile No.</th><th>Landline No</th><th>Proprietor Name</th><th>State</th><th>District</th><th>Address</th><th>Vehicle Type</th><th>Bank Name</th><th>Account Holder Name</th><th>Account Number</th><th>IFSC Code</th><th colspan="2" align="centre">Action&nbsp;Here</th></tr></thead><tbody>'
                    for x in obj:
                        value += f'<tr>'
                        value += f'<td>{ x.id }</td>'
                        value += f'<td>{ x.trans_id }</td>'
                        value += f'<td>{ x.trans_name}</td>'
                        value += f'<td>{ x.cont_no }</td>'
                        value += f'<td>{ x.land_no }</td>'
                        value += f'<td>{ x.prop_name }</td>'
                        value += f'<td>{ x.state }</td>'
                        value += f'<td>{ x.distr }</td>'
                        value += f'<td>{ x.addrs }</td>'
                        value += f'<td>{ x.veh_ty }</td>'
                        value += f'<td>{ x.bnk_name}</td>'
                        value += f'<td>{ x.acchold_name }</td>'
                        value += f'<td>{ x.acc_no }</td>'
                        value += f'<td>{ x.ifsc }</td>'
                        value += f'<td><a href="/transpoter_details_update/{x.id}/" ><i class="fa-solid fa-file-pen"></i></a></td>'
                        value += f'<td><a onclick="del(\'/transpoter_details_delete/{x.id}/\')" ><i class="fa-solid fa-trash" style="color:red;cursor:pointer;"></i></a></td>'
                        value += f'</tr>'
                    value+='</tbody></table>'
                    response ={
                        'success':True,
                        'value':value
                    }
                    return http.JsonResponse(response, safe=False)
                else:
                    response ={
                        'success':False,
                        'messages':'No records Found'
                    }
                    return http.JsonResponse(response, safe=False)
            else:
                response ={
                    'success':False,
                    'messages':'Please enter atleast one field'
                    }
                return http.JsonResponse(response, safe=False)
    else:
        return render(request, 'transpoter_details.html', {'data':data, 'dname':dname,'aman':aman})
def transpoter_details_update(request, iid):
    depot_name = request.session.get('depot_name')
    aman={
        'title' : 'PCPL | Deport Page',
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user),
        'vehicle' : models.plvehicle.objects.filter(dipo_id=depot_name)
    }
    dname = models.dipo.objects.all()
    s_user = request.s_user
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    elif s_user == 'Admin':
        aman['page_name'] = 'base.html'
        diponame = User.objects.filter(username=request.user)
        for x in diponame:
            aman['diponame'] = x.diponame
    else:
        aman['page_name'] = 'base.html'
    update = models.transporter_details.objects.get(id=iid)
    
   
    if request.method=='POST':
        update.trans_name=request.POST['trans_name']
        update.cont_no=request.POST['mob_no']
        update.land_no=request.POST['landline_no']
        update.prop_name=request.POST['pro_name']
        update.state=request.POST['state']
        update.distr=request.POST['district']
        update.addrs=request.POST['add']
        update.veh_ty=request.POST['vehicle_type']
        update.bnk_name=request.POST['bank_name']
        update.acchold_name=request.POST['ac_holder_name']
        update.acc_no=request.POST['account_no']
        update.ifsc=request.POST['ifsc']
        update.save()
        messages.success(request, 'Record Updated Enjoy !')
        return redirect('transpoter_details')
    else:
        data = models.state1.objects.get(stat=update.state)
        data= data.distr.split(',')               
        return render(request, 'transpoter_details_update.html',{'u':update ,'data':data,'dname':dname,'aman':aman})
def transpoter_details_delete(request, iid):
    models.transporter_details.objects.get(id=iid).delete()
    
    messages.success(request, 'Record Deleted Enjoy !')
    return redirect('transpoter_details')



# vehicle

    
def vehicle_entry(request):
    depot_name = request.session.get('depot_name')
    dname = models.dipo.objects.all()
    query=''
    data ={
        'vtype': models.plvehicle.objects.values('vtype').distinct(),
        'lt':models.plvehicle.objects.values('lt').distinct(),
        'cname':models.plvehicle.objects.values('cname').distinct(),
        'vtype' : models.plvehicle.objects.filter(dipo_id=depot_name).values('vtype').distinct(),
        'ltype' : models.plvehicle.objects.filter(dipo_id=depot_name).values('lt').distinct(),
        'city' : models.plvehicle.objects.filter(dipo_id=depot_name).values('cname').distinct(),
    }
    aman={
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    dname = models.dipo.objects.all()
    s_user = request.s_user
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    elif s_user == 'Admin':
        aman['page_name'] = 'base.html'
        diponame = User.objects.filter(username=request.user)
        for x in diponame:
            aman['diponame'] = x.diponame
    else:
        aman['page_name'] = 'base.html'
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method=="POST":
            vh_tpe = request.POST['vh_tpe']
            lod_typ = request.POST['lod_typ']
            cty_name = request.POST['cty_name']
            deponame = request.POST.get('deponame')

            conditions = {}
            if deponame != None :
                conditions['dipo_id'] = deponame
            if vh_tpe !='':
                conditions['vtype']=vh_tpe
            if lod_typ !='':
                conditions['lt']=lod_typ
            if cty_name !='':
                conditions['cname']=cty_name
            obj=models.plvehicle.objects.filter(**conditions).order_by('-id') 
            if obj.exists():
                value = f'<table><thead><th>Load Type</th><th>Freight</th>  <th>City Name</th><th>Vehicle Type</th><th colspan="3" align="centre">Action&nbsp;Here</th></thead><tbody>'
                for x in obj:
                    value += f'<tr>'
                    value += f'<td align="center">{ x.lt }</td>'
                    value += f'<td align="center">{ x.vprise}</td>'
                    value += f'<td align="center">{ x.cname }</td>'
                    value += f'<td align="center">{ x.vtype }</td>'
                    value += f'<td><a href="/vehicle_details_update/{x.id}/" ><i class="fa-solid fa-file-pen"></i></a></td>'
                    value += f'<td><a onclick="del(\'/vehicle_details_delete/{x.id}/\')" ><i class="fa-solid fa-trash" style="color:red;cursor:pointer;"></i></a></td>'
                    value += f'</tr>'
                value += '</tbody></table>'
                response ={
                    'success':True,
                    'value':value
                }
                return http.JsonResponse(response, safe=False)
            else:
                response ={
                    'success':False,
                    'messages':'No Data Found'
                }
                return http.JsonResponse(response, safe=False)
    else:
        return render(request,'vehicle_service.html',{'data':data, 'value':query , 'dname':dname,'aman':aman})

    
def vehicle_details(request):
    
    dname = models.dipo.objects.all()
    depot_name = request.session.get('depot_name')
    aman={
        'title' : 'PCPL | Deport Page',
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    dname = models.dipo.objects.all()
    s_user = request.s_user
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    elif s_user == 'Admin':
        aman['page_name'] = 'base.html'
        diponame = User.objects.filter(username=request.user)
        for x in diponame:
            aman['diponame'] = x.diponame
    else:
        aman['page_name'] = 'base.html'
    if request.method == 'POST':
        load_type=request.POST['load-type']
        freight=request.POST['freight']
        city_name=request.POST['cityName']
        vehicle_type=request.POST['vehicleType']
        depo_id=request.POST['depo_id']
        ventry=models.plvehicle(lt=load_type,dipo_id=depo_id,vprise=freight,cname=city_name,vtype=vehicle_type)
        ventry.save()
        messages.success(request,"Vehicle Details Added Successfully")
        return redirect('vehicle_details')
    else:
        city_name = models.distri_details.objects.filter(dipo_name=depot_name).values('city').distinct()
        return render(request,'vehicle_details.html',{'city_name':city_name, 'dname':dname,'aman':aman})

    
def vehicle_details_update(request, iid):
    dname = models.dipo.objects.all()
    data = models.plvehicle.objects.get(id=iid)
    aman={
        'title' : 'PCPL | Deport Page',
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    dname = models.dipo.objects.all()
    s_user = request.s_user
    if s_user == 'User':
        aman['page_name'] = 'base_user.html'
    else:
        aman['page_name'] = 'base.html'
    if request.method=='POST':
        data.lt=request.POST['load_type']
        data.vprise=request.POST['freight']
        data.vtype=request.POST['vtype']
        data.cname=request.POST['city']
        data.save()
        messages.success(request, 'Record Updated Enjoy !')
        return redirect('vehicle_service')
    else:
        city_name = models.distri_details.objects.values_list('city',flat=True).distinct()
        return render(request, 'vehicle_details_update.html',{'a':data, 'city_name':city_name,'dname':dname,'aman':aman})
    
def vehicle_details_delete(request, iid):
    data = models.plvehicle.objects.get(id=iid)
    data.delete()
    messages.success(request, 'Record Deleted Enjoy !')
    return redirect('vehicle_service')



# Driver Details
def driver_entry(request):
    aman={
        'title' : 'PCPL | Deport Page',
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    dname = models.dipo.objects.all()
    s_user = request.s_user
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    elif s_user == 'Admin':
        aman['page_name'] = 'base.html'
        diponame = User.objects.filter(username=request.user)
        for x in diponame:
            aman['diponame'] = x.diponame
    else:
        aman['page_name'] = 'base.html'
    dname = models.dipo.objects.all()
    if request.method == 'POST':
        picture = request.FILES.get('profile_pic')
        drv_id=request.POST['drv_id']
        dr_name=request.POST['drv-name']
        dr_contact=request.POST['drv-contact']
        dr_lisen_no=request.POST['drv-lisen-no']
        drv_sal=request.POST['drv_sal']
        depo_id=request.POST['depo_id']
        drv_addhar=request.POST['drv_addhar']
        drventry=models.drv_details(drv_pic=picture,dipo_id=depo_id,drv_id=drv_id,drv_nme=dr_name,drv_no=dr_contact,drv_lis_no=dr_lisen_no,drv_sal=drv_sal,drv_addhar=drv_addhar)
        drventry.save()
        models.automatic1.objects.filter(id=1).update(drv_id=int(models.automatic1.objects.get(id=1).drv_id)+1)
        messages.success(request,"Driver Details Added Successfully")
        return redirect('driver_entry')
    else:
        rs=models.automatic1.objects.get(id=1).drv_id
        rs=int(rs)+1
        
        if rs<10:
            drv_id='DR00'+str(rs)
        elif rs<100:
            drv_id='DR0'+str(rs)
        else:
            drv_id='DR'+str(rs)
        return render(request,'Driver-entry.html', {'drv_id':drv_id, 'dname':dname,'aman':aman})
def driver_details(request):
    depot_name = request.session.get('depot_name')
    dname = models.dipo.objects.all()
    query=''
    data = {
       'drv_id': models.drv_details.objects.values('drv_id').distinct(),
       'drv_nme': models.drv_details.objects.values('drv_nme').distinct(),
       'drv_no': models.drv_details.objects.values('drv_no').distinct(),
       'depotname' : models.drv_details.objects.filter(dipo_id=depot_name),
       
    }
    aman={
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    dname = models.dipo.objects.all()
    s_user = request.s_user
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    elif s_user == 'Admin':
        aman['page_name'] = 'base.html'
        diponame = User.objects.filter(username=request.user)
        for x in diponame:
            aman['diponame'] = x.diponame
    else:
        aman['page_name'] = 'base.html'
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method=="POST":
            drv_id = request.POST['drv_id']
            drv_nme = request.POST['drv_nme']
            drv_no = request.POST['drv_no']
            deponame = request.POST.get('deponame')

            conditions = {}
            if deponame != None :
                conditions['dipo_id'] = deponame
            if drv_id !='':
                conditions['drv_id']=drv_id
            if drv_nme !='':
                conditions['drv_nme']=drv_nme
            if drv_no !='':
                conditions['drv_no']=drv_no
            obj=models.drv_details.objects.filter(**conditions).order_by('-id') 
            if obj.exists():
                value =f'<table><thead>  <th>Driver PIC</th>  <th>Driver ID</th>  <th>Driver Name</th>  <th>Contact No.</th>  <th>Driving License No.</th><th>Driving Salary</th><th>Driving Aadhar</th><th colspan="3" align="centre">Action&nbsp;Here</th></thead><tbody>'
                for x in obj:
                    value += f'<tr>'
                    value += '<td align="center">'
                    if x.drv_pic:
                        value += f'<img src="{x.drv_pic.url}" alt="" style="width: 12rem; height: 8rem;">'
                    value += '</td>'
                    value += f'<td align="center">{ x.drv_id }</td>'
                    value += f'<td align="center">{ x.drv_nme}</td>'
                    value += f'<td align="center">{ x.drv_no }</td>'
                    value += f'<td align="center">{ x.drv_lis_no }</td>'
                    value += f'<td align="center">{ x.drv_sal }</td>'
                    value += f'<td align="center">{ x.drv_addhar }</td>'
                    value += f'<td><a href="/driver_details_update/{x.id}/" ><i class="fa-solid fa-file-pen"></i></a></td>'
                    value += f'<td><a onclick="del(\'/driver_details_delete/{x.id}/\')" ><i class="fa-solid fa-trash" style="color:red;cursor:pointer;"></i></a></td>'
                    value += f'</tr>'
                value += '</tbody></table>'
                response ={
                    'success':True,
                    'value':value
                }
                return http.JsonResponse(response, safe=False)
            else:
                response ={
                    'success':False,
                    'messages':'No Data Found'
                }
                return http.JsonResponse(response, safe=False)   
    else:
        return render(request,'Driver-details.html',{'data':data, 'value':query , 'dname':dname,'aman':aman})

def driver_details_update(request, iid):
    dname = models.dipo.objects.all()
    aman={
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    dname = models.dipo.objects.all()
    s_user = request.s_user
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    else:
        aman['page_name'] = 'base.html'
    update = models.drv_details.objects.get(id=iid)
    if request.method=='POST':
        if request.FILES.get('profile_pic'):
            update.drv_pic=request.FILES.get('profile_pic')
        update.drv_id=request.POST['drv_id']
        update.drv_nme=request.POST['drv-name']
        update.drv_no=request.POST['drv-contact']
        update.drv_lis_no=request.POST['drv-lisen-no']
        update.drv_sal=request.POST['drv_sal']
        update.drv_addhar=request.POST['drv_addhar']
        update.save()
        messages.success(request, 'Record Updated Enjoy !')
        return redirect('driver_details')
    else:
        return render(request, 'Driver_Deatls_update.html',{'u':update, 'dname':dname,'aman':aman})
    
def driver_details_delete(request, iid):
    data = models.drv_details.objects.get(id=iid)
    data.delete()
    messages.success(request, 'Record Deleted Enjoy !')
    return redirect('driver_details')

# Driver Payment


def driver_payment_entry(request):
    dname = models.dipo.objects.all()
    aman={
        'title' : 'PCPL | Deport Page',
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    dname = models.dipo.objects.all()
    s_user = request.s_user
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    elif s_user == 'Admin':
        aman['page_name'] = 'base.html'
        diponame = User.objects.filter(username=request.user)
        for x in diponame:
            aman['diponame'] = x.diponame
    else:
        aman['page_name'] = 'base.html'
    if request.method == 'POST':
        drv_name=request.POST['drv_nm']
        dr_month=request.POST['sal_month']
        dr_sal_amount=request.POST['dr_sal_amount']
        pay_mode=request.POST['pay_mode']
        pay_bal_amt=request.POST['pay_bal_amt']
        dr_sal_date=request.POST['pay_date']
        depo_id=request.POST['depo_id']
        drpayventry=models.drv_pay(drv_nm=drv_name,dipo_id=depo_id,sal_mo=dr_month,pay_amt=dr_sal_amount,pay_mode=pay_mode,pay_bal_amt=pay_bal_amt,pay_date=dr_sal_date)
        drpayventry.save()
        messages.success(request,"Driver Payment Details Added Successfully")
        return redirect('driver_payment_entry')
    else:
        data = models.drv_details.objects.values('drv_nme')
        return render(request,'driver_payment_entry.html',{'data':data, 'aman':aman,'dname':dname})

def driver_payment(request):
    depot_name = request.session.get('depot_name')
    dname = models.dipo.objects.all()
    query=''
    data = {
        'drv_nm': models.drv_pay.objects.values('drv_nm').distinct(),
        'depotname' : models.drv_pay.objects.filter(dipo_id=depot_name),
        
    }
    aman={
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    dname = models.dipo.objects.all()
    s_user = request.s_user
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    elif s_user == 'Admin':
        aman['page_name'] = 'base.html'
        diponame = User.objects.filter(username=request.user)
        for x in diponame:
            aman['diponame'] = x.diponame
    else:
        aman['page_name'] = 'base.html'
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method=="POST":
            drv_nm = request.POST['drv_nm']
            f_date = request.POST['f_date']
            t_date = request.POST['t_date']
            deponame = request.POST.get('deponame')
            conditions = {}
            if deponame != None :
                conditions['dipo_id'] = deponame
            if drv_nm !='':
                conditions['drv_nm']=drv_nm
            if f_date and  t_date!='':
                 conditions['pay_date__range']=[f_date , t_date]
            
            obj=models.drv_pay.objects.filter(**conditions).order_by('-id') 
            if obj.exists():
                value = f'<table><thead><th>Sl.No.</th><th>Driver Name</th><th>Salary Month</th><th>Amount</th><th>Payment Mode</th><th>Balence Amount</th><th>Payment Date</th><th colspan="3" align="centre">Action&nbsp;Here</th></thead><tbody>'
                for x in obj:
                    value += f'<tr>'
                    value += f'<td align="center">{ x.id }</td>'
                    value += f'<td align="center">{ x.drv_nm }</td>'
                    value += f'<td align="center">{ x.sal_mo }</td>'
                    value += f'<td align="center">{ x.pay_amt }</td>'
                    value += f'<td align="center">{ x.pay_mode }</td>'
                    value += f'<td align="center">{ x.pay_bal_amt }</td>'
                    value += f'<td align="center">{ x.pay_date }</td>'
                    value += f'<td><a href="/driver_payment/{x.id}/" ><i class="fa-solid fa-file-pen"></i></a></td>'
                    value += f'<td><a onclick="del(\'/driver_payment_delete/{x.id}/\')" ><i class="fa-solid fa-trash" style="color:red;cursor:pointer;"></i></a></td>'
                value += f'</tr>'
                value +='</tbody></table>'
                response ={
                    'success':True,
                    'value':value
                    
                }
                return http.JsonResponse(response, safe=False)
            else:
                response ={
                    'success':False,
                    'message':'No Data Found'
                }
                return http.JsonResponse(response, safe=False)           
    else:
        return render(request,'driver_payment.html',{'data':data, 'value':query,'aman':aman, 'dname':dname})

    
def driver_payment_update(request, iid):
    dname = models.dipo.objects.all()
        
    aman={
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    
    dname = models.dipo.objects.all()
    s_user = request.s_user
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    else:
        aman['page_name'] = 'base.html'
    data = models.drv_pay.objects.get(id=iid)
    if request.method=='POST':
        data.drv_nm=request.POST['drv_nm']
        data.sal_mo=request.POST['sal_month']
        data.pay_amt=request.POST['dr_sal_amount']
        data.pay_mode=request.POST['pay_mode']
        data.pay_bal_amt=request.POST['pay_bal_amt']
        data.pay_date=request.POST['pay_date']
        data.save()
        messages.success(request, 'Record Updated Enjoy !')
        return redirect('driver_payment')
    else:
        d_name = models.drv_details.objects.values('drv_nme')
        return render(request, 'driver_pay_update.html',{'data':data,'d_name':d_name, 'dname':dname,'aman':aman})
    
def driver_payment_delete(request, iid):
    data = models.drv_pay.objects.get(id=iid)
    data.delete()
    messages.success(request, 'Record Deleted Enjoy !')
    return redirect('driver_payment')

# Azax for State

def ajaxCall(request):
    cond=request.GET['cond']
    request_send=''
    if(cond=="state"):
            if request.GET['uname'].strip() == '':
                request_send='<option value="" selected disabled>---Select Any District---</option>'
            else:
                request_send=models.state1.objects.filter(stat=request.GET['uname'].strip()).values_list('distr',flat=True)
                if request_send.exists():
                    option='<option value="" selected disabled>---Select Any District---</option>'
                    for a in request_send:
                        a=a.split(',')
                        for b in a:
                            option=option+'<option value="'+b+'">'+b+'</option>'
                    request_send=option
                else:
                    request_send=None
    return JsonResponse(request_send,safe=False)

# vehicle Expense

def vehicle_expense(request):
    aman={
        'title' : 'PCPL | Deport Page',
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    dname = models.dipo.objects.all()
    s_user = request.s_user
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    elif s_user == 'Admin':
        aman['page_name'] = 'base.html'
        diponame = User.objects.filter(username=request.user)
        for x in diponame:
            aman['diponame'] = x.diponame
    else:
        aman['page_name'] = 'base.html'
    dname = models.dipo.objects.all()
    if request.method=='POST':
        veh_no=request.POST['veh_no']
        fuel_no=request.POST['fuel_no']
        fuel_qty=request.POST['fuel_qty']
        f_qty=request.POST['f_qty']
        fuel_amt=request.POST['fuel_amt']
        toll_amt=request.POST['toll_amt']
        misc_amt=request.POST['misc_amt']
        exp_date=request.POST['exp_date']
        depo_id=request.POST['depo_id']
        total_amt=request.POST['total_amt']
        obj=models.veh_exp(veh_no=veh_no,dipo_id=depo_id,fuel_no=fuel_no,fuel_amt=fuel_amt,fuel_qty=fuel_qty+f_qty,toll_amt=toll_amt,misc_amt=misc_amt,exp_date=exp_date,total_amt=total_amt)
        messages.success(request,'sucessfully inserted')
        obj.save()
        return render(request,'vehicle_expense.html',{'dname':dname,'aman':aman})
    else:
         return render(request,'vehicle_expense.html',{'dname':dname,'aman':aman})
     
def expense_update(request,iid):
    aman={
        'title' : 'PCPL | Deport Page',
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    dname = models.dipo.objects.all()
    s_user = request.s_user
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    else:
        aman['page_name'] = 'base.html'
    dname = models.dipo.objects.all()
    update= models.veh_exp.objects.get(id=iid)
    if request.method=='POST':
        update.fuel_amt=request.POST['fuel_amt']
        update.toll_amt=request.POST['toll_amt']
        update.misc_amt=request.POST['misc_amt']
        update.total_amt=request.POST['total_amt']
        update.save()
        messages.success(request,'Record Sucessfully updated')
        return redirect("expense_report")
    else:
        return render(request,'vehicle_expense_service.html',{"a":update, 'dname':dname,'aman':aman})
    
def expense_delete(request,iid):
    models.veh_exp.objects.filter(id=iid).delete()
    return redirect("expense_report")


# vehicle Reparing

def vehicle_reparing(request):
    depot_name = request.session.get('depot_name')
    dname = models.dipo.objects.all()
    aman={
        'title' : 'PCPL | Deport Page',
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user),
        'depotname' : models.veh_exp.objects.filter(dipo_id=depot_name),
    }
    s_user = request.s_user
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    elif s_user == 'Admin':
        aman['page_name'] = 'base.html'
        diponame = User.objects.filter(username=request.user)
        for x in diponame:
            aman['diponame'] = x.diponame
    else:
        aman['page_name'] = 'base.html'
    if request.method=='POST':
        veh_no=request.POST['veh_no']
        veh_part=request.POST['part']
        rep_prc=request.POST['price']
        rep_date=request.POST['rep_date']
        depo_id=request.POST['depo_id']
        obj=models.veh_rep(veh_no=veh_no,dipo_id=depo_id,veh_part=veh_part,rep_prc=rep_prc,rep_date=rep_date)
        messages.success(request,'sucessfully inserted')
        obj.save()
    val = models.veh_exp.objects.values('veh_no')
    return render(request,'vehicle_reparing.html',{'val':val, 'dname':dname,'aman':aman})

def rep_update(request,iid):
    dname = models.dipo.objects.all()
    aman={
        'title' : 'PCPL | Deport Page',
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    dname = models.dipo.objects.all()
    s_user = request.s_user
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    else:
        aman['page_name'] = 'base.html'
    update= models.veh_rep.objects.get(id=iid)
    val = models.veh_exp.objects.values('veh_no')
    if request.method=='POST':
        update.rep_date=request.POST['rep_date']
        update.veh_part=request.POST['part']
        update.rep_prc=request.POST['price']
        update.save()
        messages.success(request,'Record Sucessfully updated')
        return redirect("expense_report")
    else:
        return render(request,'repairingupdate.html',{"a":update,'val':val, 'dname':dname,'aman':aman})
        
def rep_delete(request,iid):
    models.veh_rep.objects.filter(id=iid).delete()
    return redirect("expense_report")
 


# vehicle Expense Report

def expense_report(request):
    depot_name = request.session.get('depot_name')
    aman={
        'title' : 'PCPL | Deport Page',
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user),
        'depotname' : models.veh_exp.objects.filter(dipo_id=depot_name),
    }
    dname = models.dipo.objects.all()
    s_user = request.s_user
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    elif s_user == 'Admin':
        aman['page_name'] = 'base.html'
        diponame = User.objects.filter(username=request.user)
        for x in diponame:
            aman['diponame'] = x.diponame
    else:
        aman['page_name'] = 'base.html'
    dname = models.dipo.objects.all()
    options = {
        'veh_no': models.veh_exp.objects.values('veh_no')
    }
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method=='POST':
            veh_no=request.POST['veh_no']
            f_date=request.POST['f_date']
            t_date=request.POST['t_date']
            deponame = request.POST.get('deponame')
            conditions ={}
            conditions2 ={}
            if deponame != None :
                conditions['dipo_id'] = deponame
                conditions2['dipo_id'] = deponame
            if veh_no != '':
                conditions['veh_no']=veh_no
                conditions2['veh_no']=veh_no
            if f_date and  t_date:
                conditions['exp_date__range']=[f_date , t_date]
                conditions2['rep_date__range']=[f_date , t_date]
            obj = models.veh_exp.objects.filter(**conditions)
            veh = models.veh_rep.objects.filter(**conditions2)
            response = {}
            if obj.exists():
                sno=0
                value= f' <table><thead>        <h5>Vehicle Expnese</h5>        <th>Sl.No.</th>        <th>Vehicle Number</th>        <th>Fuel Quantity</th>        <th>Fuel Amount</th>        <th>Toll Amount</th>        <th>Misc. Amount</th>        <th>Total Amount</th>        <th colspan="3" align="centre">Action&nbsp;Here</th>    </thead><tbody>'
                for d in obj:
                    sno=sno+1
                    value += f'<tr>'
                    value += f'<td align="center">'+str(sno)+'</td>'
                    value += f'<td>{d.veh_no}</td>'
                    value += f'<td>{d.fuel_qty}</td>'
                    value += f'<td>{d.fuel_amt}</td>'
                    value += f'<td>{d.toll_amt}</td>'
                    value += f'<td>{d.misc_amt}</td>'
                    value += f'<td>{d.total_amt}</td>'
                    value += f'<td><a href="/expense_update/{d.id}/" ><i class="fa-solid fa-file-pen"></i></a></td>'
                    value += f'<td><a onclick="del(\'/expense_delete/{d.id}/\')" ><i class="fa-solid fa-trash" style="color:red;cursor:pointer;"></i></a></td>'
                    value += f'<td align="center"><button style="background-color:green;" title="Share"><i class="fa-solid fa-share-from-square"></i></button></td>'
                value += f'</tr>'
                value += '</tbody></table>'
                response['success'] = True
                response['value'] = value
            if veh.exists():
                data=f'<table><thead><h5>Repair Expnese</h5>    <th>Sl.No.</th>    <th>Vehicle No.</th>    <th>Reparing Date</th>    <th>Parts Name</th>    <th>Price</th>    <th colspan="3" align="centre">Action&nbsp;Here</th></thead> <tbody>'
                for x in veh:
                    
                    data +=f'<tr>'
                    data +=f'<td align="center">'+str(sno)+'</td>'
                    data +=f'<td>{x.veh_no}</td>'
                    data +=f'<td>{x.rep_date}</td>'
                    data +=f'<td>{x.veh_part}</td>'
                    data +=f'<td>{x.rep_prc}</td>'
                    data += f'<td><a href="/rep_update/{x.id}/" ><i class="fa-solid fa-file-pen"></i></a></td>'
                    data += f'<td><a onclick="del(\'/rep_delete/{x.id}/\')" ><i class="fa-solid fa-trash" style="color:red;cursor:pointer;"></i></a></td>'
                    data +=f'<td align="center"><button style="background-color:green;" title="Share"><i class="fa-solid fa-share-from-square"></i></button></td>'
                data +=f'</tr>'
                data +='</tbody></table> '
                response['success'] = True
                response['data'] = data
            else:
                response ={
                    'success':False,
                    'messages':'please select any condition'
                }
            print(response)
            return http.JsonResponse(response, safe=False)  
    else:
        return render(request,'expense_report.html',{'opt':options, 'dname':dname,'aman':aman})
               
def expense_update(request,iid):
    dname = models.dipo.objects.all()
    aman={
        'title' : 'PCPL | Deport Page',
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    dname = models.dipo.objects.all()
    s_user = request.s_user
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    else:
        aman['page_name'] = 'base.html'
    update= models.veh_exp.objects.get(id=iid)
    if request.method=='POST':
        update.fuel_amt=request.POST['fuel_amt']
        update.toll_amt=request.POST['toll_amt']
        update.misc_amt=request.POST['misc_amt']
        update.total_amt=request.POST['total_amt']
        update.save()
        messages.success(request,'Record Sucessfully updated')
        return redirect("expense_report")
    else:
        return render(request,'vehicle_expense_service.html',{"a":update, 'dname':dname,'aman':aman})
    
def expense_delete(request,iid):
    models.veh_exp.objects.filter(id=iid).delete()
    return redirect("expense_report")

def attendence(request):
    depot_name = request.session.get('depot_name')
    data= {
        'depotname' : models.distri_details.objects.filter(dipo_name=depot_name)
        }
    dname = models.dipo.objects.all()
    
    aman={
        'username' : request.user,
        's_user' : request.s_user,
        'profile' : models.profile_update.objects.get(userid=request.user)
    }
    dname = models.dipo.objects.all()
    s_user = request.s_user
    if s_user == 'User':
        messages.info(request,'You have not permission for this page')
        return redirect('index')
    elif s_user == 'Admin':
        aman['page_name'] = 'base.html'
        diponame = User.objects.filter(username=request.user)
        for x in diponame:
            aman['diponame'] = x.diponame
    else:
        aman['page_name'] = 'base.html'
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if request.method == 'POST':
            srcid= request.POST.get('srcid')
            url={}
            if srcid!=None:
                url['emp_id']=srcid
            # data = models.distri_details.objects.all() 
            obj = models.markAttendence.objects.filter(**url)
            
            if obj.exists():   
                value=f' <table class="dis_table"><thead><th>Dist-ID</th><th>Status</th><th>Time</th><th>Date</th></thead><tbody>'
                for x in obj:
                    value+=f'<tr>'
                    
                    value+=f'<td>{x.emp_id}</td>'
                    value+=f'<td>{x.status}</td>'
                    value+=f'<td>{x.time}</td>'
                    value+=f'<td>{x.date}</td>'

                    
                    value+=f'</tr>'
                value+= '</tbody></table>'
                response ={
                    'success':True,
                    'value' :value
                }
                return http.JsonResponse(response, safe=False)
            else:
                response ={
                    'success' :False,
                    'message':'NO records Found'
                }
                return http.JsonResponse(response, safe=False)
    else:
        return render(request, 'attendence.html', {'data':data,'dname':dname,'aman':aman})
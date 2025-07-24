from django.db import models

# Create your models here.
class automatic1(models.Model):
    order_id=models.CharField(max_length=500,default=0,null=True)
    dipo_id=models.CharField(max_length=500)
    dist_id=models.CharField(max_length=500)
    trans_id=models.CharField(max_length=500,default=0)
    drv_id=models.CharField(max_length=500)
    
class order_details(models.Model):
  order_id=models.CharField(max_length=500)
  lr_date=models.CharField(max_length=500)
  dist_name=models.CharField(max_length=500)
  dist_town=models.CharField(max_length=500)
  trnas_name=models.CharField(max_length=500)
  v_type=models.CharField(max_length=500)
  v_no=models.CharField(max_length=500)
  l_type=models.CharField(max_length=500)
  invoice_no=models.CharField(max_length=500)
  invoice_val=models.CharField(max_length=500)
  quantity=models.CharField(max_length=500)
  quan=models.CharField(max_length=500,blank=True,null=True)
  weig=models.CharField(max_length=500,blank=True,null=True)
  advance_per=models.CharField(max_length=500,blank=True,null=True)
  invoice_date=models.CharField(max_length=500)
  weight=models.CharField(max_length=500)
  labour_exp=models.CharField(max_length=500)
  freight=models.CharField(max_length=500)
  misc_charge=models.CharField(max_length=500)
  total_amt=models.CharField(max_length=500)
  advance_amnt=models.CharField(max_length=500)
  due_amnt=models.CharField(max_length=500)
  product=models.CharField(max_length=500)
  diponame=models.CharField(max_length=500,null=True)


class preserve(models.Model):
  order_id=models.CharField(max_length=500,blank=True,null=True)
  lr_date=models.CharField(max_length=500,blank=True,null=True)
  dist_name=models.CharField(max_length=500,blank=True,null=True)
  dist_town=models.CharField(max_length=500,blank=True,null=True)
  trnas_name=models.CharField(max_length=500,blank=True,null=True)
  v_type=models.CharField(max_length=500,blank=True,null=True)
  v_no=models.CharField(max_length=500,blank=True,null=True)
  l_type=models.CharField(max_length=500,blank=True,null=True)
  invoice_no=models.CharField(max_length=500,blank=True,null=True)
  invoice_val=models.CharField(max_length=500,blank=True,null=True)
  quantity=models.CharField(max_length=500,blank=True,null=True)
  advance_per=models.CharField(max_length=500,blank=True,null=True)
  quan=models.CharField(max_length=500,blank=True,null=True)
  weig=models.CharField(max_length=500,blank=True,null=True)
  invoice_date=models.CharField(max_length=500,blank=True,null=True)
  weight=models.CharField(max_length=500,blank=True,null=True)
  labour_exp=models.CharField(max_length=500,blank=True,null=True)
  freight=models.CharField(max_length=500,blank=True,null=True)
  misc_charge=models.CharField(max_length=500,blank=True,null=True)
  total_amt=models.CharField(max_length=500,blank=True,null=True)
  advance_amnt=models.CharField(max_length=500,blank=True,null=True)
  due_amnt=models.CharField(max_length=500,blank=True,null=True)
  product=models.CharField(max_length=500,blank=True,null=True)
  diponame=models.CharField(max_length=500,null=True)



class signrecord(models.Model):
  username=models.CharField(max_length=500)
  role=models.CharField(max_length=500)
  dipo_name=models.CharField(max_length=500)
  status=models.CharField(max_length=500)
  
class dipo(models.Model):
    diop_id=models.CharField(max_length=500)
    pri_name=models.CharField(max_length=500)
    ope_name=models.CharField(max_length=500 ,blank= True)
    man_name=models.CharField(max_length=500)
    man_cont=models.CharField(max_length=500)
    depo_cont=models.CharField(max_length=500)
    depo_tel=models.CharField(max_length=500)
    state=models.CharField(max_length=500)
    distr=models.CharField(max_length=500)
    addr=models.CharField(max_length=500)
    gst=models.CharField(max_length=500)
    auto=models.CharField(max_length=500,blank=True,default=0)

class state1(models.Model):
    stat=models.CharField(max_length=500)
    distr=models.TextField()
    
    
class distri_details(models.Model):
  dist_id=models.CharField(max_length=500)
  dist_name=models.CharField(max_length=500)
  dipo_name=models.CharField(max_length=500)
  cont_no=models.CharField(max_length=500)
  landline_no=models.CharField(max_length=500)
  le_ex=models.CharField(max_length=500)
  state=models.CharField(max_length=500)
  city=models.CharField(max_length=500)
  addrs=models.CharField(max_length=500)
  pin=models.CharField(max_length=500)
  gst_no=models.CharField(max_length=500)
  qrCode = models.FileField(upload_to='QRCodes/', null=True)
 
class plorder(models.Model):
    lrno=models.CharField(max_length=500)
    lrdate=models.CharField(max_length=500)
    dname=models.CharField(max_length=500)
    dtown=models.CharField(max_length=500)
    tname=models.CharField(max_length=500)
    vno=models.CharField(max_length=500)
    vtype=models.CharField(max_length=500)
    it=models.CharField(max_length=500) #IT MEANS LOAD Type
    ino=models.CharField(max_length=500)
    ivalue=models.CharField(max_length=500)
    idate=models.CharField(max_length=500)
    quantity=models.CharField(max_length=500)
    weight=models.CharField(max_length=500)
    freight=models.CharField(max_length=500)
    le=models.CharField(max_length=500)
    ta=models.CharField(max_length=500)
    aa=models.CharField(max_length=500)
    da=models.CharField(max_length=500)
    diop=models.CharField(max_length=500)
    m_ch=models.CharField(max_length=500)
    pd=models.CharField(max_length=500)
    status=models.CharField(max_length=500)
    
class plvehicle (models.Model):
  vtype=models.CharField(max_length=500)
  vprise=models.CharField(max_length=500)
  cname=models.CharField(max_length=500)
  lt=models.CharField(max_length=500)
  dipo_id=models.CharField(max_length=500 ,null=True)
  

class pl_sign(models.Model):
    U_NAME=models.CharField(max_length=500)
    U_ID=models.CharField(max_length=500)
    P_WORD=models.CharField(max_length=500)
    S_QUESTIONS=models.CharField(max_length=500)
    S_ANSWER=models.CharField(max_length=500)
    R_O_L_E=models.CharField(max_length=500)
    SATU=models.CharField(max_length=500)
    dipo_id=models.CharField(max_length=500)


    
class transporter_details(models.Model):
    trans_id=models.CharField(max_length=500)
    trans_name=models.CharField(max_length=500)
    cont_no=models.CharField(max_length=10)
    land_no=models.CharField(max_length=500)
    prop_name=models.CharField(max_length=500)
    addrs=models.CharField(max_length=500)
    state=models.CharField(max_length=500)
    distr=models.CharField(max_length=500)
    bnk_name=models.CharField(max_length=500)
    acchold_name=models.CharField(max_length=500)
    acc_no=models.CharField(max_length=500)
    ifsc=models.CharField(max_length=500)
    veh_ty=models.CharField(max_length=50)
    dipo_id=models.CharField(max_length=500)
  
   
class veh_exp(models.Model):
    veh_no=models.CharField(max_length=500)
    fuel_no=models.CharField(max_length=500)
    fuel_qty=models.CharField(max_length=500)
    fuel_amt=models.CharField(max_length=500)
    toll_amt=models.CharField(max_length=500)
    misc_amt=models.CharField(max_length=500)
    exp_date=models.CharField(max_length=500)
    total_amt = models.CharField(max_length=45, default=0)
    dipo_id=models.CharField(max_length=500 ,blank=True,null=True)

class veh_rep(models.Model):
    veh_no=models.CharField(max_length=500)
    veh_part=models.CharField(max_length=500)
    rep_prc=models.CharField(max_length=500)
    rep_date=models.CharField(max_length=500)
    dipo_id=models.CharField(max_length=500 ,blank=True,null=True)


class drv_pay(models.Model):
  drv_nm=models.CharField(max_length=500)
  sal_mo=models.CharField(max_length=500)
  pay_amt=models.CharField(max_length=500)
  pay_mode=models.CharField(max_length=500, blank=True, null=True)
  pay_bal_amt=models.CharField(max_length=500, blank=True, null=True)
  pay_date=models.CharField(max_length=500)
  dipo_id=models.CharField(max_length=500 ,blank=True,null=True)
  
class drv_details(models.Model):
  drv_pic=models.FileField(max_length=50, blank=True,null=True)
  drv_id=models.CharField(max_length=500)
  drv_nme=models.CharField(max_length=500)
  drv_no=models.CharField(max_length=500)
  drv_lis_no=models.CharField(max_length=500)
  drv_sal=models.CharField(max_length=500, blank=True, null=True)
  drv_addhar=models.FileField(max_length=500,blank=True,null=True)
  dipo_id=models.CharField(max_length=500 ,blank=True,null=True)
  
  

    

class profile_update(models.Model):
  profile_pic=models.FileField(max_length=50, blank=True,null=True)
  userid=models.CharField(max_length=500)
  first_name=models.CharField(max_length=500)
  cont_no=models.CharField(max_length=500)
  email=models.CharField(max_length=500)
  gender=models.CharField(max_length=500)
  dob=models.CharField(max_length=500)
  state=models.CharField(max_length=500)
  distr=models.CharField(max_length=500)
  pincode=models.CharField(max_length=500)
  adrs=models.CharField(max_length=500)


class markAttendence(models.Model):
  emp_id=models.CharField(max_length=500)
  status = models.BooleanField(default=True)
  time = models.TimeField()
  date = models.DateField()
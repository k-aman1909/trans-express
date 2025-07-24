// ************* For Alphabets ****************
function alphapets(text){
    $(text).keydown(function (e) { 
        if(e.which == 8 ){
            $(this).siblings('span').text('');
            $(this).css('border', 'none');
            $(this).siblings('label').css('color', '#444444');
            $(this).siblings('i').css('color', 'black');
        }
    });
    $(text).keypress(function (e) { 
        if(!((e.which >= 65 && e.which <=90) || (e.which >= 97 && e.which <=122) || e.which ==32 )){
            $(this).siblings('span').text('Only Letters Are Allowed !');
            $(this).css('border', '1px solid red');
            $(this).siblings('label').css('color', 'red');
            $(this).siblings('i').css('color', 'red');
            return false;
        }
        else if(e.which == 32){
            if(e.target.selectionStart === 0)
                return false;
            else if($(this).val().slice(-1) === ' '){
                return false;
            }    
        }
        else{
            $(this).siblings('span').text('');
            $(this).css('border', 'none');
            $(this).siblings('label').css('color', '#444444');
            $(this).siblings('i').css('color', 'black');
        }
    });
    $(text).focusout(function (e) { 
        if($(this).val()==''){
            $(this).siblings('span').text('This Field Is Mandatory.');
            $(this).css('border', '1px solid red');
            $(this).siblings('label').css('color', 'red');
            $(this).siblings('i').css('color', 'red');
        }
        else{
            $(this).siblings('span').text('');
            $(this).css('border', 'none');
            $(this).siblings('label').css('color', '#444444');
            $(this).siblings('i').css('color', 'black');
        }
            
    });
}

// ************************ For Mobile Number ************************

function number(no){
    $(no).keydown(function (e) { 
        if(e.which==8){
            $(this).siblings('span').text('');
            $(this).css('border', 'none');
            $(this).siblings('label').css('color', '#444444');
            $(this).siblings('i').css('color', 'black');
        }
    });
    $(no).keypress(function (e) { 
        if(!((e.which >= 48 && e.which <=57))){
            $(this).siblings('span').text('Only Digits Are Allowed !');
            $(this).css('border', '1px solid red');
            $(this).siblings('label').css('color', 'red');
            $(this).siblings('i').css('color', 'red');
            return false;
        }
        else if($(this).val().length == 10){
            $(this).siblings('span').text('Maximum 10 Digits Are Allowed');
            $(this).css('border', '1px solid red');
            $(this).siblings('label').css('color', 'red');
            $(this).siblings('i').css('color', 'red');
            return false;
        }
        else{
            $(this).siblings('span').text('');
            $(this).css('border', 'none');
            $(this).siblings('label').css('color', '#444444');
            $(this).siblings('i').css('color', 'black');
        }
    });
    $(no).focusout(function (e) { 
        if($(this).val()==''){
            $(this).siblings('span').text('This Field Is Mandatory.');
            $(this).css('border', '1px solid red');
            $(this).siblings('label').css('color', 'red');
            $(this).siblings('i').css('color', 'red');
        }
        if($(this).val().length < 10){
            $(this).siblings('span').text('Minimum 10 Digits Required.');
            $(this).css('border', '1px solid red');
            $(this).siblings('label').css('color', 'red');
            $(this).siblings('i').css('color', 'red');
        }
        else{
            $(this).siblings('span').text('');
            $(this).css('border', 'none');
            $(this).siblings('label').css('color', '#444444');
            $(this).siblings('i').css('color', 'black');
        }
            
    });
}


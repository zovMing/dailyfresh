$(function(){
    $("#add").click(function(){
        num = parseInt($("#wnum").val());
       onecost =   parseInt($("#onecost").html());
       num+=1;
       z = num*onecost;
       z= z + '元';
       $("#wnum").val(num+'')
        $("#totalAll").html(z)
    })

    
    $("#reduce").click(function(){
        num = parseInt($("#wnum").val());
        onecost =   parseInt($("#onecost").html());
        if (num>1){
            num-=1;
        }
        z = num*onecost;
        z= z + '元';
        $("#wnum").val(num+'')
        $("#totalAll").html(z)
    })
    $("#wnum").blur(function(){
        num = parseInt($("#wnum").val());
       onecost =   parseInt($("#onecost").html());
       z = num*onecost;
       z= z + '元';
        $("#totalAll").html(z)
    })


    	var $add_x = $('#add_cart').offset().top;
		var $add_y = $('#add_cart').offset().left;

		var $to_x = $('#show_count').offset().top;
		var $to_y = $('#show_count').offset().left;

		$(".add_jump").css({'left':$add_y+80,'top':$add_x+10,'display':'block'})
    $("#add_cart").click(function(){
        $.ajax({
            url:'/shopcart/add/',
            data:{'sid':$("#add_cart").attr('spid'), 'snum':$("#wnum").val()},
            dataType:'json',
            type:'POST',
            success:function(data){                
				if (data.nologin=='1'){
					location.href='/user/login/?no=1'
					return false;
				}
                if(data.s){
                $(".add_jump").stop().animate({
				'left': $to_y+7,
				'top': $to_x+7},
				"fast", function() {
					$(".add_jump").fadeOut('fast',function(){
						$('#show_count').html(data.num);
					});

			});
                }else{
                    console.log('data error');
                }
            },
            error:function(){
                    console.log('network error');
            }
        })
    })



})
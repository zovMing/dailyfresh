$(function(){
    //全选以及全部不选择
    allNumAdd();
    $("input[type='checkbox']").prop("checked",true);
     $("#allcheck").click(function(){
         if ( $("#allcheck").is(":checked")){
            $("input[type='checkbox']").prop("checked",true);
         }
         else{
            $("input[type='checkbox']").removeAttr('checked');
         }
     })

     $("input[type='checkbox']:not(#allcheck)").click(function(){
         if ($("input[type='checkbox']:not(#allcheck)").length == $("input[type='checkbox']:checked:not(#allcheck)").length)
            {
                $("#allcheck").prop('checked', true);
            }else{
                $("#allcheck").removeAttr('checked');
            }
            allNumAdd();
     })


     

     //增加数量
     $(".add").click(function(){
        var v1 =  parseInt($(this).next().val())
        v1 += 1
        $(this).next().val(v1)        
         oneAdd($(this).next());
         allNumAdd();
     })
     
     $(".minus").click(function(){
        var v1 =  parseInt($(this).prev().val())
        if (v1==1)
        {
            del($(this).attr('spid'), $(this).parent().parent().parent());
            return ;
        }
        v1 -= 1;
        $(this).prev().val(v1);
         oneAdd($(this).prev());
         allNumAdd();
     })

     $(".delshopcart").click(function(){         
            del($(this).attr('spid'),$(this).parent().parent())
            return false;
     })


     $(".num_show").change(function(){
         oneAdd($(this));
        allNumAdd()
     })


     //单价修改 单条记录的总金额修改
     function oneAdd(obj){
        v1 = parseInt(obj.val());
        onev2 = obj.parent().parent().prev().html();
        onev2 = onev2.substring(0,onev2.length-1);
        onev2 = parseInt(onev2);
        obj.parent().parent().next().html(v1*onev2+'元');

     }
     //删除指定xx的购物车id的数据，并且移除页面中iob的元素
     function del(xx, iob){
         isDel = confirm('确定删除吗');  
        if (isDel){
            $.ajax({
                    url:'/shopcart/ajaxDel/',
                    data:{'sid':xx},
                    dataType:'JSON',
                    type:'POST',
                    success:function(data){                        
                        if (data.nologin=='1'){
					        location.href='/user/login/?no=1'
                            return false;
                        }
                        if (data.res==1){
                            iob.remove()
                        }
                    },
                    error:function(){
                        console.log('network error')
                    }
                })
        }         
     }
     //总计
     function allNumAdd(){
        var ac = 0.00
        var acount = 0 
        $("input[type='checkbox']:checked").each(function(){
            if($(this).attr('id') != 'allcheck')
            {
                fuck = $(this).parent().nextAll('.col07').html();
                ac += parseFloat(fuck);
                acount += 1;
            }
        })
        $("#allco").html(ac.toFixed(2))
        $("#allc").html(acount)

     }

     

})
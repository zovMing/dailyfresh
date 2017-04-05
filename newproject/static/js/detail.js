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
})
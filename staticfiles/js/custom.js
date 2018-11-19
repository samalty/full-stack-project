$(document).ready(function(){
    
    // Dashboard order projects select function
    
    $('#order_projects').on('change', function(){
        var url = $(this).val();
        if (url){
            window.location = url;
        }
        return false;
    });
    
    // Dashboard top and bottom horizontal scroll bars
    
    $('.wrapper1').on('scroll', function(e){
        $('.wrapper2').scrollLeft($('.wrapper1').scrollLeft());
    }); 
    $('.wrapper2').on('scroll', function(e){
        $('.wrapper1').scrollLeft($('.wrapper2').scrollLeft());
    });
    
    // Dashboard sideways scrolling animation buttons
    
    $('#right').click(function(){
        event.preventDefault();
    $('.wrapper2').animate({
        scrollLeft: "+=342px"
      }, "slow");
    });
    
    $('#left').click(function(){
        event.preventDefault();
    $('.wrapper2').animate({
        scrollLeft: "-=342px"
    }, "slow");
    });
    
});

$(window).on('load', function(e){
    $('.top-scroll').width($('table').width());
    $('.bottom-scroll').width($('table').width());
});
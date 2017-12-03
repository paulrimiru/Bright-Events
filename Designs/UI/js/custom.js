$( document ).ready(function(){
    $(".button-collapse").sideNav();
    $('.modal').modal();
    $(".datepicker").pickadate({
      selectMonths: true, 
      selectYears: 1,
      today: 'Today',
      clear: 'Clear',
      close: 'Ok',
      closeOnSelect: true
    });
    $('.tooltipped').tooltip({delay: 50});
    AOS.init({
        easing: 'ease-in-sine'
      });
})
$( document ).ready(function(){
    $(".modal").modal();
    $(".datepicker").pickadate({
      selectMonths: true, 
      selectYears: 1,
      today: 'Today',
      clear: 'Clear',
      close: 'Ok',
      closeOnSelect: true
    });
})

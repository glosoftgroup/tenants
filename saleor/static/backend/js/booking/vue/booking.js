$ = jQuery;

var parent = new Vue({
    el:"#vue-book",
    delimiters: ['${', '}'],
    data:{
       'name':'Booking',
       'days':1,
       'check_in':null,
       'check_out':null
    },
    created:function(){
       console.log('booking vue running in parent');
       if($('#days').val()){
         this.days = $('#days').val();
       }
    },
    methods:{
        checkIn:function(){

        },
        computeCheckout:function(){
            console.log('vue onchange days');
        },
        computeTotalPrice:function(rooms){
            console.log('vue change days');
        }
    },
     watch: {
    	'days': function(val, oldVal){
    	        console.log('sdfsdfsdf');
                //console.log($('#check_out').val());
                //this.check_out = moment($('#check_in').val()).add(parseInt(this.days), 'days').format('MM/DD/YYYY');
                //$('#check_out').val(this.check_out);

             }
    }
});
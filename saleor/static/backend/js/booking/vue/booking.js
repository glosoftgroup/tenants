$ = jQuery;
//var today = new Date();
var today = moment().format('MM/DD/YYYY');

var parent = new Vue({
    el:"#vue-app",
    delimiters: ['${', '}'],
    data:{
       'name':'Booking',
       'days':0,
       'check_in':null,
       'check_out':null
    },
    created:function(){
       console.log('vue running in parent');
       console.log(today);
       this.check_in = today
       $('#check_in').val(this.check_in);
       this.check_out = today
       $('#check_out').val(today);
    },
    methods:{
        checkIn:function(){

        },
        computeCheckout:function(){
            console.log(this.days);
            console.log(this.check_in);
            console.log(this.check_out);
        }

    }
});
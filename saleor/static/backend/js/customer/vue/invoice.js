/* ************************************
 *
 *  invoicing app
 *
 * ************************************
*/
$ = jQuery;
var modal = $('#payment-modal');
var dynamicData = {};

function alertUser(msg,status='bg-success',header='Well done!')
{ $.jGrowl(msg,{header: header,theme: status}); }
Vue.config.devtools = true
var parent = new Vue({
    el:"#printme",
    delimiters: ['${', '}'],
    data:{
        periods:[],
        filtered_payments:[],
        all_payments:[]
    },
    mounted:function(){
        /**get all payments  */
        var self = this;
        $.get($('.pageUrls').data('paylisturl'))
            .then(function(data){
                self.all_payments = data.results;
                $.each(data.results, function(key, val)
	            {
                    if (!self.periods.includes(val.bill.month)){
                        self.periods.push(val.bill.month)
                    }	
                });
                
                /* define the periods with name and data, data as an array */
                $.each(self.periods, function(key, val)
	            {
                    var name = Object.assign({}, {name:val, data:[]})
                    if (!self.filtered_payments.includes(name)){
                        self.filtered_payments.push(name)
                    }	
                });
                /* loop through all payments and add to their matching months */
                $.each(data.results, function(key, val)
	            {
                    for(var i=0;i<self.filtered_payments.length;i++){
                        if(val.bill.month == self.filtered_payments[i].name){
                            self.filtered_payments[i].data.push(val)
                        }
                    }	
                });
                
            }, function(error){
                console.log(error.statusText);
            });
    },
    methods:{
    }
});
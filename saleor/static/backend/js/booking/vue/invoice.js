/* ************************************
 *
 *  invoicing app
 *
 * ************************************
*/
$ = jQuery;
var modal = $('#payment-modal');

var parent = new Vue({
    el:"#printme",
    delimiters: ['${', '}'],
    data:{
       'name':'Invoicing',
       'date': null,
       'amount':null,
       'method':null,
       'description':null
    },
    methods:{
        openModal:function(){
            /* open modal */
            $('#payment-modal').modal();
            this.date = $('#date').val();
            console.log(this.date);
        }
    },
    created:function(){
        this.date = $('#date').val();
        console.log(this.date);
    }
});
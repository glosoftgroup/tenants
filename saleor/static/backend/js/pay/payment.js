/* for the form validation using vuejs */
Vue.use(VeeValidate);
/**
    uncomment the below line on development mode
    plugin required vuejs in mozilla or chrome
    url:https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/
**/

Vue.config.devtools = true
var parent = new Vue({
    el:"#vue-app-modal",
    delimiters: ['${', '}'],
    data:{
        /* filters */
        month:'',
        monthDisplay:'',
        search:'',
        status:'',
        date_paid:'',
        date_paid_display:'',
        /* cart */
        totalBillsAmount:0,
        billsList:[],
        billsToBePaid:[],
        paymentOptions:[],
        paymentToBeUsed:[],
        totalPages: 1,
        visiblePages: 4,
        page_size: 10,

        show_balance: false,
        show_change: false,
    },
    mounted:function(){
            var self = this,
                billsUrl = $('#billsUrl').val(),
                paymentOptionsUrl = $('#paymentOptionsUrl').val();
            self.tenant = $('#tenantPk').val();
            self.room = $('#roomPk').val();
            $.get(billsUrl+'?status=pending', function(data)
            {
                self.billsList = data.results;
                self.totalPages = data.total_pages;
                self.pagination(data.total_pages);
            })

            $.get(paymentOptionsUrl, function(data)
            {
                self.paymentOptions = data.results;
            })

            $('.monthpicker').datepicker({
                format: "MM/yyyy",
                autoclose: true,
                minViewMode: "months"})
            .on('changeDate', function(e){
                var month = String(e.date.getMonth()+1).length === 1 ? 
                            '0'+String(e.date.getMonth()+1) : 
                            String(e.date.getMonth()+1);
                var year  = e.date.getFullYear();
                var date  = e.date.getFullYear()+'-'+month+'-'+'01';

                $('.monthpicker').val(date);
                self.monthDisplay = e.date.toLocaleString('en-us', {month: "long"})+'/'+e.date.getFullYear();
                self.month        = date;
                var params = 'page_size='+self.page_size+'&q='+self.search+'&status='+self.status+'&month='+self.month;
                $.get(billsUrl+'?'+params, function(data)
                {
                    self.billsList = data.results;
                    self.totalPages = data.total_pages;
                });
            });

            $('.date_paid').datepicker({
                format: "dd-mm-yyyy",
                autoclose: true})
            .on('changeDate', function(e){
                var day = String(e.date.getDate()).length === 1 ? 
                            '0'+String(e.date.getDate()) : 
                            String(e.date.getDate());

                var month = String(e.date.getMonth()+1).length === 1 ? 
                            '0'+String(e.date.getMonth()+1) : 
                            String(e.date.getMonth()+1);

                var year  = e.date.getFullYear();
                var date  = year+'-'+month+'-'+day;

                $('.date_paid').val(date);
                self.date_paid = date;
                self.date_paid_display = day+'-'+month+'-'+year;
            });

    },
    methods:{
        alert: function(msg,status='bg-success',header=null){ 
            $.jGrowl(msg,{header: header,theme: status}); 
        },
        /* cart methods */
        addTobillsToBePaid: function(bill){
            var found = false;
            this.billsToBePaid.forEach(item => {
                /* check if exists */
                if (item.id === bill.id) {
                    found = true;
                    this.alert(
                        item.billtype.name+' bill for '+ 
                        item.room.name +' has already been added','bg-danger');
                    return;
                }
            });

            /* if it doesn't exist */
            if (found === false) {
                this.billsToBePaid.push(Vue.util.extend({}, bill));
                this.totalBillsAmount += bill.amount
                this.alert(bill.billtype.name+' bill has been added successfully','bg-success');
            }

        },
        removeBill: function(bill) {
          this.billsToBePaid.splice(bill, 1)
          this.totalBillsAmount -= bill.amount
          this.alert(bill.billtype.name+' bill has been removed successfully','bg-success');
        },
        goToPaymentTab: function(){
            $('#dues-tab').removeClass('active');
            $('#dues').removeClass('active');
            //activate payment tab
            $('#pay-tab').addClass('active');
            $('#pay').addClass('active');
        },
        goToDuesTab: function(){
            $('#pay-tab').removeClass('active');
            $('#pay').removeClass('active');
            $('#dues-tab').addClass('active');
            $('#dues').addClass('active');
        },

        /* input change */
        inputChangeEvent:function(){
            /* make api request on events filter */
            var self = this, data;

            var billsUrl = $('#billsUrl').val();
            var params = 'page_size='+this.page_size+'&q='+this.search+'&status='+this.status+'&month='+this.month;
            $.get(billsUrl+'?'+params, function(data)
            {
                self.billsList = data.results;
                self.totalPages = data.total_pages;
            });
        },
        /* payment options cart and handlers */
        addPayment: function(payment) {
            var found = false;
            // Check if the item was already added to cart
            // If so them add it to the qty field
            this.paymentToBeUsed.forEach(item => {
                if (item.id === payment.id) {
                  found = true;
                }
            });

            if (found === false) {
                this.paymentToBeUsed.push(Vue.util.extend({}, payment));
                this.alert(payment.name+' option has been added successfully','bg-success');
            }
        },
        removePayment(payment) {
          this.paymentToBeUsed.splice(payment, 1)
          this.alert(payment.name+' has been removed successfully','bg-success');
        },
        /* complete payment */
        getDue: function(total,tendered){
            due = parseInt(total) - parseInt(tendered);
            if(due <= 0){
                this.show_change = true;
                this.show_balance = false;
                due = parseInt(tendered) - parseInt(total);
            }else{
                this.show_balance = true;
                this.show_change = false;
            }
            return due
        },
        listItems:function(num){
        /* make api request when pagination pages are clicked */
            var self = this,
                billsUrl = $('#billsUrl').val();
            this.$http.get(billsUrl+'?page='+num+'&page_size='+self.page_size+'&q='+self.search+'&status='+self.status+'&month='+self.month)
                .then(function(data){
                    data = JSON.parse(data.bodyText);
                    self.billsList = data.results;
                }, function(error){
                    console.log(error.statusText);
            });
        },
        pagination: function(val){
        /* include twbsPagination on vue app */
            var self=this ;
            /* restructure pagination */
            $('.mbootpag-callback').twbsPagination({
                totalPages: parseInt(val),
                visiblePages: self.visiblePages,
                prev: '<span aria-hidden="true">&laquo;</span>',
                next: '<span aria-hidden="true">&raquo;</span>',
                onPageClick: function (event, page) {
                    $('.pages-nav').text('Page ' + page + ' of '+self.totalPages);
                }
            }).on('page',function(event,page){
                self.listItems(page);
            });
        },
        completePayment: function(event){
            var self = this;
            if (self.totalBillsAmount == 0) {
                self.alert('Nothing to pay against, please check again!', 'bg-danger')
                return;
            }
            if (parent.Tendered == 0) {
                self.alert('No Amount has been paid', 'bg-danger', '!Oops')
                return;
            }
            if (!self.date_paid) {
                self.alert('Please set the date paid', 'bg-danger', '!Oops')
                return;
            }
            if (self.show_balance) {
                self.alert('Please fill in full payment', 'bg-danger', '!Oops')
                return;
            }

            var data = new FormData();
            var billPaymentCreateUrl = $('#billPaymentCreateUrl').val();

            dynamicData = {};
            dynamicData['total_bills_amount'] = parent.Total;
            dynamicData['total_bills_amount_paid'] = parent.Tendered;
            dynamicData['total_bills_balance'] = this.getDue(parent.Total, parent.Tendered);
            // dynamicData['bills'] = JSON.stringify(this.billsToBePaid);
            dynamicData['bills'] = this.billsToBePaid;
            // dynamicData['paymentoptions'] = JSON.stringify(this.paymentToBeUsed);
            dynamicData['paymentoptions'] = this.paymentToBeUsed;
            dynamicData['date_paid'] = this.date_paid;

            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios.defaults.xsrfCookieName = 'csrftoken';


            /* create if update url is null */
            axios.post(billPaymentCreateUrl, dynamicData)
            .then(function (response) {
                self.alert('Payment settled successfully', 'bg-success', 'Success!');
                $('#modal_instance').modal('hide');
                window.location = ($("#redirectUrl").val()) +'?payments=edit';
            })
            .catch(function (error) {
                if(error.response.status == '400'){
                    self.alert('That Payment Already Exists','bg-danger','Oops!');
                }else{
                    self.alert('Please check the fields and retry again','bg-danger','Oops!');
                }
                console.log(error);
            });
        }
    },
    computed: {
        Total: function() {
          var total = 0;
          this.billsToBePaid.forEach(item => {
            if(item.amount){
                total += item.amount;
            }
          });
          return total;
        },
        Tendered: function() {
            var tendered = 0;
            this.paymentToBeUsed.forEach(item=>{
                if(item.tendered){
                    tendered += parseInt(item.tendered);
                }
            });
            return tendered;
        },
        'totalPages': function(val, oldVal){
            var self=this ;
            /* destroy pagination on page size change */
            $('.mbootpag-callback').twbsPagination('destroy');

            /* restructure pagination */
            $('.mbootpag-callback').twbsPagination({
                totalPages: parseInt(val),
                visiblePages: self.visiblePages,
                prev: '<span aria-hidden="true">&laquo;</span>',
                next: '<span aria-hidden="true">&raquo;</span>',
                onPageClick: function (event, page) {
                    $('.pages-nav').text('Page ' + page + ' of '+self.totalPages);
                }
            }).on('page',function(event,page){
                self.listItems(page);
            });
        }
    },
})

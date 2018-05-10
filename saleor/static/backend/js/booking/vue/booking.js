$ = jQuery;
/* global variables */
var dynamicData = {};
var global_data = [];

function formatNumber(n, c, d, t){
	var c = isNaN(c = Math.abs(c)) ? 2 : c,
			d = d === undefined ? '.' : d,
			t = t === undefined ? ',' : t,
			s = n < 0 ? '-' : '',
			i = String(parseInt(n = Math.abs(Number(n) || 0).toFixed(c))),
			j = (j = i.length) > 3 ? j % 3 : 0;
	return s + (j ? i.substr(0, j) + t : '') + i.substr(j).replace(/(\d{3})(?=\d)/g, '$1' + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : '');
};
//vue filters
Vue.filter('formatCurrency', function (value) {
  return formatNumber(value, 2, '.', ',');
})

Vue.filter('formatDate', function (value) {
  value += '-01'
  return moment(value, 'YYYY/MM/DD').format('MMMM/YYYY');
})

Vue.filter('formatCheckOutDate', function (value) {
  value += '-01'
  return moment(value, 'YYYY/MM/DD').add(-1, 'M').format('MMMM/YYYY');
})

//select2 component wrapper
Vue.component('select2', {
  props: ['options', 'value','placeholder','url', 'data'],
  template: '#select2-template',
  methods:{
      format(item){ return item.name; },
  },
  mounted: function () {
    var vm = this
    $(this.$el)
      // init select2
      .select2({
        // data: this.options,
        width:'100%',
        placeholder: this.placeholder,
        formatSelection: this.format,
        formatResult: this.format,
        ajax: {
          url: function (params) {
            return vm.url+'?' + params.term;
          },
          // url: getAcademicYearsUrl,
          processResults: function (data) {
            // Tranforms the top-level key of the response object from 'items' to 'results'
            // console.log(data.results);
            data = data.results;
            global_data = data;
            return {
                  results :
                      data.map(function(item) {
                          return {
                              id : item.id,
                              text : item.name
                          };
                      }
              )};
          }
        },
        debug: true,
        delay: 250,
      })
      .val(this.value)
      .trigger('change')
      // emit event on change.
      .on('change', function () {
        vm.$emit('input', this.value)
        global_data.map((arr, index)=>{
            if(arr.id == this.value){
               parent.customer_name = arr.name;
               parent.customer_mobile = arr.mobile;
            }

        })
      })
  },
  watch: {
    value: function (value) {
      // update value
      $(this.$el)
      	.val(value)
      	.trigger('change')
    },
    options: function (options) {
      // update options
      $(this.$el).empty().select2({ data: options })
    }
  },
  destroyed: function () {
    $(this.$el).off().select2('destroy')
  }
})

Vue.component('dt-picker',{
    props: ['value', 'placeholder'],
    template: '#dt-template',
    watch: {
        value: function (value) {
          // update value
          $(this.$el).datepicker('update', value);
          this.$emit('input', value);
        }
    },
    mounted: function () {
    var vm = this
    $(this.$el)
      // init datepicker
      .datepicker({
        format: "yyyy-mm",
		autoclose: true,
		minViewMode: "months"
        }).on('changeDate', function(chosen_date){
                vm.$emit('input', chosen_date.format('yyyy-mm'));
		});
    }
})

Vue.use('vue-snotify')
var parent = new Vue({
    el:"#vue-app",
    delimiters: ['${', '}'],
    data: {
       name:'Booking',
       roomName:'',
       days:1,
       check_in: moment().format('YYYY-MM'),
       check_out: moment().add(1, 'months').format('YYYY-MM'),
       in_real_date: moment().format('YYYY-MM'),
       out_real_date: moment().add(1, 'months').format('YYYY-MM'),
       oneDay: 24*60*60*1000,
       customer: null,
       customer_name: '',
       customer_mobile: '',
       invoice_number: null,
       deposit_period: 1,
       deposit: 0,
       child: 0,
       adult: 1,
       rentPrice: 0, // house rent
       servicePrice: 0, // monthly service charge
       totalRent: 0,
       totalService: 0,
       errors: {},
       payment_date:'', // last paid bill month(date)
       real_days: 0, // days from booking during update
       checkInDisplay: '',
       checkOutDisplay: '',
       alert_user:{
           alert_type: 'alert-info',
           alert_show: false,
           alert_message: 'Alert message ...',
           alert_link: 'javascript:;',
           alert_link_message: 'Click me'
       }

    },
    created:function(){
       axios.defaults.xsrfHeaderName = "X-CSRFToken";
       axios.defaults.xsrfCookieName = 'csrftoken';
       if(pk){
            this.getRoomDetails(pk);
       }
       if(instance_id){
            this.getBookingDetails(instance_id);
       }

    },
    methods:{
        reformatDate(date){
            if(date.length < 10){
                 return date+'-01';
            }else{
                return date;
            }
        },
        bookProperty(e){
            e.preventDefault();
            var self = this;
            var errors = this.validateFields();
            var isValid = Object.keys(errors).length === 0;

            if(isValid){
                // populate form data
                var data = new FormData();
                data.append('invoice_number', this.invoice_number);
                data.append('total_rent', parseInt(this.totalRentComputed+'.00'));
                data.append('total_service',this.totalServiceComputed);
                data.append('total_deposit', this.totalDeposit);
                data.append('days', this.days);
                data.append('deposit_months', this.deposit_period);
                data.append('child', this.child);
                data.append('adult', this.adult);
                data.append('check_in', this.reformatDate(this.check_in));
                data.append('check_out', this.reformatDate(this.check_out));
                if(this.customer){
                    data.append('customer', this.customer);
                }
                data.append('customer_name', this.customer_name);
                data.append('customer_mobile', this.customer_mobile);
                data.append('room', pk);

                if(instance_id){
                    // update
                    axios.put('/api/booking/update/'+instance_id+'/', data)
                    .then(function (response) {
                        window.location.href = '/dashboard/booking/';
                    })
                    .catch(function (error) {
                        console.log(error);
                    });
                }else{
                    // create
                    axios.post('/api/booking/create/', data)
                    .then(function (response) {
                        window.location.href = '/dashboard/booking/';
                    })
                    .catch(function (error) {
                        console.log(error);
                    });

                }
            }
        },
        validateFields(){
            // validate
            var errors = {};
            let self = this;
            if(this.customer_name === '') errors.customer_name = 'Field required';
            if(this.customer_mobile === '') errors.customer_mobile = 'Field required';
            if(this.check_out === '') errors.check_out = 'Field required';
            if(this.check_in === '') errors.check_in = 'Field required';
            // if(!this.customer) errors.customer_mobile = 'Field required';
            if(!this.rentPrice) errors.rentPrice = 'Field required';
            if(!this.servicePrice) errors.servicePrice = 'Field required';
            if(!this.totalRentComputed) errors.totalRentComputed = 'Field required';
            // if(!this.totalServiceComputed) errors.totalServiceComputed = 'Field required';
            if(this.days < 1) errors.days = 'Field required';

            this.errors = errors;
            return errors;

        },
        getRoomDetails(pk){
            // fetch room details
            var vm = this;

            axios.get('/api/property/update/'+pk+'/')
            .then(function (response) {
                vm.roomName = response.data.name;
                vm.rentPrice = response.data.price;
                vm.servicePrice = response.data.service_charges;
            })
            .catch(function (error) {
                console.log(error);
            });
        },
        getBookingDetails(pk){
            // fetch room details
            var vm = this;

            axios.get('/api/booking/update/'+pk+'/')
            .then(function (response) {
                data = response.data;
                vm.invoice_number = data.invoice_number;
                vm.totalRent = data.total_rent;
                vm.totalService = data.total_service;
                vm.rentPrice = data.room_rent_price;
                vm.servicePrice = data.room_service_price;
                vm.deposit_period = data.deposit_months;
                vm.total_deposit = data.total_deposit;
                vm.days = data.days;
                vm.child = data.child;
                vm.adult = data.adult;
                vm.check_in = data.check_in;
                vm.check_out = data.check_out;
                vm.customer = data.customer;
                vm.customer_name = data.customer_name;
                vm.customer_mobile = data.customer_mobile;
                vm.room = data.room;

                // disable payment if customer has made a payment
                if(data.last_payment){
                    vm.payment_date = data.last_payment[0].month;
                    vm.real_days = data.last_payment[0].days;
                    var alert_message = data.customer_name+' has committed for ';
                    alert_message += data.last_payment[0].month +' '+ data.last_payment[0].billtype;
                    alert_message += ' bill. Some fields will be disabled.';
                    var alert_user = {
                         alert_type: 'alert-warning',
                         alert_show: true,
                         alert_message: alert_message,
                         alert_link: 'javascript:;',
                         alert_link_message: ''
                    }
                    vm.alert_user = alert_user;
                    vm.timeOutAlert();

                    // block fields
                    $('#select-tenant').attr('disabled','disabled');
                    $('#c_name').attr('disabled','disabled');
                    $('#mobile').attr('disabled','disabled');
                    $('#deposit_period').attr('disabled','disabled');
                }

            })
            .catch(function (error) {
                console.log(error);
            });
        },
        addDays(start, days){
            days = parseInt(days);

            var currentDate = start;
            var futureMonth = moment(currentDate).hour(12).add(days, 'M');
            var futureMonthEnd = moment(futureMonth).endOf('month');
            if(currentDate != futureMonth && futureMonth.isSame(futureMonthEnd.format('YYYY-MM-DD'))) {
                futureMonth = futureMonth.add(1, 'd');
            }
            return futureMonth.format('YYYY-MM');
        },
        getDays(start,end){
            var oneDay = 24*60*60*1000; // hours*minutes*seconds*milliseconds

            if(moment(end).isAfter(moment(start))){
                var firstDate = new Date(moment(start));
                var secondDate = new Date(moment(end));

                // var diffDays = Math.round(Math.abs((firstDate.getTime() - secondDate.getTime())/(oneDay)));
                var diffMonths = moment(end).diff(moment(start), 'months', true);
                return parseInt(diffMonths);
            }else{
                return 0;
            }
        },
        computeCheckout(){
            // console.log('vue onchange days');
        },
        computeTotalPrice(rooms){
            // console.log('vue change days');
        },
        timeOutAlert(){
            var vm = this;
            window.scrollTo(0, 0);
            setTimeout(function(){
                var alert_user = {}
                alert_user.alert_show = false;
                vm.alert_user = alert_user;
            }, 6000);
        },
        validateFromPayment(check_in){
            var vm = this;
            if(moment(check_in).isAfter(moment(this.payment_date))){
    	        // console.log(check_in+' is after '+this.payment_date)
    	        var alert_message = data.customer_name+' has committed for ';
                    alert_message += this.payment_date +' '+ data.last_payment[0].billtype;
                    alert_message += ' bill.  Check-In date cannot be more than '+this.payment_date +'.';
                    var alert_user = {
                         alert_type: 'alert-danger',
                         alert_show: true,
                         alert_message: alert_message,
                         alert_link: 'javascript:;',
                         alert_link_message: ''
                    }
                    vm.alert_user = alert_user;
                    this.timeOutAlert();

    	        this.check_in = this.payment_date;
    	        this.days = this.real_days;
    	        $('#check_in_date').datepicker('update', this.payment_date)
    	    }
        }
    },
    watch: {
    	'days': function(val, oldVal){
    	    this.check_out = this.addDays(this.check_in, val);
    	    this.errors.days = '';
    	},
    	'check_in': function(val, oldVal){
    	    this.days = this.getDays(this.check_in, this.check_out);
    	    this.errors.check_in = '';
    	    this.checkInDisplay = moment(val).format('YYYY-MM-DD');
    	    console.log(this.checkInDisplay);
    	    if(this.payment_date != ''){
    	        this.validateFromPayment(val);
    	    }
    	},
    	'check_out': function(val, oldVal){
    	    this.days = this.getDays(this.check_in, this.check_out);
    	    this.errors.check_out = '';
    	},
    	'customer_name': function(val, oldVal){
    	    this.errors.customer_name = '';
    	},
    	'customer_mobile': function(val, oldVal){
    	    this.errors.customer_mobile = '';
    	},
    	'totalRent': function(val, oldVal){
    	    this.errors.totalRent = '';
    	}
    },
    computed: {
        // a computed getter
        totalRentComputed() {
          // `this` points to the vm instance
          this.errors.totalRentComputed = '';
          return parseInt(this.rentPrice) * this.days;
        },
        totalServiceComputed() {
           // compute total service in lease time
           this.errors.totalServiceComputed = '';
           return parseInt(this.servicePrice) * this.days;
        },
        totalDeposit(){
            return parseInt(this.rentPrice) * this.deposit_period;
        },
        grandTotalComputed(){
            return (parseInt(this.rentPrice) * this.days)
             + parseInt(this.servicePrice) * this.days
             + parseInt(this.rentPrice) * this.deposit_period;
        }
    }
});
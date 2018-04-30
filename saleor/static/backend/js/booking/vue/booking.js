$ = jQuery;
/* global variables */
var dynamicData = {};
var global_data = [];
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
          $(this.$el)
            .val(value)
        }
    },
    mounted: function () {
    var vm = this
    $(this.$el)
      // init datepicker
      .daterangepicker({
        singleDatePicker: true,
        locale:{format: 'YYYY-MM-DD'},
        showDropdowns:true,
        autoUpdateInput:false,
        // maxDate: new Date()
        },function(chosen_date) {
              vm.$emit('input', chosen_date.format('YYYY-MM-DD'));
              console.log(chosen_date.format('YYYY-MM-DD'));
        });
    }
})
var parent = new Vue({
    el:"#vue-app",
    delimiters: ['${', '}'],
    data:{
       name:'Booking',
       roomName:'',
       days:2,
       check_in: moment().format('YYYY-MM-DD'),
       check_out: moment().add(1, 'months').format('YYYY-MM-DD'),
       oneDay: 24*60*60*1000,
       customer: null,
       customer_name: '',
       customer_mobile: '',
       invoice_number: null,
       child: 0,
       adult: 1,
       rentPrice: 0, // house rent
       servicePrice: 0, // monthly service charge
       totalRent: 0,
       totalService: 0,
       errors: {}
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
                data.append('days', this.days);
                data.append('child', this.child);
                data.append('adult', this.adult);
                data.append('check_in', this.check_in);
                data.append('check_out', this.check_out);
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
                        console.log(response);
                        window.location.href = '/dashboard/booking/';
                    })
                    .catch(function (error) {
                        console.log(error);
                    });
                }else{
                    // create
                    axios.post('/api/booking/create/', data)
                    .then(function (response) {
                        console.log(response);
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
            if(!this.totalServiceComputed) errors.totalServiceComputed = 'Field required';
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
                vm.invoice_number = response.data.invoice_number;
                vm.totalRent = response.data.total_rent;
                vm.totalService = response.data.total_service;
                vm.rentPrice = response.data.room_rent_price;
                vm.servicePrice = response.data.room_service_price;
                vm.days = response.data.days;
                vm.child = response.data.child;
                vm.adult = response.data.adult;
                vm.check_in = response.data.check_in;
                vm.check_out = response.data.check_out;
                vm.customer = response.data.customer;
                vm.customer_name = response.data.customer_name;
                vm.customer_mobile = response.data.customer_mobile;
                vm.room = response.data.room;

               console.log(response.data.room);
            })
            .catch(function (error) {
                console.log(error);
            });
        },
        addDays(start, days){
            return moment(start).add(parseInt(days), 'months').format('YYYY-MM-DD');
        },
        getDays(start,end){
            var oneDay = 24*60*60*1000; // hours*minutes*seconds*milliseconds

            if(moment(end).isAfter(moment(start))){
                var firstDate = new Date(moment(start));
                var secondDate = new Date(moment(end));

                // var diffDays = Math.round(Math.abs((firstDate.getTime() - secondDate.getTime())/(oneDay)));
                var diffMonths = moment(end).diff(moment(start), 'months', true)
                return parseInt(diffMonths);
            }else{
                return 0;
            }
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
    	    this.check_out = this.addDays(this.check_in, val);
    	    this.errors.days = '';
    	},
    	'check_in': function(val, oldVal){
    	    this.days = this.getDays(this.check_in, this.check_out);
    	    this.errors.check_in = '';
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
        totalRentComputed: function () {
          // `this` points to the vm instance
          this.errors.totalRentComputed = '';
          return parseInt(this.rentPrice) * this.days;
        },
        totalServiceComputed: function() {
           // compute total service in lease time
           this.errors.totalServiceComputed = '';
           return parseInt(this.servicePrice) * this.days;
        }
    }
});
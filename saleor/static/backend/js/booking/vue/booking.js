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
       days:1,
       check_in: moment().format('YYYY-MM-DD'),
       check_out: moment().add(1, 'months').format('YYYY-MM-DD'),
       oneDay: 24*60*60*1000,
       customer: null,
       customer_name: '',
       customer_mobile: '',
       rentPrice: 0, // house rent
       servicePrice: 0, // monthly service charge
       totalRent: 0,
       totalService: 0
    },
    created:function(){
       axios.defaults.xsrfHeaderName = "X-CSRFToken"
       axios.defaults.xsrfCookieName = 'csrftoken'

       if(pk){
            this.getRoomDetails(pk);
       }

    },
    methods:{
        bookProperty(e){
            e.preventDefault();
            alert('Sorry!. Ongoing');
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
    	    this.check_out = this.addDays(this.check_in, val);
    	},
    	'check_in': function(val, oldVal){
    	    this.days = this.getDays(this.check_in, this.check_out);
    	},
    	'check_out': function(val, oldVal){
    	    this.days = this.getDays(this.check_in, this.check_out);
    	}
    },
    computed: {
        // a computed getter
        totalRentComputed: function () {
          // `this` points to the vm instance
          return parseInt(this.rentPrice) * this.days;
        },
        totalServiceComputed: function() {
           // compute total service in lease time
           return parseInt(this.servicePrice) * this.days;
        }
    }
});
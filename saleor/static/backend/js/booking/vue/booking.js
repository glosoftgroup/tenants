$ = jQuery;
/* global variables */
var dynamicData = {};
var today = moment().format('YYYY-MM-DD');
var tomorrow = moment().add(1, 'months').format('YYYY-MM-DD');

//select2 component wrapper
Vue.component('select2', {
  props: ['options', 'value','placeholder','url'],
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

var parent = new Vue({
    el:"#vue-book",
    delimiters: ['${', '}'],
    data:{
       name:'Booking',
       days:1,
       today: moment().format('YYYY-MM-DD'),
       tomorrow: moment().add(1, 'months').format('YYYY-MM-DD'),
       check_in: null,
       check_out: null,
       selected: 2,
       options: [
          { id: 1, text: 'Hello' },
          { id: 2, text: 'World' }
        ]
    },
    created:function(){
       console.log(this.today);
       console.log(this.tomorrow);
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
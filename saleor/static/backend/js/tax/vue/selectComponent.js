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
          allowClear: true,
          width:'100%',
          placeholder: this.placeholder,
          formatSelection: this.format,
          formatResult: this.format,
          ajax: {
            url: function (params) {
              return vm.url+'?' + params.term;
            },
            processResults: function (data) {
              // Tranforms the top-level key of the response object from 'items' to 'results'
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
                 parent.room.name = arr.name;
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
$ = jQuery;

function api(url){
    return axios.get(url)
        .then(response => {
            return response;
        }).catch(error => {
            throw error;
        });
}

function formatNumber(n, c, d, t){
	var c = isNaN(c = Math.abs(c)) ? 2 : c,
			d = d === undefined ? '.' : d,
			t = t === undefined ? ',' : t,
			s = n < 0 ? '-' : '',
			i = String(parseInt(n = Math.abs(Number(n) || 0).toFixed(c))),
			j = (j = i.length) > 3 ? j % 3 : 0;
	return s + (j ? i.substr(0, j) + t : '') + i.substr(j).replace(/(\d{3})(?=\d)/g, '$1' + t) + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : '');
};

// vue filters
Vue.filter('formatCurrency', function (value) {
  return formatNumber(value, 2, '.', ',');
})

// vue filters
Vue.filter('formatDate', function (value) {
  value += '-01'
  return moment(value, 'YYYY/MM/DD').format('MMMM/YYYY');
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
//vue
var chart = new Vue({
    el:"#vue-app",
    delimiters: ['${', '}'],
    data:{
       'name':'Book Listing',
       items:[],
       loader:true,
       check_in: moment().format('YYYY-MM'),
       check_out: moment().add(2, 'M').format('YYYY-MM'),
       server_error: false,
       total_occupied: 0,
       total_empty: 0,
       pending_rent: 0,
       paid_rent: 0
    },
    watch:{
        'check_in': function(value, oldVal){
            this.getOccupiedRooms();
        },
        'check_out': function(value, oldVal){
            this.getOccupiedRooms();
        }
    },
    methods:{
        getOccupiedRooms(){
            var vm = this;
            var url = '/dashboard/booking/occupied/?check_in=';
            if(this.check_in)
                url += this.check_in+'-01';
            if(this.check_out)
                url += '&check_out='+this.check_out+'-28';

            api(url)
            .then(function(response){
                response = response.data.results;
                vm.total_empty = response.total_empty;
                vm.total_occupied  = response.total_occupied;
                vm.pending_rent = response.pending_rent;
                vm.paid_rent = response.paid_rent;
            })
            .catch(function(error){
                console.error(error);
            })
        },
        yearlyVisitsChart:function(data){
            Highcharts.chart('yearly-visits-chart', {
                chart: {
                    type: 'line'
                },
                title: {
                    text: 'Number of Visitors Monthly report'
                },

                xAxis: {
                    categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                },
                yAxis: {
                    title: {
                        text: 'Total Visits(s)'
                    }
                },
                plotOptions: {
                    line: {
                        dataLabels: {
                            enabled: true
                        },
                        enableMouseTracking: false
                    }
                },
                series: [
                    {
                        name: 'Property Booking',
                        data: data
                    },
                ]
            });

            $('.yearly-visits-chart').css('display', 'none');

        },
        yearlyAmountChart:function(data){
            Highcharts.chart('yearly-amount-chart', {
                chart: {
                    type: 'line'
                },
                title: {
                    text: 'Amount Earned Monthly report'
                },

                xAxis: {
                    categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                },
                yAxis: {
                    title: {
                        text: 'Total Amount(s)'
                    }
                },
                plotOptions: {
                    line: {
                        dataLabels: {
                            enabled: true
                        },
                        enableMouseTracking: false
                    }
                },
                series: [
                    {
                        name: 'Property Booking',
                        data: data
                    },
                ]
            });

            $('.container').css('display', 'none');

        },
        lastVisitsChart: function(data){
            $('#last-visits-chart').highcharts({
                title: {
                  text: 'Last Property Booking Report',
                },
                xAxis: {
                  type: 'datetime'
                },
                yAxis: {
                    title: {
                        text: 'Total Visits(s)'
                    }
                },
                series: [{
                  name: 'Visits',
                  data:  data
                  }]
            });
        },
        lastAmountChart: function(data){
            $('#last-amount-chart').highcharts({
                title: {
                  text: 'Latest Booking Report',
                },
                subtitle: {
                    text: 'Total Amount Generated on Last Visits Report'
                },
                xAxis: {
                  type: 'datetime'
                },
                yAxis: {
                    title: {
                        text: 'Total Amount(s)'
                    }
                },
                series: [{
                  name: 'Total',
                  data:  data
                  }]
            });
        }
    },
    mounted:function(){
        axios.defaults.xsrfHeaderName = "X-CSRFToken"
        axios.defaults.xsrfCookieName = 'csrftoken'

        this.getOccupiedRooms();
    /* initailize chart */
        this.$http.get($('.pageUrls').data('listurl'))
            .then(function(data){
                /* decode json response */
                data = JSON.parse(data.bodyText);

                /* 1.1 get yearly visits */
                this.items = data.results.yearly_visits;
                /* render chart */
                this.yearlyVisitsChart(this.items);

                /* 1.2 get yearly visits */
                this.items = data.results.yearly_amount;
                /* render chart */
                this.yearlyAmountChart(this.items);

                /* 2. get last visits */
                var obj = data.results.last_visits;
                var temp = [];
                 Object.keys(obj).forEach(function(key) {
                    var temp2 = [moment.utc(obj[key].date).valueOf(),parseInt(obj[key].total)];
                    temp.push(temp2);
                });
                /* render chart */
                this.lastVisitsChart(temp);

                /* 3. get last booking total prices */
                var obj = data.results.last_amount;
                var temp = [];
                 Object.keys(obj).forEach(function(key) {
                    var temp2 = [moment.utc(obj[key].date).valueOf(),parseInt(obj[key].total)];
                    temp.push(temp2);
                });
                /* render chart */
                this.lastAmountChart(temp);

                this.loader = false;
            }, function(error){
                this.server_error = true
                console.log(error.statusText);
        });

    },
});
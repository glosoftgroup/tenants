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
    el:"#summary-app",
    delimiters: ['${', '}'],
    data:{
       name: 'Book Listing',
       items: [],
       bill_type_summary: [],
       loader:true,
       check_in: moment().format('YYYY-MM'),
       check_out: moment().add(2, 'M').format('YYYY-MM'),
       server_error: false,
       exportType: 'none',
       total_occupied: 0,
       total_empty: 0,
       pending_rent: 0,
       paid_rent: 0,
       chartData: []
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
            var url = '/dashboard/room/summary/'+pk+'/';
            if(this.check_in)
                url += '?start_date='+this.check_in+'-01';
            if(this.check_out)
                url += '&end_date='+this.check_out+'-28';
            api(url)
            .then(function(response){
                response = response.data.results;
                vm.bill_type_summary = response.bill_types_summary;
                vm.total_empty = response.total_empty;
                vm.total_occupied  = response.total_occupied;
                vm.pending_rent = response.pending_rent;
                vm.paid_rent = response.paid_rent;

                var data = []; // [['X-Small', 5], ['Small', 27]]
                vm.bill_type_summary.map((value, key)=>{

                data.push(
                [vm.bill_type_summary[key].type+' paid',
                 vm.bill_type_summary[key].paid],
                [vm.bill_type_summary[key].type+' pending', vm.bill_type_summary[key].pending]
                )
            })
            console.log(data)
            vm.chartData = data;


            })
            .catch(function(error){
                console.error(error);
            })
        },
        exportItems:function(){
        /* take care  of excel and pdf exports on filter panel */
            if(this.exportType == 'excel'){
                JSONToCSVConvertor(this.items, "Booking Report", true);
            }
            if(this.exportType == 'pdf'){
                $("#summary-app").printThis({
                    debug: false, // show the iframe for debugging
                    importCSS: true, // import page CSS
                    importStyle: true, // import style tags
                    printContainer: true, // grab outer container as well as the contents of the selector
                    loadCSS: "my.css", // path to additional css file - us an array [] for multiple
                    pageTitle: "Tenant Reservation Summary Report", // add title to print page
                    removeInline: false, // remove all inline styles from print elements
                    printDelay: 333, // variable print delay
                    header: null, // prefix to html
                    formValues: true //preserve input/form values)
                });
            }

        }
    },
    mounted:function(){
        axios.defaults.xsrfHeaderName = "X-CSRFToken"
        axios.defaults.xsrfCookieName = 'csrftoken'

        this.getOccupiedRooms();


    },
});

//convert csv to excel
function JSONToCSVConvertor(JSONData, ReportTitle, ShowLabel) {
    //If JSONData is not an object then JSON.parse will parse the JSON string in an Object
    var arrData = typeof JSONData != 'object' ? JSON.parse(JSONData) : JSONData;

    var CSV = '';
    //Set Report title in first row or line

    CSV += ReportTitle + '\r\n\n';

    //This condition will generate the Label/Header
    if (ShowLabel) {
        var row = "";

        //This loop will extract the label from 1st index of on array
        for (var index in arrData[0]) {

            //Now convert each value to string and comma-seprated
            row += index + ',';
        }

        row = row.slice(0, -1);

        //append Label row with line break
        CSV += row + '\r\n';
    }

    //1st loop is to extract each row
    for (var i = 0; i < arrData.length; i++) {
        var row = "";

        //2nd loop will extract each column and convert it in string comma-seprated
        for (var index in arrData[i]) {
            row += '"' + arrData[i][index] + '",';
        }

        row.slice(0, row.length - 1);

        //add a line break after each row
        CSV += row + '\r\n';
    }

    if (CSV == '') {
        alert("Invalid data");
        return;
    }

    //Generate a file name
    var fileName = "MyReport_";
    //this will remove the blank-spaces from the title and replace it with an underscore
    fileName += ReportTitle.replace(/ /g,"_");

    //Initialize file format you want csv or xls
    var uri = 'data:text/csv;charset=utf-8,' + escape(CSV);

    // Now the little tricky part.
    // you can use either>> window.open(uri);
    // but this will not work in some browsers
    // or you will not get the correct file extension

    //this trick will generate a temp <a /> tag
    var link = document.createElement("a");
    link.href = uri;

    //set the visibility hidden so it will not effect on your web-layout
    link.style = "visibility:hidden";
    link.download = fileName + ".csv";

    //this part will append the anchor tag and remove it after automatic click
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
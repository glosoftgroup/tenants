$ = jQuery;
var $pagination = $('.bootpag-callback');
var $modal = $('#modal_instance');
var $deleteModal = $('#modal_delete');
var date;

/* datepicker component */
var vp = Vue.component('date-picker', {
    template: '<input class="form-control" />',
    props: [ 'format', 'type' ],
    mounted: function() {
        var self = this;
        $(this.$el).datepicker({
            autoclose: true,
            minViewMode: "months",
            format: self.format
        }) .on('changeDate', function(e){
            var type = self.type;
            if(type === 'month-to'){
                var end_date = new Date(e.date.getFullYear(), e.date.getMonth() + 1, 0)
                var day = String(end_date.getDate());
                var month = String(end_date.getMonth()+1).length === 1 ? 
                            '0'+String(end_date.getMonth()+1) : 
                            String(end_date.getMonth()+1);
                var year = String(end_date.getFullYear());
                var date  = end_date.getFullYear()+'-'+month+'-'+day;
            }else{
                var month = String(e.date.getMonth()+1).length === 1 ? 
                '0'+String(e.date.getMonth()+1) : 
                String(e.date.getMonth()+1);
                var year  = String(e.date.getFullYear());
                var date  = e.date.getFullYear()+'-'+month+'-'+'01';
            }
            var display = $(this).val();

            self.$emit('update-date', {type, date, month, year, display});
        });
    },
    beforeDestroy: function() {
      $(this.$el).datepicker('hide').datepicker('destroy');
    }
  });

  
Vue.config.devtools = true
//vue
var parent = new Vue({
    el:"#vue-app",
    delimiters: ['${', '}'],
    data:{
       name: 'Listing',
       items: [],
       loader: true,
       totalPages: 1,
       visiblePages: 4,
       page_size: 10,
       search: '',
       status: 'all',
       exportType: 'none',
       date: 'Select date',
       period:'',
       property:'',
       totalTax:'0.00',
       totalAmount:'0.00',
       totalIncome:'0.00',
       detailUrl: '',
       filter:{
           month:true,
           range:false,
           display_name:'MONTH'
       },
       singleMonth:{
            month:'',
            year:'',
            display:''
        },
       monthFrom:{
           date:'',
           month:'',
           year:'',
           display:''
       },
       monthTo:{
            date:'',
            month:'',
            year:'',
            display:''
        },
        room:{
            id:'',
            name:''
        }
    },
    mounted:function(){
        var self = this;
        $.get($('.pageUrls').data('listurl'), function(data)
        {
            self.loader = false;
            self.items = data.results;
            self.totalPages = data.total_pages;
            self.pagination(data.total_pages);
            self.totalTax = (parseFloat(data.totalTax)).toFixed(2);
            self.totalAmount = (parseFloat(data.totalAmount)).toFixed(2);
            self.totalIncome = (parseFloat(data.totalAmount) - parseFloat(data.totalTax)).toFixed(2);
            self.period = data.period;
            self.property = data.property;
            self.detailUrl = data.results.length >= 1 ? data.results[0].detail_url : '';
        }).fail(function(data) {
            self.loader = false;
            self.items = '';
            self.totalTax = '';
            self.totalAmount = '';
            self.totalIncome = '';
            self.alert("!Oops, "+ 
                "please reload the page to get data! "+
                "if problem persists contact the admin", "bg-danger")
        });
    },
    methods:{
        clearRangeMonth:function(){
            var self = this;
            self.monthFrom.date = '';
            self.monthFrom.month = '';
            self.monthFrom.year = '';
            self.monthFrom.display = '';

            self.monthTo.date = '';
            self.monthTo.month = '';
            self.monthTo.year = '';
            self.monthTo.display = '';
        },
        clearSingleMonth:function(){
            var self = this;
            self.singleMonth.month = ''
            self.singleMonth.year = '';
        },
        updateDate: function(data) {
            var self = this;

            if(data.type === 'single-month'){
                self.clearRangeMonth();
                self.singleMonth.month = data.month;
                self.singleMonth.year = data.year;
                self.singleMonth.display = data.display;
            }else if(data.type === 'month-from'){
                self.monthFrom.date = data.date;
                self.monthFrom.month = data.month;
                self.monthFrom.year = data.year;
                self.monthFrom.display = data.display;
                self.clearSingleMonth();
            }else if(data.type === 'month-to'){
                self.monthTo.date = data.date;
                self.monthTo.month = data.month;
                self.monthTo.year = data.year;
                self.monthTo.display = data.display;
                self.clearSingleMonth();
            }

            var month_from = parseInt(self.monthFrom.month);
            var year_from = parseInt(self.monthFrom.year);

            var month_to = parseInt(self.monthTo.month);
            var year_to = parseInt(self.monthTo.year);
            /* conditions */
            var periods_not_null = (year_to != ''|| year_from != '');
            var endperiod_is_less_than_startperiod = ((year_to < year_from) || 
                        ((year_to == year_from ) && (month_to < month_from)));
            var not_condition =  periods_not_null && endperiod_is_less_than_startperiod;
            
            if(data.type == 'single-month'){
                var url = String($('.pageUrls').data('listurl'))
                        +'?month='+self.singleMonth.month
                        +'&year='+self.singleMonth.year
                        +'&property='+self.room.name;
                /* get data for a single month */
                $.get(url, function(data)
                {
                    self.period = self.singleMonth.display;
                    self.property = data.property;
                    self.loader = false;
                    self.items = data.results;
                    self.totalPages = data.total_pages;
                    self.pagination(data.total_pages);
                    self.totalTax = (parseFloat(data.totalTax)).toFixed(2);
                    self.totalAmount = (parseFloat(data.totalAmount)).toFixed(2);
                    self.totalIncome = (parseFloat(data.totalAmount) - parseFloat(data.totalTax)).toFixed(2);
                    self.detailUrl = data.results.length >= 1 ? data.results[0].detail_url : '';
                }).fail(function(data) {
                    self.period = '';
                    self.loader = false;
                    self.items = '';
                    self.totalTax = '';
                    self.totalAmount = '';
                    self.totalIncome = '';
                    self.alert("!Oops, "+ 
                        "please reload the page to get data! "+
                        "if problem persists contact the admin", "bg-danger")
                });

            }else{
                /* get data for the month range */
                if(not_condition){
                    self.alert('End period cannot be less than Start period', 'bg-danger');
                    return;
                }
                if ((self.monthFrom.date != '' && self.monthTo.date != '')){
                    var url = String($('.pageUrls').data('listurl'))
                        +'?month_from='+self.monthFrom.date
                        +'&month_to='+self.monthTo.date
                        +'&property='+self.room.name;
                    /* get data for a single month */
                    $.get(url, function(data)
                    {
                        if(self.monthFrom.display == self.monthTo.display){
                            self.period = self.monthFrom.display
                        }else{
                            self.period = String(self.monthFrom.display)+
                            ' \xa0\xa0\xa0\xa0\xa0\xa0\xa0 - \xa0\xa0\xa0\xa0\xa0\xa0\xa0 '+ 
                            String(self.monthTo.display)
                        }
                        self.property = data.property;
                        self.loader = false;
                        self.items = data.results;
                        self.totalPages = data.total_pages;
                        self.pagination(data.total_pages);
                        self.totalTax = (parseFloat(data.totalTax)).toFixed(2);
                        self.totalAmount = (parseFloat(data.totalAmount)).toFixed(2);
                        self.totalIncome = (parseFloat(data.totalAmount) - parseFloat(data.totalTax)).toFixed(2);
                        self.detailUrl = data.results.length >= 1 ? data.results[0].detail_url : '';
                    }).fail(function(data) {
                        self.period = '';
                        self.loader = false;
                        self.items = '';
                        self.totalTax = '';
                        self.totalAmount = '';
                        self.totalIncome = '';
                        self.alert("!Oops, "+ 
                            "please reload the page to get data! "+
                            "if problem persists contact the admin", "bg-danger")
                    });
                }
            }
            
        },
        alert:function(msg,status='bg-success',header=null)
            { $.jGrowl(msg,{header: header,theme: status}); 
        },
        toggleDateFilter(name){
            this.filter.display_name = name;
            if(name == "RANGE"){
                this.filter.range = true
                this.filter.month = false
            }else{
                this.filter.range = false
                this.filter.month = true
                this.clearRangeMonth();
            }
        },
        goTo: function(url){
            window.location.href = url;
        },
        deleteInstance: function(url,id){
            // open delete modal and set delete url
            // ___________________
            // var deleteUrl = this.deleteUrl;
            var self = this;
            if(url){
                $('#modal_delete').modal();
                self.deleteUrl = url;
                self.deleteId = id;
                return;
            }

            if(!self.deleteUrl){
                $('#modal_delete').modal();
                self.deleteUrl = url;
                self.deleteId = id;
                return;
            }else{
                axios.defaults.xsrfHeaderName = "X-CSRFToken"
                axios.defaults.xsrfCookieName = 'csrftoken'
                
                axios.delete(self.deleteUrl)
                .then(function (response) {
                    alertUser('Data deleted successfully');
                    // hide modal & remove item
                    $('#modal_delete').modal('hide');
                    // this.removeItem();
                    console.log($('#'+self.deleteId).html());
                    $('#'+self.deleteId).html('').remove();
                    self.deleteUrl = false;
                    self.deleteId = false;
                })
                .catch(function (error) {
                    // display error from serializer valueError
                    if(error.response.data[0]){
                        alertUser(error.response.data[0], 'bg-danger','Error!');
                        $('#modal_delete').modal('hide');
                    }

                });
                
            }
        },
        inputChangeEvent:function(){
            /* make api request on events filter */
            var self = this;
            if( self.monthFrom.date == ''){
            var url = String($('.pageUrls').data('listurl'))
                        +'?month='+self.singleMonth.month
                        +'&year='+self.singleMonth.year
                        +'&q='+self.search;
            }else{
            var url = String($('.pageUrls').data('listurl'))
                        +'?month_from='+self.monthFrom.date
                        +'&month_to='+self.monthTo.date
                        +'&q='+self.search;
            }

            $.get(url, function(data)
            {
                self.property = data.property;
                self.loader = false;
                self.items = data.results;
                self.totalPages = data.total_pages;
                self.pagination(data.total_pages);
                self.totalTax = (parseFloat(data.totalTax)).toFixed(2);
                self.totalAmount = (parseFloat(data.totalAmount)).toFixed(2);
                self.totalIncome = (parseFloat(data.totalAmount) - parseFloat(data.totalTax)).toFixed(2);
                self.detailUrl = data.results.length >= 1 ? data.results[0].detail_url : '';
            }).fail(function(error) {
                console.log(error)
                self.period = '';
                self.loader = false;
                self.items = '';
                self.totalTax = '';
                self.totalAmount = '';
                self.totalIncome = '';
                self.alert("!Oops, "+ 
                    "please reload the page to get data! "+
                    "if problem persists contact the admin", "bg-danger")
            });
        },
        listItems:function(num){
        /* make api request when pagination pages are clicked */
            if(this.date == 'Select date'){
                date = '';
            }else{ date = this.date; }
            this.$http.get($('.pageUrls').data('listurl')+'?page='+num+'&page_size='+this.page_size+'&status='+this.status+'&date='+date)
                .then(function(data){
                    this.loader = false;
                    data = JSON.parse(data.bodyText);
                    this.items = data.results;
                }, function(error){
                    console.log(error.statusText);
            });
        },
        removeItem(index) {
          this.items.splice(index, 1);
        },
        exportItems:function(){
        /* take care  of excel and pdf exports on filter panel */
            if(this.exportType == 'excel'){
                JSONToCSVConvertor(this.items, "Booking Report", true);
            }
            if(this.exportType == 'pdf'){
                $("#printme").printThis({
                    debug: false, // show the iframe for debugging
                    importCSS: true, // import page CSS
                    importStyle: true, // import style tags
                    printContainer: true, // grab outer container as well as the contents of the selector
                    loadCSS: "my.css", // path to additional css file - us an array [] for multiple
                    pageTitle: "Room Booking Report", // add title to print page
                    removeInline: false, // remove all inline styles from print elements
                    printDelay: 333, // variable print delay
                    header: null, // prefix to html
                    formValues: true //preserve input/form values)
                });
            }

        },
        pagination: function(val){
        /* include twbsPagination on vue app */
            var self=this ;
            /* restructure pagination */
            $('.bootpag-callback').twbsPagination({
                totalPages: parseInt(val),
                visiblePages: this.visiblePages,
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
    watch: {
        'room.id':function(val, oldVal){
            var self = this;
            if(val == ''){
                self.room.name = '';
            }
        },
        'room.name':function(val, oldVal){
            console.log(val)
            /* make api request on events filter */
            var self = this;
            var url = String($('.pageUrls').data('listurl'))
                        +'?month_from='+self.monthFrom.date
                        +'&month_to='+self.monthTo.date
                        +'&month='+self.singleMonth.month
                        +'&year='+self.singleMonth.year
                        +'&property='+self.room.name;

            $.get(url, function(data)
            {
                self.property = data.property;
                self.loader = false;
                self.items = data.results;
                self.totalPages = data.total_pages;
                self.pagination(data.total_pages);
                self.totalTax = (parseFloat(data.totalTax)).toFixed(2);
                self.totalAmount = (parseFloat(data.totalAmount)).toFixed(2);
                self.totalIncome = (parseFloat(data.totalAmount) - parseFloat(data.totalTax)).toFixed(2);
                self.detailUrl = data.results.length >= 1 ? data.results[0].detail_url : '';
            }).fail(function(error) {
                self.period = '';
                self.loader = false;
                self.items = '';
                self.totalTax = '';
                self.totalAmount = '';
                self.totalIncome = '';
                self.alert("!Oops, "+ 
                    "please reload the page to get data! "+
                    "if problem persists contact the admin", "bg-danger")
            });
        },
        'monthFrom.date':function(val, oldVal){
            if(val == ''){
                var self = this;
                $.get($('.pageUrls').data('listurl'), function(data)
                {
                    self.loader = false;
                    self.items = data.results;
                    self.totalPages = data.total_pages;
                    self.pagination(data.total_pages);
                    self.totalTax = (parseFloat(data.totalTax)).toFixed(2);
                    self.totalAmount = (parseFloat(data.totalAmount)).toFixed(2);
                    self.totalIncome = (parseFloat(data.totalAmount) - parseFloat(data.totalTax)).toFixed(2);
                }).fail(function(data) {
                    self.loader = false;
                    self.items = '';
                    self.totalTax = '';
                    self.totalAmount = ''
                    self.totalIncome = '';
                    self.alert("!Oops, "+ 
                        "please reload the page to get data! "+
                        "if problem persists contact the admin", "bg-danger")
                });
            }
        },
        /* listen to app data changes and restructure pagination when page size changes */
        'date': function(val, oldVal){
            this.inputChangeEvent();
        },
    	'totalPages': function(val, oldVal){
            var self=this ;
            /* destroy pagination on page size change */
            $('.bootpag-callback').twbsPagination('destroy');

            /* restructure pagination */
            $('.bootpag-callback').twbsPagination({
                totalPages: parseInt(val),
                visiblePages: this.visiblePages,
                prev: '<span aria-hidden="true">&laquo;</span>',
                next: '<span aria-hidden="true">&raquo;</span>',
                onPageClick: function (event, page) {
                    $('.pages-nav').text('Page ' + page + ' of '+self.totalPages);
                }
            }).on('page',function(event,page){
                self.listItems(page);
            });
        }
    }

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

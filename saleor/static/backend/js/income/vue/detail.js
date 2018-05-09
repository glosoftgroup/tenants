/**
    uncomment the below line on development mode
    plugin required vuejs in mozilla or chrome
    url:https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/
**/

Vue.config.devtools = true
var parent = new Vue({
    el:"#vue-app",
    delimiters: ['${', '}'],
    data:{
        /* filters */
        items:'',
        totalTax:'',
        totalAmount:'',
        totalIncome:'',
        period:'',
        property:'',
        months:[
            "January", "February", "March", "April", 
            "May", "June", "July", "August", 
            "September", "October", "November", "December"
        ]
    },
    mounted:function(){
        var self = this,
            url = $('.requestData').data('url'),
            month = $('.requestData').data('month'),
            year = $('.requestData').data('year'),
            month_from = $('.requestData').data('month_from'),
            month_to = $('.requestData').data('month_to'),
            property = $('.requestData').data('property'),
            date_from = String(self.months[(new Date(month_from)).getMonth()])+' '+String((new Date(month_from)).getFullYear()),
            date_to = String(self.months[(new Date(month_to)).getMonth()])+' '+String((new Date(month_to)).getFullYear()),
            date = month ? String(self.months[parseInt(month)-1 ])+' '+String(year) : '';

            url = year != '' ? 
                '/billpayment/income/api/list/?month='+month+'&year='+year+'&property='+property : 
                '/billpayment/income/api/list/?month_from='+month_from+'&month_to='+month_to+'&property='+property;
            console.log(url);
            var date_period = month_from ? date_from+' \xa0\xa0\xa0\xa0\xa0\ - \xa0\xa0\xa0\xa0\xa0'+date_to : (date ? date : '');
            self.period = date_period;

        $.get(url, function(data)
        {
            self.items = data.results;
            self.totalTax = (parseFloat(data.totalTax)).toFixed(2);
            self.totalAmount = (parseFloat(data.totalAmount)).toFixed(2);
            self.totalIncome = (parseFloat(data.totalAmount) - parseFloat(data.totalTax)).toFixed(2);
            if(data.results.length > 1){
                var period = String(data.results[0].period)+' - '+ String(data.results[data.results.length - 1].period);
                self.period = (self.period == '') ? (period) : (self.period);
                self.property = property;
            }else{
                var period = String(data.results[0].period);
                self.period = (self.period == '') ? (period) : (self.period);
                self.property = property;
            }
        }).fail(function(data) {
            self.alert("!Oops, "+ 
                "please reload the page to get data! "+
                "if problem persists contact the admin", "bg-danger")
        });

    },
    methods:{
        alert: function(msg,status='bg-success',header=null){ 
            $.jGrowl(msg,{header: header,theme: status}); 
        },
        exportItems:function(){
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
    watch:{

    }
})

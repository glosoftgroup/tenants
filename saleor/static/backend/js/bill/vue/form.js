/* for the form validation using vuejs */
Vue.use(VeeValidate);
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
    	tenant:{
    		id:'',
    		name:''
    	},
    	property:{
    		id:'',
    		name:''
    	},
    	billtype:{
    		id:'',
    		name:'',
            tax:''
		},
		invoice_number:'',
    	description:'',
    	amount:'',
    	month:'',
    	monthDisplay:'',
    	updateUrl:'',
    	tax:'',
    	is_taxable:false,
        tenantsList:[],
    	billTypesList:[],
    	status:'pending'
    },
    mounted:function(){
    		var self = this;

    		/* get update data */
    		var updateUrl = $('.updateUrl').val();
			if(updateUrl){
				self.updateUrl = updateUrl;
				self.invoice_number = $('.edit_invoice_number').val();
				self.billtype.id = $('.edit_billtype_id').val();
				self.billtype.name = $('.edit_billtype_name').val();
				self.billtype.tax = $('.edit_billtype_tax').val();
				self.amount = $('.edit_amount').val();
				self.tax = $('.edit_tax').val();
				self.is_taxable = $('.edit_is_taxable').val() == 'true' ? true : false;
				self.property.id = $('.edit_room_id').val();
				self.property.name = $('.edit_room_name').val();
				self.tenant.id = $('.edit_customer_id').val();
				self.tenant.name = $('.edit_customer_name').val();
				self.month = $('.edit_month').val();
				self.monthDisplay = $('.edit_monthDsiplay').val();
                self.description = $('.edit_description').val();
				self.status = $('.edit_status').val();
			}

    		/* datepicker month (mode) plugin initialization */
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
		    });

		    /* load tenants options from the bill apis */
		    var tenantSelect = $('.tenants');
	        var url          = tenantSelect.attr('data-url');
	        var tenantList   = [];
            $.get(url, function(data)
	        {
	        	self.tenantsList = data.results;
	        	if(updateUrl == ''){
		        	self.tenant.id     = data.results[0].customer.id
		        	self.tenant.name   = data.results[0].customer.name
		        	self.property.id   = data.results[0].room.id
		        	self.property.name = data.results[0].room.name
		        }

	            $.each(data.results, function(key, val)
	            {
	            	if(updateUrl && val.customer.id == self.tenant.id){
	            		tenantList.push('<option value="' + self.tenant.id + '" selected>' + self.tenant.name + '</option>')
		            }else{
		                tenantList.push('<option value="' + val.customer.id + '">' + val.customer.name + '</option>')
		            }
	            });

	            tenantSelect.html(tenantList.join(''));
	            tenantSelect.selectpicker('refresh');
	        })

            /* load billtypes options from the billtypes apis */
	        var billTypeSelect = $('.billtypes');
	        var url            = billTypeSelect.attr('data-url');
	        var billTypeList   = [];
            $.get(url, function(data)
	        {
                self.billTypesList = data.results;
	        	if(updateUrl == ''){
		        	self.billtype.id   = data.results[0].id
                    self.billtype.name = data.results[0].name
		        	self.billtype.tax = data.results[0].tax
		        }           

	            $.each(data.results, function(key, val)
	            {
	            	if(updateUrl && val.id == self.billtype.id){
		            	billTypeList.push('<option value="' + self.billtype.id + '" selected>' + self.billtype.name + '</option>')
		            }else{
		                billTypeList.push('<option value="' + val.id + '">' + val.name + '</option>')
		            }
	            });

	            billTypeSelect.html(billTypeList.join(''));
	            billTypeSelect.selectpicker('refresh');
	        })


    },
    methods:{
    	setTenantProperty: function(){
    		var selectedTenant = this.tenantsList.filter(
    			filteredTenant=>this.tenant.id==filteredTenant.customer.id
    			)
    		this.property.id   = selectedTenant[0].room.id
    		this.property.name = selectedTenant[0].room.name
    	},
        setTax: function(){
            var selectedBillType = this.billTypesList.filter(
                filteredBillType=>this.billtype.id==filteredBillType.id
                )
            this.billtype.id   = selectedBillType[0].id
            this.billtype.name = selectedBillType[0].name
            this.billtype.tax   = selectedBillType[0].tax;
            this.tax = ( selectedBillType[0].tax * this.amount )/100;
        },
    	handleSubmit: function(event){
    		this.$validator.validateAll()
      
			if (this.errors.any()) {
				return;
			}

    		var self = this;
            var data = new FormData();

            data.append('invoice_number', '');
            data.append('customer', self.tenant.id);
            data.append('room', self.property.id);
            data.append('billtype', self.billtype.id);
            data.append('amount', self.amount);
            data.append('tax', self.tax);
            data.append('is_taxable', self.is_taxable);
            data.append('month', self.month);
            data.append('status', 'pending');
            data.append('description', self.description);

            axios.defaults.xsrfHeaderName = "X-CSRFToken";
            axios.defaults.xsrfCookieName = 'csrftoken';

            if(this.updateUrl !== ''){
                /* update if update url is not null */
                axios.put(self.updateUrl, data)
                .then(function (response) {
                    alertUser('Data updated successfully');
                    self.updateUrl = '';
                    window.location = $('.pageUrls').data('listurl')
                })
                .catch(function (error) {
                    console.log(error);
                    alertUser('Please check the fields and retry again','bg-danger','Oops!');
                });
            }else{
            	/* create if update url is null */
                axios.post($('.pageUrls').data('createurl'), data)
                .then(function (response) {
                    alertUser('Data added successfully');
                    window.location = $('.pageUrls').data('listurl')
                })
                .catch(function (error) {
                	if(error.response.status == '400'){
                		alertUser('That Bill Already Exists','bg-danger','Oops!');
                	}else{
                		alertUser('Please check the fields and retry again','bg-danger','Oops!');
                	}
                    console.log(error);
                });
            }
    	}
    },
    watch:{
        'amount':function(nvl, ovl){
            this.tax= nvl != '' ?(this.billtype.tax*nvl)/100 : this.tax;
        }
    }
})

$ = jQuery;
Vue.use(VeeValidate);
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
    		name:''
    	},
    	description:'',
    	amount:'',
    	month:'',
    	monthDisplay:'',
    	email:'',
    	updateUrl:'',
    	errors:{amount:false},
    	tenantsList:[]
    },
    mounted:function(){
    		var self = this;

    		/* get update data */
    		var updateUrl = $('.updateUrl').val();
			if(updateUrl){
				self.updateUrl = updateUrl;
				self.billtype.id = $('.edit_billtype_id').val();
				self.billtype.name = $('.edit_billtype_name').val();
				self.amount = $('.edit_amount').val();
				self.property.id = $('.edit_room_id').val();
				self.property.name = $('.edit_room_name').val();
				self.tenant.id = $('.edit_customer_id').val();
				self.tenant.name = $('.edit_customer_name').val();
				self.month = $('.edit_month').val();
				self.monthDisplay = $('.edit_monthDsiplay').val();
				self.description = $('.edit_description').val();
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
		        var year = e.date.getFullYear();

		        var date = e.date.getFullYear()+'-'+month+'-'+'01';

		        $('.monthpicker').val(date);
		        self.monthDisplay = e.date.toLocaleString('en-us', {month: "long"})+'/'+e.date.getFullYear();
		        self.month = date;
		    });
		    /* load tenants options from the bill apis */
		    var tenantSelect = $('.tenants');
	        var url    = tenantSelect.attr('data-url');
	        var tenantList   = [];
            $.get(url, function(data)
	        {
	        	self.tenantsList = data.results;
	        	if(updateUrl == ''){
		        	self.tenant.id = data.results[0].customer.id
		        	self.tenant.name = data.results[0].customer.name
		        	self.property.id = data.results[0].room.id
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
	        var url    = billTypeSelect.attr('data-url');
	        var billTypeList   = [];
            $.get(url, function(data)
	        {
	        	if(updateUrl == ''){
		        	self.billtype.id = data.results[0].id
		        	self.billtype.name = data.results[0].name
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
    		var that = this.tenantsList.filter(person=>this.tenant.id==person.customer.id)
    		this.property.id = that[0].room.id
    		this.property.name = that[0].room.name
    	},
    	handleInputChange: function(event){
    		var target = event.target;
	        var value = target.type === 'checkbox' ? target.checked : target.value;
	        var name = target.name;

	        if(isEmpty(value)){
	            this.errors[name] = "This field is required";
	        }else{
	            this.errors[name] = '';
	        }
    	},
    	handleSubmit: function(event){
    		var self = this;
            var data = new FormData();

            data.append('invoice_number', '');
            data.append('customer', self.tenant.id);
            data.append('room', self.property.id);
            data.append('billtype', self.billtype.id);
            data.append('amount', self.amount);
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
    }
})

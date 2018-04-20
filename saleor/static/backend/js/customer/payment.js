/*
***************************************************************
***************************************************************
Author         : GlosoftGroup Limited
Author URI     : https://www.glosoftgroup.com
File           : add/update.js
***************************************************************
***************************************************************/

(function ($) {
    "use strict";
    var allFunctions = {
        $window: $(window),
        el:{
            /** form field ids */
            datePaid         :  $("#date_paid"),
            amount_paid      :  $("#amount_paid"),
            showModalBtn     :  $('.showModalBtn'),

            /** modal form*/
            addForm          :  $('#payment-form'),
            paymentModal     :  $('#modal_instance'),

            /**urls */
            postUrl          :  $("#postUrl").val(),
            tenantPk         :  $("#tenantPk").val(),

            minimumBalance   :  $("#minimumBalance").val(),

            postMethod       : "POST"
        },
        populateData:{
            init:function (){
                
            }
        },
        notification:function(status, message , header){
            $.jGrowl(message, {
                header: header,
                theme: 'bg-'+status
            });
        },
        plugins:{
            init:function(){
                $('.bootstrap-select').selectpicker({
                    iconBase: 'fa',
                    addIcon:'fa-plus-circle'
                });
                allFunctions.el.datePaid.daterangepicker({
                        singleDatePicker: true,
                        locale:{format: 'YYYY-MM-DD'},
                        showDropdowns:false,
                        autoUpdateInput:false,
                        maxDate: new Date(),
                        orientation:'left'
                    },function(chosen_date) {
                        allFunctions.el.datePaid.val(chosen_date.format('YYYY-MM-DD'));

                 });

                allFunctions.el.showModalBtn.on('click',function(){
                  allFunctions.el.paymentModal.modal();
                });
            },
        },
        ajaxForms: {
            validateForm: function () {
                var minimum_amount = allFunctions.el.minimumBalance == 0 || 
                                     allFunctions.el.minimumBalance == 0 ?
                                     100000: allFunctions.el.minimumBalance
                                     ;
                jQuery.validator.addMethod("greaterThanBalance", function(value, element) {
                    return this.optional(element) || (parseFloat(value) <= minimum_amount);
                }, "* should be less than (KShs."+ minimum_amount +" )");

                allFunctions.el.addForm.validate({
                    onkeyup: function(element) {$(element).valid()},
                    rules:{
                        date_paid: {required:true},
                        amount_paid: {required:true, digits:true, greaterThanBalance : true}
                    },
                    submitHandler: function() {
                      var form = document.getElementById('payment-form'),
                          formData = new FormData(form);
                      allFunctions.ajaxForms.ajaxFormHandle(formData, form);
                    }
                  });
            },
            ajaxFormHandle: function (formData, form) {
                if (formData) {
                    var postUrl    = allFunctions.el.postUrl;
                    var postMethod = allFunctions.el.postMethod;

                    axios.defaults.xsrfHeaderName = "X-CSRFToken";
                    axios.defaults.xsrfCookieName = 'csrftoken';

                    axios.post(postUrl,formData)
                    .then(function (response) {
                       allFunctions.el.paymentModal.modal('hide');
                       if(response.status == 200 || response.status == 201){
                          allFunctions.notification("success", "Added successfully", "Well Done!");
                          allFunctions.ajaxForms.resetAddForm(form);
                          // window.location = allFunctions.el.redirectUrl;
                          window.location.reload();
                       }else{
                          allFunctions.notification("danger", data.message, "Oops!");
                       }
                    })
                    .catch(function (error) {
                        allFunctions.el.paymentModal.modal('hide');
                        allFunctions.notification("danger", error, "Oops!");;
                    });

                }
            },
            resetAddForm: function (form) {
                form.reset();
            },
        }

    }


    $(document).ready(function () {
        allFunctions.plugins.init();
        allFunctions.ajaxForms.validateForm();
    });

})(jQuery);
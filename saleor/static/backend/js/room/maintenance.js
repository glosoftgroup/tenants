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
            issue            :  $("#issue"),
            paidBySelect     :  $("#paid_by"),
            dateReported     :  $("#date_reported"),
            period           :  $("#period"),
            cost             :  $("#cost"),
            modalButton      :  $('.modalbtn'),

            /** modal form*/
            addForm          :  $('#issues-form'),
            issueModal       :  $('#issue-modal'),

            /**urls */
            postUrl          :  $("#addIssueUrl").val(),
            updatePk         : "none",

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
                allFunctions.el.dateReported.daterangepicker({
                        singleDatePicker: true,
                        locale:{format: 'YYYY-MM-DD'},
                        showDropdowns:false,
                        autoUpdateInput:false,
                        maxDate: new Date(),
                        orientation:'left'
                    },function(chosen_date) {
                        allFunctions.el.dateReported.val(chosen_date.format('YYYY-MM-DD'));

                 });


                $('.input-group').on('change', '.sel', function(){
                   var $thisVal = $(this).val();
                   if($thisVal == 'add'){
                         var selected = $(this).find('option:selected'),
                             url = selected.data('href'),
                             prompt_text = selected.data('title'),
                             modal = selected.data('ta'),
                             select = selected.data('select'),
                             cat = selected.data('cat'),
                             label = selected.data('label');

                         allFunctions.plugins.modaldetails(
                                      label, url, select,
                                      prompt_text, cat, modal
                                      );
                   }

                });

                $('#is_taxable').change(function(){
                     if($(this).is(':checked')){
                          $(this).val('True');
                     }else{
                          $(this).val('False');
                     }
                });

                allFunctions.el.modalButton.on('click',function(){
                  allFunctions.el.issueModal.modal();
                });
            },
        },
        ajaxForms: {
            validateForm: function () {
                allFunctions.el.addForm.validate({
                    onkeyup: function(element) {$(element).valid()},
                    rules:{
                        date_reported: {required:true},
                        cost:{required:true, digits:true},
                        issue: {required:true}
                    },
                    submitHandler: function() {
                      var form = document.getElementById('issues-form'),
                          formData = new FormData(form);
                          formData.append('is_taxable', $('#is_taxable').val());
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

                    if(allFunctions.el.updatePk == "none"){
                        axios.post(postUrl,formData)
                        .then(function (response) {
                           allFunctions.el.issueModal.modal('hide');
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
                            allFunctions.el.issueModal.modal('hide');
                            allFunctions.notification("danger", error, "Oops!");;
                        });
                    }else{
                      console.log('update')
                        // axios.put(postUrl, formData)
                        // .then(function (response) {
                        //    allFunctions.el.issueModal.modal('hide');
                        //    if(response.status == 200 || response.status == 201){
                        //       allFunctions.notification("success", "Updated successfully", "Well Done!");
                        //       window.location = allFunctions.el.redirectUrl;
                        //    }else{
                        //       allFunctions.notification("danger", data.message, "Oops!");
                        //    }
                        // })
                        // .catch(function (error) {
                        //     allFunctions.el.issueModal.modal('hide');
                        //     allFunctions.notification("danger", error, "Oops!");;
                        // });

                    }

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
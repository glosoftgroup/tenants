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
            revealTopicBtn   :  $("#reveal-topic-btn"),
            cancelTopicBtn   :  $("#cancel-topic-btn"),
            addForm          :  $('#addForm'),
            subject          :  $("#subject"),
            topic            :  $("#topic"),
            subtopic         :  $("#subtopic"),
            period           :  $("#period"),
            objective        :  $("#objective"),
            competencies     :  $("#competencies"),
            values           :  $("#values"),
            /** modal form*/
            subjectForm      :  $('#subjectForm'),

            //elements
            subjectSelect    :  $("#subject"),

            //urls
            subjectUrl       :  $("#subjectUrl").val(),
            redirectUrl      :  $("#redirectUrl").val(),
            postUrl          :  $('#postUrl').val(),
            postMethod       :  $('#postMethod').val(),

            updatePk         :  $("#pk").val(),
            subjectPk        :  $("#subjectPk").val(),
            subjectStatus    :  $("#subjectStatus")
        },
        populateData:{
            init:function (){
                $.get(allFunctions.el.subjectUrl, function (response){
                    var streamOptions = response.results;

                    if(streamOptions != ""){

                        if(allFunctions.el.updatePk == "none"){
                            allFunctions.el.subjectSelect.find('option').not(':first').remove();
                            $.each(streamOptions,function(key, value){
                                allFunctions.el.subjectSelect.append('<option value=' + value['id'] + '>' + value['name'] + '</option>');
                            });
                        }else{
                            allFunctions.el.subjectSelect.find('option').not(":nth-child(1)").not(":nth-child(2)").remove();
                            $.each(streamOptions,function(key, value){
                                if(value['id'] != allFunctions.el.subjectPk){
                                    allFunctions.el.subjectSelect.append('<option value=' + value['id'] + '>' + value['name'] + '</option>');
                                }
                            });
                        }

                        allFunctions.el.subjectSelect.append(
                                    '<option value="add"'+
                                            'data-icon="fa-plus-circle"'+
                                            'data-ta="#subject_modal_instance"'+
                                            'data-title="Add New Subject"'+
                                            'data-select="#subjects"'+
                                            'data-href="/subject/api/create/"'+
                                            'data-cat="name" data-label="Subject Name:">'+
                                        'add new subject'+
                                    '</option>'
                        );

                        allFunctions.el.subjectSelect.selectpicker('refresh');
                        if(allFunctions.el.subjectStatus.val() == "true"){
                            if(allFunctions.el.updatePk == "none"){
                                allFunctions.el.subjectSelect.val(
                                    allFunctions.el.subjectSelect.find('option').eq(1).val()
                                );
                            }else{
                                allFunctions.el.subjectSelect.val(
                                    allFunctions.el.subjectSelect.find('option').eq(2).val()
                                );
                            }
                            allFunctions.el.subjectSelect.selectpicker('refresh');
                        }



                    }

                });
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

                $('.modal-trigger').on('click', function (e) {

                    var url = $(this).data('href'),
                        prompt_text = $(this).data('title'),
                        modal = $(this).data('ta'),
                        select = $(this).data('select'),
                        cat = $(this).data('cat'),
                        label = $(this).data('label');

                     allFunctions.plugins.modaldetails(
                                      label, url, select,
                                      prompt_text, cat, modal
                                      );
                });

                allFunctions.el.revealTopicBtn.click(function(){
                    $("#topic-div").slideToggle( "slow" );
                });
                allFunctions.el.cancelTopicBtn.click(function(){
                    $("#topic-div").slideToggle( "slow" );
                });
            },
            modaldetails: function(label, url, select, prompt_text, cat, modal){
                $('.cat_label').html(label);
                $('.eitem-url').val(url);
                $('.eitem-select').val(select);
                $('.modal-title').html(prompt_text);
                $('.edit_class').attr('name', cat)
                $(modal).modal();
                $('.delete_form').attr('action',url);

                var form = allFunctions.el.subjectForm, validator = form.validate();
                validator.resetForm();
                form.find(".error").removeClass("error");

                $("#subjectForm input[name='" + cat + "']").rules(
                "add", {required:true}
                );
            }
        },
        ajaxForms: {
            validateForm: function () {
                allFunctions.el.addForm.validate({
                    onkeyup: function(element) {$(element).valid()},
                    rules:{
                        topic: {required:true},
                        subtopic: {required:true},
                        competencies:{required: true},
                        period:{required:true},
                        subject:{required:true},
                        objective:{required:true},
                        values:{required:true}
                    },
                    submitHandler: function() {
                      var form = document.getElementById('addForm'),
                          formData = new FormData(form);
                      allFunctions.ajaxForms.ajaxFormHandle(formData, form);
                    }
                  });
            },
            validateSubjectForm: function () {
                allFunctions.el.subjectForm.validate({
                    onkeyup: function(element) {$(element).valid()},
                    rules:{
                        category: {required:true}
                    },
                    submitHandler: function() {
                     $('#subject_modal_instance').modal('hide');
                      var form = document.getElementById('subjectForm'),
                          formData = new FormData(form),
                          postUrl = $('.eitem-url').val();

                      axios.defaults.xsrfHeaderName = "X-CSRFToken";
                      axios.defaults.xsrfCookieName = 'csrftoken';
                      allFunctions.ajaxForms.post(postUrl, formData, form);
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
                           if(response.status == 200 || response.status == 201){
                              allFunctions.notification("success", "Added successfully", "Well Done!");
                              allFunctions.ajaxForms.resetAddForm(form);
                              window.location = allFunctions.el.redirectUrl;
                           }else{
                              allFunctions.notification("danger", data.message, "Oops!");
                           }
                        })
                        .catch(function (error) {
                            allFunctions.notification("danger", error, "Oops!");;
                        });
                    }else{
                        axios.put(postUrl, formData)
                        .then(function (response) {
                           if(response.status == 200 || response.status == 201){
                              allFunctions.notification("success", "Updated successfully", "Well Done!");
                              window.location = allFunctions.el.redirectUrl;
                           }else{
                              allFunctions.notification("danger", data.message, "Oops!");
                           }
                        })
                        .catch(function (error) {
                            allFunctions.notification("danger", error, "Oops!");;
                        });

                    }

                }
            },
            post: function(postUrl, formData, form){
                axios.post(postUrl,formData)
                        .then(function (response) {
                           if(response.status == 200 || response.status == 201){
                              allFunctions.notification("success", "Added successfully", "Well Done!");
                              allFunctions.ajaxForms.resetAddForm(form);
                              allFunctions.el.subjectStatus.val("true");
                              allFunctions.populateData.init();
                           }else{
                              allFunctions.notification("danger", data.message, "Oops!");
                           }
                        })
                        .catch(function (error) {
                            allFunctions.notification("danger", error, "Oops!");;
                        });

            },
            resetAddForm: function (form) {
                form.reset();
            },
        }

    }


    $(document).ready(function () {
        allFunctions.plugins.init();
        allFunctions.populateData.init();
        allFunctions.ajaxForms.validateForm();
        allFunctions.ajaxForms.validateSubjectForm();
    });

})(jQuery);
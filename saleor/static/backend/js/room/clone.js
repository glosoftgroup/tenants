/* ------------------------------------------------------------------------------
*
*  # clone room js scripts
*
*  Specific JS code additions for G-POS backend pages
*
*  Version: 1.0
*  Latest update: Aug 19, 2017
*
* ---------------------------------------------------------------------------- */
// alertUser
function alertUser(msg,status='bg-success',header='Well done!')
{ $.jGrowl(msg,{header: header,theme: status}); }
//add productDetails
function ajaxSky(dynamicData,url,method){
  dynamicData["csrfmiddlewaretoken"]  = jQuery("[name=csrfmiddlewaretoken]").val();
  return $.ajax({
      url: url,
      type: method,
      data: dynamicData
    });

}
var dynamicData = {};

$(function() {
    /* app global */
    var roomId = 0;
    //  urls
    var pageUrls = $('.pageUrls');
    var roomsUrl = pageUrls.data('roomurl');
    var cloneUrl = '#';

   // dom selectors
   var cloneRoom = $('.clone');
   var modal = $('#modal_clone');
   var myForm = $('#cloning-form');
   var times = myForm.find('#times');
   var room = myForm.find('#room-id');
   var cloneBtn = myForm.find('#clone-btn');

   cloneRoom.on('click',function(){
        /* open modal */
        cloneUrl = $(this).data('cloneurl');
        roomId = $(this).data('pk');
        modal.modal();
   });

   cloneBtn.on('click', function(){
        /* validate */
        if(!times.val()){
            alertUser('Enter how many rooms do you want cloned', 'bg-warning','Field required');
        }
        dynamicData = {};
        dynamicData['room'] = roomId;
        dynamicData['times'] = times.val();

        ajaxSky(dynamicData, cloneUrl, 'post')
        .done(function(data){
            console.log('success!');
            window.location.reload();
        })
        .fail(function(){
            console.log('failed');
        });
   });

});
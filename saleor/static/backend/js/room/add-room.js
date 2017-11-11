/* ------------------------------------------------------------------------------
*
*  # addproduct js scripts
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
function addRoomDetails(dynamicData,url,method){
  dynamicData["csrfmiddlewaretoken"]  = jQuery("[name=csrfmiddlewaretoken]").val();
  return $.ajax({
      url: url,
      type: method,
      data: dynamicData
    });

}
var dynamicData = {};

$(function() {
    //  urls
    var pageUrls = $('.pageUrls');
    var roomUrl = pageUrls.data('roomdata');
    var getAmentiesurl = pageUrls.data('amenitiesurl');
    var addAmenitiesUrl = pageUrls.data('addamenitiesurl');

    // refresh dom elementes
    var newAmenitiesDiv = $('#add_new_amenities');
    var addNewAmBtn = $('#add_new_amenities_btn');

    // form data
    var name = $('#name');
    var description = $('#description');
    var price  = $('#price');
    var addRoomBtn = $('#add-room-btn');
    var amenities = $('.amenities');
    var new_amenities = $('.new_amenities');
    var new_amenities_btn = $('#new_amenities_btn');

    //  toggle new amenities division
    addNewAmBtn.on('click',function(){
        newAmenitiesDiv.toggle('slow');
    });

    //    add list of new amenities
    new_amenities_btn.on('click',function(){
        if(!new_amenities.val())
        {
            alertUser('Amenities required');
            return false;
        }
        dynamicData = {};
        dynamicData['track'] = 'add amenities';
        dynamicData['amenities'] = JSON.stringify(new_amenities.val());

        addRoomDetails(dynamicData, addAmenitiesUrl, 'POST')
        .done(function(data){
            // clear select field
            alertUser('Amenities added successfully');
            newAmenitiesDiv.toggle('slow');
            new_amenities.parents('div').find('li.token').remove();
            new_amenities.val('');
        })
        .fail(function(error){
            console.log(error);
        });

    });

    //    ./new amenities


    addRoomBtn.on('click',function(){
        if(!name.val()){
            alertUser('name required');
            return false;
        }
        if(!description.val()){
            alertUser('description required');
            return false;
        }
        if(!price.val()){
            alertUser('room type required');
            return false;
        }

        dynamicData['name'] = name.val();
        dynamicData['description'] = description.val();
        dynamicData['price'] = price.val();
        addRoomDetails(dynamicData,roomUrl,'post')
        .done(function(data){
            console.log(data);
        })
        .fail(function(error){
            console.log('error');
        });
    });

     //    take care of tokenized select field

      amenities.on('tokenize:select', function(container){
      $(this).tokenize2().trigger('tokenize:search', [$(this).tokenize2().input.val()]);
       });
      // get amenities
      amenities.tokenize2({
        placeholder: 'Select Amenities(s)',
        displayNoResultsMessage:true,
        //searchMinLength:3,
        sortable: true,
        dataSource: function(search, object){
            $.ajax(getAmentiesurl, {
                data: { search: search, start: 1, group:'users' },
                dataType: 'json',
                success: function(data){
                    var $items = [];
                    $.each(data, function(k, v){
                        $items.push(v);
                    });
                    object.trigger('tokenize:dropdown:fill', [$items]);
                }
            });
        }
    });

    //    create new amenities
     new_amenities.tokenize2({
        placeholder: 'Add Amenities(s)',
        tokensAllowCustom: true
        });
    //./tokenize


});
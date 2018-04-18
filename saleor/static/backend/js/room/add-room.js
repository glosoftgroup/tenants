/* ------------------------------------------------------------------------------
*
*  # add room js scripts
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
    var roomListUrl = pageUrls.data('roomurl');

    // refresh dom elements
    var newAmenitiesDiv = $('#add_new_amenities');
    var addNewAmBtn = $('#add_new_amenities_btn');

    // delete room
    var deleteBtn = $('#delete');
    var confirmDeleteBtn = $('#confirm-delete');

    // form data
    var dataForm = $('#room-form');
    var name = dataForm.find('#name');
    var roomId = dataForm.find('#room_id');
    var description = dataForm.find('#description');
    var price  = dataForm.find('#price');
    var addRoomBtn = dataForm.find('#add-room-btn');
    var amenities = dataForm.find('.amenities');
    var floor = dataForm.find('.floor');
    var new_amenities = dataForm.find('.new_amenities');
    var new_amenities_btn = dataForm.find('#new_amenities_btn');
    var dayTime = dataForm.find('#daytime');
    var nightly = dataForm.find('#nightly');
    var daily = dataForm.find('#daily');
    var weekly = dataForm.find('#weekly');
    var monthly = dataForm.find('#monthly');
    var bedrooms = dataForm.find('#bedrooms');
    var units = dataForm.find('#units');
    var service_charges = dataForm.find('#service_charges');
    var floor_space = dataForm.find('#floor_space');
    var wing = dataForm.find('#wing');
    var propertytype = dataForm.find('#propertytype');
    var parking_space = dataForm.find('#parking_space');

    // handle deleting a room
    deleteBtn.on('click',function(e){
        $(this).nextAll('.confirm-delete:first').html('sdfe').toggle('slow');
    });

    //  toggle new amenities division
    addNewAmBtn.on('click',function(){
        newAmenitiesDiv.toggle('slow');
    });

    //    add list of new amenities
    new_amenities_btn.on('click',function(){
        if(!new_amenities.val())
        {
            new_amenities.nextAll('.help-block:first').addClass('text-warning').html('Please Hit <span class="label label-warning">Enter</span> Key. This field is required.');
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

    // ./new amenities

    //    remove help block
    name.on('focusin',function(){
          $(this).nextAll('.help-block:first').html('');
    });
    price.on('focusin',function(){
          $(this).nextAll('.help-block:first').html('');
    });
    service_charges.on('focusin',function(){
          $(this).nextAll('.help-block:first').html('');
    });
    units.on('focusin',function(){
          $(this).nextAll('.help-block:first').html('');
    });
    floor_space.on('focusin',function(){
          $(this).nextAll('.help-block:first').html('');
    });
    wing.on('focusin',function(){
          $(this).nextAll('.help-block:first').html('');
    });
    propertytype.on('focusin',function(){
          $(this).nextAll('.help-block:first').html('');
    });
    amenities.on('focusin',function(){
          $(this).nextAll('.help-block:first').html('');
    });
    bedrooms.on('focusin',function(){
          $(this).nextAll('.help-block:first').html('');
    });
    new_amenities.on('focusin',function(){
          $(this).nextAll('.help-block:first').html('');
    });
    dayTime.on('focusin',function(){
          $(this).nextAll('.help-block:first').html('');
    });
    daily.on('focusin',function(){
          $(this).nextAll('.help-block:first').html('');
    });
    nightly.on('focusin',function(){
          $(this).nextAll('.help-block:first').html('');
    });
    weekly.on('focusin',function(){
          $(this).nextAll('.help-block:first').html('');
    });
    monthly.on('focusin',function(){
          $(this).nextAll('.help-block:first').html('');
    });

    addRoomBtn.on('click',function(e){
        e.preventDefault()
        dynamicData = {}; //clear dynamic data
        //    validation
        if(!name.val()){
            name.nextAll('.help-block:first').addClass('text-warning').html('This field is required');
            return false;
        }
        /*
        if(!floor.val())
        {
            floor.nextAll('.help-block:first').addClass('text-warning').html('This field is required');
            return false;
        }*/

        if(description.val()){
            dynamicData['description'] = description.val();
        }
        if(parking_space.val()){
            dynamicData['parking_space'] = parking_space.val();
        }
        if(roomId.val()){
            dynamicData['pk'] = roomId.val();
        }

        if(!amenities.val())
        {
            console.log('amenities invalid')
            amenities.nextAll('.help-block:first').addClass('text-warning').html('This field is required');
            return false;
        }

        if(bedrooms.val()){
            dynamicData['monthly'] = monthly.val();
        }else{
            bedrooms.nextAll('.help-block:first').addClass('text-warning').html('This field is required');
            return false;
        }

        if(service_charges.val()){
            dynamicData['service_charges'] = service_charges.val();
        }
        if(units.val()){
            dynamicData['units'] = units.val();
        }
        if(floor_space.val()){
            dynamicData['floor_space'] = floor_space.val();
        }
        if(parent.wing){
            dynamicData['wing'] = parent.wing;
        }

        if(parent.propertytype){
            dynamicData['propertytype'] = parent.propertytype;
        }
        // add dynamic post data
        dynamicData['name'] = name.val();
        dynamicData['price'] = price.val();
        dynamicData['track'] = 'add room';
        dynamicData['amenities'] = JSON.stringify(amenities.val());
        // dynamicData['floor'] = floor.val()[0];

        // post form data
        addRoomDetails(dynamicData,roomUrl,'post')
        .done(function(data){
            alertUser('Data sent successfully');
            // redirect
            window.location.href= data.edit_url; //window.location.href = roomListUrl;
        })
        .fail(function(error){
            console.log('error');
            alertUser('Choose a unique name','bg-danger','Error');
            if(!name.val()){
            name.nextAll('.help-block:first').addClass('text-warning').html('Name exists is required');
            return false;
        }
        });
    });

      // take care of tokenize2 select field

      floor.on('tokenize:select', function(container){
        $(this).tokenize2().trigger('tokenize:search', [$(this).tokenize2().input.val()]);
      });

      floor.on('tokenize:dropdown:show', function(e, value){
        floor.val('');
        floor.parents('#parent-div').find('li.token').remove();
        $(".floor option[data-type='custom']").remove();
      });

      floor.tokenize2({
        placeholder: 'Select Floor',
        tokensMaxItems:1,
        tokensAllowCustom:true,
      });

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


     dataForm.validate({
        onkeyup: function(element) {$(element).valid()},
        rules:{
            name: {
              required:true
            },
            price: {
              required: true
            },
            bedrooms: {
              required: true
            },
            propertytype: {
              required: true
            },
            daily: {
              required:true
            },
            weekly: {
              required:true
            },
            nightly: {
              required:true
            },
          }
        });

        // delete room image
        // -----------------------------------
        var deleteImage = $('.delete-image');
        var pk;
        deleteImage.on('click',function(){
            dynamicData = {};
            pk = $(this).data('pk');
            dynamicData['track'] = 'Delete room image';
            addRoomDetails(dynamicData,$(this).data('href'),'post')
            .done(function(data){
                $('#delete-image'+pk).remove();
                alertUser('Image deleted');
                console.log(data);
            })
            .fail(function(err){
                console.warn(err);
            });
        });


});
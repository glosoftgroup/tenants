/* ------------------------------------------------------------------------------
*
*  # book room js scripts
*
*  Specific JS code additions for G-POS backend pages
*
*  Version: 1.0
*  Latest update: Aug 27, 2017
*
* ---------------------------------------------------------------------------- */
// alertUser
function alertUser(msg,status='bg-success',header='Well done!')
{ $.jGrowl(msg,{header: header,theme: status}); }
//add productDetails
function ajaxsky(dynamicData,url,method){
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
    var getRoomsUrl = pageUrls.data('getroomsurl');
    var addAmenitiesUrl = pageUrls.data('instancedata');
    var roomListUrl = pageUrls.data('bookingurl');
    var computeTotalPriceUrl = pageUrls.data('computetotal');

    // refresh dom elements
    var newAmenitiesDiv = $('#add_new_amenities');
    var addNewAmBtn = $('#add_new_amenities_btn');

    // delete room
    var deleteBtn = $('#delete');
    var confirmDeleteBtn = $('#confirm-delete');

    // form data
    var name = $('#name');
    var roomId = $('#room_id');
    var description = $('#description');
    var price  = $('#price');
    var addRoomBtn = $('#add-room-btn');
    var rooms = $('.rooms');
    var totalCost = 0;

    //    remove help block
    name.on('focusin',function(){
          $(this).nextAll('.help-block:first').html('');
    });
    price.on('focusin',function(){
          $(this).nextAll('.help-block:first').html('');
    });
    rooms.on('focusin',function(){
          $(this).nextAll('.help-block:first').html('');
    });


    addRoomBtn.on('click',function(){
        dynamicData = {}; //clear dynamic data
        //    validation
        if(!name.val()){
            name.nextAll('.help-block:first').addClass('text-warning').html('This field is required');
            return false;
        }
        if(description.val()){
            dynamicData['description'] = description.val();
        }
        if(roomId.val()){
            dynamicData['pk'] = roomId.val();
        }
        if(!price.val()){
            price.nextAll('.help-block:first').addClass('text-warning').html('This field is required. Please enter a number');
            return false;
        }
        if(!rooms.val())
        {
            rooms.nextAll('.help-block:first').addClass('text-warning').html('This field is required');
            return false;
        }

        // add dynamic post data
        dynamicData['name'] = name.val();
        dynamicData['price'] = price.val();
        dynamicData['track'] = 'add room';
        dynamicData['amenities'] = JSON.stringify(rooms.val());

        // post form data
        ajaxsky(dynamicData,roomUrl,'post')
        .done(function(data){
            console.log(data);
            rooms.parents('div').find('li.token').remove();
            rooms.val('');
            window.location.href = roomListUrl;
        })
        .fail(function(error){
            console.log('error');
        });
    });

      //sends rooms id: response total cost of selected rooms
      function computeTotalPrice(roomsArr){
        dynamicData = {};
        console.log(JSON.stringify(roomsArr))
        dynamicData['rooms'] = JSON.stringify(roomsArr);
        ajaxsky(dynamicData,computeTotalPriceUrl,'post')
        .done(function(response){
            totalCost = response.price;
            price.val(response.price);
            return response.price;
        })
        .fail(function(){
         return 0;
        });
      }

     //    take care of tokenized select field
      //  show rooms on focusin
      rooms.on('tokenize:select', function(container){
         $(this).tokenize2().trigger('tokenize:search', [$(this).tokenize2().input.val()]);
      });

      rooms.on('tokenize:dropdown:hide', function(e, value){
            computeTotalPrice(rooms.val());
            console.log(rooms.val());
      });
      rooms.on('tokenize:tokens:remove',function(e, value){
            console.log(rooms.val());
            console.log('you removed');
            var arr = rooms.val();
            var index = arr.indexOf(value);

            if (index > -1) {
               arr.splice(index, 1);
            }
            computeTotalPrice(arr);
            console.log(value);
      });
      rooms.on('tokenize:tokens:change',function(e, value){
            computeTotalPrice(rooms.val());
            console.log(rooms.val());
            console.log('changed');
      });

      // get amenities
      rooms.tokenize2({
        placeholder: 'Select Room(s)',
        displayNoResultsMessage:true,
        //searchMinLength:3,
        sortable: true,
        dataSource: function(search, object){
            $.ajax(getRoomsUrl, {
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




});
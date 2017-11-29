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
function ajaxSky(dynamicData,url,method){
  dynamicData["csrfmiddlewaretoken"]  = jQuery("[name=csrfmiddlewaretoken]").val();
  return $.ajax({
      url: url,
      type: method,
      data: dynamicData
    });

}

/* global variables */
var dynamicData = {};
var today = moment().format('MM/DD/YYYY');

$(function() {
    //  urls
    var pageUrls = $('.pageUrls');
    var roomUrl = pageUrls.data('roomdata');
    var getRoomsUrl = pageUrls.data('getroomsurl');
    var getCustomerUrl = pageUrls.data('getcustomerurl');
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
    var customer = $('.customer');
    var daysId = $('#days');
    var stayDays = 0;
    var totalCost = 0;
    var pk = 0;
    var customerName = $('#c_name');
    var mobile = $('#mobile');
    var checkInDate = $('#check_in');
    var checkOutDate = $('#check_out');

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
        ajaxSky(dynamicData,roomUrl,'post')
        .done(function(data){
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
        dynamicData['rooms'] = JSON.stringify(roomsArr);
        dynamicData['days'] = daysId.val();
        ajaxSky(dynamicData,computeTotalPriceUrl,'post')
        .done(function(response){
            totalCost = response.price;
            price.val(response.price);
            return response.price;
        })
        .fail(function(){
         return 0;
        });
      }

      //  take care of tokenized select field
      //  show rooms on focusin
      rooms.on('tokenize:select', function(container){
         $(this).tokenize2().trigger('tokenize:search', [$(this).tokenize2().input.val()]);
      });

      rooms.on('tokenize:dropdown:hide', function(e, value){
            computeTotalPrice(rooms.val());
      });
      rooms.on('tokenize:tokens:remove',function(e, value){
            var arr = rooms.val();
            var index = arr.indexOf(value);

            if (index > -1) {
               arr.splice(index, 1);
            }
            computeTotalPrice(arr);
      });

      // get amenities
      rooms.tokenize2({
        placeholder: 'Select Room(s)',
        displayNoResultsMessage:true,
        tokensMaxItems:1,
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
    //    ./amenities

    /* *******************************
     *
     * customer token events handler
     *
     *********************************/

    /* change customer field detail functions */
     function setCustomer(pk){
        dynamicData = {};
        dynamicData['customer'] = pk;
        dynamicData['track'] = 'Set Customer';
        ajaxSky(dynamicData,getCustomerUrl,'get')
        .done(function(response){
            console.log(response.results);
            customerName.val(response.results.text);
            mobile.val(response.results.mobile);
        })
        .fail(function(err){
            console.log(err);
        });
     }
    /* focusin event */
    customer.on('tokenize:select', function(container){
         $(this).tokenize2().trigger('tokenize:search', [$(this).tokenize2().input.val()]);
    });

    /* on add customer */
    customer.on('tokenize:dropdown:hide', function(e, value){
            console.log(customer.val()[0]);
            pk = customer.val()[0];
            setCustomer(pk);
    });

    /* on remove customer */
    customer.on('tokenize:tokens:remove',function(e, value){
            /* clear customer details */
            customerName.val('');
            mobile.val('');
    });

    /* customer search token */
    customer.tokenize2({
        placeholder: 'Select Customer',
        displayNoResultsMessage:true,
        tokensMaxItems:1,
        //sortable: true,
        dataSource: function(search, object){
            $.ajax(getCustomerUrl, {
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

    /* *****************************
     *
     * datepicker functions
     *
     * ******************************/

    var checkIn = $('.check-in');
    var checkOut = $('.check-out');


    function getDays(start,end){
        var oneDay = 24*60*60*1000; // hours*minutes*seconds*milliseconds

        if(moment(end).isAfter(moment(start))){
            var firstDate = new Date(moment(start));
            var secondDate = new Date(moment(end));

            var diffDays = Math.round(Math.abs((firstDate.getTime() - secondDate.getTime())/(oneDay)));
            return diffDays;
        }else{
            return 0;
        }


    }

    checkIn.datepicker().on('changeDate', function(e) {
        stayDays = getDays(checkIn.val(),checkOut.val());
        daysId.val(stayDays);
        computeTotalPrice(rooms.val());
    });

    checkOut.datepicker().on('changeDate', function(e) {
        stayDays = getDays(checkIn.val(),checkOut.val());
        daysId.val(stayDays);
        computeTotalPrice(rooms.val());
    });

    /* set default dates */
    checkInDate.val(today);
    checkOutDate.val(today);

});
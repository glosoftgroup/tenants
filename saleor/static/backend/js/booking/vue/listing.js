$ = jQuery;
var $pagination = $('.bootpag-callback');
var $modal = $('#modal_instance');
//vue
var parent = new Vue({
    el:"#vue-app",
    delimiters: ['${', '}'],
    data:{
       'name':'Book Listing',
       items:[],
       totalPages:1,
       visiblePages:4,
       page_size:10,
       search:''
    },
    methods:{
        deleteBooking: function(url,id){
            /* open modal */
            $modal.modal();

            /* set dynamic form data*/
            console.log(url);
            var prompt_text = $(this).data('title');
            $('.del').attr('data-id', id);
            $('.del').attr('data-href', url);
            $('.modal-title').html(prompt_text);
            $modal.modal();
            $('.delete_form').attr('action',url);
        },
        inputChangeEvent:function(){
            var self = this;
            this.$http.get($('.pageUrls').data('bookinglisturl')+'?page_size='+self.page_size+'&q='+this.search)
                .then(function(data){
                    data = JSON.parse(data.bodyText);
                    this.items = data.results;
                    this.totalPages = data.total_pages;
                }, function(error){
                    console.log(error.statusText);
            });
        },
        listItems:function(num){
            this.$http.get($('.pageUrls').data('bookinglisturl')+'?page='+num+'&page_size='+this.page_size)
                .then(function(data){
                    data = JSON.parse(data.bodyText);
                    this.items = data.results;
                }, function(error){
                    console.log(error.statusText);
            });
        },
        pagination:function(){

        }
    },
    mounted:function(){
        this.$http.get($('.pageUrls').data('bookinglisturl'))
            .then(function(data){
                data = JSON.parse(data.bodyText);
                this.items = data.results;
                this.totalPages = data.total_pages;
            }, function(error){
                console.log(error.statusText);
        });

    },
    watch: {
    	'totalPages': function(val, oldVal){
            var self=this ;
            /* destroy pagination on page size change */
            $('.bootpag-callback').twbsPagination('destroy');

            /* restructure pagination */
            $('.bootpag-callback').twbsPagination({
                totalPages: parseInt(val),
                visiblePages: this.visiblePages,
                prev: '<span aria-hidden="true">&laquo;</span>',
                next: '<span aria-hidden="true">&raquo;</span>',
                onPageClick: function (event, page) {
                    $('.pages-nav').text('Page ' + page + ' of '+self.totalPages);
                }
            }).on('page',function(event,page){
                self.listItems(page);
            });
        }
    }

});

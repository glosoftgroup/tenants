/* for the form validation using vuejs */
Vue.use(VeeValidate);
/**
    uncomment the below line on development mode
    plugin required vuejs in mozilla or chrome
    url:https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/
**/

Vue.config.devtools = true
Vue.component('dues',{
    template:'#dues',
    delimiters: ['${', '}'],
    data(){
        return {
            test:'',
            disableSubmitButton : true,
        }
    },
    props:[
        'number'
    ],
    methods:{
        goToPay(){
            this.$emit('change','pay');
            this.$emit('shareData',this.test);
            this.disableSubmitButton = false;
        },
        submit(){
            alert('Great you have completed this project, keep learning.')
        }
    }
});

Vue.component('pay',{
    template:'#pay',
    delimiters: ['${', '}'],
    props:[
        'number'
    ],
    methods:{
        back_to_dues(){
            this.$emit('change','dues');
        }
    }
});

new Vue({
    el:'#app',
    delimiters: ['${', '}'],
    data:{
        componentName:'dues',
        nm:'erico'
    },
    methods:{
        change: function(newComp){
            this.componentName = newComp;
        },
        shareData: function(data){
            this.nm = data;
            console.log("name is "+this.nm)
        }
    }
})
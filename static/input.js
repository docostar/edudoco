var app=new Vue({
      el:"#app",
      data:{
          showResult:false
      },
      methods:{
        showInput: function(){
            this.showResult=!this.showResult
          }

      },
      delimiters: ['[[',']]']
})

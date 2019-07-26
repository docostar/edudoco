var app=new Vue({
      el:"#app",
      data:{
            right:0,
            wring:0,
            e:0,
            totalQuestion:0,
            marks:0,
            rightQNo:0,
            WrongQNo:0,
            showResult:true,
            demo:1
      },
      methods:{
        changeResult: function(){
            this.showResult=!this.showResult
            this.demo+=2
          }
      },
      delimiters: ['[[',']]']
})

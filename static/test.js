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
            showResult:false,
            demo:1,
            ans:[][],
            rightans:[11],
            total:0,
            color:""
      },
      methods:{
        changeResult: function(){
            this.showResult=!this.showResult
            this.total+=1
          }

      },
      delimiters: ['[[',']]']
})

<script>

export default {

    props: ["Content"],

    data(){
        return {
            timers: [],
            globe_timer: null,
            eve: null
        }
    },
    methods: {
        randomColor(){
            var color = "rgb("  
            var r = parseInt(64 + Math.random()*192);  
            var g = parseInt(Math.random()*192);  
            var b = parseInt(Math.random()*256);  
            color = color+r+","+g+","+b+")";  
            return color; 
        },

        Fireworks(Div, x, y){
            Div.style.backgroundColor=this.randomColor();
            document.body.appendChild(Div);  
            Div.style.position="absolute";
            Div.style.width="6px";
            Div.style.height="6px";
            Div.style.borderRadius="6px";
            Div.style.boxShadow="0 0 3px lightgray";


            Div.style.left=x+"px";
            Div.style.top=y+"px";  
            var speedX = (parseInt(Math.random()*2) == 0 ? 1 : -1)*parseInt(Math.random()*16 + 1); 
            var speedY = (parseInt(Math.random()*2) == 0 ? 1 : -1)*parseInt(Math.random()*20 + 1);
            
            var i = 3;
            var time1=setInterval(function(){  
                i+=1;
                Div.style.left=Div.offsetLeft+speedX+"px";            
                Div.style.top=Div.offsetTop+speedY+ (i) +"px";
                if(Div.offsetLeft+Div.offsetWidth>window.innerWidth 
                    || Div.offsetLeft<2 
                    || Div.offsetTop+Div.offsetHeight>window.innerHeight
                    || Div.offsetTop<2 ){  
                    Div.remove();
                    clearInterval(time1);
                }  
            }, 30);  
        },

        mouseenter(e){
            this.eve = e||window.event;
            if (this.globe_timer == null){
                this.globe_timer = setInterval(() => {
                    var evt=this.eve;
                    for(var i=0;i<88;i++){
                        var div=document.createElement("div");  
                        this.Fireworks(div,evt.pageX,evt.pageY);                  
                    }
                }, 2000);
            };
        },

        mouseleave(e){
            clearInterval(this.globe_timer);
            this.globe_timer = null;
        },

        mousemove(e){
            this.eve = e||window.event;
        }
    },

    computed:{
        is_over(){
            let temp_timers = [];
            for (var timer_idx in this.timers){
                let t = this.timers[timer_idx];
                if (t.active){
                    temp_timers.push(t);
                }
            }
            this.timers = temp_timers;
            if (temp_timers.length == 0){
                return true;
            } else {
                return false;
            }
        }
    },
}
</script>
<template>
    <div class="FireworkComponent">
        <span v-html="Content.substr(0, Content.search('Congratulation'))">
        </span>
        <span class="FireworkPart"  @mouseenter="mouseenter(e)" @mouseleave="mouseleave(e)" @mousemove="mousemove(e)" v-html="Content.substr(Content.search('Congratulation'))">
        </span>
    </div>
</template>

<style scoped>
.FireworkPart:hover{
    color: red;
    font-weight: bold;
}
</style>

<template>
    <div>
        <div class="body">
            <div style="height: 30vh; display: flex; justify-content: center; flex-direction: column;">
                <ghost :left="ghost_eye.left" :right="ghost_eye.right" :top="ghost_eye.top" :bottom="ghost_eye.bottom" ref="ghost" ></ghost>
            </div>
        </div>
        <div class="info">
            <div>
                <p>The page you were looking for is not here.</p>
                <p>Why don't you try the <a href="./">homepage</a>?</p>
            </div>
        </div>
    </div>
</template>

<script>
import ghost from '../components/404/ghost.vue';

export default{
    components:{
        ghost
    },
    
    data(){
        return {
            ghost_eye: {
                left: false,
                right: false,
                top: false,
                bottom: false
            }
        }
    },


    mounted(){
        document.onmousemove=(e) =>
		{
            let ghost_pos = this.$refs.ghost.$el.getBoundingClientRect();

            if (e.clientX > ghost_pos.x + 80){
                this.ghost_eye.right = true;
                this.ghost_eye.left = false;
            }else if (e.clientX < ghost_pos.x + 40){
                this.ghost_eye.right = false;
                this.ghost_eye.left = true;
            }else{
                this.ghost_eye.right = false;
                this.ghost_eye.left = false;
            }

            if (e.clientY < ghost_pos.y + 35){
                this.ghost_eye.top = true;
                this.ghost_eye.bottom = false;
            }else if (e.clientY > ghost_pos.y + 75){
                this.ghost_eye.top = false;
                this.ghost_eye.bottom = true;
            }else{
                this.ghost_eye.top = false;
                this.ghost_eye.bottom = false;
            }
		}
    }
}
</script>

<style scoped>
.body {
    width: 100%;
    height: 50vh;
    display: flex;
    flex-direction: column-reverse;
    justify-content: flex-start;
    align-items: center;
    background: darkslategray;
}


.body::after {
    min-width: 400px;
    text-align: center;
    content: "PAGE NOT FOUND";
    font-size: max(3vw, 35px);
    font-weight: bolder;
    background: white;
    color: transparent;
    -webkit-background-clip: text;
    height: max(2.5vw, 30px);
    position: absolute;
    top: calc(50vh - max(2.5vw, 30px));
}

.body::before {
    min-width: 400px;
    text-align: center;
    content: "PAGE NOT FOUND";
    font-size: max(3vw, 35px);
    font-weight: bolder;
    background: darkslategray;
    color: transparent;
    -webkit-background-clip: text;
    position: absolute;
    top: calc(50vh - max(2.5vw, 30px));

}

.info {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
}

.info div {
    margin-top: calc(max(2vw, 30px) + 50px);
    text-align: left;
}

.info p {
    font-size: max(2vw, 16px);
    font-weight: 600;
    color: darkslategray;
}

.info a {
    font-weight: 600;
}

</style>
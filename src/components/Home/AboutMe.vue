<script>
import authorConfig from '../../config/author.config';
import Me from '../icons/Me.vue';

export default {
    props: ['largeFont', 'smallFont'],

    components:{
        Me
    },

    data(){
        return {
            content: authorConfig.aboutMe
        }
    }
  
}
</script>

<template>
  <div class="AboutMe">
    <div class="title unselect">
        <!-- <div class="icon" :style="`width:` + this.largeFont + '; height:' + this.largeFont">
            <Me/>
        </div> -->
        <span :style="`font-size:` + this.largeFont">🐣 About Me</span>
    </div>

    <div class="content">
        <span :style="`font-size:` + this.smallFont" v-html="content"></span>
    </div>

  </div>
</template>

<style scoped>
.AboutMe {
    width: 100%;
}

.title {
    margin-bottom: 20px;
    display: flex;
    align-items: center;
}

.title span {
    font-weight: bold;
}

.icon {
    display: inline-block;
    box-sizing: content-box;
    padding-right: 10px;
}

.icon svg{
    width: 100%;
    height: 100%;
}

</style>

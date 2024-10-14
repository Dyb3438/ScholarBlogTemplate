<script>
import Like from '../icons/Like.vue';
import Like_Full from '../icons/Like_Full.vue';
import Hide from '../icons/Hide.vue';

export default {
    props: ['largeFont', 'smallFont', 'id', 'username', 'region', 'comment', 'time', 'like_num', 'uid', 'deletable'],

    components: {
        Like,
        Like_Full,
        Hide
    },

    computed: {
        escape_comment(){
            var wrapper= document.createElement('div');
            wrapper.innerHTML=this.comment;
            var divs = wrapper.getElementsByTagName('div');
            for(let id=0; id < divs.length; id++){
                let div = divs[id];
                div.style = 'display: inline-block; cursor: pointer; text-decoration: underline; color: hsl(200.02deg 95.59% 47.48%);'
            }
            return wrapper.innerHTML;
        }
    },

    watch: {
        like_num(val, old){
            if (val === "+1"){
                this.$refs.like_num_div.style = 'color: red;';
            } else {
                this.$refs.like_num_div.style = 'color: black;';
            }
        }
    },

    mounted(){
        
    },

    methods: {
        like(){
            this.$emit('like', this.uid);
        },

        hide(){
            this.$emit('hide', this.uid);
        }
    }
}
</script>

<template>
    <div class="comment_body" :style="`--smallFont:` + this.smallFont + '; --largeFont:' + this.largeFont">
        <div class="userinfo">
            <div class="id">#{{ id }}&nbsp;&nbsp;</div>
            <div class="username">{{ username }}:&nbsp;</div>
            <div class="region">(Region: {{ region }})</div>
            <div style="flex: 1; min-width: 10px;"></div>
            <div class="time">{{ time }}</div>
        </div>
        <div class="comment" v-html="escape_comment"></div>
        <div  style="text-align: right; transition: all 1s; line-height: normal;">
            <div class="likeNum" ref="like_num_div">{{ like_num }}</div>&nbsp;
            <Like style="width: calc(var(--smallFont) * 1.2); height: calc(var(--smallFont) * 1.2); vertical-align: bottom;" @click="like"></Like>
            <Hide style="width: calc(var(--smallFont) * 1.2); height: calc(var(--smallFont) * 1.2); vertical-align: bottom; margin-left: 10px" @click="hide" v-if="deletable"></Hide>
        </div>
    </div>
</template>

<style scoped>
.comment_body{
    width: 100%;
    border: 1px solid gray;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    padding: 5px;
    padding-bottom: 10px;
    animation: fadeIn 2s;
}

@keyframes fadeIn {
  0% { opacity: 0; }
  100% { opacity: 1; }
}

.userinfo {
    font-size: calc(var(--smallFont) * 0.9);
    display: flex;
    flex-direction: row;
}

.id {
    font-style: italic;
    font-weight: bold;
    align-self: end;
    flex-shrink: 0;
}

.username{
    font-weight: bold;
    align-self: end;
    text-overflow: ellipsis;
    white-space: nowrap;
    word-break: break-all;
    overflow: hidden;
}

.region {
    align-self: end;
    flex-shrink: 0;
}

.time {
    font-style: italic;
    font-size: calc(var(--smallFont) * 0.8);
    align-self: end;
    flex-shrink: 0;
}

.comment {
    padding-left: var(--smallFont);
    padding-right: var(--smallFont);
    font-size: var(--smallFont);
    word-break: break-all;
    text-align: justify
}

.likeNum {
    font-size: var(--smallFont);
    display: inline-block;
    vertical-align: bottom;
}


</style>
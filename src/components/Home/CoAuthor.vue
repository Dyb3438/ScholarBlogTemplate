<script>
import authorConfig from '../../config/author.config';

export default {
    props: ['largeFont', 'smallFont', "screenWidth"],

    components:{
    },

    data(){
        return {
            content: authorConfig.co_authors,
            number: {}
        }
    },

    computed:{
        isPC(){
            return this.screenWidth >= 800;
        }
    },

    mounted(){
        for (let name in this.content){
            this.number[name] = 0;
        }
        for (let year in authorConfig.publications){
            for (let idx in authorConfig.publications[year]){
                const publication=authorConfig.publications[year][idx];
                for (let name in this.number){
                    if (publication.author.search(name) >= 0){
                        this.number[name] += 1;
                    }
                }
            }
        }
        console.log(this.number);
    }
  
}
</script>

<template>
  <div class="CoAuthor">
    <div class="title unselect">
        <span :style="`font-size:` + this.largeFont">😘 Co-Authors</span>
    </div>

    <div class="content">
        <div class="authorList">
            <div class="author" v-for="author, name in content" :style="[author.hasOwnProperty('relationship') && author['relationship'] == 'Teacher' ? 'box-shadow: 0px 0px 7px #ffba00; border-color: rgb(255, 127, 0)' : '']">
                <div class="count">
                    {{ number[name] }}
                </div>
                <div class="head">
                    <img :src="`./imgs/co-authors/Default.png`" v-if="!author.hasOwnProperty('image') || author['image'] == ''"/>
                    <img :src="author.image" v-else/> 
                </div>
                <div class="name" style="text-align: center; font-size: var(--smallFont);">
                    <span>
                        <a :href="author.url" v-if="author.hasOwnProperty('url')"><b>{{ name }}</b></a>
                        <b v-else>{{ name }}</b>
                    </span>
                </div>
                <div class="position" style="text-align: center; font-size: var(--smallFont);">
                    <span>
                        {{ author.position }}
                    </span>
                </div>
                <div class="institute">
                    <span>
                        {{ author.institute }}
                    </span>
                </div>
            </div>
        </div>
    </div>

  </div>
</template>

<style scoped>
.CoAuthor {
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

.content {
    overflow-x: auto;
    width: 100%;
    display: flex;
}

.authorList {
    display: flex;
    flex-direction: row;
    padding: 5px 0;
}

.author {
    min-width: 160px;
    min-height: 240px;
    
    width: 12vw;
    height: 18vw;
    flex-grow: 0;
    padding: 9px;
    border: 1px solid lightgray;
    border-radius: 10px;
    margin: 0 5px;
    display:flex;
    flex-direction: column;
    line-height: 1.2;
    overflow: hidden;
    position: relative
}

.count {
    position: absolute;
    right: 0;
    background: red;
    top: 0;
    padding: 5px 10px;
    font-size: var(--smallFont);
    font-weight: bold;
    color: white;
    border-bottom-left-radius: 10px;
    box-shadow: -1px 1px 3px gray;;
}

.head img{
    border-radius: 5px;
    width: calc(max(12vw, 160px) - 20px); 
    height: calc(max(12vw, 160px) - 20px); 
    overflow: hidden; 
    object-fit: contain;
    /* object-position: top; */
}

.institute {
    flex-grow: 1; 
    text-align: center; 
    font-size: calc(var(--smallFont) * 0.9); 
    justify-content: center;
    display: flex;
    flex-direction: column;
}
</style>

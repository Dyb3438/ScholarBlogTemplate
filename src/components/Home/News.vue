<script>
import authorConfig from '../../config/author.config';
import News from '../icons/News.vue';
import Firework from '../Firework.vue';

export default {
    props: ['largeFont', 'smallFont', "screenWidth"],

    components:{
        News,
        Firework
    },

    data(){
        return {
            content: authorConfig.news,
            content_height: '100%',
            new_description_div: null
        }
    },

    mounted(){
        this.content_height = "calc(100% - "+ (this.$refs.Title.clientHeight + 20) +"px)";
        this.$refs.Content.style.setProperty(
            "height",
            this.content_height
        );
        if (this.isPC){
            // this.new_description_div = document.createElement('div');
            // this.new_description_div.style='display: none';
            // document.body.appendChild(this.new_description_div);

            for (let idx=0; idx < this.$refs.NewsList.getElementsByTagName('b').length; idx++){
                const bold_elem = this.$refs.NewsList.getElementsByTagName('b')[idx];
                const bold_text = bold_elem.textContent;
                Object.values(authorConfig.publications).forEach((pubs) => {
                    pubs.forEach((pub) => {
                        if (pub.title == bold_text){
                            // let showDiv = (e) => {
                            //     this.new_description_div.style=" \
                            //         display: block;              \
                            //         position: absolute;          \
                            //         top: " + (e.pageY + 20) + "px;    \
                            //         left: " + (e.pageX + 10) + "px;   \
                            //         width: 20vw;                \
                            //     ";
                            //     this.new_description_div.innerHTML = " \
                            //         <img src="+ pub.image +" style='width: 100%; height: auto; box-shadow: 0px 0px 10px lightgray'\> \
                            //     ";
                            // };

                            // let hideDiv = (e) => {
                            //     this.new_description_div.style=" \
                            //         display: none;              \
                            //     ";
                            //     this.new_description_div.innerHTML="";
                            // };

                            // bold_elem.addEventListener('mouseover', showDiv);
                            // bold_elem.addEventListener('mousemove', showDiv);
                            // bold_elem.addEventListener('mouseout', hideDiv);
                            bold_elem.addEventListener('click', (e) => {
                                window.location.href="#" + this.getPubId(pub.image);
                                // hideDiv(e);
                            });

                            bold_elem.style.cursor = "pointer";
                        }
                    })
                });
            }
        }
    },

    computed:{
        isPC(){
            return this.screenWidth >= 800;
        },
    },

    methods: {
        getPubId(image_url){
            return image_url.split('/')[image_url.split('/').length - 1].split('.')[0];
        }
    },
}
</script>

<template>
  <div class="News">
    <div class="title unselect"  ref="Title">
        <!-- <div class="icon" :style="`width:` + this.largeFont + '; height:' + this.largeFont">
            <News/>
        </div> -->
        <span :style="`font-size:` + this.largeFont">🔥 News</span>
    </div>

    <div class="content" ref="Content">
        <div style="overflow-y: auto; display: flex; flex-direction: column; height: 100%;">
            <ul style="padding-left: 20px" ref="NewsList">
                <li v-for="newsItem, key in content" style="margin-bottom: 5px">
                    <Firework v-if="(newsItem.search('Congratulation') > 0) && isPC" :style="`font-size:` + this.smallFont" :Content="newsItem">
                    </Firework>
                    <div :style="`font-size:` + this.smallFont" v-html="newsItem" v-else></div>
                </li>
            </ul>
        </div>
    </div>

  </div>
</template>

<style scoped>
.News {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
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

.content{
    width: 100%;
    flex: 1 0 auto;
    display: flex;
    flex-flow: column;
    cursor: default;
}

</style>

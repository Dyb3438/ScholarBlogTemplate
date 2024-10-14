<script>
import { onMounted } from 'vue';
import authorConfig from '../../config/author.config';
import Publication from '../icons/Publication.vue';
import GoogleScholar from '../icons/GoogleScholar.vue';

export default {
    props: ['largeFont', 'smallFont', "screenWidth", "discussionCount", "googleScholarInfo", "enableDiscussionRoom"],

    components:{
        Publication,
        GoogleScholar
    },

    data(){
        return {
            config_publications: authorConfig.publications,
            config_publication_category: authorConfig.publication_category,
            content: authorConfig.publications,
            optionColors: [
                '#5555bb',
                "#bb5555",
                '#55bb55',
                '#bb55bb',
                '#55bbbb',
                '#bbbb55',
                "#222255",
            ],
            stars: {},
            show_by_year: true,
        }
    },

    computed:{
        getSecTitle(){
            if (this.show_by_year){
                return this.getYears;
            } else {
                return Object.keys(this.getSecContent);
            }
        },
        getSecContent(){
            if (this.show_by_year){
                return this.config_publications;
            } else {
                let content = {};
                for (let secTitleId in this.config_publication_category){
                    const secTitle = this.config_publication_category[secTitleId];
                    content[secTitle] = [];
                }
                content['Others'] = [];

                const years = this.getYears;
                for (let idx in years){
                    const year = years[idx];
                    const publications = this.config_publications[year];
                    for (let publication_idx in publications){
                        const publication = publications[publication_idx];
                        let pushed = false;

                        for (let secTitleId in this.config_publication_category){
                            const secTitle = this.config_publication_category[secTitleId];
                            let secTitles = [];

                            if (secTitle.search("/") > 0){
                                let secSubTitles = secTitle.split("/");
                                for (let secSubTitleId in secSubTitles){
                                    secTitles.push(secSubTitles[secSubTitleId].trim());
                                }
                            } else {
                                secTitles.push(secTitle.trim());
                            }

                            for (let secTitleId in secTitles){
                                const secTitle_ = secTitles[secTitleId];
                                if (publication.keywords.includes(secTitle_)){
                                    content[secTitle].push(publication);
                                    pushed=true;
                                    break;
                                }
                            }
                        }

                        if (!pushed){
                            content['Others'].push(publication);
                        }
                    }
                }

                for (let secTitleId in this.config_publication_category){
                    const secTitle = this.config_publication_category[secTitleId];
                    content[secTitle] = content[secTitle].sort(function(a, b){return b.scholarInfo.citation - a.scholarInfo.citation});
                }

                if (content['Others'].length == 0){
                    delete content['Others'];
                } else {
                    content['Others'] = content['Others'].sort(function(a, b){return b.scholarInfo.citation - a.scholarInfo.citation});
                }
                return content;
            }
        },
        getYears(){
            return Object.keys(this.config_publications).sort((a,b)=>{return b-a;});
        },
        isPC(){
            return this.screenWidth >= 800;
        },
        pub_len(){
            let num=0;
            const years = this.getYears;
            for (let idx in years){
                const year = years[idx];
                const publications = this.config_publications[year];
                for (let pub_idx in publications){
                    num++;
                    let pub = publications[pub_idx];
                    this.config_publications[year][pub_idx]['scholarInfo'] = {
                        'citation': 0,
                    };
                    // update pub citation num
                    if ('publications' in this.googleScholarInfo){
                        for (let i in this.googleScholarInfo['publications']){
                            const scholarInfo = this.googleScholarInfo['publications'][i];
                            if (pub['title'].toLowerCase().trim() == scholarInfo['bib']['title'].toLowerCase().trim() && scholarInfo['num_citations'] > 0){
                                this.config_publications[year][pub_idx]['scholarInfo'] = {
                                    'citation': scholarInfo['num_citations'],
                                    'googleScholarUrl': scholarInfo['citedby_url']
                                }
                            }
                        }
                    }
                    
                }
            }
            return num;
        }
    },

    methods: {
        optionColor(index){
            if (index >= this.optionColors.length){
                return '#bbbbbb';
            }else{
                return this.optionColors[index];
            }
        },
        createKeywordUrl(keyword){
            return 'https://www.google.com/search?q=' + encodeURI(keyword);
        },
        getPubId(image_url){
            return image_url.split('/')[image_url.split('/').length - 1].split('.')[0];
        },
        showDiscussionRoom(title, paper_url){
            this.$emit('showDR', title, paper_url);
        },
        switch_list(listby){
            if (listby == 'year'){
                this.show_by_year=true;
            }else{
                this.show_by_year=false;
            }
        },
        handleHashChange() {
            let hash = unescape(window.location.hash.replace("#",""));
            if (this.config_publication_category.includes(hash)){
                if (this.show_by_year){
                    this.switch_list("category");
                    this.$nextTick(()=>{
                        this.$refs[hash][0].scrollIntoView();
                    });
                }
            }
        }
    },

    async mounted(){
        this.handleHashChange();
        if (this.isPC){
            const years = this.getYears;
            for (let idx in years){
                const year = years[idx];
                const publications = this.config_publications[year];
                for (let publication_idx in publications){
                    const publication = publications[publication_idx];
                    if (Object.keys(publication.options).indexOf("Code") >= 0){
                        let url = publication.options.Code;
                        if (url.indexOf("github") < 0){
                            continue;
                        }
                        try{
                            url = url.replace("github.com", "api.github.com/repos");
                            const response = await fetch(url);
                            const content = await response.json();
                            this.stars[publication.options.Code] = content.stargazers_count;
                        }catch(e){
                            console.log(e);
                        }
                    }
                }
            }
        }

        window.addEventListener('popstate',(event) => {
            let state = history.state||event.state;
            let hash = unescape(state.current.split('#')[1]);
            if (this.config_publication_category.includes(hash)){
                if (this.show_by_year){
                    this.switch_list("category");
                    this.$nextTick(()=>{
                        this.$refs[hash][0].scrollIntoView();
                    });
                } else {
                    this.$refs[hash][0].scrollIntoView();
                }
                event.preventDefault();
            }
        })
    }
}
</script>

<template>
  <div class="Publications">
    <div class="title unselect">
        <!-- <div class="icon" :style="`width:` + this.largeFont + '; height:' + this.largeFont">
            <Publication/>
        </div> -->
        <span :style="`font-size:` + this.largeFont">
            🏆 Selected Publications
            <div :style="`background-color: var(--color-text); border-radius: 100%; padding: calc(0.1 *`+ this.largeFont +`) calc(0.2 *`+ this.largeFont +`); color: white; height: `+ this.largeFont +`; text-align: center; line-height: 100%; display: inline-block; box-sizing: content-box;`">
                {{ pub_len }}
            </div>
        </span>
    </div>

    <div class="content" ref="content">
        <div :style="`font-size:` + this.smallFont">
            <equal></equal> denotes `Equal Contribution`.
        </div>
        <div class="YearBlock Item">
            <div class="Switcher" >
                <div class="SwitcherForeground" :style="show_by_year ? `--offset_x: 0%` : `--offset_x: 100%`">
                </div>
                <div class="SwitcherBlock"  :class="show_by_year? `SwitcherActive` : ``"   @click="switch_list('year')">
                    <span>By Year</span>
                </div>
                <div class="SwitcherBlock" :class="!show_by_year? `SwitcherActive` : ``"  @click="switch_list('category')">
                    <span>By Category</span>
                </div>
            </div>
        </div>

        <div v-for="secTitle in getSecTitle" class="ListOneYear" style="margin-top: 30px">
            <div class="YearBlock Item" :ref="secTitle" :id="secTitle">
                <div class="LeftPart"></div>
                <span :style="`font-size:` + this.smallFont + `; margin: 0 10px;`"><b>{{ secTitle }}</b></span>
                <div class="RightPart"></div>
            </div>
            <div class="Item" v-for="publication in getSecContent[secTitle]" :id="getPubId(publication.image)">
                <div v-if="Object.keys(publication.options).length > 0" v-bind:class="[isPC ? 'Publication': 'Publication_Mobile']">
                    <div class="PublicationImage">
                        <a :href="publication.image" target="_blank">
                            <img :src="publication.image" style="width: 100%;">
                        </a>
                    </div>
                    <div class="PublicationDesc">
                        <div class="PublicationTitle" :style="`font-size:` + this.smallFont" v-html="[publication.new ? `<span style='font-size: var(--largeFont)'>💥 </span>` : ``] + publication.title"></div>
                        <div class="PublicationAuthor" :style="`font-size:` + this.smallFont" v-html="publication.author"></div>
                        <div class="PublicationPublisher" :style="`font-size:` + this.smallFont" v-html="publication.publisher"></div>
                        <div class="PublicationKeyword" :style="`font-size:` + this.smallFont">
                            <span style="font-weight: bold">
                                Keywords: 
                            </span>
                            <div class="KeywordList">
                                <a :href="createKeywordUrl(keyword)" target='_blank' v-for="keyword in publication.keywords">
                                    <div class="unselect KeywordItem">
                                        {{ keyword }}
                                    </div>
                                </a>
                            </div>
                        </div>
                        <div class="PublicationScholar" :style="`font-size:` + this.smallFont" v-if="'scholarInfo' in publication && publication.scholarInfo.citation > 0">
                            <GoogleScholar :style="`height:  calc(` +this.smallFont + ` * 1.1); vertical-align: text-bottom;`"/>&nbsp;
                            <a :href="publication.scholarInfo['googleScholarUrl']" target="_blank" style="text-decoration-color: #4285f4 !important; color: #4285f4 !important">
                                <span>Citations: </span>
                                <span>{{ publication.scholarInfo.citation }}</span>
                            </a>
                        </div>
                        <div class="PublicationOptions" :style="`font-size:` + this.smallFont">
                            <div style="display: flex;" v-bind:style="isPC ? 'flex: 0 0 auto; margin: 5px 10px 5px 0' : 'flex: 1 0 auto; margin: 5px'" v-for="(value, key, index) in publication.options" >
                                <a  :href="value" style="display:inline-block; flex: 10" v-if="key == `Project Page` && value.indexOf('./') == 0">
                                    <div :style="`--btn_color:` + optionColors[index]" class="unselect OptionItem">
                                        {{ key }}
                                    </div>
                                </a>
                                <a  :href="value" style="display:inline-block; flex: 10" v-else-if="key == `Code`">
                                    <div :style="`--btn_color:` + optionColors[index]" class="unselect OptionItem">
                                        <span style="font-weight: bold">{{ key }}</span>
                                        <span style="margin-left:5px; border-left: 2px dotted; padding-left: 5px; font-weight: bold" v-if="value in stars">☆ {{ stars[value] }}</span>
                                    </div>
                                </a>
                                <a  :href="value" target="_blank" style="display:inline-block; flex: 10" v-else>
                                    <div :style="`--btn_color:` + optionColors[index]" class="unselect OptionItem">
                                        {{ key }}
                                    </div>
                                </a>
                            </div>
                            <div style="display: flex; flex: 0 0 auto; margin: 5px 10px 5px 0" v-if="isPC && publication.paper_url != '' && this.enableDiscussionRoom" @click="showDiscussionRoom(publication.title, publication.paper_url)">
                                <a  style="display:inline-block; flex: 10">
                                    <div :style="`--btn_color:` + optionColors[6]" class="unselect OptionItem">
                                        Discussion Room
                                        <span style="margin-left:5px; border-left: 2px dotted; padding-left: 5px; font-weight: bold" v-if="publication.title in discussionCount && discussionCount[publication.title] > 0"> {{ discussionCount[publication.title] }} </span>
                                    </div>
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-else v-bind:class="isPC ? 'Publication': 'Publication_Mobile'">
                    <div class="PublicationDesc" style="align-items: center;" v-bind:style="isPC ? 'margin-right: 30px' : ''">
                        <div class="PublicationTitle" :style="`font-size:` + this.smallFont" v-html="publication.title" style="text-align: center; word-break: break-word; word-wrap: break-word;"></div>
                        <div class="PublicationAuthor" :style="`font-size:` + this.smallFont" v-html="'Anonymous Authors'" style="text-align: center; word-break: break-word; word-wrap: break-word;"></div>
                        <div class="PublicationComment" :style="`font-size:` + this.largeFont">Coming soon~</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

  </div>
</template>

<style scoped>
.Publications {
    width: 100%;
}

.title {
    margin-bottom: 20px;
    display: flex;
    align-items: center;
}

.title * {
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


.Item {
    margin: 10px 0;
    position: relative
}

.Switcher {
    width: 100%;
    text-align: center;
    display: flex;
    border-bottom: 2px solid black;
    box-shadow: 0 6px 6px lightgray;
    border-radius: 10px 10px 0 0;
}

.SwitcherBlock{
    flex: 1;
    z-index: 999;
    cursor: pointer;
}

.SwitcherBlock:hover{
    background: rgb(230, 230, 230);
    border-radius: 10px 10px 0 0;
}

.SwitcherActive:hover{
    background: rgba(0,0,0,0) !important;
    cursor: default;
}

.SwitcherBlock span {
    font-size: var(--largeFont);
    font-weight: 500;
    color: black;
    transition-duration: 0.5s;
}

.SwitcherForeground{
    position: absolute;
    width: 50%;
    height: 100%;
    background: lightgray;
    transform: translateX(var(--offset_x));
    border-radius: 10px 10px 0 0;
    transition-duration: 0.5s;
    border: 1px solid black;
    border-bottom: 2px solid black;
}

.YearBlock {
    display: flex;
    align-items: center;
}
.YearBlock .LeftPart{
    height: 5px;
    color: white;
    background: -moz-linear-gradient(left, rgba(0,0,0,0) 0%, rgba(0,0,0,0) 25%, rgba(0,0,0,1) 100%);
    background: -webkit-gradient(linear, left top, right top, color-stop(0%,rgba(0,0,0,0)), color-stop(25%,rgba(0,0,0,0)), color-stop(100%,rgba(0,0,0,1)));
    background: -webkit-linear-gradient(left, rgba(0,0,0,0) 0%,rgba(0,0,0,0) 25%,rgba(0,0,0,1) 100%);
    background: -o-linear-gradient(left, rgba(0,0,0,0) 0%,rgba(0,0,0,0) 25%,rgba(0,0,0,1) 100%);
    background: -ms-linear-gradient(left, rgba(0,0,0,0) 0%,rgba(0,0,0,0) 25%,rgba(0,0,0,1) 100%);
    background: linear-gradient(to right, rgba(0,0,0,0) 0%,rgba(0,0,0,0) 25%,rgba(0,0,0,1) 100%);
    display: inline-block;
    flex: 1;
    border-radius: 5px;
}

.YearBlock .RightPart{
    height: 5px;
    color: white;
    background: -moz-linear-gradient(right, rgba(0,0,0,0) 0%, rgba(0,0,0,0) 25%, rgba(0,0,0,1) 100%);
    background: -webkit-gradient(linear, right top, left top, color-stop(0%,rgba(0,0,0,0)), color-stop(25%,rgba(0,0,0,0)), color-stop(100%,rgba(0,0,0,1)));
    background: -webkit-linear-gradient(right, rgba(0,0,0,0) 0%,rgba(0,0,0,0) 25%,rgba(0,0,0,1) 100%);
    background: -o-linear-gradient(right, rgba(0,0,0,0) 0%,rgba(0,0,0,0) 25%,rgba(0,0,0,1) 100%);
    background: -ms-linear-gradient(right, rgba(0,0,0,0) 0%,rgba(0,0,0,0) 25%,rgba(0,0,0,1) 100%);
    background: linear-gradient(to left, rgba(0,0,0,0) 0%,rgba(0,0,0,0) 25%,rgba(0,0,0,1) 100%);
    display: inline-block;
    flex: 1;
    border-radius: 5px;
}

.Publication {
    width: 100%;
    display: flex;
    align-items: top;
    padding: 10px;
    border-radius: 10px;
}

.Publication:hover {
    transition: 0.3s;
    box-shadow: 0px 0px 20px lightgray;
    /* transform: translateY(-3px); */
}

.PublicationImage{
    width: 20vw;
    height: auto;
    flex: 0 0 auto;
    display: flex;
    align-items: center;
}

.PublicationDesc {
    display: flex;
    flex-direction: column;
    margin-left: 30px;
    flex: 1
}

.PublicationTitle {
    font-weight: bold;
    color: black;
}

.PublicationAuthor {
    color: rgb(100, 100, 100);
}

.PublicationPublisher {
    font-weight: 500;
}


.PublicationScholar *{
    /* color: var(--color-text) !important; */
    font-weight: 500;
}

.PublicationKeyword {
    margin-top: 5px;
    display: flex;
}

.PublicationComment {
    font-weight: bold;
}

.KeywordList {
    display: flex;
    flex-wrap: wrap;
    justify-content: left;
}

.PublicationKeyword a {
    text-align: center;
    text-decoration: none;
    color: var(--color-text);
    margin: 0 5px;
    margin-bottom: 5px;
}

.KeywordItem {
    flex: 0 0 auto;
    font-size: calc(var(--smallFont) * 0.8);
    padding: calc(var(--smallFont) * 0.1) calc(var(--smallFont) * 0.3);
    border-radius: calc(var(--smallFont)  * 0.3);
    border: 1px solid black;
    cursor: pointer;
    font-weight: 600;
}

.KeywordItem:hover {
    background-color: lightgoldenrodyellow;
    transform: translateY(-5%);
}

.KeywordItem:active {
    background-color: white;
    transform: translateY(0%);
}

.PublicationOptions {
  display: flex;
  flex-wrap: wrap;
  margin-top: 5px;
  justify-content: left;
}

.PublicationOptions a {
  margin-right: auto;
  text-align: center;
  text-decoration: none
}

.OptionItem {
  flex: 0 0 auto;

  font-size: calc(var(--smallFont) * 0.8);
  font-weight: bold;
  padding: calc(var(--smallFont) / 3) calc(var(--smallFont) / 3 * 2);
  border-radius: calc(var(--smallFont) / 3 * 2);
  color: var(--btn_color);
  border: 2px solid var(--btn_color);

  cursor: pointer;
}

.OptionItem:hover{
  transform: translateY(-5%);

  background-color: color-mix(in srgb, var(--btn_color) 30%, white);
}

.OptionItem:active {
  box-shadow: none;
  transform: translateY(0%);
}



.Publication_Mobile {
    width: 100%;
    display: flex;
    align-items: center;
    flex-direction: column;
    border: 1px solid gray;
    border-radius: 10px;
    padding: 10px;
    box-shadow: 2px 2px 2px gray;
}

.Publication_Mobile .PublicationOptions {
    justify-content: center;

}


.Publication_Mobile .PublicationOptions a {
  margin: auto;
}

.Publication_Mobile .PublicationDesc {
    margin-left: 0;
}

.Publication_Mobile .PublicationImage{
    width: 80%;
}

.Publication_Mobile .KeywordItem {
    background-color: lightgoldenrodyellow;
}

.Publication_Mobile .OptionItem {
    color: white;
    background-color: var(--btn_color);
}



</style>

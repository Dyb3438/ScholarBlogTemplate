<script>
import authorConfig from '../../config/author.config';
import Avatar from './Avatar.vue';
import AuthorItem from './AuthorItem.vue';
import Comment from './Comment.vue';
import Close from '../icons/Close.vue';
import apiConfig from '../../config/api.config';

export default {
    props: ['largeFont', 'smallFont', "screenWidth", "channel", "discussion_url"],

    components:{
        Avatar,
        AuthorItem,
        Comment,
        Close
    },

    data(){
        return {
            number: {},
            key: 0,


            authorName: authorConfig.name,
            authorRole: authorConfig.role,
            authorSchool: authorConfig.school,
            authorCollege: authorConfig.college,
            authorEmail: authorConfig.email,

            comments: [],
            page_src: this.discussion_url,
            t: 1,
            order: 'Time',
            title_offset: 0,

            t1: null,
            t2: null,

            hiding: false,
        }
    },

    watch: {
        
    },

    computed:{
        isPC(){
            return this.screenWidth >= 800;
        },

        local_channel(){
            return this.channel;
        },

        EmailHref(){
            return "mailto:" + authorConfig.email;
        },
        EmailShow(){
            return authorConfig.email.replace("@", " AT ");
        },
    },

    mounted(){
        window.loadPage = this.loadPage;

        this.getComments(this.scrollCommentToBottom);

        this.t1 = setInterval(()=>{
            this.getLikes(this.getComments);
        }, 1000 * 30);
        const title_width = this.$refs.title.clientWidth ? this.$refs.title.clientWidth : this.$refs.title.offsetWidth;

        if (this.$refs.title.scrollWidth > title_width){
            this.$refs.title.style.setProperty('padding-right', '10%');
            this.$refs.title.style.setProperty('padding-left', '10%');

            var that = this;
            this.t2 = setInterval(() => {
                if (that.$refs.title.scrollLeft + title_width >= that.$refs.title.scrollWidth - 10){
                    that.title_offset = 0;
                } else {
                    that.title_offset += 5;
                }
                that.$refs.title.scrollLeft = that.title_offset;
            }, 100);
        }

        this.$refs.alias_name.value = localStorage.getItem('alias_name');

    },

    beforeUnmount(){
        clearInterval(this.t1);
        this.t1 = null;
        if (this.t2 != null){
            clearInterval(this.t2);
            this.t2 = null;
        }
    },

    methods: {
        post(e){
            const saveText = this.$refs.input_ta.value;
            const show_region = this.$refs.show_region.checked;
            const alias_name = this.$refs.alias_name.value;

            if (alias_name != ''){
                localStorage.setItem('alias_name', alias_name);
            }

            if (saveText == ''){
                alert('Empty content can not be posted.');
                return;
            }
            const response = fetch(apiConfig.baseURL + '/Discussion/Post', {
                method: "POST",
                // mode: "cors",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    'alias_name': alias_name,
                    'show_region': show_region,
                    'cite': this.local_channel,
                    'comment': saveText,
                    'token': localStorage.getItem('token')
                }),
            });

            this.$refs.input_ta.readonly = true;
            this.$refs.input_ta.value='Sending...';
            e.target.disabled = true;
            if (this.local_channel != 'Global'){
                this.$refs.insert_btn.style.setProperty('pointer-events', 'none');
            }
            this.$refs.post_btn.style.setProperty('pointer-events', 'none');

            response.then(e => e.json())
                    .then(e => {
                        if (e['success']){
                            alert('The comment success to send.');
                            localStorage.setItem("token", e['token']);
                            this.getComments(this.scrollCommentToBottom);
                        }else{
                            alert('The comment failed to send.');
                        }
                    })
                    .catch(e => {
                        console.log('error: ' + e);
                        alert('The comment failed to send.');
                    })
                    .finally(() => {
                        this.$refs.input_ta.readonly = false;
                        this.$refs.input_ta.value = '';
                        this.$refs.show_region.checked = true;
                        if (this.local_channel != 'Global'){
                            this.$refs.insert_btn.style.setProperty('pointer-events', '');
                        }
                        this.$refs.post_btn.style.setProperty('pointer-events', '');
                    });
        },

        getComments(callback=null){
            const response = fetch(apiConfig.baseURL + '/Discussion/GetComment?cite='+this.local_channel + '&order=' + this.order + '&token=' + localStorage.getItem('token'), {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
                // mode: "cors",
            });

            response.then(e => e.json())
                    .then(e => {
                        if (e['success']){
                            this.comments = e['comments'];
                            if (callback != null){
                                callback();
                            }
                        }
                    })
                    .catch(e => {
                        console.log('error: ' + e);
                    });
        },

        switchOrder(event){
            this.order = event.target.value;
            let callback_fun;
            if (this.order == 'Time'){
                callback_fun = this.scrollCommentToBottom;
            }else{
                callback_fun = this.scrollCommentToTop;
            }
            this.getComments(callback_fun);
        },

        getLikes(callback=null){
            const response = fetch(apiConfig.baseURL + '/Discussion/GetAllLike?cite='+this.local_channel + '&order=' + this.order, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
                // mode: "cors",
            });

            response.then(e => e.json())
                    .then(e => {
                        if (e['success']){
                            if (e['cites'].length != this.comments.length){
                                callback();
                                return;
                            }
                            for (let idx = 0; idx < e['cites'].length; idx++){
                                const cite = e['cites'][idx];
                                const comment = this.comments[idx];
                                if (cite['UID'] == comment['UID']){
                                    this.comments[idx]['LIKE'] = cite['LIKE'];
                                } else {
                                    callback();
                                    break;
                                }
                            }
                        }
                    })
                    .catch(e => {
                        console.log('error: ' + e);
                    });
        },

        clickLike(id){
            let comment;
            for (let idx = 0; idx < this.comments.length; idx++){
                comment = this.comments[idx];
                if (comment['UID'] == id){
                    break;
                }
            }
            comment['LIKE'] = "+1";

            const response = fetch(apiConfig.baseURL + '/Discussion/Like', {
                method: "POST",
                // mode: "cors",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    'uid': id
                }),
            });

            response.then(e => e.json())
                    .then(e => {
                        comment['LIKE'] = e['num'];
                    })
                    .catch(e => {
                        console.log('error: ' + e);
                    });
        },

        clickHide(id){
            if (this.hiding){
                alert('Waiting for previous deletion.');
                return
            }
            this.hiding = true;
            const response = fetch(apiConfig.baseURL + '/Discussion/Hide', {
                method: "POST",
                // mode: "cors",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    'uid': id,
                    'token': localStorage.getItem('token')
                }),
            });

            response.then(e => e.json())
                    .then(e => {
                        if (e['success']){
                            this.getComments();
                            alert('Delete successfully!');
                        } else {
                            alert('You can not delete this comment now!');
                        }
                    })
                    .catch(e => {
                        console.log('error: ' + e);
                        alert('Exception Error!');
                    }).finally(() => {
                        this.hiding = false;
                    });
        },

        scrollCommentToBottom(){
            this.$nextTick(() => {
                this.$refs.show_area.scrollTop = this.$refs.show_area.scrollHeight;
            });
        },

        scrollCommentToTop(){
            this.$nextTick(() => {
                this.$refs.show_area.scrollTop = 0;
            });
        },

        insertAnchor(){
            document.execCommand('insertText', false, '📎1');
        },

        moveCursorToEnd(dom) {
            if (window.getSelection) {
                var range = window.getSelection();
                range.selectAllChildren(dom);
                range.collapseToEnd();
            }
            else if (document.selection) {
                var range = document.selection.createRange();
                range.moveToElementText(dom);
                range.collapse(false);
                range.select();
            }
        },

        loadPage(page){
            // this.page_src = this.discussion_url + '?t=' + this.t + '#page=' + page;
            this.page_src = this.discussion_url + "#page=" + page;
            // this.t = 1 - this.t;
            this.key += 1;
        },
        
        close(){
            this.$emit('close', null);
        }

    }
  
}
</script>

<template>
    <div style="position: fixed; z-index: 10000;">
        <div class="background">
        </div>

        <div class="discussion_body" :style="`--smallFont:` + this.smallFont + '; --largeFont:' + this.largeFont">
            <div class="header">
                <div style="display: inline-block; flex-shrink: 0;">Discussion Room&nbsp;@&nbsp;</div>
                <div style="color: darkred; font-weight: bold; overflow-x: auto; display: inline-block; white-space: nowrap;" ref="title" class="title">{{ this.local_channel }}</div>
                <div style="width: 0; flex: 1"></div>
                <div class="close_btn" @click="close">
                    <Close></Close>
                </div>
            </div>

            <div class="content">
                <div v-if="this.local_channel == 'Global'" class="left_area" style="--size: 14vw; width: max(20vw, 200px)">
                    <Avatar size="var(--size)" radius="20px"></Avatar>

                    <AuthorItem font_size="var(--largeFont)" font_weight="bold" style="margin-top: 30px">
                        <template v-slot:Text>
                        👨🏻‍💻 {{authorName}}
                        </template>
                    </AuthorItem>

                    <AuthorItem font_size="var(--smallFont)">
                        <template v-slot:Text>
                        🎓 {{authorRole}}
                        </template>
                    </AuthorItem>

                    <AuthorItem font_size="var(--smallFont)">
                        <template v-slot:Text>
                        🏫 {{authorSchool.name}}
                        <div v-if="authorCollege.name != ``" style="display: inline-block;">
                        <span>,&nbsp&nbsp{{authorCollege.name}}</span>
                        </div>
                        </template>
                    </AuthorItem>

                    <AuthorItem font_size="var(--smallFont)">
                        <template v-slot:Text>
                        📮 {{ this.EmailShow }}
                        </template>
                    </AuthorItem>
                </div>

                <div v-else class="left_area" style="width: max(32vw, 320px)">
                    <iframe :src="page_src" style="width: 100%; height: 100%; border-radius: 10px" frameborder='0' ref="paper_frame" :key="key" allow="fullscreen"></iframe>
                </div>

                <div class="right_area" :style="this.local_channel != 'Global' ? `--left: max(32vw, 320px)`: `--left: max(20vw, 200px)`">
                    <div class="controll_area">
                        <div>
                            Sort ↓: 
                            <select name="sort" style="text-align: center; font-size: calc(var(--smallFont) * 0.8)" @change="switchOrder">
                                <option value="Time">Time</option>
                                <option value="Popular">Popular</option>
                            </select>
                        </div>
                    </div>
                    <div class="show_area" ref="show_area">
                        <div v-for="comment in comments" style="margin-bottom: 10px">
                            <Comment :largeFont=this.largeFont :smallFont=this.smallFont :id="comment['ID']" :username="comment['USERNAME']" :region="comment['COUNTRY']" :comment="comment['COMMENT']" :time="comment['TIME']" :like_num="comment['LIKE']" :uid="comment['UID']" :deletable="comment['DELETABLE']" @like="clickLike" @hide="clickHide"></Comment>
                        </div>
                    </div>

                    <div class="input_area">
                        <div class="input_btn">
                            <div class="term unselect">
                                <span>Alias Name:</span>
                                <input type="text" class="alias_name_text" placeholder="Optional" style="margin-left: 5px" ref="alias_name">
                            </div>
                            <div class="term unselect" style="margin-left: 15px">
                                <span>Show Region:</span>
                                <input type="checkbox" checked style="margin-left: 5px" ref="show_region">
                            </div>
                            <div style="flex: 1"></div>

                            <div class="insert term btn unselect" @click="insertAnchor" ref="insert_btn" v-if="this.local_channel != 'Global'">
                                <span>Insert Page Anchor</span>
                            </div>

                            <div class="post term btn unselect" style="margin-left: 15px" @click="post($event)" ref="post_btn">
                                <span>Post</span>
                            </div>
                        </div>
                        <textarea class="textarea" style="flex: 1; font-size: var(--smallFont); padding: 5px;" ref="input_ta"></textarea>
                    </div>

                </div>
            </div>

        </div>
    </div>
</template>

<style scoped>

.background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: lightgray;
    opacity: 0.7;
}
.discussion_body {
    position: fixed;
    z-index: 100000;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;

    width: max(80vw, 800px);
    height: 90vh;

    margin: auto;

    background: white;
    opacity: 1;
    border-radius: 10px;
    border: 1px solid black;
    box-shadow: 0px 0px 10px gray;

    padding: calc(var(--smallFont) * 0.8);

    display: flex;
    flex-direction: column;
}

.header {
    font-size: var(--largeFont);
    font-weight: bold;
    width: 100%;
    text-align: left;
    height: calc(1.2 * var(--largeFont));
    display: flex;

}

.title {
    scrollbar-width: none;
    -ms-overflow-style: none;
    font-size: calc(var(--largeFont) * 0.9);
}

.title::-webkit-scrollbar {
    display: none;
}

.close_btn svg {
    width: calc(1.2 * var(--largeFont));
    height: calc(1.2 * var(--largeFont));
    margin-left: var(--largeFont);
    cursor: pointer;
}

@keyframes rotate{
  0%{
    -webkit-transform: rotate(0deg);
  }
  100%{
    -webkit-transform: rotate(360deg);
  }
}

.close_btn svg:hover {
    animation: rotate 1s infinite;
}

.content {
    width: 100%;
    display: flex;
    flex: 1;
    margin-top: calc(var(--smallFont) * 0.8);
    height: calc(100% - 1.2 * var(--largeFont) - var(--smallFont) * 1.6);
}

.left_area {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    flex-shrink: 0;
}

.right_area {
    margin-left: calc(var(--smallFont) * 0.8);
    border: 1px solid black;
    border-radius: 10px;
    width: calc(max(80vw, 800px) - var(--left) - 3 * calc(var(--smallFont) * 0.8));
    height: 100%;

    display: flex;
    flex-direction: column;
}

.controll_area {
    display: flex;
    flex-direction: row-reverse;
    padding-left: 10px;
    padding-right: 10px;
    font-size: var(--smallFont);
}

.show_area {
    /* height: 80%; */
    flex: 1;
    padding: 5px;
    border-bottom: 1px solid black;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    transition: all 2s ease;
}

.input_area {
    display: flex;

    flex-direction: column;
    padding: 10px;
    padding-top: 5px;
    height: 20%;

    background: lightgray;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;

}

.input_btn {
    display: flex;
    flex-direction: row;
    width: 100%;
    padding-bottom: 5px;
}

.input_btn .term span{
    font-size: var(--smallFont);
    font-weight: bold;
}

.alias_name_text {
    border: 0;
    border-bottom: 1px solid gray;
    width: 7vw;
    font-size: var(--smallFont);
    background: transparent;

    transition: 0.5;
}

.alias_name_text:focus {
    outline: none;
    border-bottom: 1px solid black;
}

.btn {
    background: white;
    padding-left: 10px;
    padding-right: 10px;
    border-radius: 10px;
    border: 1px solid black;
    cursor: pointer;
}

.btn:hover {
    box-shadow: 0px 0px 2px gray;
    transform: translateY(-5%);
}

.btn:active {
    box-shadow: none;
    transform: translateY(0);
}

.textarea {
    font-family: monospace;
    text-rendering: auto;
    color: fieldtext;
    letter-spacing: normal;
    word-spacing: normal;
    line-height: normal;
    text-transform: none;
    text-indent: 0px;
    text-shadow: none;
    display: inline-block;
    text-align: start;
    appearance: auto;
    -webkit-rtl-ordering: logical;
    cursor: text;
    overflow-wrap: break-word;
    background-color: field;
    column-count: initial !important;
    margin: 0em;
    border-width: 1px;
    border-style: solid;
    border-color: -internal-light-dark(rgb(118, 118, 118), rgb(133, 133, 133));
    border-image: initial;
    padding: 2px;
    /* white-space: pre-wrap; */
    overflow-y: auto;
    resize:none
}

</style>
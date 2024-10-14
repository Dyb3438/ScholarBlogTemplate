<script>
import authorConfig from '../../config/author.config';

export default {
    props: ['largeFont', 'smallFont', "screenWidth"],

    data(){
        return {
            content: authorConfig.academicFootprints
        }
    },

    computed:{
        isPC(){
            return this.screenWidth >= 800;
        }
    },
  
}
</script>

<template>
  <div class="AcademicFootprints">
    <div class="title unselect">
        <span :style="`font-size:` + this.largeFont">🐾 Academic Footprints</span>
    </div>

    <div class="content" :style="[`font-size:` + this.smallFont, isPC ?`flex-direction: row` :`flex-direction: column`]">
        <div v-for="sub_content, key in content" class="subContent" :style="[isPC ?`margin: 0 10px;` : `margin-bottom: 10px`]">
            <div style="font-weight: bold" v-html="key">
            </div>
            <ul>
                <li v-for="lines in sub_content">
                    <span v-for="line in lines" style="display: block" v-html="line">
                    </span>
                </li>
            </ul>
        </div>
    </div>

  </div>
</template>

<style scoped>
.AcademicFootprints {
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
    display: flex;
}

.subContent {
    display: flex;
    flex-direction: column; 
    flex: 1
}

ul {
    padding-inline-start: calc(2 * var(--smallFont));
}

</style>

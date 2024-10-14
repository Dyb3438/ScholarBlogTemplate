<script>
export default {

  props: {
    font_size: {
        type: String,
        default: "20px"
    },
    font_weight: {
        type: String,
        default: "normal"
    }
  },
}
</script>

<template>
   <div class="Item" ref="Item">
        <div class="Icon" :style="`width:` + this.font_size + '; height:' + this.font_size" v-if="$slots.Icon">
          <span>
            <slot name="Icon"></slot>
          </span>
        </div>
        <span class="Text" :style="`font-weight:` + this.font_weight + `; font-size:` + this.font_size">
            <slot name="Text"></slot>
        </span>
    </div>
</template>

<style scoped>

.Item {
  width: 100%;
  text-align: left;
  margin-top: 5px;
  display: flex;
  align-items: center;

}

.Icon {
  display: inline-block;
  box-sizing: content-box;
  padding-right: 10px;
}

.Icon svg {
  width: 100%;
  height: 100%;
}

</style>

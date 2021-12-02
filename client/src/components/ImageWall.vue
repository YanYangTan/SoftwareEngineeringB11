<template>
  <div>
   <el-image v-if="showViewer" :on-close="closeViewer" :url-list="[src_list]"/>
  <el-row :gutter="20">
        <el-col :span="4" v-for="item in imagelist" :key="item.id" style="height:200px">
          <el-card :body-style="{ padding: '0px 0px' }">
            <div slot="header">
            <img style="object-fit: contain;height:125px" src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQDE40bmA4cGxSyAVj1_824eK4iUtIK511FgQ&usqp=CAU" class="image" /></div>
            <el-button
              size="mini"
              icon="el-icon-zoom-in"
              style="padding: 1px 1px;"
              type="text"
              class="button"
              @click="showBig(item)"
            >大图</el-button>
            <el-button
              size="mini"
              icon="el-icon-edit-outline"
              style="padding: 1px 2px;"
              type="text"
              class="button"
              @click="editOne(item)"
            >标注</el-button>
          </el-card>
        </el-col>
      </el-row>
  </div>
</template>

<script>

export default {
  name: 'ImageWall',
  data() {
    return {
      imagelist: [{}, {}, {}],
      showViewer: false,
      src_list: '',
      view_index: 0,
    };
  },
  methods: {
    showBig(pic) {
      // eslint-disable-next-line no-unused-expressions
      pic;
      this.src_list = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQDE40bmA4cGxSyAVj1_824eK4iUtIK511FgQ&usqp=CAU';
      this.showViewer = true;
    },
    closeViewer() {
      this.showViewer = false;
    },
  },
};
</script>

<style scoped>

</style>

<template>
  <div>
  <el-row :gutter="20">
        <el-col :span="4" v-for="item in imagelist" :key="item.id" style="height:200px">
          <el-card :body-style="{ padding: '0px 0px' }">
            <div slot="header">
              <el-image
    style="width: auto; height: 160px"
    :src="url"
    :preview-src-list="srcList">
  </el-image>
</div>
            <el-button
              size="mini"
              icon="el-icon-zoom-in"
              style="padding: 1px 1px;"
              type="text"
              class="button"
              @click="like(item)"
            >点赞</el-button>
            <el-button
              size="mini"
              icon="el-icon-edit-outline"
              style="padding: 1px 2px;"
              type="text"
              class="button"
              @click="editOne(item)"
            >详情</el-button>
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
      url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
      srcList: [
        'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
        'https://fuss10.elemecdn.com/8/27/f01c15bb73e1ef3793e64e6b7bbccjpeg.jpeg',
        'https://fuss10.elemecdn.com/1/8e/aeffeb4de74e2fde4bd74fc7b4486jpeg.jpeg',
      ],
    };
  },
  methods: {
    // showBig(pic) {
    //   // eslint-disable-next-line no-unused-expressions
    //   pic;
    //   this.src_list = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQDE40bmA4cGxSyAVj1_824eK4iUtIK511FgQ&usqp=CAU';
    //   this.showViewer = true;
    // },
    // closeViewer() {
    //   this.showViewer = false;
    // },
  },
};
</script>

<style scoped>

</style>
